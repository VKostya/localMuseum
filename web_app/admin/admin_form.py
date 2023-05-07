from typing import List
from typing import Optional

from fastapi import Request


class MuseumCreateForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.title: Optional[str] = None
        self.description: Optional[str] = None
        self.contact_url: Optional[str] = None
        self.address: Optional[str] = None
        self.ticket_price: Optional[float] = None
        self.schedule: Optional[str] = None
        self.manager_id: Optional[int] = None

    async def load_data(self):
        form = await self.request.form()
        self.title = form.get("title")
        self.description = form.get("description")
        self.contact_url = form.get("contact_url")
        self.address = form.get("address")
        self.ticket_price = form.get("ticket_price")
        self.schedule = form.get("schedule")
        self.manager_id = form.get("manager_id")

    def is_valid(self):
        if not self.title or not len(self.title) >= 4:
            self.errors.append("A valid title is required")
        if not self.contact_url or not (self.contact_url.__contains__("http")):
            self.errors.append("Valid Url is required e.g. https://example.com")
        if not self.address:
            self.errors.append("A valid company is required")
        if not self.description or not len(self.description) >= 20:
            self.errors.append("Description too short")
        if not self.errors:
            return True
        return False


class UserRoleForm:
    def __init__(self, request):
        self.request: Request = request
        self.errors: List = []
        self.role: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.role = form.get("role")

    def is_valid(self):
        if not self.role:
            self.errors.append("A valid role is required")
        if not self.errors:
            return True
        return False
