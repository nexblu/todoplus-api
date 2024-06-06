class EmailNotValid(Exception):
    def __init__(self, message="email not active"):
        self.message = message
        super().__init__(self.message)


class PasswordNotSecure(Exception):
    def __init__(self, message="password not secure"):
        self.message = message
        super().__init__(self.message)
