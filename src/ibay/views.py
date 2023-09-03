from dependency_injector.wiring import inject, Provide
from fast_depends.dependencies import Depends
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse
from config_fastapi.fastapi_mgr import templates
from src.auth.containers import Container
from src.auth.dependencies.jwt_aut import AutoModernJWTAuth
from src.auth.services.auth import AuthService

ibay_views = APIRouter()
user_profile = AutoModernJWTAuth()


@ibay_views.get('/ibay', include_in_schema=False)
@inject
async def profile(request: Request):
    return templates.TemplateResponse(name='ibay.html', context={'request': request})