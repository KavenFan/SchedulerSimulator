#-*- coding: UTF-8 -*-

import Translation as TRANS
import Logger
import time

class ReportCollector:
    def __init__(self, res):
        self.tasks_exceed_deadline = None
        self.tasks_within_deadline = None
        self.tasks_in_time = None
        self.tasks_not_in_time = None
        self.tasks = None
        self.res = res
        return
    
    def __str__(self):
#        g = lambda name, data: "%-30s \t %s" % (name, data)
        FMT = "%-30s : %15d"
        FLOAT_FMT = "%-30s : %15.2f"
        
        t = [
            (TRANS.RC_CPU_AMOUNT,len(self.res.gCPUS)),
            (TRANS.RC_TASK_AMOUNT,len(self.tasks)),
            (TRANS.RC_EXCEED_DEADLINE_AMOUNT,len(self.tasks_exceed_deadline)),
            (TRANS.RC_WITHIN_DEADLINE_AMOUNT,len(self.tasks_within_deadline)),
            (TRANS.RC_IN_TIME_AMOUNT,len(self.tasks_in_time)),
            (TRANS.RC_NOT_IN_TIME_AMOUNT,len(self.tasks_not_in_time)),
            (TRANS.RC_TASK_TYPE,len(self.tasks_task_type)),
             ]
        t = [FMT%x for x in t]
        for item in self.tasks_task_type:
            t.append("    %s : %s"%(str(item), len(self.tasks_task_type[item])))
            pass
        t.append(FMT%(TRANS.RC_CPUS_INIT_CPU,len(self.cpus_init_cpu)))
        for item in self.cpus_init_cpu:
            t.append("    %s : %s"%(str(item), len(self.cpus_init_cpu[item])))
            pass
        total_allocated_jiffies = sum([task.allocated_jiffies for task in self.tasks])
        
            
        t += [
            FLOAT_FMT % (TRANS.M_START_TIME, self.start_time),
            FLOAT_FMT % (TRANS.M_END_TIME, self.end_time),
            FLOAT_FMT % (TRANS.M_TOTAL_TIME, self.end_time - self.start_time),
            FMT % (TRANS.M_START_JIFFIES, self.start_jiffies),
            FMT % (TRANS.M_END_JIFFIES, self.end_jiffies),
            FMT % (TRANS.M_TOTAL_JIFFIES, self.end_jiffies - self.start_jiffies),
            FMT % (TRANS.RC_TOTAL_ALLOCATED_JIFFIES,total_allocated_jiffies),
            ]
        
        return "\n".join(t)
    
    def collect_start(self):
        self.start_time = time.time()
        self.start_jiffies = self.res.gTIMER.jiffies
        return
    
    def collect_end(self):
        self.end_jiffies = self.res.gTIMER.jiffies
        self.end_time = time.time()
        return
        
    
    def collect(self, tasks):
        self.tasks = tasks
        self.tasks_exceed_deadline = [task for task in tasks if task.actual_finish_jiffies > task.deadline]
        self.tasks_within_deadline = [task for task in tasks if task.actual_finish_jiffies <= task.deadline]
        self.tasks_in_time = [task for task in tasks if task.actual_jiffies <= task.allocated_jiffies]
        self.tasks_not_in_time = [task for task in tasks if task.actual_jiffies > task.allocated_jiffies]
        self.tasks_task_type ={}
        self.cpus_init_cpu={}
        for task in tasks:
            if self.tasks_task_type.has_key(task.task_type):
                self.tasks_task_type[task.task_type].append(task)
            else: self.tasks_task_type[task.task_type]=[task,]
            
            if self.cpus_init_cpu.has_key(task.initial_cpu):
                self.cpus_init_cpu[task.initial_cpu].append(task)
            else: self.cpus_init_cpu[task.initial_cpu]=[task,]
            pass
            
        return
    
    def record_task_list(self, task_list, file_name):
        def persistence_list(task):
            t = {
                 "pid": task.pid,
                 "start_jiffies": task.start_jiffies,
                 "finish_jiffies": task.start_jiffies+task.allocated_jiffies,
                 "allocated_jiffies": task.allocated_jiffies,
                 "actual_start_jiffies": task.actual_start_jiffies,
                 "actual_consumed_jiffies": task.actual_jiffies,
                 "task_type": task.task_type,
                 "static_priority": task.static_priority,
                 "initial_cpu": task.initial_cpu,
                 "actual_finish_jiffies": task.actual_finish_jiffies,
                 "deadline": task.deadline,
                 "counter": task.counter,
                 "task_counter": task.task_counter,
                 "dynamic_priority": task.dynamic_priority,
                 "bonus": task.bonus,
                 "start_time": task.start_time,
                 "finish_time": task.finish_time,
                 "actual_time": task.actual_time,
                 "cpu_priority": task.cpu_priority,
                 }
        
            return t
        
        if task_list==[]:return
        
        w = Logger.Logger(file_name, False)
        keys = [
                 "pid",
                 "task_type",
                 "static_priority",
                 "start_jiffies",
                 "finish_jiffies",
                 "deadline",
                 "allocated_jiffies",
                 "actual_start_jiffies",
                 "actual_finish_jiffies",
                 "actual_consumed_jiffies",
                 "cpu_priority",
                 "initial_cpu",
                 "counter",
                 "task_counter",
                 "dynamic_priority",
                 "bonus",
                 "start_time",
                 "finish_time",
                 "actual_time",
                 ]
        result = []
        
        result.append('\t'.join(keys))
        for task in task_list:
            D = persistence_list(task)
            t = [str(D[x]) for x in keys]
            result.append('\t'.join(t))
            pass
        
        w.log('\n'.join(result))
        return
