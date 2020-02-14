import subprocess
from pyad import adquery


class Computer:
    def __init__(self, ipAddress):
        self.ipAddress = ipAddress
        self.floor = self.getFloor(self.ipAddress)
        self.citrixNumber = self.getCitrixNumber(self.ipAddress)
        self.serialNumber = self.getSerialNumber(self.ipAddress)
        self.pcName = self.getpcName(self.ipAddress)
        self.operatingSystem = self.getOperatingSystem(self.ipAddress)
        self.model = self.getModel(self.ipAddress)
        self.loggedOnUser = self.getLoggedOnUser(self.ipAddress)
        self.userADName = self.getUserADName(self.loggedOnUser)
        self.allInfo = [
            self.floor,
            self.citrixNumber,
            self.serialNumber,
            self.pcName,
            self.operatingSystem,
            self.model,
            self.ipAddress,
            self.loggedOnUser,
            self.userADName,
        ]

    def getFloor(self, ipAddress):
        floor = ipAddress.split(".")
        floor = floor[2]

        if floor == "24":
            return "KMA"
        elif floor == "68":
            return "Floor 1"
        elif floor == "70" or floor == "94":
            return "Floor 2"
        elif floor == "72":
            return "Floor 3"
        elif floor == "74":
            return "Floor 4"
        elif floor == "90":
            return "Wireless"
        else:
            return "Unknown"

    def getCitrixNumber(self, ipAddress):
        command = fr'REG QUERY "\\{ipAddress}\HKEY_LOCAL_MACHINE\SOFTWARE\Citrix\ICA Client" /v ClientName'
        citrixNumber = subprocess.Popen(command, stdout=subprocess.PIPE)

        citrixNumber = str(citrixNumber.communicate()[0])
        citrixNumber = citrixNumber.split()[-1]
        citrixNumber = citrixNumber.replace("\\r\\n\\r\\n'", "")
        if citrixNumber == r"b''" or citrixNumber == r"b'":
            return "\n"

        return citrixNumber

    def getSerialNumber(self, ipAddress):
        command = f"wmic /node:{ipAddress} BIOS GET SERIALNUMBER"
        serialNumber = subprocess.Popen(command, stdout=subprocess.PIPE)

        serialNumber = str(serialNumber.communicate()[0])
        if "Access is denied." in serialNumber:
            return "\n"
        serialNumber = serialNumber.split()[1:]
        serialNumber = [word.replace("\\r", "") for word in serialNumber]
        serialNumber = [word.replace("\\n", "") for word in serialNumber]
        serialNumber = " ".join(serialNumber)[:-1]

        return serialNumber

    def getpcName(self, ipAddress):
        command = f"nslookup {ipAddress}"
        name = subprocess.Popen(command, stdout=subprocess.PIPE)
        
        name = str(name.communicate())
        name = name.replace(r"""\r\n""", "")
        name = name.split()
        name = name[3].split(".")
        name = name[0]
        name = name.upper()

        return name

    def getOperatingSystem(self, ipAddress):
        command = f"wmic /node:{ipAddress} os get Caption"
        operatingSystem = subprocess.Popen(command, stdout=subprocess.PIPE)

        operatingSystem = str(operatingSystem.communicate()[0])
        if "Access is denied." in operatingSystem:
            return "\n"
        operatingSystem = operatingSystem.split()[1:]
        operatingSystem = [word.replace("\\r", "") for word in operatingSystem]
        operatingSystem = [word.replace("\\n", "") for word in operatingSystem]
        operatingSystem = " ".join(operatingSystem)[:-1]

        return operatingSystem

    def getModel(self, ipAddress):
        command = f"wmic /node:{ipAddress} computersystem get model"
        model = subprocess.Popen(command, stdout=subprocess.PIPE)

        model = str(model.communicate()[0])
        model = model.split()[1:]
        model = [word.replace("\\r", "") for word in model]
        model = [word.replace("\\n", "") for word in model]
        model = " ".join(model)[:-1]

        return model

    def getLoggedOnUser(self, ipAddress):
        command = f"wmic /node:{ipAddress} computersystem get username"
        user = subprocess.Popen(command, stdout=subprocess.PIPE)

        user = str(user.communicate()[0]).split()
        if len(user) < 3:
            return "\n"
        user = user[1].replace("\\r\\r\\nCC\\\\", "")
        if user == r"\r\r\n":
            return "\n"

        return user.lower()

    def getUserADName(self, loggedOnUser):
        try:
            q = adquery.ADQuery()
            q.execute_query(
                attributes=["cn"], where_clause=f"SamAccountName = '{loggedOnUser}'"
            )
            return q.get_single_result()["cn"]
        except:
            return loggedOnUser

