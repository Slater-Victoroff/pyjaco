def dict1():
    a = {1: 3, "s": 4}
    return len(a)

def dict2():
    a = {1: 3, "s": 4}
    return a[1] + a["s"]

def dict3():
    a = {1: 3, "s": 4}
    return a[1] + a["s"]

print dict1()
print dict2()
print dict3()
