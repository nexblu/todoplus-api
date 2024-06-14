class Miscellaneous:
    @staticmethod
    async def validate_register(username, email, password, confirm_password):
        errors = {}
        if not username or username.isspace():
            errors["username"] = "username is empty"
        if not email or email.isspace():
            errors["email"] = "email is empty"
        if not password or password.isspace():
            errors["password"] = "password is empty"
        if not confirm_password or confirm_password.isspace():
            errors["confirm_password"] = "confirm password is empty"
        if password != confirm_password:
            errors["password_match"] = "password and confirm password are not the same"
        return errors

    @staticmethod
    async def validate_task(task, tags):
        errors = {}
        if not task or task.isspace():
            errors["task"] = "task is empty"
        if not isinstance(tags, list):
            errors["tags"] = "tags must be array"
        else:
            if not tags or len(tags) == 0:
                errors["password"] = "password is empty"
        return errors
