import dtos.location
import models
from services.base_service import BaseService

class LocationService(BaseService):
    def __init__(self, db: models.Db):
        super(LocationService, self).__init__(db)

    def create(self, req: dtos.location.CreateLocationReq):
        location = models.Location(
            name=req.name,
            address=req.address,
            zip_code=req.zipcode,
            city=req.city,
        )

        self.db.add(location)
        self.db.commit()

        return location

    def get_all(self):
        locations = self.db.query(models.Location).all()
        return locations
