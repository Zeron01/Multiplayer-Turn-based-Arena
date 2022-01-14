file = open('settings.txt')

content = file.readlines()

print(content[0][4:-1])
print(content[1][6:])