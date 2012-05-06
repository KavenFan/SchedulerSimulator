#-*- coding: UTF-8 -*-

import Translation as TRANS
#import random
class Task:
    def __init__(self, conf):
        self.conf = conf
        
        #-------------------------------------
        self.pid = None
        self.start_jiffies = None
        self.actual_start_jiffies = None
        self.allocated_jiffies = None
        self.actual_jiffies = None
        self.actual_finish_jiffies = None
        self.deadline = None
        self.static_priority = None
        self.initial_cpu = None
        self.current_cpu = None
        
#        if static_prioriy <120: counter = (140-static_priority)*20
#        else: counter = (140-static_priority)*5
        self.counter = None # HZ
        self.task_counter = None
        
#        dynamic_priority=max(100, min(static_priority - bonus+5,139))
        self.dynamic_priority = None
        
#        bonus <10 and bonus >0
#        bonus = min(average_sleep_time /100, 10)
        self.bonus = None
        
        self.start_time = None
        self.finish_time = None
        self.actual_time = None
        '''set a prioriy to every cpu, scheduler will select 
        the cpu with highest priority to run this process
        (cpu, priority)'''
        
        self.cpu_priority = [(None, None)]
        '''if type is the same with the cpu's type, 
        process will perform better on this cpu'''
        
#        if dynamic_priority <=3*static_priority/4+28:
#            task_type = INTERATIVE
#        it is the same as:
#        if bonus-5>=static_priority/4-28:
#            task_type = INTERATIVE
        self.task_type = None
        
        pass
    
    def __str__(self):
        t = [
             (TRANS.T_PID, self.pid),
             (TRANS.T_INITIAL_CPU, self.initial_cpu),
             (TRANS.T_PRIORITY, self.static_priority),
             (TRANS.T_START_JIFFIES, self.start_jiffies),
             (TRANS.T_ALLOCATED_JIFFIES, self.allocated_jiffies),
             (TRANS.T_DEADLINE, self.deadline),
             (TRANS.T_ACTUAL_STATRT_JIFFIES, self.actual_start_jiffies),
             (TRANS.T_ACTUAL_JIFFIES, self.actual_jiffies),
             (TRANS.T_FINISH_JIFFIES, self.actual_finish_jiffies),
             (TRANS.T_COUNTER, self.counter),
             (TRANS.T_TASK_COUNTER, self.task_counter),
             (TRANS.T_START_TIME, self.start_time),
             (TRANS.T_FINISH_TIME, self.finish_time),
             (TRANS.T_ACTUAL_TIME, self.actual_time),
             ]
        FMT = '%-40s : %10s'
        t = [FMT % x for x in t]
        return "\n".join(t)
    pass

        
        
