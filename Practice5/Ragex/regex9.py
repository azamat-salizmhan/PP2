import re
print(re.sub(r'(?<!^)(?=[A-Z])', ' ', input()))