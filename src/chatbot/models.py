from datetime import datetime

from pydantic import BaseModel


class MsgDetail(BaseModel):
    MsgText: str
    UserName: str
    Time: datetime
