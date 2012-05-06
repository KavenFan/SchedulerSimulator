#-*- coding: UTF-8 -*-
import time

from Include.TaskGenerator import TaskGenerator
from Include.ReportCollector import ReportCollector
from Include.Logger import Logger

from Include.GlobalResource import GlobalResource 
from Include.Config import Configuration

import Include.Translation as TRANS

conf = Configuration()
res = GlobalResource(conf)
task_generator = TaskGenerator(conf, res)
Scheduler = conf.SCHEDULER

if conf.DEBUG:
    debug_log = Logger(conf.DEBUG_LOG_FILE, conf.LOG_VERBOSE)
    log = debug_log
elif conf.LOG:
    debug_log = Logger(None, False)
    log = Logger(conf.LOG_FILE, conf.LOG_VERBOSE)
else:
    debug_log = Logger(None, False)
    log = Logger(None, False)
    pass

def debug(s):
    debug_log.log(s)
    return

def tick():
    global res
    
    res.gSCHEDULER.schedule()
    res.gTIMER.jiffies += conf.TIME_INCREMET
    for i, cpu in enumerate(res.gCPUS):
        task = cpu.current_task
        if task == None:
            continue
        #----------------------
        ## 消耗基频数，即，运行进程
        #  这里使用时间片进程处理，所以在调度中也应该处理好时间片的相关情况。
        task.counter -= conf.TIME_INCREMET
        res.gCPUS[i] = cpu
        #--------------------------------------------------
        debug(task)
        debug('> res.gTIMER.jiffies \t %d' % res.gTIMER.jiffies)
        debug('> CPU \t %d' % cpu.id)
        debug('> task amount in res.gTASKS_ACTIVE \t %d' % len(res.gTASKS_ACTIVE))
        debug('> task amount in res.gTASKS_TO_RUN \t %d' % len(res.gTASKS_TO_RUN))
        debug('> task amount in res.gTASKS_FINISHED \t %d' % len(res.gTASKS_FINISHED))
        debug('> task amount in res.gTASKS_EXPIRED \t %d' % len(res.gTASKS_EXPIRED))
        debug_log.log_subsection()
        pass

    return

def done():
    global res
    t = [cpu.current_task for cpu in res.gCPUS]
    if any(t):
        return False
    if len(res.gTASKS_ACTIVE) > 0:
        return False
    if len(res.gTASKS_TO_RUN) > 0:
        return False
    if len(res.gTASKS_EXPIRED) > 0:
        return False
    
    return True

import sys
def ParseArg():
    if len(sys.argv)<1:
        return
    i = 1
    while i<len(sys.argv):
        if argv[i]=='--scheduler' and i+1 <len(sys.argv):
            exec ('conf.SCHEDULER = %s' %sys.argv[i])
            pass
        pass
    return


if __name__ == "__main__":
    #----------------------------------------------
    ## 解析命令行
    # todo: 还没有实现，需要能够选择配置文件，配置一些基本的设置
    ParseArg()
    report_collector = ReportCollector(res)
    
    #----------------------------------------------
    ## 开始
    log.log_start()
    log.log(conf)
    
    #----------------------------------------------
    ## 生成进程序列
    log.log_section()
    if conf.LOAD_TASKS:
        log.log(TRANS.M_LOAD_TASKS)
        res.gTASKS_TO_RUN = task_generator.load_task_list(conf.TASKS_LOAD_FROM_FILE)
    else:
        log.log(TRANS.M_GENERATION_START)
        res.gTASKS_TO_RUN = task_generator.generate_tasks()
        pass
    
    if conf.SAVE_TASKS:
        log.log(TRANS.M_SAVE_TASKS)
        task_generator.save_task_list(res.gTASKS_TO_RUN, conf.TASKS_SAVE_TO_FILE)
        pass
    
    for task in res.gTASKS_TO_RUN:
        debug(task)
        debug_log.log_subsection()
        pass
    
    #----------------------------------------------
    ## 选择调度器
    # todo:这里可以改进
    res.gSCHEDULER = Scheduler(res)
    
    
    #----------------------------------------------
    ## 模拟
    report_collector.collect_start()
    log.log_section()
    log.log(TRANS.M_SIMULATION_START)
    if (conf.SIMULATE):
        while not done():
            tick()
        pass
    report_collector.collect_end()
    
    log.log(TRANS.M_SIMULATION_END)
    
    #----------------------------------------------
    ## 收集进程
    log.log_section()
    log.log(TRANS.M_COLLECT_TASK)
    
    
    #----------------------------------------------
    ## 确保完成的进程以开始时间排序
    def cmp_tasks(taskA, taskB):
        ret = cmp(taskA.start_jiffies, taskB.start_jiffies)
        if ret == 0:
            ret = cmp(taskA.dynamic_priority, taskB.dynamic_priority)
        return ret
    res.gTASKS_FINISHED.sort(cmp_tasks)
    for task in res.gTASKS_FINISHED:
        log.log_subsection()
        log.log(task)
        pass
    
    #----------------------------------------------
    ## 收集报告
    log.log_section()
    log.log(TRANS.M_COLLECT_REPORT)
    report_collector.collect(res.gTASKS_FINISHED)
    log.log_subsection()
    log.log(report_collector)
    
    if conf.RECORD_TASKS:
        report_collector.record_task_list(res.gTASKS_FINISHED,conf.TASKS_RECORD_FILE)
    
    #----------------------------------------------
    ## 结束
    log.log_end()
    
