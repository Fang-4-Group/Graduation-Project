from datetime import datetime

from pydantic import BaseModel


# Define the structure of group messages
class MsgDetail(BaseModel):
    UserName: str
    MsgText: str
    Time: datetime
