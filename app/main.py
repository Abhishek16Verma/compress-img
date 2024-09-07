from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from uuid import uuid4
import csv
import requests
from . import oprations, schemas, db, data_handler
from PIL import Image
from urllib.parse import urljoin
import io, os

app = FastAPI()
COMPRESSED_IMAGE_DIR = "compressed_images"
os.makedirs(COMPRESSED_IMAGE_DIR, exist_ok=True)

oprations.Base.metadata.create_all(bind=db.engine)

def compress_image(image_data: bytes, quality: int = 50) -> bytes:
    with Image.open(io.BytesIO(image_data)) as img:
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=quality)
        return buffer.getvalue()

@app.post("/upload/")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(db.get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    csv_content = await file.read()
    csv_reader = csv.DictReader(csv_content.decode('utf-8').splitlines())

    products = []
    opt_urls = ''
    for row in csv_reader:
        unique_id = str(uuid4())
        product_name = row['Product Name']
        serial_number = row['S. No.']
        image_urls = row['Input Image Urls']
        
        for url in image_urls.split(','):
            img_unique = str(uuid4())
            image_data = requests.get(url.strip(' '))
            image_name = os.path.basename(product_name)
            compressed_image_data = compress_image(image_data=image_data.content)
            compressed_image_path = os.path.join(COMPRESSED_IMAGE_DIR, f"compressed_{image_name}_{img_unique}.png")
            with open(compressed_image_path, "wb") as f:
                f.write(compressed_image_data)
        
            base_url = "http://127.0.0.1:8000/"
            compressed_image_url = urljoin(base_url, f"{COMPRESSED_IMAGE_DIR}/compressed_{image_name}_{img_unique}.png")
            opt_urls += compressed_image_url + ", "
        product = schemas.Product(unique_id=unique_id,name=product_name, serial_number=serial_number, image_urls=image_urls,output_urls=opt_urls)
        data_handler.create_product(db, product)
        products.append(unique_id)
        

    # for product in products:
    #     db_product = data_handler.create_product(db, product)
    #     for image in product.images:
    #         task = celery_worker.process_image.delay(image.input_url)
    #         # Optionally store the task ID or handle it as needed
    #         image.output_url = f'Processing task {task.id}...'
    #         data_handler.create_image(db, image, db_product.id)
    return JSONResponse(content={"unique_images_entries": products}, status_code=200)
    


@app.get("/status/{product_id}")
def get_status(product_id: str, db: Session = Depends(db.get_db)):
    product = data_handler.get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
