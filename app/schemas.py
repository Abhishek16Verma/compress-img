from pydantic import BaseModel



class ProductBase(BaseModel):
    unique_id: str
    name: str
    serial_number: str
    image_urls: str
    output_urls: str



class Product(ProductBase):
    unique_id: str
    name: str
    serial_number: str
    image_urls: str
    output_urls: str

    class Config:
        orm_mode = True
