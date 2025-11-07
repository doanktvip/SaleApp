import hashlib
from models import Category, Product, User
from saleapp import app


def load_categories():
    return Category.query.all()


def load_products(q=None, cate_id=None, page=None):
    query = Product.query
    if q:
        query = query.filter(Product.name.__eq__(q))
    if cate_id:
        query = query.filter(Product.cate_id.__eq__(cate_id))
    if page:
        size = app.config["PAGE_SIZE"]
        start = (int(page) - 1) * size
        end = start + size
        query = query.slice(start, end)
    return query.all()


def count_product():
    return Product.query.count()


def get_product_by_id(id):
    return Product.query.get(id)


def login(username, password):
    password = str(hashlib.md5(password.encode("utf-8")).hexdigest())
    return User.query.filter(User.username.__eq__(username) or User.password.__eq__(password)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)
