from flask import redirect
from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_admin.theme import Bootstrap4Theme
from flask_login import current_user, logout_user
from saleapp import app, db
from models import Category, Product, UserEnum
from wtforms import TextAreaField
from wtforms.widgets import TextArea


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class AuthenticatedView(ModelView):
    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.role == UserEnum.ADMIN


class MyCategoryView(AuthenticatedView):
    column_list = ['name', 'products']
    column_searchable_list = ['name']
    column_labels = {
        'name': "Tên loại",
        'products': 'Danh sách sản phẩm'
    }


class MyProductView(AuthenticatedView):
    column_list = ['name', 'price', 'description', 'category']
    column_searchable_list = ['name', 'price']
    column_labels = {
        'name': 'Tên sản phẩm',
        'price': 'Giá sản phẩm',
        'description': 'Mô tả',
        'category': "Loại sản phẩm"
    }
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']

    form_overrides = {
        'description': CKTextAreaField
    }


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self) -> str:
        return self.render('admin/index.html')


class MyAdminLogoutView(BaseView):
    @expose('/')
    def index(self) -> str:
        logout_user()
        return redirect('/admin')

    def is_accessible(self) -> bool:
        return current_user.is_authenticated

class StatsView(BaseView):
    @expose('/')
    def index(self) -> str:
        return self.render('admin/stats.html')

admin = Admin(app=app, name="E-COMMERCE", theme=Bootstrap4Theme(), index_view=MyAdminIndexView())

admin.add_view(MyCategoryView(Category, db.session))
admin.add_view(MyProductView(Product, db.session))
admin.add_view((StatsView("Thống kế")))
admin.add_view((MyAdminLogoutView("Đăng xuất")))
