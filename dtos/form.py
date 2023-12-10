from pydantic import BaseModel


    # id = Column(INTEGER(11), primary_key=True)
    # createdAt = Column(DateTime, nullable=False)
    # closedAt = Column(DateTime)
    # user_id = Column(ForeignKey('user.id'), nullable=False, index=True)
    # environment_id = Column(ForeignKey('environment.id'), index=True)
    # inspectiontarget_id = Column(ForeignKey('inspectiontarget.id'), index=True)
    # inspectiontype_id = Column(ForeignKey('inspectiontype.id'), nullable=False, index=True)
    #
    # environment = relationship('Environment')
    # inspectiontarget = relationship('Inspectiontarget')
    # inspectiontype = relationship('Inspectiontype')
    # user = relationship('User')
    #
    # files = relationship('File')


class FormRes(BaseModel):
    id: int
    # createdAt: datetine.datetime
    # closedAt: Optional[datetine.datetine, None] = None
    # user: User
    # environment: Environment
    # inspectiontarget: Target
    # inspectiontype: InspectionType