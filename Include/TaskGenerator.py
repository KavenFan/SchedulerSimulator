#-*- coding: UTF-8 -*-
from Task import Task
#from CPU import CPU

from random import randint
import random

import Logger

class TaskGenerator:
    
    def __init__(self, conf, res):
        self.conf = conf
        self.res = res
        self.tasks = None
        return
    
    def get_rand(self,left_end, right_end):
        return random.randrange(left_end, right_end, 1)
    
    def adjust_task(self, task):
        task.deadline = task.start_jiffies + task.allocated_jiffies + task.conf.TOLERANT_JIFFIES
        task.task_counter = task.allocated_jiffies
        task.counter = 0 # HZ
        task.current_cpu = task.initial_cpu
#        bonus <10 and bonus >0
#        bonus = min(average_sleep_time /100, 10)
        task.bonus = 0
#        if static_prioriy <120: counter = (140-static_priority)*20
#        else: counter = (140-static_priority)*5
        
        dynamic_priority=max(100, min(task.static_priority - task.bonus+5,139))
        task.dynamic_priority = None
        
        return task
    
    def adjust_distribution(self,distribution_list):
        temp = 0
        result = []
        #((left_end, right_end), (proportion_left, proportion_right)),
        for item in distribution_list:
            ends = item[0]
            t = (temp, temp+item[1])
            temp += item[1]
            t = [ends, t]
            result.append(t)
            pass
        
        return result
    
    def get_rand_from_distribution(self, adjusted_list):
        max_proportion = adjusted_list[-1][1][1]
        t = self.get_rand(0, max_proportion)
        for item in adjusted_list:
            if t>= item[1][0] and t< item[1][1]:
                ends = item[0]
                pass
            pass
        
        if type(item[0])==type((0,0)):
            return self.get_rand(ends[0], ends[1])
        else:
            return ends
        
    def generate_tasks(self):
        self.tasks = []
        run_time_distribution_list = self.adjust_distribution(self.conf.RUN_TIME_DISTRIBUTION)
        start_time_distribution_list =  self.adjust_distribution(self.conf.START_TIME_DISTRIBUTION)
        task_type_distribution_list =  self.adjust_distribution(self.conf.TASK_TYPE_DISTRIBUTION)
        initial_cpu_distribution_list = self.adjust_distribution(self.conf.INITIAL_CPU_DISTRIBUTION)
        static_priority_distribution = self.adjust_distribution(self.conf.STATIC_PRIORITY_DISTRIBUTION)
        for i in range(1, self.conf.TASK_AMOUNT + 1):
            task = Task(self.conf)
            task.pid = i
            task.start_jiffies = self.get_rand_from_distribution(start_time_distribution_list)
            task.allocated_jiffies = self.get_rand_from_distribution(run_time_distribution_list)
            task.static_priority = self.get_rand_from_distribution(static_priority_distribution)
            
            task.initial_cpu = self.get_rand_from_distribution(initial_cpu_distribution_list)
            '''if task_type is the same with the cpu's type, 
            process will perform better on this cpu'''
            task.task_type = self.get_rand_from_distribution(task_type_distribution_list)
            task = self.adjust_task(task)
            self.tasks.append(task)
            pass
                
        return self.tasks
    
   
    def __str__(self):
        t = []
        SUBSECTION = "-" * 70
        for task in self.tasks:
            t.append(str(task))
            t.append(SUBSECTION)
        return "\n".join(t)
    
    def save_task_list(self, task_list, file_name):
        def persistence_list(task):
            t = [
                 ("pid", task.pid),
                 ("start_jiffies", task.start_jiffies),
                 ("allocated_jiffies", task.allocated_jiffies),
                 ("task_type", task.task_type),
                 ("static_priority", task.static_priority),
                 ("initial_cpu", task.initial_cpu),
                 ]
            return t
        
        w = Logger.Logger(file_name, False)
        FMT = '%20s : %s'
        SEPERATOR = '-' * 70
        for task in task_list:
            t = [FMT % x for x in persistence_list(task)]
            w.log('\n'.join(t))
            w.log(SEPERATOR)
            pass
        return
    
    def load_task_list(self, file_name):
        f = open(file_name, "r")
        t = f.readlines()
        f.close()
        t = [x.split(':') for x in t]
        
        task_list = []
        index = 0
        for i in range(len(t)):
            if len(t[i]) < 2:
                temp_list = t[index:i]
                index = i + 1
                if temp_list == []: continue
                task = Task(self.conf)
                temp_list = [(x[0].strip(), x[1].strip()) for x in temp_list]
                for x in temp_list: exec('task.%s = %s' % (x[0], x[1]))
                task = self.adjust_task(task)
                task_list.append(task)
                pass
            pass
        return task_list
    
    pass

        
            
        
        
        
