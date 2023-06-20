s = """
akjsdhfka
adkfjahldskjf
asdkjfahlkjsdf
asdkfjahlkdsjf
""" * 10

for i in range(1, 1000):
    f = open("./text/{}.txt".format(i), 'a')
    f.write(s)
    f.close()
