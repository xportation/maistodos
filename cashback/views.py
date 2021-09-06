
from fastapi import APIRouter

from cashback import schemas

router = APIRouter()


@router.post('/api/cashback', response_model=schemas.Order, status_code=201)
async def add_cashback(order: schemas.Order):
    return order
