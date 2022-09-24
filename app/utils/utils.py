import datetime


def ms_to_timestamp(ms) -> str:
    seconds = ms / 1000
    b = int((seconds % 3600) // 60)
    c = int((seconds % 3600) % 60)
    dt = datetime.time(0, b, c)
    return dt.strftime("%M:%S")
