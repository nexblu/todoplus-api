class EmailNotValid(Exception):
    def __init__(self, message="email not active"):
        self.message = message
        super().__init__(self.message)


class PasswordNotSecure(Exception):
    def __init__(self, message="password not secure"):
        self.message = message
        super().__init__(self.message)


class UserNotFound(Exception):
    def __init__(self, message="user not found"):
        self.message = message
        super().__init__(self.message)


class TaskNotFound(Exception):
    def __init__(self, message="task not found"):
        self.message = message
        super().__init__(self.message)


class CommentNotFound(Exception):
    def __init__(self, message="comment not found"):
        self.message = message
        super().__init__(self.message)
