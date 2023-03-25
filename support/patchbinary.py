#Source: https://github.com/dortania/OpenCore-Legacy-Patcher/blob/main/Build-Binary.command#L303-L329
print("Patching LC_VERSION_MIN_MACOSX")
path = './dist/fetcharchivetube'
find = b'\x00\x0D\x0A\x00'
replace = b'\x00\x09\x0A\x00'
with open(path, 'rb') as f:
    data = f.read()
    data = data.replace(find, replace, 1)
    with open(path, 'wb') as f:
        f.write(data)
print("Done")
