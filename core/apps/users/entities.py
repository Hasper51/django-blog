from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    email: str
    date_joined: datetime