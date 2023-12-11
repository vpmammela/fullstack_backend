import models
from services.base_service import BaseService
from fastapi import Depends

class FileService(BaseService):
    
    def __init__(self, db: models.Db):
        super(FileService, self).__init__(db)
        
    def upload(self, form_id: int, original_name: str, random_name: str):
        file = models.File(inspectionform_id=form_id, original_name=original_name, random_name=random_name)
        self.db.add(file)
        self.db.commit()
        return True

    def download(self, inspectionform_id: int, file_id: int):
        file_record = self.db.query(models.File).filter(models.File.inspectionform_id == inspectionform_id, models.File.id == file_id).first()
        return file_record
