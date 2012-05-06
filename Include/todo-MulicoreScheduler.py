#-*- coding: UTF-8 -*-
import Scheduler
import time

# Todo:
class MulticoreScheduler(Scheduler.BasicScheduler):
    
    def UpdateTasks(self):
        
        #----------------------
        # 选择task
        while self.res.gTASKS_TO_RUN != []:
            task = self.res.gTASKS_TO_RUN[0]
            #------------------------
            # 还没有轮到时
            if task.start_jiffies > self.res.gTIMER.jiffies:
                break
            
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
            
            
            
#            i = task.initial_cpu
#            if i>=len(self.res.gCPUS) or i<0: 
#                i = task.pid % (len(self.res.gCPUS))
#                pass
#            self.res.gCPUS[i].active_task_list.append(task)
            
            self.res.gTASKS_TO_RUN.pop(0)
            pass
        return

    def RunCPU(self, cpu):
        assert cpu.active_task_list != []
        assert cpu.expired_task_list != []
        
        if cpu.current_task == None:
            return cpu

        #----------------------
        # 处理当前任务
        task = cpu.current_task
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
                
                cpu.gTASKS_ACTIVE.append(task)
                pass
        else: cpu.gTASKS_ACTIVE.append(task)
        return cpu
    
    def Run(self):
        #----------------------
        # 执行task
        for i in range(len(self.res.gCPUS)):
            cpu = self.res.gCPUS[i]
            self.res.gCPUS[i] = self.RunCPU(cpu)
            pass
        return
    def ScheduleCPU(self, cpu):
        def cmp_tasks(taskA, taskB):
            ret = cmp(taskA.start_jiffies, taskB.start_jiffies)
            if ret == 0: ret = cmp(taskA.dynamic_priority, taskB.dynamic_priority)
            return ret
        
        def get_best_cpu(current_cpu, task):
            #------------------------
            # TODO: 这里只选了运行进程最少的CPU来处理产生的task
            for i, cpu in self.res.gCPUS:
                if cpu.current_task == None:
                    return self.res.gCPUS[i]
                    break
                pass
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
