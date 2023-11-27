from fastapi import APIRouter
from pydantic import BaseModel
from starlette import status

router = APIRouter()

class Test(BaseModel):
    test: str

@router.get('/api/v1/test', status_code=status.HTTP_200_OK, response_model=Test)
async def get_test_response():

    response_string = {'test': 'Tämä on testi stringi bäkendistä!!!!'}
    return response_string
