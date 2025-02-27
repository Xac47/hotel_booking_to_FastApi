import shutil

from fastapi import APIRouter, UploadFile

from app.tasks.tasks import process_pic

router = APIRouter(prefix="/images", tags=["Загрузка картинок"])


@router.post("/hotels/add")
async def add_hotels_image(name_file: int, file: UploadFile):
    image_path = f"app/static/images/{name_file}.webp"
    with open(image_path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    process_pic.delay(image_path)
