from app.category.repository import CategoryRepository


class CategoryService:

    @staticmethod
    def get_categories(user_id):
        try:
            rows = CategoryRepository.find_all(user_id)
            categories = []
            for row in rows:
                categories.append({
                    "id": row[0],
                    "name": row[1],
                    "type": row[2],
                    "is_default": row[3]
                })
            return categories, 200
        except Exception as e:
            return {
                "message": "Error al obtener las categorías.",
                "error": str(e)
            }, 500

    @staticmethod
    def create_category(user_id, data):
        try:
            if not data or "name" not in data or "type" not in data:
                return {
                    "message": "Todos los campos son obligatorios."
                }, 400

            name = data.get("name")
            category_type = data.get("type")

            if name is None or not str(name).strip():
                return {
                    "message": "Todos los campos son obligatorios."
                }, 400

            if category_type not in ["income", "expense"]:
                return {
                    "message": "Tipo de categoría inválido."
                }, 400

            # Check for duplicate category (either default or owned by user)
            existing = CategoryRepository.find_by_name_and_type(name, category_type, user_id)
            if existing:
                return {
                    "message": "La categoría ya existe."
                }, 409

            CategoryRepository.create(name, category_type, False, user_id)
            return {
                "message": "Categoría creada correctamente."
            }, 201

        except Exception as e:
            return {
                "message": "Error al crear la categoría.",
                "error": str(e)
            }, 500

    @staticmethod
    def update_category(user_id, category_id, data):
        try:
            if not data or "name" not in data or "type" not in data:
                return {
                    "message": "Todos los campos son obligatorios."
                }, 400

            name = data.get("name")
            category_type = data.get("type")

            if name is None or not str(name).strip():
                return {
                    "message": "Todos los campos son obligatorios."
                }, 400

            if category_type not in ["income", "expense"]:
                return {
                    "message": "Tipo de categoría inválido."
                }, 400

            # Check if category exists
            category = CategoryRepository.find_by_id(category_id)
            if not category:
                return {
                    "message": "Categoría no encontrada."
                }, 404

            # Columns: id, name, type, is_default, user_id
            is_default = category[3]
            owner_id = category[4]

            if is_default:
                return {
                    "message": "No se pueden modificar categorías por defecto."
                }, 403

            if owner_id != user_id:
                return {
                    "message": "Categoría no encontrada."
                }, 404

            # Check if updated category name/type duplicates another existing category
            existing = CategoryRepository.find_by_name_and_type(name, category_type, user_id)
            if existing and existing[0] != category_id:
                return {
                    "message": "La categoría ya existe."
                }, 409

            CategoryRepository.update(category_id, name, category_type)
            return {
                "message": "Categoría actualizada correctamente."
            }, 200

        except Exception as e:
            return {
                "message": "Error al actualizar la categoría.",
                "error": str(e)
            }, 500

    @staticmethod
    def delete_category(user_id, category_id):
        try:
            # Check if category exists
            category = CategoryRepository.find_by_id(category_id)
            if not category:
                return {
                    "message": "Categoría no encontrada."
                }, 404

            # Columns: id, name, type, is_default, user_id
            is_default = category[3]
            owner_id = category[4]

            if is_default:
                return {
                    "message": "No se pueden eliminar categorías por defecto."
                }, 403

            if owner_id != user_id:
                return {
                    "message": "Categoría no encontrada."
                }, 404

            CategoryRepository.delete(category_id)
            return {
                "message": "Categoría eliminada correctamente."
            }, 200

        except Exception as e:
            return {
                "message": "Error al eliminar la categoría.",
                "error": str(e)
            }, 500
