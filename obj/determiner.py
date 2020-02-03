from runclient import sk

# 判断器必须返回该消息唯一的keyword
# 1.函数判断器
@sk.determine
def judge(key, message):
    pass


# 2. 类判断器
@sk.determine
class Judge(object):
    def __init__(self, key, message):
        pass

    def do(self):
        pass
