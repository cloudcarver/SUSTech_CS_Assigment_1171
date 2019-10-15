import time
import Config

# The Cache object is acted like an normal container.
class Cache(object):

    ANSWER_NOT_FOUND = "ANSWER_NOT_FOUND"
    ANSWER_EXPIRE = "ANSWER_EXPIRE"

    def __init__(self):
        self.itemdict = {}
        self.cleanCounter = 0
        self.CLEAN_PERIOD = Config.CLEAN_PERIOD
    
    def clean(self):
        out_of_date_keys = [] # deal with "RuntimeError: dictionary changed size during iteration"
        cnt = 0
        for key in self.itemdict.keys():
            val = self.itemdict[key]
            if time.time() >= val["time_to_live"]:
                cnt += 1
                out_of_date_keys.append(key)
        for key in out_of_date_keys:
            self.itemdict.pop(key)
        if Config.VERBOSE:
            print("{} out of date cached response are deleted.".format(cnt))

    # Add new query and its answer to the cache
    def append(self, key, val, time_to_live):
        self.itemdict[key] = {"answer" : val, 
                              "time_to_live" : time.time() + time_to_live}
    
    # 1. Find the answer in the cache with the query key: qname and qtype.
    # 2. The answer will be returned only if the answer is out of date or 
    #    answer is not found in the dict.
    def get(self, key):
        self.cleanCounter = (self.cleanCounter + 1) % self.CLEAN_PERIOD
        if self.cleanCounter == 0:
            self.clean()
        if key in self.itemdict :
            val = self.itemdict[key]
            if time.time() >= val["time_to_live"]:
                self.itemdict.pop(key)
                return Cache.ANSWER_EXPIRE 
            else:
                return val["answer"]
        else:
            return Cache.ANSWER_NOT_FOUND