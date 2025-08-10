import re

pattern = re.compile(r"^09\d{9}$")

if pattern.match("0304120157"):
    print("valid")
else:
    print("not valid")