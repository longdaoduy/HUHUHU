def bai01():
    s = "I'm a student"
    return s
#bai03
def bai03():
    a = int(input("Nhap a: "))
    b = int(input("Nhap b: "))
    return a + b
#bai02
def bai02():
    x = 1/7
    return f"{x:.5f}"
#bai04
def bai04():
    filename = input("Enter the file name to read: ")
    if filename == "output.txt":
        print("Không thể đọc lại chính file output.txt")
        return
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            with open("output.txt", "a", encoding="utf-8") as f:
                print("\n--- File Content ---", file=f)
                print(content, file=f)
    except FileNotFoundError:
        with open("output.txt", "a", encoding="utf-8") as f:
            print("Error: The file does not exist.", file=f)

def bai06():
    s = "Hôm nay trời đẹp."
    with open("output.txt", "ab") as f:
        f.write((s + '\n').encode("utf-8"))

f = open("output.txt", "a", encoding="utf-8")
print(bai01(), file=f)
print(bai02(), file=f)
print(bai03(), file=f)
bai04()
bai06()
f.close()



