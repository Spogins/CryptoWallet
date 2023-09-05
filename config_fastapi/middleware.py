# # Middleware для создания сессии пользователя
# from starlette.requests import Request
# from starlette.responses import RedirectResponse
#
# from config_fastapi.app import app
# from dependency_injector.wiring import inject, Provide
# from fastapi import Depends
# from src.auth.containers import Container
# from src.auth.services.auth import AuthService
#
#
# @app.middleware("http")
# async def add_current_user_to_context(request: Request, call_next, auth_service: AuthService = Depends(Provide[Container.auth_service])):
#     user = await auth_service.get_auth(request)
#     if not user:
#         return RedirectResponse(url="/auth_login")
#     request.state.user = user
#     response = await call_next(request)
#     return response