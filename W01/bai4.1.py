def leapYear(n):

    if n % 400 == 0 or (n % 4 == 0 and n % 100 != 0):
        return True
    return False

n = int(input("Input Year: "))
print(leapYear(n))