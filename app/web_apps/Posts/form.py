from typing import Optional

from fastapi import Request


class post_form:
    def __init__(self, request: Request):
        self.request: Request = request
        self.content: Optional[str] = ""
        self.media: Optional[str] = ""

    async def load_data(self):

        form = await self.request.form()
        self.content = form.get("content")
        self.media = form.get("media")

    async def validate_data(self):
        if self.content and self.media == "":
            return False
        return True
