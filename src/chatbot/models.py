from datetime import datetime

from pydantic import BaseModel


# Define the structure of message records
class MsgDetail(BaseModel):
    UserName: str
    MsgText: str
    Time: datetime
