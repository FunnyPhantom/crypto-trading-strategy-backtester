import os
import requests
import zipfile
import sys


base_url = "https://data.binance.vision"

# Add the path to the root directory of your project
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)


def download_klines_data(
    market="spot", symbol="BTCUSDT", interval="1m", year=2023, month=4
):
    # Create the directory path to store the unzipped data
    current_dir = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.join(
        current_dir, f"./data/{market}/monthly/klines/{symbol}/{interval}"
    )
    os.makedirs(directory, exist_ok=True)

    month = str(month).zfill(2)

    def _file_path(ext="zip"):
        return f"{symbol}-{interval}-{str(year)}-{month}.{ext}"

    # do not download already downloaded file
    potential_file_path = os.path.join(directory, _file_path(ext="csv"))
    if os.path.exists(potential_file_path):
        print(f"file path: {_file_path(ext='csv')} already exists")
        return

    # Make the HTTP GET request to download the ZIP file
    url = f"{base_url}/data/{market}/monthly/klines/{symbol}/{interval}/{symbol}-{interval}-{str(year)}-{month}.zip"
    print(url)
    r = requests.get(url)

    # Save the ZIP file to disk
    zip_path = os.path.join(directory, _file_path())
    with open(zip_path, "wb") as f:
        f.write(r.content)

    # Extract the contents of the ZIP file
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(directory)

    # Remove the downloaded ZIP file
    os.remove(zip_path)


def to_interval_(timeframe):
    timeframe_to_interval = {
        "m1": "1m",
        "m5": "5m",
        "m15": "15m",
        "m30": "30m",
        "h1": "1h",
        "h2": "2h",
        "h4": "4h",
        "d1": "1d",
        "w1": "1w",
    }
    return timeframe_to_interval.get(timeframe)


def to_tf_(interval):
    interval_to_timeframe = {
        "1m": "m1",
        "5m": "m5",
        "15m": "m15",
        "30m": "m30",
        "1h": "h1",
        "2h": "h2",
        "4h": "h4",
        "1d": "d1",
        "1w": "w1",
    }
    return interval_to_timeframe.get(interval)


def generate_year_month_list(start_year, start_month, end_year, end_month):
    year_month_list = []

    # Iterate over the years and months
    for year in range(start_year, end_year + 1):
        # Determine the range of months for the current year
        if year == start_year:
            start_m = start_month
        else:
            start_m = 1
        if year == end_year:
            end_m = end_month
        else:
            end_m = 12

        # Iterate over the months for the current year
        for month in range(start_m, end_m + 1):
            year_month_list.append((year, month))

    return year_month_list


from config import (
    ALL_TIMEFRAMES_LIST,
    COINS_SYMBOL,
    START_YEAR,
    START_MONTH,
    END_YEAR,
    END_MONTH,
)


def download_all_kline_data(
    symbol=COINS_SYMBOL,
    start_year=START_YEAR,
    start_month=START_MONTH,
    end_year=END_YEAR,
    end_month=END_MONTH,
    time_frames=ALL_TIMEFRAMES_LIST,
):
    if not isinstance(time_frames, list):
        time_frames = [time_frames]

    year_month_list = generate_year_month_list(
        start_year, start_month, end_year, end_month
    )

    for time_frame in time_frames:
        corresponding_interval = to_interval_(time_frame)
        for year, month in year_month_list:
            download_klines_data(
                symbol=symbol, interval=corresponding_interval, year=year, month=month
            )


if __name__ == "__main__":
    download_all_kline_data()
