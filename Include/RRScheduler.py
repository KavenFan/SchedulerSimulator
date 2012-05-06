#-*- coding: UTF-8 -*-
import Scheduler
import time

## Roll Robin Scheduler
class RRScheduler(Scheduler.BasicScheduler):
    def schedule_cpu(self, cpu):
        #----------------------
        ## 处理当前任务
        task = cpu.current_task
        #----------------------
        ## 当前处理器没有运行任务
        if task == None: 
            if cpu.active_task_list == []: return cpu
            #----------------------
            ## 从活动进程队列中选择一个进程
            task = cpu.active_task_list[0]
            cpu.active_task_list.pop(0)
            cpu.current_task = task
            #----------------------
            ## 直接返回
            return cpu
        
        #------------------------
        ## 时间片用完时
        if task.counter <= 0:
            if task.task_counter<=0:
                #------------------------
                ## 进程结束时的处理
                #------------------------
                ## 先来先服务没有时间片的限制，所以就直接使用task_counter
                task = self.finish_task(task)
                cpu.current_task=None
                if cpu.active_task_list == []: return cpu
                #----------------------
                ## 从活动进程队列中选择一个进程
                task = cpu.active_task_list[0]
                cpu.active_task_list.pop(0)
                cpu.current_task = task
                #----------------------
                ## 直接返回
                return cpu
            #------------------------
            ## 时间片用完，但进程没有结束
            #------------------------
            ## 重新计算进程的时间片
            task.counter = self.res.conf.INIT_TIME_COUNTER_JIFFIES
            if task.counter>task.task_counter:
                task.counter = task.task_counter
            task.task_counter -= task.counter
            
            #------------------------
            ## 重把时间片用完的进程放到活动进程的尾部
            cpu.active_task_list.append(task)
            
            #----------------------
            ## 重新从活动进程队列中选择一个进程
            #  有几种情况：
            #  - 这个进程就是刚放进来的，在选择进程之前，活动队列只有一个进程
            #  - 这个进程不是刚放进来的，在选择进程之前，活动队列不止一个进程
            #  - 进程队列中应该不可能没有进程，没有进程的情况已经处理过了
            #----------------------
            ## 活动进程队列不应该没有进程
            assert cpu.active_task_list != []
            #----------------------
            ## 从活动队列中选择进程
            task = cpu.active_task_list[0]
            cpu.active_task_list.pop(0)
            cpu.current_task = task
            #----------------------
            ## 直接返回
            return cpu
        
        #----------------------
        ## 返回处理后的结果
        ## 有以下情况：
        #  - 没有当前进程，且该处理器的活动进程队列为空
        #  - 分配了一个当前进程，活动进程队列可能为空，也可能不为空
        #  - 
        return cpu
    
    
    def update_active_tasks(self):
        #----------------------
        ## 当将要运行的进程池中还有进程，选择task
        #  进程池中的进程应该已经以start_jiffies排过序
        while self.res.gTASKS_TO_RUN != []:
            task = self.res.gTASKS_TO_RUN[0]
            #------------------------
            ## 任务还没开始，因为已经排序，所以就结束循环
            if task.start_jiffies > self.res.gTIMER.jiffies:
                break
            
            #------------------------
            ## 设置将要开始的进程的开始时间 
            task.start_time = time.time()
            task.actual_start_jiffies = self.res.gTIMER.jiffies
            
            #------------------------
            ## 设置将要开始的进程的绑定CPU
            #  在这里只让进程绑定在给定的CPU上
            i = task.initial_cpu
            #------------------------
            ## 给定的CPU不合法，则分配一个合法的
            if i>=len(self.res.gCPUS) or i<0: 
                i = task.pid % (len(self.res.gCPUS))
                pass
            #------------------------
            ## 加入到绑定CPU的活动进程队列
            self.res.gCPUS[i].active_task_list.append(task)
            
            #------------------------
            ## 从进程池中删除
            self.res.gTASKS_TO_RUN.pop(0)
            pass
        return
    
    def schedule(self):
        #----------------------
        ## 从gTASKS_TO_RUN中对gTASKS_ACTIVE更新
        self.update_active_tasks()

        #----------------------
        ## 用来收集每个CPU中的活动进程
        self.res.gTASKS_ACTIVE = []
        #----------------------
        ## 让每个CPU执行调度
        for i, cpu in enumerate(self.res.gCPUS):
            self.res.gCPUS[i] = self.schedule_cpu(cpu)
            
            #----------------------
            ## 收集活动进程
            self.res.gTASKS_ACTIVE += cpu.active_task_list
            #----------------------
            ## current_task并不在处理器的actvie_task_list里
            #  不为空时收集
            if cpu.current_task!=None:
                self.res.gTASKS_ACTIVE +[cpu.current_task]
            pass
        
        return
    
    pass
