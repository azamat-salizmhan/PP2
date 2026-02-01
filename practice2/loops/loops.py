# While Loop
i = 1
while i <= 5:
    print(i)
    i += 1

# While Loop Break
i = 1
while i <= 10:
    if i == 6:
        break
    print(i)
    i += 1

# While Loop Continue
i = 0
while i < 5:
    i += 1
    if i == 3:
        continue
    print(i)

# For Loop
for x in range(5):
    print(x)

# For Loop Break
for x in range(10):
    if x == 5:
        break
    print(x)

# For Loop Continue
for x in range(6):
    if x == 2:
        continue
    print(x)