from enum import Enum


class Role(Enum):
    SINH_VIEN = "sinh_vien"
    ADMIN = "admin"


class TrangThaiDangKy(Enum):
    DANG_KY = "dang_ky"
    DA_HUY = "da_huy"


class TrangThaiGiuaKy(Enum):
    CHUA_THI = "chua_thi"
    DA_THI = "da_thi"