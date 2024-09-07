from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base

class Product(Base):
    __tablename__ = "products"
    unique_id=Column(String, index=True)
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    serial_number = Column(String, index=True)
    images_urls= Column(String, index=True)
    output_urls= Column(String, index=True)
    

# class Image(Base):
#     __tablename__ = "images"

#     id = Column(Integer, primary_key=True, index=True)
#     input_url = Column(String, index=True)
#     output_url = Column(String, index=True)
#     product_id = Column(Integer, ForeignKey("products.id"))

#     product = relationship("Product", back_populates="images")
