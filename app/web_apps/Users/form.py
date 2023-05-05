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


class update_user:
    def __init__(self, request: Request):
        self.request: Request = request
        self.username: Optional[str] = None
        self.description: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()

        self.username = form.get("username")
        self.description = form.get("description")

    async def is_valid(self):
        if not self.username:
            return False
        return True


class change_email:
    def __init__(self, request: Request):
        self.request: Request = request
        self.new_email: Optional[str] = None
        self.password: Optional[str] = None
        self.errors: List = []

    async def load_data(self):
        form = await self.request.form()
        self.new_email = form.get("email")
        self.password = form.get("password")
        
    async def is_valid(self):
        if not self.new_email or not (self.new_email.__contains__("@")):
            self.errors.append("Write a valid email")
        if not self.password:
            self.errors.append("Password missed")
        if self.errors:
            return False
        return True

class change_password_form:
    def __init__(self,request:Request):
        self.request: Request = request 
        self.current_password: Optional[str] = None 
        self.new_password: Optional[str] = None 
        self.new_password2: Optional[str] = None 
        self.errors: List = []
        
    async def load_data(self):
        form = await self.request.form()
        self.current_password = form.get("password")
        self.new_password = form.get("new_password")
        self.new_password2 = form.get("new_password2")
    
    async def is_valid(self):
        if not self.current_password:
            self.errors.append("Necesary the current password")
        if not self.new_password == self.new_password2:
            self.errors.append("Passwords don't match")
        if self.errors:
            return False 
        return True 