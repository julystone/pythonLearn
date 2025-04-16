#  _____            ___             ____     __
# /\___ \          /\_ \           /\  _`\  /\ \__
# \/__/\ \   __  __\//\ \    __  __\ \,\L\_\\ \ ,_\    ___     ___       __
#    _\ \ \ /\ \/\ \ \ \ \  /\ \/\ \\/_\__ \ \ \ \/   / __`\ /' _ `\   /'__`\
#   /\ \_\ \\ \ \_\ \ \_\ \_\ \ \_\ \ /\ \L\ \\ \ \_ /\ \L\ \/\ \/\ \ /\  __/
#   \ \____/ \ \____/ /\____\\/`____ \\ `\____\\ \__\\ \____/\ \_\ \_\\ \____\
#    \/___/   \/___/  \/____/ `/___/> \\/_____/ \/__/ \/___/  \/_/\/_/ \/____/
#                                /\___/
#                                \/__/
# encoding: utf-8

from typing import Union

import uvicorn
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel

from favorite.pc_synchronize_pa import SourceType, DataType, DeviceType, Synchronize

app = FastAPI()
router = APIRouter()


class Connection(BaseModel):
    userNo: str = 'Estest015'
    sourceType: int = SourceType.App
    dataType: int = DataType.Self
    deviceType: int = DeviceType.And

@router.post("/conn/")
async def sync_get(conn: Connection):
    out = Synchronize(conn.userNo.upper(), conn.sourceType, conn.dataType, conn.deviceType)
    out.common_get()
    return out.out

app.include_router(router)