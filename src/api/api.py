from fastapi import APIRouter

from src.api.endpoints import (
    users,
    nas,
    radacct,
    radgroupreply,
    radgroupcheck,
    radusergroup,
    radreply,
)

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(nas.router, prefix="/nas", tags=["nas"])
api_router.include_router(radacct.router, prefix="/radacct", tags=["radacct"])
api_router.include_router(radgroupreply.router, prefix="/radgroupreply", tags=["radgroupreply"])
api_router.include_router(radgroupcheck.router, prefix="/radgroupcheck", tags=["radgroupcheck"])
api_router.include_router(radusergroup.router, prefix="/radusergroup", tags=["radusergroup"])
api_router.include_router(radreply.router, prefix="/radreply", tags=["radreply"])
