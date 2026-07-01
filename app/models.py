from sqlalchemy import Column, Integer, String, Float
from app.database import Base  # ✅ تغيير هنا

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0.0)

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', quantity={self.quantity}, price={self.price})>"