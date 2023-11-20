from pydantic import BaseModel


class CreateLocationReq(BaseModel):
    name: str
    address: str
    zipcode: str
    city: str

class CreateLocationResp(BaseModel):
    id: int
    name: str

