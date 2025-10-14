filename = input("Enter the file name to read: ")
try:
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
        print("\n--- File Content ---")
        print(content)
except FileNotFoundError:
    print("Error: The file does not exist or the path is incorrect.")
except Exception as e:
    print("An unexpected error occurred:", e)