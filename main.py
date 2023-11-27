from fastapi import FastAPI
import os
import uvicorn
from h11 import Request
from starlette.responses import JSONResponse

import fullstack_token
from controllers import auth_controller, test_controller, location_controller
from config.cors import configure_cors
from dotenv import load_dotenv

app = FastAPI()

configure_cors(app)
app.include_router(auth_controller.router)
app.include_router(test_controller.router)
app.include_router(location_controller.router)

#Checking the correctness of the csrf token in every request except get and head
@app.middleware("http")
async def check_csrf(request: Request, call_next):
    response = await call_next(request)
    if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
        if str(request.url).find('login') == -1:  #Check all URLs except for the login.
            try:
                _token = fullstack_token.token.init_token()
                csrf = _token.validate(request.cookies.get('csrf_token_cookie'))
                access = _token.validate(request.cookies.get('access_token_cookie'))
                if csrf is None or access is None:
                    return JSONResponse(content={'err': 'forbidden'}, status_code =403)
                if csrf['sub'] != access['csrf']:
                    return JSONResponse(content={'err': 'forbidden'}, status_code=403)
            except Exception as e:
                return JSONResponse(content={'err': 'forbidden'}, status_code=403)
    return response



if __name__=='__main__':
    load_dotenv()
    if os.getenv('SSL') == '0':
        uvicorn.run('main:app', port=8001, reload=False)
    elif os.getenv('SSL') == '1':
        uvicorn.run('main:app', port=8001, reload=False, ssl_keyfile='./cert/CA/localhost/localhost.decrypted.key',
                    ssl_certfile='./cert/CA/localhost/localhost.crt')
