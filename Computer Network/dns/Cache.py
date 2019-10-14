import time

# The Cache object is acted like an normal container.
class Cache(object):

    ANSWER_NOT_FOUND = "ANSWER_NOT_FOUND"
    ANSWER_EXPIRE = "ANSWER_EXPIRE"

    def __init__(self):
        self.itemdict = {}
    
    # Add new query and its answer to the cache
    def append(self, key, val, time_to_live):
        self.itemdict[key] = {"answer" : val, 
                              "time_to_live" : time.time() + time_to_live}
    
    # 1. Find the answer in the cache with the query key: qname and qtype.
    # 2. The answer will be returned only if the answer is out of date or 
    #    answer is not found in the dict.
    def get(self, key):
        if key in self.itemdict :
            val = self.itemdict[key]
            if time.time() >= val["time_to_live"]:
                self.itemdict.pop(key)
                return Cache.ANSWER_EXPIRE 
            else:
                return val["answer"]
        else:
            return Cache.ANSWER_NOT_FOUND