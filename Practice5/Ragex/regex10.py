import re
s=input()
print(re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower())