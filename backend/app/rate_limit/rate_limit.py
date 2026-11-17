import redis

clint  = redis.Redis(host="localhost" , port=6379 , db=0)




def test_rate_limit(key , limit , expire):
    new_count = clint.incr(key)
    # print(clint.get(key))
    if new_count == 1 :
        clint.expire(key , expire)
    elif new_count > limit :
        return True
    return False
        

      

# result = test_rate_limit("test_marks" , 5 )
# print(result)  

def read_count(key , limit):
    marks = clint.get(key)
    if marks is None:
        return False
    else:
        int_marks = int(marks)
        return int_marks >= limit


# result = read_count("test_marks" , 5 )
# print(result)    

def clear_count(key):
    clint.delete(key)
