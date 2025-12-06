from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ExchangeRate(BaseModel):
    currency_pair: str 
    price_buy: float
    price_sell: float
    source: str 
    last_updated: datetime = datetime.now()
