from app.contact.repository import ContactRepository


class ContactService:

    @staticmethod
    def create_contact(data):
        try:
            if not data or "full_name" not in data or "email" not in data or "subject" not in data or "message" not in data:
                return {
                    "message": "Todos los campos son obligatorios."
                }, 400

            full_name = data.get("full_name")
            email = data.get("email")
            subject = data.get("subject")
            message = data.get("message")

            if full_name is None or not str(full_name).strip() or \
               email is None or not str(email).strip() or \
               subject is None or not str(subject).strip() or \
               message is None or not str(message).strip():
                return {
                    "message": "Todos los campos son obligatorios."
                }, 400

            contact_id = ContactRepository.create(full_name, email, subject, message)
            return {
                "message": "Mensaje de contacto enviado correctamente.",
                "contact_id": contact_id
            }, 201

        except Exception as e:
            return {
                "message": "Error al enviar el mensaje de contacto.",
                "error": str(e)
            }, 500
