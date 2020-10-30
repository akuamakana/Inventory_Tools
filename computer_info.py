import subprocess
import os
from pyad import adquery


class Computer:
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.floor = self.get_floor(self.ip_address)
        self.citrix_number = self.get_citrix_number(self.ip_address)
        self.serial_number = self.get_serial_number(self.ip_address)
        self.pc_name = self.get_pc_name(self.ip_address)
        self.operating_system = self.get_operating_system(self.ip_address)
        self.model = self.get_model(self.ip_address)
        self.logged_on_user = self.get_logged_on_user(self.ip_address)
        self.user_ad_name = self.get_username(self.logged_on_user)
        self.is_installed = self.get_installed_program(
            self.ip_address, "Computer Panic Button 9.9.9"
        )
        self.all_info = [
            self.floor,
            self.citrix_number,
            self.serial_number,
            self.pc_name,
            self.operating_system,
            self.model,
            self.ip_address,
            self.logged_on_user,
            self.user_ad_name,
            self.is_installed,
        ]

    def get_floor(self, ip_address):
        floor = ip_address.split(".")
        floor = floor[2]

        if floor == "24":
            return "WMC"
        elif floor == "68" or floor == "66":
            return "Floor 1"
        elif floor == "70" or floor == "94":
            return "Floor 2"
        elif floor == "72":
            return "Floor 3"
        elif floor == "74":
            return "Floor 4"
        elif floor == "76":
            return "PT"
        elif floor == "90" or floor == "92":
            return "Wireless"
        else:
            return "Unknown"

    def get_citrix_number(self, ip_address):
        command = fr'REG QUERY "\\{ip_address}\HKEY_LOCAL_MACHINE\SOFTWARE\Citrix\ICA Client" /v ClientName'
        citrix_number = subprocess.Popen(command, stdout=subprocess.PIPE)
        citrix_number = str(citrix_number.communicate()[0])
        citrix_number = citrix_number.split()[-1]
        citrix_number = citrix_number.replace("\\r\\n\\r\\n'", "")
        if citrix_number == r"b''" or citrix_number == r"b'":
            return "\n"

        return citrix_number

    def get_serial_number(self, ip_address):
        command = f"wmic /node:{ip_address} BIOS GET SERIALNUMBER"
        serial_number = subprocess.Popen(command, stdout=subprocess.PIPE)
        serial_number = str(serial_number.communicate()[0])
        if "Access is denied." in serial_number:
            return "\n"
        serial_number = serial_number.split()[1:]
        serial_number = [word.replace("\\r", "") for word in serial_number]
        serial_number = [word.replace("\\n", "") for word in serial_number]
        serial_number = " ".join(serial_number)[:-1]

        return serial_number

    def get_pc_name(self, ip_address):
        command = f"nslookup {ip_address}"
        name = subprocess.Popen(command, stdout=subprocess.PIPE)
        name = str(name.communicate())
        name = name.replace(r"""\r\n""", "")
        name = name.split()
        name = name[3].split(".")
        name = name[0]
        name = name.upper()

        return name

    def get_operating_system(self, ip_address):
        command = f"wmic /node:{ip_address} os get Caption"
        operating_system = subprocess.Popen(command, stdout=subprocess.PIPE)
        operating_system = str(operating_system.communicate()[0])
        if "Access is denied." in operating_system:
            return "\n"
        operating_system = operating_system.split()[1:]
        operating_system = [word.replace("\\r", "") for word in operating_system]
        operating_system = [word.replace("\\n", "") for word in operating_system]
        operating_system = " ".join(operating_system)[:-1]

        return operating_system

    def get_model(self, ip_address):
        command = f"wmic /node:{ip_address} computersystem get model"
        model = subprocess.Popen(command, stdout=subprocess.PIPE)
        model = str(model.communicate()[0])
        model = model.split()[1:]
        model = [word.replace("\\r", "") for word in model]
        model = [word.replace("\\n", "") for word in model]
        model = " ".join(model)[:-1]

        return model

    def get_logged_on_user(self, ip_address):
        command = f"wmic /node:{ip_address} computersystem get username"
        user = subprocess.Popen(command, stdout=subprocess.PIPE)
        user = str(user.communicate()[0]).split()
        if len(user) < 3:
            return "\n"
        user = user[1].replace("\\r\\r\\nCC\\\\", "")
        if user == r"\r\r\n":
            return "\n"

        return user.lower()

    def get_username(self, logged_on_user):
        try:
            username = adquery.ADQuery()
            username.execute_query(
                attributes=["cn"], where_clause=f"SamAccountName = '{logged_on_user}'"
            )
            username = username.get_single_result()["cn"]
            username = username.replace(" ", "")
            username = username.split(",")
            username = username[::-1]
            username = " ".join(username)
            return username
        except:
            return logged_on_user

    def get_zzz_programs(self, pc):
        try:
            zzz_programs = os.listdir(rf"\\{pc}\c$\Masters\SRC")

            return zzz_programs
        except:
            return []

    def get_installed_program(self, ip_address, program):
        all_programs = self.get_zzz_programs(ip_address)

        if len(all_programs) == 0:
            return "n/a"

        return program in all_programs

