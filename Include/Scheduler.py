#-*- coding: UTF-8 -*-

import time

class BasicScheduler:
    def __init__(self, res):
        self.res = res
        def cmp_tasks(taskA, taskB):
            ret = cmp(taskA.start_jiffies, taskB.start_jiffies)
#            if ret == 0: ret = cmp(taskA.dynamic_priority, taskB.dynamic_priority)
            return ret
        self.res.gTASKS_TO_RUN.sort(cmp_tasks)
        return
    
    def __str__(self):
        t = [ "%30s : %s" % (x, eval("self." + x)) for x in dir(self) if str.isalpha(x[0])]
        return "\n".join(t)
    
    def finish_task(self,task):
        task.finish_time = time.time()
        task.actual_time = task.finish_time - task.start_time
        task.actual_finish_jiffies = self.res.gTIMER.jiffies
        task.actual_jiffies = task.actual_finish_jiffies - task.actual_start_jiffies
        self.res.gTASKS_FINISHED.append(task)
        
        return task
    
    pass

class NormalScheduler(BasicScheduler):
    ''' Normal Schedule '''
    '''这个Scheduler认为只有一个进程池，每一次运行都会先把所有的进程放在进程池gTASKS_TO_RUN中，
    然后一个一个从中选出进程，顺序放到各个处理器中    
    '''
    def schedule(self):
        for cpu in self.res.gCPUS:
            if cpu.current_task == None:
                continue
            if cpu.current_task.task_counter > 0:
                self.res.gTASKS_ACTIVE.append(cpu.current_task)
            else:
                task = self.finish_task(cpu.current_task)
                self.res.gTASKS_FINISHED.append(task)
                pass
            cpu.current_task = None
            pass
        
        if not any([self.res.gTASKS_TO_RUN,
                    self.res.gTASKS_ACTIVE,
                    self.res.gTASKS_EXPIRED]):
            return
        
        def cmp_tasks(taskA, taskB):
            ret = cmp(taskA.start_jiffies, taskB.start_jiffies)
            if ret == 0:
                ret = cmp(taskA.dynamic_priority, taskB.dynamic_priority)
            return ret
        self.res.gTASKS_TO_RUN.sort(cmp_tasks)
        
        for i in range(len(self.res.gTASKS_TO_RUN)):
            task = self.res.gTASKS_TO_RUN[0]
            if task.start_jiffies > self.res.gTIMER.jiffies:
                break
            task.start_time = time.time()
            self.res.gTASKS_ACTIVE.append(task)
            self.res.gTASKS_TO_RUN.pop(0)
            pass
        self.res.gTASKS_ACTIVE.sort(cmp_tasks)
        
        for cpu in self.res.gCPUS:
            # if tasks are all allocated, then return
            if self.res.gTASKS_ACTIVE == []:
                return
            cpu.current_task = self.res.gTASKS_ACTIVE[0]
            self.res.gTASKS_ACTIVE.pop(0)
            if cpu.current_task.actual_start_jiffies == None:
                cpu.current_task.actual_start_jiffies = self.res.gTIMER.jiffies
        
        return
    
    pass

