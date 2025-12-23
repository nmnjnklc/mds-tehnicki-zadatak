from typing import Dict
from enum import Enum


class Order(str, Enum):
    ASCENDING = "asc"
    DESCENDING = "desc"


OrderBy = Dict[str, Order]
