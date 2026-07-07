from flask import Blueprint
from app.category.controller import get_categories, create_category, update_category, delete_category
from app.middleware.auth_middleware import login_required


category_bp = Blueprint("categories", __name__, url_prefix="/api/categories")


@category_bp.route("", methods=["GET"])
@login_required
def get_categories_route():
    return get_categories()


@category_bp.route("", methods=["POST"])
@login_required
def create_category_route():
    return create_category()


@category_bp.route("/<int:category_id>", methods=["PUT"])
@login_required
def update_category_route(category_id):
    return update_category(category_id)


@category_bp.route("/<int:category_id>", methods=["DELETE"])
@login_required
def delete_category_route(category_id):
    return delete_category(category_id)
