names = ["Alice", "Bob", "Charlie"]
scores = [85, 90, 78]

# enumerate example
for index, name in enumerate(names):
    print(index, name)

# zip example
for name, score in zip(names, scores):
    print(name, score)

# sorted example
nums = [5, 2, 9, 1]
print("Sorted numbers:", sorted(nums))

# type conversion
num = "10"
converted = int(num)
print(type(converted), converted)
