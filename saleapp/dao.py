import json
from models import Category, Product


def load_categories():
    return Category.query.all()


def load_products(q=None, cate_id=None):
    query = Product.query

    if q:
        query = query.filter(Product.name.contains(q))

    if cate_id:
        query = query.filter(Product.cate_id.__eq__(cate_id))

    return query.all()


def count_product():
    return Product.query.count()


def get_product_by_id(id):
    return Product.query.get(id)
