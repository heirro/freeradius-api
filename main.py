from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.api.endpoints import (
    nas_router,
    radgroupreply_router,
    radgroupcheck_router,
    radreply_router,
    radusergroup_router,
    users_router,
    disconnect_router,
)
from src.api.endpoints.radacct import router as radacct_router
from src.api.endpoints.auth import get_current_username
from src.core.config import get_settings

settings = get_settings()
security = HTTPBasic()

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.APP_DEBUG,
    docs_url=None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"hello": "world"}


app.include_router(users_router, prefix="/api/v1", tags=["users"])
app.include_router(radusergroup_router, prefix="/api/v1", tags=["radusergroup"])
app.include_router(radgroupreply_router, prefix="/api/v1", tags=["radgroupreply"])
app.include_router(radgroupcheck_router, prefix="/api/v1", tags=["radgroupcheck"])
app.include_router(radreply_router, prefix="/api/v1", tags=["radreply"])
app.include_router(nas_router, prefix="/api/v1", tags=["nas"])
app.include_router(radacct_router, prefix="/api/v1/radacct", tags=["radacct"])
app.include_router(disconnect_router, prefix="/api/v1", tags=["disconnect"])


@app.get("/docs", include_in_schema=False)
async def get_documentation(credentials: HTTPBasicCredentials = Depends(security)):
    if not get_current_username(credentials):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=settings.APP_NAME + " - Swagger UI",
        oauth2_redirect_url="/docs/oauth2-redirect",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui.css",
    )


@app.get("/openapi.json", include_in_schema=False)
async def get_openapi_endpoint(credentials: HTTPBasicCredentials = Depends(security)):
    if not get_current_username(credentials):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return get_openapi(
        title=settings.APP_NAME,
        version="1.0.0",
        description="API documentation",
        routes=app.routes,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
