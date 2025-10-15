def isTriangle(a, b, c):
    if a + b > c or a + c > b or b + c > a:
        return True
    return False

a = int(input("Nhap a: "))
b = int(input("Nhap b: "))
c = int(input("Nhap c: "))
print(isTriangle(a, b, c))


f = open("output.txt", "a")
print(isTriangle, file = f)
f.close()
