import subprocess
import re
import sys
import os


def get_pc_name(pc):
    command = f"nslookup {pc}"
    pc_name = subprocess.Popen(command, stdout=subprocess.PIPE)

    pc_name = str(pc_name.communicate()[0])
    pc_name = pc_name.split()[3]
    pc_name = pc_name.split(".")[0]
    pc_name = pc_name.upper()

    return pc_name


def get_citrix_number(pc):
    command = fr'REG QUERY "\\{pc}\HKEY_LOCAL_MACHINE\SOFTWARE\Citrix\ICA Client" /v ClientName'
    citrix_number = subprocess.Popen(command, stdout=subprocess.PIPE)

    citrix_number = str(citrix_number.communicate()[0])
    citrix_number = citrix_number.split()[-1]
    citrix_number = citrix_number.replace("\\r\\n\\r\\n'", "")

    return citrix_number


def get_programs(pc):
    command = f"wmic /node:{pc} product get name, version"
    programs = subprocess.Popen(command, stdout=subprocess.PIPE)

    programs = str(programs.communicate()[0])
    programs = programs.replace(r"""\r\r\n""", "")
    programs = re.split(r"\s{2,}", programs)[2:-1]

    programs = [" ".join(program) for program in zip(programs[0::2], programs[1::2])]

    return sorted(programs)


def get_printers(pc):
    command = f"wmic /node:{pc} printer get name, portname"
    printers = subprocess.Popen(command, stdout=subprocess.PIPE)

    printers = str(printers.communicate()[0])
    printers = printers.replace(r"""\r\r\n""", "")
    printers = printers.replace("""b\'""", "")
    printers = re.split(r"\s{2,}", printers)
    printers = ["\t".join(printer) for printer in zip(printers[0::2], printers[1::2])]

    return printers


def get_zzz_programs(oldPc, newPc):
    zzz_programs = []
    old_zzz_programs = os.listdir(rf"\\{oldPc}\c$\Masters\SRC")
    new_zzz_programs = os.listdir(rf"\\{newPc}\c$\Masters\SRC")

    for program in old_zzz_programs:
        if program not in new_zzz_programs:
            zzz_programs.append(program)

    return zzz_programs


def write_to_file(
    pc_name, old_w_number, old_programs, new_programs, zzz_programs, printers, new_ip
):
    missing_programs = []
    misc_programs = [
        "Intel(R)",
        "Microsoft VC++",
        "Microsoft Visual C++",
        "MSXML 4.0",
        "Intelr Trusted",
        "AgentInstall",
        "Local Administrator",
    ]
    for program in old_programs:
        if program not in new_programs:
            missing_programs.append(program)

    for program in missing_programs:
        for misc in misc_programs:
            if misc in program:
                missing_programs.remove(program)

    try:
        os.mkdir(rf"C:\source\pcswaps")
    except:
        pass

    os.chdir(rf"C:\source\pcswaps")
    file = open(f"{pc_name}.txt", "w+")

    file.write(f"Name: {pc_name} | W#: {old_w_number}\n")

    file.write("Missing Programs:\n")
    for program in missing_programs:
        file.write(f"{program}\n")

    file.write("\nzzzPrograms:\n")
    for program in zzz_programs:
        file.write(f"{program}\n")

    file.write("\nPrinters:\n")
    for printer in printers:
        file.write(f"{printer}\n")

    file.write("\nOld Programs:\n")
    for program in old_programs:
        file.write(f"{program}\n")

    file.close()

    try:
        os.mkdir(rf"\\{new_ip}\c$\source")
    except:
        pass

    os.chdir(rf"\\{new_ip}\c$\source")
    file = open(f"{pc_name}.txt", "w+")

    file.write(f"Name: {pc_name} | W#: {old_w_number}\n")

    file.write("Missing Programs:\n")
    for program in missing_programs:
        file.write(f"{program}\n")

    file.write("\nzzzPrograms:\n")
    for program in zzz_programs:
        file.write(f"{program}\n")

    file.write("\nPrinters:\n")
    for printer in printers:
        file.write(f"{printer}\n")

    file.write("\nOld Programs:\n")
    for program in old_programs:
        file.write(f"{program}\n")

    file.close()


old_pc = sys.argv[1]
new_pc = sys.argv[2]
old_pc_name = get_pc_name(old_pc)
old_w_number = get_citrix_number(old_pc)
old_pc_programs = get_programs(old_pc)
new_pc_programs = get_programs(new_pc)
zzz_programs = get_zzz_programs(old_pc, new_pc)
printers = get_printers(old_pc)

write_to_file(
    old_pc_name, old_w_number, old_pc_programs, new_pc_programs, zzz_programs, printers, new_pc
)

