from datetime import datetime

current_date = datetime.today()
print(current_date)

format_date = datetime.strftime(current_date,
                                "%d-%m-%Y %H:%M:%S")
print(format_date)