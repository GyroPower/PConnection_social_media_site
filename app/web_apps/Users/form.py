from typing import List
from typing import Optional

from fastapi import Request


class create_user_form:
    def __init__(self, request: Request):
        self.request: Request = request
        self.email: Optional[str] = None
        self.username: Optional[str] = ""
        self.password: Optional[str] = None
        self.r_password: Optional[str] = None
        self.errors: List = []

    async def load_data(self):
        form = await self.request.form()
        self.email = form.get("email")
        self.password = form.get("password")
        self.r_password = form.get("r_password")

    async def is_valid(self):
        if not self.email or not (self.email.__contains__("@")):
            self.errors.append("Invalid email")
        if not self.password or not self.password == self.r_password:
            self.errors.append("Passwords are not the same")
        if not len(self.password) >= 4:
            self.errors.append("Password too short")
        if self.errors:
            return False
        return True
