from datetime import datetime
from app.movement.repository import MovementRepository
from app.category.repository import CategoryRepository


class MovementService:

    @staticmethod
    def get_movements(user_id):
        try:
            rows = MovementRepository.find_all(user_id)
            movements = []
            for row in rows:
                m_date = row[3]
                if m_date and hasattr(m_date, "strftime"):
                    formatted_date = m_date.strftime("%Y-%m-%d")
                else:
                    formatted_date = str(m_date) if m_date else ""

                movements.append({
                    "id": row[0],
                    "description": row[1],
                    "amount": float(row[2]) if row[2] is not None else 0.0,
                    "movement_date": formatted_date,
                    "category_id": row[4],
                    "category_name": row[5],
                    "type": row[6]
                })
            return movements, 200
        except Exception as e:
            return {
                "message": "Error al obtener los movimientos.",
                "error": str(e)
            }, 500

    @staticmethod
    def create_movement(user_id, data):
        try:
            if not data or "description" not in data or "amount" not in data or "movement_date" not in data or "category_id" not in data:
                return {
                    "message": "Todos los campos son obligatorios."
                }, 400

            description = data.get("description")
            amount = data.get("amount")
            movement_date = data.get("movement_date")
            category_id = data.get("category_id")

            if (description is None or not str(description).strip() or
                amount is None or
                movement_date is None or not str(movement_date).strip() or
                category_id is None):
                return {
                    "message": "Todos los campos son obligatorios."
                }, 400

            clean_date = str(movement_date).strip()
            try:
                datetime.strptime(clean_date, "%Y-%m-%d")
            except ValueError:
                return {
                    "message": "Todos los campos son obligatorios."
                }, 400

            try:
                amount_val = float(amount)
            except (ValueError, TypeError):
                return {
                    "message": "El monto debe ser mayor que cero."
                }, 400

            if amount_val <= 0:
                return {
                    "message": "El monto debe ser mayor que cero."
                }, 400

            category = CategoryRepository.find_by_id(category_id)
            if not category:
                return {
                    "message": "Categoría no encontrada."
                }, 404

            is_default = category[3]
            owner_id = category[4]

            if not is_default and owner_id != user_id:
                return {
                    "message": "Categoría no encontrada."
                }, 404

            MovementRepository.create(
                description=description.strip(),
                amount=amount_val,
                movement_date=clean_date,
                category_id=category_id,
                user_id=user_id
            )

            return {
                "message": "Movimiento creado correctamente."
            }, 201

        except Exception as e:
            return {
                "message": "Error al crear el movimiento.",
                "error": str(e)
            }, 500

    @staticmethod
    def update_movement(user_id, movement_id, data):
        try:
            if not data or "description" not in data or "amount" not in data or "movement_date" not in data or "category_id" not in data:
                return {
                    "message": "Todos los campos son obligatorios."
                }, 400

            description = data.get("description")
            amount = data.get("amount")
            movement_date = data.get("movement_date")
            category_id = data.get("category_id")

            if (description is None or not str(description).strip() or
                amount is None or
                movement_date is None or not str(movement_date).strip() or
                category_id is None):
                return {
                    "message": "Todos los campos son obligatorios."
                }, 400

            clean_date = str(movement_date).strip()
            try:
                datetime.strptime(clean_date, "%Y-%m-%d")
            except ValueError:
                return {
                    "message": "Todos los campos son obligatorios."
                }, 400

            try:
                amount_val = float(amount)
            except (ValueError, TypeError):
                return {
                    "message": "El monto debe ser mayor que cero."
                }, 400

            if amount_val <= 0:
                return {
                    "message": "El monto debe ser mayor que cero."
                }, 400

            movement = MovementRepository.find_by_id(movement_id)
            if not movement:
                return {
                    "message": "Movimiento no encontrado."
                }, 404

            movement_owner_id = movement[5]
            if movement_owner_id != user_id:
                return {
                    "message": "Movimiento no encontrado."
                }, 404

            category = CategoryRepository.find_by_id(category_id)
            if not category:
                return {
                    "message": "Categoría no encontrada."
                }, 404

            is_default = category[3]
            category_owner_id = category[4]

            if not is_default and category_owner_id != user_id:
                return {
                    "message": "Categoría no encontrada."
                }, 404

            MovementRepository.update(
                movement_id=movement_id,
                description=description.strip(),
                amount=amount_val,
                movement_date=clean_date,
                category_id=category_id
            )

            return {
                "message": "Movimiento actualizado correctamente."
            }, 200

        except Exception as e:
            return {
                "message": "Error al actualizar el movimiento.",
                "error": str(e)
            }, 500

    @staticmethod
    def delete_movement(user_id, movement_id):
        try:
            movement = MovementRepository.find_by_id(movement_id)
            if not movement:
                return {
                    "message": "Movimiento no encontrado."
                }, 404

            movement_owner_id = movement[5]
            if movement_owner_id != user_id:
                return {
                    "message": "Movimiento no encontrado."
                }, 404

            MovementRepository.delete(movement_id)

            return {
                "message": "Movimiento eliminado correctamente."
            }, 200

        except Exception as e:
            return {
                "message": "Error al eliminar el movimiento.",
                "error": str(e)
            }, 500
