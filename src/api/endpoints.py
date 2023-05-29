import fastapi

from .routes import cargo_router

router = fastapi.APIRouter()


router.include_router(router=cargo_router)
