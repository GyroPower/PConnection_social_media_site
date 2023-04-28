from typing import List
from typing import Optional

from fastapi import Request


class form_login_user:
    def __init__(self, request: Request):
        self.request: Request = request
        self.username: Optional[str] = None
        self.password: Optional[str] = None
        self.errors: List = None

    async def load_data(self):
        form = await self.request.form()

        self.username = form.get("email")
        self.password = form.get("password")
        self.errors = []

    async def is_valid(self):
        if not self.username or not (self.username.__contains__("@")):
            self.errors.append("Introduce a valid email")
        if not self.password:
            self.errors.append("Introduce a password")
        if self.errors:
            return False
        return True
