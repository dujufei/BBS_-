
import random

tmp = []
for i in range(5):
    n = str(random.randint(0, 9))
    l = chr(random.randint(65, 90))
    u = chr(random.randint(97, 122))
    r = random.choice([n, l, u])
    tmp.append(r)
ret = "".join(tmp)
print(ret)
