import subprocess
import re
import sys
import os


def getPcName(pc):
    command = f"nslookup {pc}"
    pcName = subprocess.Popen(command, stdout=subprocess.PIPE)

    pcName = str(pcName.communicate()[0])
    pcName = pcName.split()[3]
    pcName = pcName.split(".")[0]
    pcName = pcName.upper()

    return pcName


def getWCitrix(pc):
    command = fr'REG QUERY "\\{pc}\HKEY_LOCAL_MACHINE\SOFTWARE\Citrix\ICA Client" /v ClientName'
    citrixNumber = subprocess.Popen(command, stdout=subprocess.PIPE)

    citrixNumber = str(citrixNumber.communicate()[0])
    citrixNumber = citrixNumber.split()[-1]
    citrixNumber = citrixNumber.replace("\\r\\n\\r\\n'", "")

    return citrixNumber


def getPrograms(pc):
    command = f"wmic /node:{pc} product get name, version"
    programs = subprocess.Popen(command, stdout=subprocess.PIPE)

    programs = str(programs.communicate()[0])
    programs = programs.replace(r"""\r\r\n""", "")
    programs = re.split(r"\s{2,}", programs)[2:-1]

    programs = [" ".join(program) for program in zip(programs[0::2], programs[1::2])]

    return sorted(programs)


def getPrinters(pc):
    command = f"wmic /node:{pc} printer get name, portname"
    printers = subprocess.Popen(command, stdout=subprocess.PIPE)

    printers = str(printers.communicate()[0])
    printers = printers.replace(r"""\r\r\n""", "")
    printers = printers.replace("""b\'""", "")
    printers = re.split(r"\s{2,}", printers)
    printers = ["\t".join(printer) for printer in zip(printers[0::2], printers[1::2])]

    return printers


def getZzzPrograms(oldPc, newPc):
    zzzPrograms = []
    oldZzzPrograms = os.listdir(rf"\\{oldPc}\c$\Masters\SRC")
    newZzzPrograms = os.listdir(rf"\\{newPc}\c$\Masters\SRC")

    for program in oldZzzPrograms:
        if program not in newZzzPrograms:
            zzzPrograms.append(program)

    return zzzPrograms


def writeToFile(
    pcName, oldWNumber, oldPrograms, newPrograms, zzzPrograms, printers, newIp
):
    missingPrograms = []
    miscPrograms = [
        "Intel(R)",
        "Microsoft VC++",
        "Microsoft Visual C++",
        "MSXML 4.0",
        "Intelr Trusted",
        "AgentInstall",
        "Local Administrator",
    ]
    for program in oldPrograms:
        if program not in newPrograms:
            missingPrograms.append(program)

    for program in missingPrograms:
        for misc in miscPrograms:
            if misc in program:
                missingPrograms.remove(program)

    try:
        os.mkdir(rf"C:\source\pcswaps")
    except:
        pass

    os.chdir(rf"C:\source\pcswaps")
    file = open(f"{pcName}.txt", "w+")

    file.write(f"Name: {pcName} | W#: {oldWNumber}\n")

    file.write("Missing Programs:\n")
    for program in missingPrograms:
        file.write(f"{program}\n")

    file.write("\nzzzPrograms:\n")
    for program in zzzPrograms:
        file.write(f"{program}\n")

    file.write("\nPrinters:\n")
    for printer in printers:
        file.write(f"{printer}\n")

    file.write("\nOld Programs:\n")
    for program in oldPrograms:
        file.write(f"{program}\n")

    file.close()

    try:
        os.mkdir(rf"\\{newIp}\c$\source")
    except:
        pass

    os.chdir(rf"\\{newIp}\c$\source")
    file = open(f"{pcName}.txt", "w+")

    file.write(f"Name: {pcName} | W#: {oldWNumber}\n")

    file.write("Missing Programs:\n")
    for program in missingPrograms:
        file.write(f"{program}\n")

    file.write("\nzzzPrograms:\n")
    for program in zzzPrograms:
        file.write(f"{program}\n")

    file.write("\nPrinters:\n")
    for printer in printers:
        file.write(f"{printer}\n")

    file.write("\nOld Programs:\n")
    for program in oldPrograms:
        file.write(f"{program}\n")

    file.close()


oldPc = sys.argv[1]
newPc = sys.argv[2]
oldPcName = getPcName(oldPc)
oldWNumber = getWCitrix(oldPc)
oldPcPrograms = getPrograms(oldPc)
newPcPrograms = getPrograms(newPc)
zzzPrograms = getZzzPrograms(oldPc, newPc)
printers = getPrinters(oldPc)

writeToFile(
    oldPcName, oldWNumber, oldPcPrograms, newPcPrograms, zzzPrograms, printers, newPc
)

