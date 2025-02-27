from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.hotels.router import list_hotels

router = APIRouter(prefix="/pages", tags=["Фронтенд"])

templates = Jinja2Templates(directory="app/templates")


@router.get("/hotels")
async def list_hotels_page(request: Request, hotels=Depends(list_hotels)):
    return templates.TemplateResponse(
        request, name="hotels.html", context={"hotels": hotels}
    )
