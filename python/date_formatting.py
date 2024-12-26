from datetime import datetime

current_datetime = datetime.now()
print(current_datetime)

print(datetime.strftime(current_datetime,
                        "%d/%m/%Y %H:%M:%S"))
