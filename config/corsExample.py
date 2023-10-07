# create cors.py file with following lines:

from fastapi.middleware.cors import CORSMiddleware
#
# origins = [
#     "",  # Update with the actual origin of your React app
# ]
#
# def configure_cors(app):
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=origins,
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )