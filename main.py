from fastapi import FastAPI
import uvicorn
from controllers import auth_controller, test_controller
from config.cors import configure_cors

app = FastAPI()
configure_cors(app)
app.include_router(auth_controller.router)
app.include_router(test_controller.router)


if __name__=='__main__':
    uvicorn.run('main:app', port=8001, reload=False)