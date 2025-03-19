def crypt(inp: str, salt: str, passwd: str)-> str:
    wp= salt+passwd
    table_let= "abcdefghijklmnopqrstuvwxyz"
    table_num= "1234567890"
    table_upp= table_let.upper()
    table_sym= "~!@#$%^&*()_+-=[]{};':\",.<>/?\\|`"
    table= table_let+table_num+table_upp+table_sym
    objects= []
    onjects =[]
    i= 0

    for c in inp:
        j= 0
        if not c in table:
            onjects.append(127)
            continue

        for x in table:
            if x == c:
                onjects.append(j)

            j= j + 1


    for c in wp:
        j= 0
        if not c in table:
            objects.append(127)
            continue

        for x in table:
            if x == c:
                objects.append(j)

            j= j + 1

    for o in onjects:
        onjects[i]= o + objects[i]
        i= i + 1

    table= table + table_sym + table + table_upp + table_sym + table_upp + table + table + "uwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwu"
    string_of_doom= ""
    for w in onjects:
        string_of_doom= string_of_doom + table[w]

    return string_of_doom

if __name__ == "__main__":
    print("Hello, World")
    print(crypt("Hello, World", "1234", "password"))
    print(crypt("Hello, World", "5678", "grassdoor"))
