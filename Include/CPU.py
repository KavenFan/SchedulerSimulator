#-*- coding: UTF-8 -*-

class CPU:
    def __init__(self, cpu_id):
        self.id = cpu_id
        self.type = None
        self.current_task = None
        self.active_task_list = []
        self.expired_task_list = []
        return
    
    def __str__(self):
        g = lambda x: "%30s : %s" % (x, eval("self." + x))
        t = [g(x) for x in dir(self) if str.isalpha(x[0])]
        return "\n".join(t)