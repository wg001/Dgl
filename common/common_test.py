def createGenerator():
    mylist = range(10)
    for i in mylist:
        yield i * i


mygenerator = createGenerator()

print(mygenerator)

for i in mygenerator:
    print(i)
