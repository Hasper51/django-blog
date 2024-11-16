from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserEntity:
    email: str
    date_joined: datetime