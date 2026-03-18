def splitrelation(str):
    str = str.split()
    a = str[2:]
    w2 = ""
    for i in a:
        w2 = w2 + " " + i
    return w2


#linput = input("Entrez un input du format suivant : mot1 relation mot2\n")
linput = "cloporte r_isa animal de compagnie"
separer = splitrelation(linput)
print(separer)