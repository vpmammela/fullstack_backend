from fastapi import FastAPI, Depends
import uvicorn
from pydantic import BaseModel
from starlette import status

app = FastAPI()

class Test(BaseModel):
    test: str

@app.get('/api/v1/test', status_code=status.HTTP_200_OK, response_model=Test)
async def get_test_response():

    response_string = {'test': 'Tämä on testi stringi bäkendistä'}
    return response_string

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8001, reload=True)
