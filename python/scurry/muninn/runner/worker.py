import datetime

from celery import Celery

import scurry.octoprint as octoprint
import scurry.muninn.models as models
import scurry.muninn.config as config
import scurry.log as log


def main():
    conf = config.load_default()
    conf.database.connect()

    app = Celery(
        "redis",
        broker="redis://localhost:6379/0",
        backend=(
            "db+postgres://%s:%s@%s/celery"
            % (conf.database.user, conf.database.password, conf.database.host)
        ),
    )

    octo_client = octoprint.Client(
        "http://octoprint", "A3C96C2498E948FE9D74D3A985423279"
    )

    @app.on_after_configure.connect
    def setup_periodic_tasks(sender, **kwargs):
        # Calls test('hello') every 10 seconds.
        session = conf.database.Session()

        printers = session.query(models.Printer).all()

        for p in printers:
            sender.add_periodic_task(
                15.0,
                scan_octoprint_jobs.s(p.id),
                name=f"scan printer {p.name}",
            )

    @app.task
    def scan_octoprint_jobs(printer_id: int):
        logger = log.get_logger("worker")

        logger.debug("getting printer jobs", printer_id=printer_id)

        session = conf.database.Session()

        printer = session.query(models.Printer).get(printer_id)

        client = octoprint.Client(printer.url, printer.api_key)
        result = client.jobs()

        entry = models.PrinterStatus(
            timestamp=datetime.datetime.now(),
            status=result.state,
            printer_id=printer_id,
        )
        session.add(entry)
        session.commit()
        return result
