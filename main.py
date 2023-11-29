from fastapi import FastAPI
import os
import uvicorn
from h11 import Request
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles

import fullstack_token
import models
from controllers import auth_controller, test_controller, location_controller
from config.cors import configure_cors
from dotenv import load_dotenv
from fastapi import HTTPException
from typing import List

app = FastAPI()

configure_cors(app)
app.include_router(auth_controller.router)
app.include_router(test_controller.router)
app.include_router(location_controller.router)

app.mount("/", StaticFiles(directory="static"), name="static")
models.metadata.create_all(bind=models.engine)

#Checking the correctness of the csrf token in every request except get and head
@app.middleware("http")
async def check_csrf(request: Request, call_next):
    if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:

        if str(request.url).find('login') == -1 and str(request.url).find('register') == -1: #Check all URLs except for the login and register.
            try:

                _token = fullstack_token.token.init_token()
                csrf = _token.validate(request.cookies.get('csrf_token_cookie'))
                access = _token.validate(request.cookies.get('access_token_cookie'))
                if csrf is None or access is None:
                    return JSONResponse(content={'err': 'forbidden'}, status_code=403)
                if csrf['sub'] != access['csrf']:
                    return JSONResponse(content={'err': 'forbidden'}, status_code=403)
            except Exception as e:
                return JSONResponse(content={'err': 'forbidden'}, status_code=403)
    response = await call_next(request)
    return response
'''
# Define a route to get reports
@app.get("/reports", response_model=List[models.Report])
async def get_reports():
    # TODO: Replace with actual logic to fetch reports from database.
    reports = models.get_reports() 
    return reports
'''

if __name__=='__main__':
    load_dotenv()
    if os.getenv('SSL') == '0':
        uvicorn.run('main:app', port=8001, reload=False)
    elif os.getenv('SSL') == '1':
        uvicorn.run('main:app', port=8001, reload=False, ssl_keyfile='./cert/CA/localhost/localhost.decrypted.key',
                    ssl_certfile='./cert/CA/localhost/localhost.crt')


'''''
# https://www.section.io/engineering-education/how-to-get-ssl-https-for-localhost/?fbclid=IwAR1uk5NY4TTLg4MpnMMwYMLB6hB7tjjkBlcvAzZhAjyuybhlcNa3o1eRPZ8
import models
from fastapi.staticfiles import StaticFiles

from fastapi import FastAPI
import os
import uvicorn
from controllers import auth_controller, test_controller, location_controller
from config.cors import configure_cors
from dotenv import load_dotenv

app = FastAPI()
configure_cors(app)
app.include_router(auth_controller.router)
app.include_router(test_controller.router)
app.include_router(location_controller.router)

app.mount("/", StaticFiles(directory="static"), name="static")

models.metadata.create_all(bind=models.engine)

if __name__=='__main__':
    #load_dotenv()
    if os.getenv('SSL') == '0':
        uvicorn.run('main:app', port=8001, reload=False)
    elif os.getenv('SSL') == '1':
        uvicorn.run('main:app', port=8001, reload=False, ssl_keyfile='./cert/CA/localhost/localhost.decrypted.key',
                    ssl_certfile='./cert/CA/localhost/localhost.crt')

'''''