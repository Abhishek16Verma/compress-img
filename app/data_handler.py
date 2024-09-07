from sqlalchemy.orm import Session
from . import oprations, schemas

def create_product(db: Session, product: schemas.Product):
    db_product = oprations.Product(unique_id=product.unique_id, name=product.name, serial_number=product.serial_number,images_urls=product.image_urls, output_urls=product.output_urls)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product.unique_id

def get_product(db: Session, product_id: str):
   
    return db.query(oprations.Product).filter(oprations.Product.unique_id == product_id).first()

