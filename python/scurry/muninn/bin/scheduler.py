import time

import muninn.worker as worker

while True:
    prom = worker.scan_octoprint_jobs.delay(1)

    while not prom.ready():
        time.sleep(1)
    prom.forget()
    time.sleep(5)
