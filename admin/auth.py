
import json
from typing import Optional
from fastapi import Depends, Request, Response
from sqladmin.authentication import AuthenticationBackend
from starlette.responses import RedirectResponse
from dependency_injector.wiring import inject, Provide
from src.auth.containers import Container
from src.auth.services.auth import AuthService


class AuthenticationAdmin(AuthenticationBackend):


    auth = False

    @inject
    async def login(self, request: Request, auth_service: AuthService = Depends(Provide[Container.auth_service])):
        form_data = await request.form()
        username = form_data.get('username')
        password = form_data.get('password')
        data = await auth_service.admin_token(username, password)
        self.auth = data
        return self.auth



    @inject
    async def authenticate(self, request: Request, auth_service: AuthService = Depends(Provide[Container.auth_service])) -> Optional[Response]:
        access = await auth_service.get_auth(request)
        print(access)
        if not self.auth:
            return RedirectResponse("/admin/login")


    async def logout(self, request: Request) -> bool:
        self.auth = False
        return RedirectResponse("/admin/login")

