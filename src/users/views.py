from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from starlette.requests import Request
from starlette.responses import RedirectResponse
from config_fastapi.fastapi_mgr import templates
from src.auth.containers import Container as AuthContainer
from src.auth.dependencies.jwt_aut import AutoModernJWTAuth
from src.auth.services.auth import AuthService
from src.users.containers import Container as UserContainer
from src.users.services.user import UserService

user_views = APIRouter()

user_auth = AutoModernJWTAuth()


@user_views.get('/', include_in_schema=False)
@inject
async def profile(request: Request, auth_service: AuthService = Depends(Provide[AuthContainer.auth_service])):
    auth = await auth_service.get_auth(request)
    if not auth:
        return RedirectResponse(url="/auth_login")
    return templates.TemplateResponse(name='index.html', context={'request': request})


@user_views.get('/profile', include_in_schema=False)
@inject
async def profile(request: Request, user_service: UserService = Depends(Provide[UserContainer.user_service]),
                  auth_service: AuthService = Depends(Provide[AuthContainer.auth_service])):
    auth_user = await auth_service.get_auth(request)
    if not auth_user:
        return RedirectResponse(url="/auth_login")

    return templates.TemplateResponse(name='profile.html', context={'request': request, 'user': auth_user})
