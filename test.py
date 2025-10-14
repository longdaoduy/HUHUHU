def triangle():
    for i in range(7):
        for j in range(7):
            if j < i : 
                print("*", end = "")
        print('\n')

triangle()