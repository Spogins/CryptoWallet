from datetime import datetime


async def convert_date(original_date_str):
    # Исходная дата в строковом формате
    # original_date_str = "2023-08-13 12:44:18.686"

    # Преобразование строки в объект datetime
    original_date = datetime.strptime(original_date_str, "%Y-%m-%d %H:%M:%S.%f")

    # Преобразование в новый желаемый формат
    new_date_str = original_date.strftime("%y %b %d:%H:%M")

    return new_date_str
