from flask import request, g
from app.category.service import CategoryService


def get_categories():
    return CategoryService.get_categories(g.user_id)


def create_category():
    data = request.get_json()
    return CategoryService.create_category(g.user_id, data)


def update_category(category_id):
    data = request.get_json()
    return CategoryService.update_category(g.user_id, category_id, data)


def delete_category(category_id):
    return CategoryService.delete_category(g.user_id, category_id)
