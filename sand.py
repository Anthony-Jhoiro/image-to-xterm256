import os

# you can do like this
columns, lines = os.get_terminal_size()

os.system("clear")

print("+", end="")
for i in range(columns - 2):
    print("-", end="")
print("+")

for  j in range(lines - 2):
    print("|", end="")
    for i in range(columns - 2):
        print(" ", end="")
    print("|")

print("+", end="")
for i in range(columns - 2):
    print("-", end="")
print("+")
