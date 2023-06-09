from typing import List
from typing import Optional

from fastapi import Request


class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get("email")
        self.password = form.get("password")

    async def is_valid(self):
        if not self.username or not (self.username.__contains__("@")):
            self.errors.append("email is required")
        if not self.password:
            self.errors.append("A valid password is required")
        if not self.errors:
            return True
        return False


class RegisterForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.username: Optional[str] = None
        self.password: Optional[str] = None
        self.repeated_password: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get("email")
        self.password = form.get("password")
        self.repeated_password = form.get("repeated_password")

    async def is_valid(self):
        if not self.username or not (self.username.__contains__("@")):
            self.errors.append("неверный формат - требуется действительный email")
        if not self.password:
            self.errors.append("Введите пароль")
        if not self.password == self.repeated_password:
            self.errors.append("Пароли должны совпадать")
        if not self.errors:
            return True
        return False

