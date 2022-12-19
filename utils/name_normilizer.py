import re


def normalize_name(name: str):
    name = re.sub(r'\W', '', name)
    name = name.split(" ")
    for i in range(0, len(name)):
        n = name[i]
        n = n.strip()
        if n == "" and n in name:
            name.remove(n)
            continue
        n[0].upper()
        name[i] = n
    return ''.join(name)[0:200]
