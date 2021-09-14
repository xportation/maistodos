from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from cashback import schemas, services
from cashback.di import Container

router = APIRouter()


@router.post('/api/cashback', response_model=schemas.Cashback, status_code=201)
@inject
async def add_cashback(
        order: schemas.Order,
        cashback_service: services.CashbackService = Depends(Provide[Container.cashback_service])
):
    return cashback_service.create_cashback(order.dict())
