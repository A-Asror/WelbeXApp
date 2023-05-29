import fastapi

from fastapi import status, Depends, Query

from src.api.dependencies.repository import get_repository
from src.repository.crud.cargo import *
from src.models import schemas


router = fastapi.APIRouter(prefix="/cargo", tags=["cargo"])


@router.post(
    '',
    name='transport:create_cargo',
    response_model=schemas.CargoOutMainInfoSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_cargo(
    payload: schemas.CargoInCreateSchema,
    cargo_repo: CargoCRUDRepository = Depends(get_repository(repo_type=CargoCRUDRepository)),
):
    return await cargo_repo.create_cargo(instance=payload)


@router.delete('', name='transport:delete_cargo', status_code=status.HTTP_200_OK)
async def create_cargo(
    pk: int,
    cargo_repo: CargoCRUDRepository = Depends(get_repository(repo_type=CargoCRUDRepository)),
):
    return await cargo_repo.delete_by_id(cargo_id=pk)


@router.patch(
    '',
    name='transport:delete_cargo',
    response_model=schemas.CargoOutMainInfoSchema,
    status_code=status.HTTP_200_OK
)
async def update_cargo(
    pk: int,
    payload: schemas.CargoInUpdateSchema,
    cargo_repo: CargoCRUDRepository = Depends(get_repository(repo_type=CargoCRUDRepository))
):

    return await cargo_repo.update_by_id(cargo_id=pk, payload=payload)


@router.get(
    '',
    response_model=list[schemas.CargoOutListMinInfoSchema],
    status_code=status.HTTP_200_OK
)
async def read_cargo_many(
    page: int = Query(default=1, ge=1),
    cargo_repo: CargoCRUDRepository = Depends(get_repository(repo_type=CargoCRUDRepository))
):
    return await cargo_repo.read_all_cargo(page=page)


@router.get(
    '/{cargo_id}',
    response_model=schemas.CargoInfoOutSchema,
    response_model_exclude={'transports': {"__all__": {'location_lat', 'location_lng'}}},
    status_code=status.HTTP_200_OK
)
async def read_cargo_many(
    cargo_id: int,
    cargo_repo: CargoCRUDRepository = Depends(get_repository(repo_type=CargoCRUDRepository))
):
    cargo = await cargo_repo.read_by_id(cargo_id=cargo_id)
    transports = await cargo_repo.read_all_transports()

    response = schemas.CargoInfoOutSchema(
        id=cargo.id,
        pick_up_post_code=cargo.pick_up_post_code,
        delivery_post_code=cargo.delivery_post_code,
        weight=cargo.weight,
        description=cargo.description,
        transports=transports
    )
    response.distance(lat=cargo.pick_up_lat, lng=cargo.pick_up_lng)
    return response


@router.get(
    '/filter/',
    response_model=list[schemas.CargoFilterByRadiusWeightOutSchema],
    response_model_exclude={'transports': {"__all__": {'location_lat', 'location_lng'}}},
    status_code=status.HTTP_200_OK
)
async def read_cargo_filter(
    query: schemas.CargoInQueryParamsSchema = Depends(),
    cargo_repo: CargoCRUDRepository = Depends(get_repository(repo_type=CargoCRUDRepository))
):

    return await cargo_repo.filter_by_radius_and_weight(radius=query.radius, weight=query.weight, page=query.page)
