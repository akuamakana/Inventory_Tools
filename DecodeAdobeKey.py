import sqlite3
import sys


def read_cache_db(filename):
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
    for encrypted_char, cypher in zip(encrypted_key, adobe_cypher):
        yield cypher[int(encrypted_char)]


def format_key(key_gen, size=4, separator="-"):
    key_gen = list(key_gen)
    return separator.join(
        ["".join(key_gen[i : i + size]) for i in range(0, len(key_gen), size)]
    )


ip_address = "10.148.24.65"

# read key from sqlite db
encrypted_key = read_cache_db(
    rf"\\{ip_address}\C$\Program Files\Common Files\Adobe\Adobe PCD\cache\cache.db"
)
print(f"encrypted: {encrypted_key}")

# decode and print grouped by 4 chars
decrypted_key = format_key(decode_adobe_key(encrypted_key))
print(f"decrypted: {decrypted_key}")

