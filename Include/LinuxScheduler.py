#-*- coding: UTF-8 -*-
import Scheduler
import time

# Todo:
class LinuxScheduler(Scheduler.BasicScheduler):
    
    def UpdateTasks(self):
        
        #----------------------
        # 选择task
        while self.res.gTASKS_TO_RUN != []:
            task = self.res.gTASKS_TO_RUN[0]
            #------------------------
            #任务还没开始
            if task.start_jiffies > self.res.gTIMER.jiffies:
                break
            #------------------------
            task.start_time = time.time()
            task.actual_start_jiffies = self.res.gTIMER.jiffies
            #------------------------
            #根据静态优先级计算基本时间片
            if task.static_priority<120: 
                task.counter=(140-task.static_priority)*20
            else: task.counter=(140-task.static_priority)*5
            
#            task.counter *= self.res.conf.JIFFIES_PER_MICROSECOND
            if task.counter>task.task_counter:
                task.counter = task.task_counter
            task.task_counter -= task.counter
            
            #------------------------
            # TODO: 这里只选了原始的CPU来处理产生的task
            i = task.initial_cpu
            if i>=len(self.res.gCPUS) or i<0: 
                i = task.pid % (len(self.res.gCPUS))
                pass
            self.res.gCPUS[i].active_task_list.append(task)
            
            self.res.gTASKS_TO_RUN.pop(0)
            pass
        return

#    def RunTask(self, task):
#        
#        return task
    
    def RunCPU(self, cpu):
        if cpu.current_task == None and cpu.active_task_list == []:
            if cpu.expired_task_list == []: return cpu
            
            #----------------------
            # 直接使用expired_task_list
            cpu.active_task_list = cpu.expired_task_list
            cpu.expired_task_list = []
            for i in range(len(cpu.active_task_list)):
                cpu.active_task_list[i].counter = self.res.conf.INIT_TIME_COUNTER_JIFFIES
                cpu.active_task_list[i].task_counter -=cpu.active_task_list[i].counter
                pass
            return cpu
            pass
        #----------------------
        # 处理当前任务
        task = cpu.current_task
        if task == None: 
            task = cpu.active_task_list[0]
            cpu.active_task_list.pop(0)
            pass
        cpu.current_task = None
        task.counter -= self.res.conf.TIME_INCREMET
        if task.counter <= 0:
            if task.task_counter <= 0:
                task.finish_time = time.time()
                task.actual_time = task.finish_time - task.start_time
                task.actual_finish_jiffies = self.res.gTIMER.jiffies
                task.actual_jiffies = task.actual_finish_jiffies - task.actual_start_jiffies
                self.res.gTASKS_FINISHED.append(task)
            else: 
                if task.static_priority<120: 
                    task.counter=(140-task.static_priority)*20
                else: task.counter=(140-task.static_priority)*5
                
#                task.counter *= self.res.conf.JIFFIES_PER_MICROSECOND
                if task.counter>task.task_counter:
                    task.counter = task.task_counter
                task.task_counter -= task.counter
                
                #----------------------
                # 时间片用完，但任务还未结束
                cpu.expired_task_list.append(task)
                pass
        else: cpu.active_task_list.append(task)
        return cpu
    
    def Run(self):
        #----------------------
        # 执行task
        self.res.gTASKS_ACTIVE = []
        self.res.gTASKS_EXPIRED = []
        for i in range(len(self.res.gCPUS)):
            cpu = self.res.gCPUS[i]
            self.res.gCPUS[i] = self.RunCPU(cpu)

            self.res.gTASKS_ACTIVE += cpu.active_task_list
            self.res.gTASKS_EXPIRED += cpu.expired_task_list            
            pass
        return
    
    def ScheduleCPU(self, cpu):
        def cmp_tasks(taskA, taskB):
            ret = cmp(taskA.start_jiffies, taskB.start_jiffies)
            if ret == 0: ret = cmp(taskA.dynamic_priority, taskB.dynamic_priority)
            return ret
        
        def get_best_cpu(current_cpu, task):
            return current_cpu
        if cpu.active_task_list == []: return cpu
        #----------------------
        # 调度开始
        #----------------------
        if cpu.current_task != None:
            cpu.active_task_list.append(cpu.current_task)
            cpu.current_task = None
            pass
        #----------------------
        # 排序
        cpu.active_task_list.sort(cmp_tasks)
        #----------------------
        # 选择最高优先级的task
        task = cpu.active_task_list[0]
        cpu.active_task_list.pop(0)
        #----------------------
        # 选择最高优先级的CPU
        best_cpu = get_best_cpu(cpu, task)
        if best_cpu != cpu:
            best_cpu.active_task_list.append(task)
            #----------------------
            # 选择下一个最高优先级的task
            if cpu.active_task_list == []: return cpu
            task = cpu.active_task_list[0]
            cpu.active_task_list.pop(0)
            pass
        assert cpu.current_task == None
        cpu.current_task = task
        return cpu
    
    def schedule(self):
        self.UpdateTasks()
        for i in range(len(self.res.gCPUS)):
            cpu = self.res.gCPUS[i]
            self.res.gCPUS[i] = self.ScheduleCPU(cpu)
            pass
        self.Run()
        
        return
    
    pass
