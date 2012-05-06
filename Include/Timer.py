#-*- coding: UTF-8 -*-


class Timer:
    def __init__(self):
        self.jiffies = 0
        pass
    def __str__(self):
        t = [ "%30s : %s" % (x, eval("self." + x)) for x in dir(self) if str.isalpha(x[0])]
        return "\n".join(t)