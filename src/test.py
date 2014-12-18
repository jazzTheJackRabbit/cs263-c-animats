import random

i = 0
diction = dict()
for i in range(0,10):
    diction["key"+str(i)] = "value"+str(i)

keys = diction.keys()
print "Before randomizing:"
print keys

for i in range(0,len(keys)):
    random_index = random.randrange(i,len(keys))
    temp = keys[random_index]
    keys[random_index] = keys[i]
    keys[i] = temp

print "after randomizing"
print [diction[key] for key in keys]