import pprint
import re
import json

pp = pprint.PrettyPrinter(indent=4)

# Load file
f = open("log.current.txt", "r")
f = f.read()

# Seperate file in to array
f = f.split("\n")
f = f[-2]
reg = re.sub("\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}[\[]\D{4}[\]]", "", f)
reg = reg.replace("Post to Checkin/Checkin ", "")
reg = json.loads(reg)
reg = reg["Machine"]

# pp.pprint(f)
print(json.dumps(reg, indent=4, sort_keys=True))
