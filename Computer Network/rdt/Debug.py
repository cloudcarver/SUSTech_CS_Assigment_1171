import Config
def debug_print(msg):
    if Config.DEBUG:
        print(msg)

def verbose_print(msg):
    if Config.VERBOSE or Config.DEBUG:
        print(msg)