from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from config_fastapi.fastapi_mgr import templates
from src.auth.containers import Container
from src.auth.dependencies.jwt_aut import AutoModernJWTAuth
from src.auth.services.auth import AuthService

auth_views = APIRouter()
user_auth = AutoModernJWTAuth()


@auth_views.get('/auth_login', include_in_schema=False)
@inject
async def auth_login(request: Request, auth_service: AuthService = Depends(Provide[Container.auth_service])):
    access = await auth_service.get_auth(request)
    if access:
        return RedirectResponse("/profile")
    return templates.TemplateResponse(name='auth_login.html', context={'request': request})


@auth_views.get('/registration', include_in_schema=False)
@inject
async def registration(request: Request, auth_service: AuthService = Depends(Provide[Container.auth_service])):
    access = await auth_service.get_auth(request)
    if access:
        return RedirectResponse("/profile")
    return templates.TemplateResponse(name='registration.html', context={'request': request})
