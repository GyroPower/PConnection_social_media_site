from typing import List
from typing import Optional

from fastapi import Request


class form_comment:
    def __init__(self, request: Request):
        self.request: Request = request
        self.content: Optional[str] = None
        self.errors: List = []

    async def load_data(self):
        form = await self.request.form()

        self.content = form.get("content")

    async def validate_data(self):
        if self.content == "":
            self.errors.append("can't comment a empty comment")
        if not self.errors:
            return True
        return False
