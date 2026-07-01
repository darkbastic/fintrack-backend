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