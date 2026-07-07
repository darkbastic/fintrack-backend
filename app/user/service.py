import bcrypt
from app.user.repository import UserRepository
from app.common.jwt_service import JwtService

class UserService:

    @staticmethod
    def register(data):
        try:
            user = UserRepository.find_by_email(data["email"])

            if user:
                return {
                    "message": "El correo ya está registrado."
                }, 409

            password = bcrypt.hashpw(
                data["password"].encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")

            user_id = UserRepository.create(
                data["name"],
                data["lastname"],
                data["email"],
                password
            )

            return {
                "message": "Usuario registrado correctamente.",
                "user_id": user_id
            }, 201
        except Exception as e:
            return {
                "message": "Error al registrar el usuario.",
                "error": str(e)
            }, 500
        
    @staticmethod
    def login(data):
        try:
            user = UserRepository.find_by_email(data["email"])

            if not user:
                return {
                    "message": "Correo o contraseña incorrectos."
                }, 401

            password_correct = bcrypt.checkpw(
                data["password"].encode("utf-8"),
                user[4].encode("utf-8")
            )

            if not password_correct:
                return {
                    "message": "Correo o contraseña incorrectos."
                }, 401

            token = JwtService.generate_token(user[0])
            return {
                "message": "Inicio de sesión exitoso.",
                "token": token
            }, 200
        except Exception as e:
            return {
                "message": "Error al iniciar sesión.",
                "error": str(e)
            }, 500

    @staticmethod
    def get_profile(user_id):
        try:
            user = UserRepository.find_by_id(user_id)
            if not user:
                return {
                    "message": "Usuario no encontrado."
                }, 404

            return {
                "id": user[0],
                "name": user[1],
                "lastname": user[2],
                "email": user[3]
            }, 200
        except Exception as e:
            return {
                "message": "Error al obtener el perfil.",
                "error": str(e)
            }, 500

    @staticmethod
    def update_profile(user_id, data):
        try:
            if not data or "name" not in data or "lastname" not in data:
                return {
                    "message": "Faltan campos requeridos."
                }, 400

            user = UserRepository.find_by_id(user_id)
            if not user:
                return {
                    "message": "Usuario no encontrado."
                }, 404

            UserRepository.update_profile(user_id, data["name"], data["lastname"])
            return {
                "message": "Perfil actualizado correctamente."
            }, 200
        except Exception as e:
            return {
                "message": "Error al actualizar el perfil.",
                "error": str(e)
            }, 500

    @staticmethod
    def update_password(user_id, data):
        try:
            if not data or "current_password" not in data or "new_password" not in data:
                return {
                    "message": "Faltan campos requeridos."
                }, 400

            user = UserRepository.find_by_id(user_id)
            if not user:
                return {
                    "message": "Usuario no encontrado."
                }, 404

            password_correct = bcrypt.checkpw(
                data["current_password"].encode("utf-8"),
                user[4].encode("utf-8")
            )

            if not password_correct:
                return {
                    "message": "La contraseña actual es incorrecta."
                }, 400

            hashed_password = bcrypt.hashpw(
                data["new_password"].encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")

            UserRepository.update_password(user_id, hashed_password)
            return {
                "message": "Contraseña actualizada correctamente."
            }, 200
        except Exception as e:
            return {
                "message": "Error al actualizar la contraseña.",
                "error": str(e)
            }, 500