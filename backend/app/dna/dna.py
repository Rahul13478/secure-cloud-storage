# the process of making DNA will be like this --->
# 1. we will use hashlib SHA256 first to conver normal string into hash
# 2. now convert the hast str into int then binary 
# 3. Python list comprehension split string every 2 characters
# 4. maping 
# 4. making like DNA

import hashlib 

def dna_make(token):
    a = token
    b = hashlib.sha256(a.encode())
    c = b.hexdigest()
    d = len(c)*4
    e = bin(int(c,16))[2:].zfill(d)
    f = [e[i:i+2]for i in range(0, len(e),2)]
    g = {"00":"A","10":"C","01":"T","11":"G"}
    h = [g[o]for o in f]
    j = "".join(h)
    k = j[0:12]
    return k 
    



