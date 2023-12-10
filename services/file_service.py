import models
from services.base_service import BaseService
from typing import Annotated
from fastapi import Depends

class FileService(BaseService):
    
    def __init__(self, db: models.Db):
        super(FileService, self).__init__(db)
        
    def upload(self, form_id: int, original_name: str, random_name: str):
        file = models.File(inspectionform_id=form_id, original_name=original_name, random_name=random_name)
        self.db.add(file)
        self.db.commit()
        return True
    
def init_file_service(db: models.Db):
    return FileService(db)

FileService = Annotated[FileService, Depends(init_file_service)]
