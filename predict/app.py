"""Local review dashboard. Single user, no auth, localhost only."""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from .book import accept_view, reject_view
from .db import connect, init_schema
from .queries import gate_line, queue_rows

TEMPLATES = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))


def create_app(db_path=None) -> FastAPI:
    app = FastAPI(title="proposition engine")

    def db():
        c = connect(db_path)
        init_schema(c)
        return c

    @app.get("/", response_class=HTMLResponse)
    def queue(request: Request):
        conn = db()
        try:
            return TEMPLATES.TemplateResponse(
                request, "queue.html",
                {"rows": queue_rows(conn), "gate": gate_line(conn)})
        finally:
            conn.close()

    @app.post("/views/{view_id}/accept")
    def accept(view_id: int, market_id: int = Form(...), direction: str = Form(...)):
        conn = db()
        try:
            accept_view(conn, view_id, market_id, direction)
        except ValueError as e:
            return HTMLResponse(str(e), status_code=400)
        finally:
            conn.close()
        return RedirectResponse("/", status_code=303)

    @app.post("/views/{view_id}/reject")
    def reject(view_id: int, reason: str = Form(...), note: str = Form("")):
        conn = db()
        try:
            reject_view(conn, view_id, reason, note)
        except ValueError as e:
            return HTMLResponse(str(e), status_code=400)
        finally:
            conn.close()
        return RedirectResponse("/", status_code=303)

    return app
