from enum import Enum


class Role(Enum):
    STUDENT = "STUDENT"
    ADMIN = "ADMIN"


class StatusRegistration(Enum):
    REGISTRATION = "dang_ky"
    CANCELED = "da_huy"


class StatusMidterm(Enum):
    NOT_STARTED = "chua_thi"
    COMPLETED = "da_thi"