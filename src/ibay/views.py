from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import RedirectResponse
from config_fastapi.fastapi_mgr import templates
from src.auth.containers import Container
from src.auth.dependencies.jwt_aut import AutoModernJWTAuth
from src.auth.services.auth import AuthService

ibay_views = APIRouter()
user_profile = AutoModernJWTAuth()


@ibay_views.get('/ibay', include_in_schema=False)
@inject
async def profile(request: Request, auth_service: AuthService = Depends(Provide[Container.auth_service])):
    access = await auth_service.get_auth(request)
    if not access:
        return RedirectResponse("/auth_login")
    return templates.TemplateResponse(name='ibay.html', context={'request': request})