import math
from flask import render_template, request, redirect
from flask_login import login_user, current_user

import dao
from saleapp import app, login_manager


@app.route("/")
def index():
    q = request.args.get("q")
    cate_id = request.args.get("cate_id")
    page = request.args.get("page")
    prods = dao.load_products(q=q, cate_id=cate_id, page=page)
    pages = math.ceil(dao.count_product() / app.config["PAGE_SIZE"])
    return render_template("index.html", prods=prods, pages=pages)


@app.route("/products/<int:id>")
def details(id):
    prod = dao.get_product_by_id(id)
    return render_template("product-details.html", prod=prod)


@app.context_processor
def common_attribute():
    return {
        "cates": dao.load_categories()
    }


@app.route("/login", methods=["GET", "POST"])
def login():
    err_msg = None
    if current_user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = dao.login(username, password)
        if user:
            login_user(user)
            return redirect("/")
        else:
            err_msg = "Tài khoản không chính xác"
    return render_template("login.html",err_msg=err_msg)


@login_manager.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)
