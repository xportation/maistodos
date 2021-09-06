
from fastapi import APIRouter

from cashback import schemas

router = APIRouter()


@router.get('/')
async def hello_world():
    return {'Hello': 'World'}


@router.post('/api/cashback', response_model=schemas.Order, status_code=201)
async def add_cashback(order: schemas.Order):
    return order
