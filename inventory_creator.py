from openpyxl import Workbook, load_workbook
from computer_info import Computer
import datetime

## scan text: 10.148.68.1-254, 10.148.70.1-254, 10.148.72.1-254, 10.148.74.1-254, 10.148.94.1-254, 10.148.90.1-254, 10.148.24.1-254

ip_addresses = """10.148.74.136
10.148.72.91
10.148.68.217
10.148.68.206
10.148.68.167
10.148.68.62
10.148.74.167
""".split()


def write_to_excel(ip_addresses):
    sheet_name = str(datetime.date.today())
    headers = [
        "Location",
        "Citrix Number",
        "Serial Number",
        "Name",
        "OS",
        "Model",
        "IP",
        "Logged On",
        "Username",
    ]

    try:
        wb = load_workbook("pcInventory.xlsx")
    except FileNotFoundError:
        wb = Workbook()
    wb.create_sheet(sheet_name, -1)
    ws = wb[sheet_name]
    ws.append(headers)

    for ip_address in ip_addresses:
        pcInfo = Computer(ip_address)
        write_to_row = pcInfo.all_info
        ws.append(write_to_row)

    wb.save("pcInventory.xlsx")


write_to_excel(ip_addresses)
