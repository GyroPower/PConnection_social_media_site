from typing import Optional

from fastapi import Request
from fastapi import UploadFile


class post_form:
    def __init__(self, request: Request):
        self.request: Request = request
        self.content: Optional[str] = ""
        self.media: Optional[UploadFile] = None 

    async def load_data(self):

        form = await self.request.form()
        self.content = form.get("content")
        self.media = form.get("file")
        print(self.media.filename)

    async def validate_data(self):
        if self.content == "" and self.media.filename == "":
            return False
        return True
