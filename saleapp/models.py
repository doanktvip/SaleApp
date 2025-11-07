import json
from datetime import datetime
from enum import Enum as RoleEnum

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from saleapp import db, app


class UserEnum(RoleEnum):
    USER = 1,
    ADMIN = 2


class Base(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())

    def __str__(self):
        return self.name


class User(Base, UserMixin):
    username = Column(String(150), nullable=False, unique=True)
    password = Column(String(150), nullable=False)
    avatar = Column(String(150), default="https://cdn-icons-png.flaticon.com/512/6858/6858504.png")
    role = Column(Enum(UserEnum), default=UserEnum.USER)


class Category(Base):
    products = relationship('Product', backref="category", lazy=True)


class Product(Base):
    image = Column(String(300),
                   default="https://res.cloudinary.com/dy1unykph/image/upload/v1740037805/apple-iphone-16-pro-natural-titanium_lcnlu2.webp")
    price = Column(Float, default=0.0)
    cate_id = Column(Integer, ForeignKey(Category.id), nullable=False)


# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()
#         c1 = Category(name="Laptop")
#         c2 = Category(name="Mobile")
#         c3 = Category(name="Tablet")
#         db.session.add_all([c1, c2, c3])
#         db.session.commit()
#         with open("data/product.json", encoding="utf-8") as f:
#             products = json.load(f)
#             for p in products:
#                 db.session.add(Product(**p))
#         import hashlib
#
#         u = User(name="User", username="user", password=str(hashlib.md5("123".encode("utf-8")).hexdigest()))
#         db.session.add(u)
#         db.session.commit()
