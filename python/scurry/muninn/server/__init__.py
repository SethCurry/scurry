from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import joinedload

import markdown2

import scurry.muninn.config as config
import scurry.muninn.models as models


def main():
    app = FastAPI()
    app.mount("/static", StaticFiles(directory="web/static"), name="static")
    templates = Jinja2Templates(directory="web/templates")

    conf = config.load_default()
    conf.database.connect()

    @app.get("/printers/{printer_id}", response_class=HTMLResponse)
    async def get_printer(request: Request, printer_id: str):
        session = conf.database.Session()
        printer = session.query(models.Printer).get(printer_id)
        printer_status = (
            session.query(models.PrinterStatus)
            .filter(models.PrinterStatus.printer_id == printer_id)
            .order_by(models.PrinterStatus.timestamp.desc())
            .limit(1)
            .one()
        )

        session.close()
        return templates.TemplateResponse(
            "printer.html",
            {"request": request, "printer": printer, "latest_status": printer_status},
        )

    @app.get("/printers", response_class=HTMLResponse)
    async def list_printers(request: Request):
        session = conf.database.Session()
        printers = session.query(models.Printer).all()
        session.close()
        return templates.TemplateResponse(
            "printer_list.html",
            {"request": request, "printers": printers},
        )

    @app.get("/pets/genuses", response_class=HTMLResponse)
    async def list_genuses(request: Request):
        session = conf.database.Session()
        genuses = session.query(models.Genus).all()
        session.close()
        return templates.TemplateResponse(
            "genus_list.html",
            {"request": request, "genuses": genuses},
        )

    @app.get("/pets/genuses/{genus_id}", response_class=HTMLResponse)
    async def get_genus(request: Request, genus_id: int):
        session = conf.database.Session()
        genus = session.query(models.Genus).options(joinedload("species")).get(genus_id)
        session.close()

        notes = ""
        if genus.notes is not None:
            notes = markdown2.markdown(genus.notes)
            print(notes)
        return templates.TemplateResponse(
            "genus.html",
            {"request": request, "genus": genus, "notes": notes},
        )

    @app.get("/pets/species/{species_id}", response_class=HTMLResponse)
    async def get_species(request: Request, species_id: int):
        session = conf.database.Session()
        species = (
            session.query(models.Species)
            .options(joinedload("creatures"), joinedload("genus"))
            .get(species_id)
        )
        session.close()

        notes = ""
        if species.notes is not None:
            notes = markdown2.markdown(species.notes)
        return templates.TemplateResponse(
            "species.html",
            {"request": request, "species": species, "notes": notes},
        )

    @app.get("/api/printers")
    async def api_list_printers():
        session = conf.database.Session()

        printers = session.query(models.Printer).all()
        session.close()

        return printers

    @app.get("/api/printers/{printer_id}/status")
    async def printer_status(printer_id: int):
        session = conf.database.Session()

        printer_status = (
            session.query(models.PrinterStatus)
            .filter(models.PrinterStatus.printer_id == printer_id)
            .order_by(models.PrinterStatus.timestamp.desc())
            .limit(1)
            .one()
        )
        session.close()
        return printer_status


if __name__ == "__main__":
    main()