from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import RedirectResponse
from config_fastapi.fastapi_mgr import templates
from src.auth.containers import Container
from src.auth.dependencies.jwt_aut import AutoModernJWTAuth
from src.auth.services.auth import AuthService


chat_views = APIRouter()
user_profile = AutoModernJWTAuth()
asyncapi_views_router = APIRouter()


@chat_views.get('/chat', include_in_schema=False)
@inject
async def chat(request: Request, auth_service: AuthService = Depends(Provide[Container.auth_service])):
    access = await auth_service.get_auth(request)
    if not access:
        return RedirectResponse("/auth_login")
    return templates.TemplateResponse(name='chat.html', context={'request': request})


@asyncapi_views_router.get('/asyncapi_docs')
@inject
async def asyncapi_docs(request: Request, auth_service: AuthService = Depends(Provide[Container.auth_service])):
    access = await auth_service.get_auth(request)
    if not access:
        return RedirectResponse("/auth_login")
    return templates.TemplateResponse('asyncapi/index.html', context={"request": request})