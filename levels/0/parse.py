a = -2147483622
with open('level__1_terrain.csv') as f:
    text = f.read()
with open('level__1_terrain_mod.csv', 'w') as f:
    for i in range(16):
        if not (text.find(str(a - i)) == -1):
            print(str(a-i), str(i))
            text = text.replace(str(a - i), str(i))
    f.write(text)
