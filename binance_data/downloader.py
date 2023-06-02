base_url = "https://data.binance.vision"

import requests
import json
from types import SimpleNamespace


def download_klines_data(
    market="spot", symbol="BTCUSDT", interval="1m", year=2023, month=5
):
    month = str(month)
    month = month.zfill(2)
    r = requests.get(
        f"{base_url}/data/{market}/monthly/klines/{symbol}/{interval}/{symbol}-{interval}-{str(year)}-{month}.zip"
    )
    # m = json.loads(r.content, object_hook=lambda d: SimpleNamespace(**d))
