import subprocess
import re
import sys
import os
import sqlite3


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


def get_missing_programs(old_programs, new_programs):
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

    return missing_programs


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


def write_to_file(pc_name, path, missing_programs, old_programs, encrypted_key, decrypted_key):
    try:
        os.mkdir(path)
    except:
        pass

    os.chdir(path)
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


def read_adobe_reg(ip_address):
    versions = ["9.0", "10.0", "11.0"]
    for version in versions:
        try:
            command = fr'REG QUERY "\\{ip_address}\HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Adobe\Adobe Acrobat\{version}\Registration" /v ClientName'
            encrypted_key = subprocess.Popen(command, stdout=subprocess.PIPE)
            encrypted_key = str(encrypted_key.communicate()[0])
            encrypted_key = encrypted_key.split()[-1]
            encrypted_key = encrypted_key.replace("\\r\\n\\r\\n'", "")
            return encrypted_key
        except:
            encrypted_key = ""
            pass
    if encrypted_key == "":
        return "No Acrobat License"


def read_cache_db(filename="cache.db"):
    with sqlite3.connect(filename) as conn:
        c = conn.cursor()
        encrypted_key = c.execute(
            "select value from domain_data where key='SN'"
        ).fetchone()[0]
        c.close()

    if len(encrypted_key) != 24:
        print("serial number is expected to be 24 chars long!")
        sys.exit(1)

    return encrypted_key


def decode_adobe_key(encrypted_key):
    adobe_cypher = (
        "0000000001",
        "5038647192",
        "1456053789",
        "2604371895",
        "4753896210",
        "8145962073",
        "0319728564",
        "7901235846",
        "7901235846",
        "0319728564",
        "8145962073",
        "4753896210",
        "2604371895",
        "1426053789",
        "5038647192",
        "3267408951",
        "5038647192",
        "2604371895",
        "8145962073",
        "7901235846",
        "3267408951",
        "1426053789",
        "4753896210",
        "0319728564",
    )
    if encrypted_key == "No Acrobat License":
        return "No Acrobat License"
    for encrypted_char, cypher in zip(encrypted_key, adobe_cypher):
        yield cypher[int(encrypted_char)]


def format_key(key_gen, size=4, separator="-"):
    key_gen = list(key_gen)
    return separator.join(
        ["".join(key_gen[i : i + size]) for i in range(0, len(key_gen), size)]
    )


def process_files(
    pc_name, old_w_number, old_programs, new_programs, zzz_programs, printers, new_ip, encrypted_key='No Acrobat Key', decrypted_key='No Acrobat Key'
):
    missing_programs = get_missing_programs(old_programs, new_programs)
    local_pc = r"C:\source\pcswaps"
    new_pc = r"\\{new_ip}\c$\source"
    write_to_file(pc_name, local_pc, missing_programs, old_programs, encrypted_key, decrypted_key)
    write_to_file(pc_name, new_pc, missing_programs, old_programs, encrypted_key, decrypted_key)


old_pc = sys.argv[1]
new_pc = sys.argv[2]
old_pc_name = get_pc_name(old_pc)
old_w_number = get_citrix_number(old_pc)
old_pc_programs = get_programs(old_pc)
new_pc_programs = get_programs(new_pc)
zzz_programs = get_zzz_programs(old_pc, new_pc)
printers = get_printers(old_pc)
try:
    encrypted_key = read_cache_db(
        rf"\\{old_pc}\C$\Program Files\Common Files\Adobe\Adobe PCD\cache\cache.db"
    )
    decrypted_key = format_key(decode_adobe_key(encrypted_key))
except:
    pass

process_files(
    old_pc_name,
    old_w_number,
    old_pc_programs,
    new_pc_programs,
    zzz_programs,
    printers,
    new_pc,
    encrypted_key,
    decrypted_key,
)

