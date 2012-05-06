#-*- coding: UTF-8 -*-
import os

import Translation as TRANS

class Configuration:
    
    ## configure all configurable settings
    def __init__(self):     
           
        #------------------------------------------------------------
        ## Scheduler settings
        #----------------------------
        ## Normal Scheduler
#        import Scheduler
#        self.SCHEDULER = Scheduler.NormalScheduler
        #----------------------------
        ## FCFS Scheduler
        import FCFSScheduler
        self.SCHEDULER = FCFSScheduler.FCFSScheduler
        #----------------------------
        ## CPU Priority Scheduler
#        import CPUPriorityScheduler
#        self.SCHEDULER = CPUPriorityScheduler.CPUPriorityScheduler
        
        #------------------------------------------------------------
        #----------------------------
        # TASKS_SAVE_TO_FILE is used to save task, and then with same tasks list,
        # they will be used for next comparation
        self.SAVE_TASKS = False
        self.TASKS_SAVE_TO_FILE = 'Results/saved-tasks.txt'
        self.LOAD_TASKS = True
        self.TASKS_LOAD_FROM_FILE = 'Results/saved-tasks.txt'
        self.LOG = True
        self.LOG_VERBOSE = True
        self.LOG_FILE = 'Results/run_log.txt'
        self.RECORD_TASKS = True
        self.TASKS_RECORD_FILE = 'Results/record-task.txt'
        
        #------------------------------------------------------------
        ## CPUs settings
        self.CPU_AMOUNT = 4
        
        #------------------------------------------------------------
        ## Tasks settings
        #----------------------------
        ## Basic Task settings
        self.TASK_AMOUNT = 200
        self.TASK_START_TIME = 0 # HZ
#        self.TASK_END_TIME = 200000 #HZ
        
        
        #------------------------------------------------------------
        ## Log settings
        #----------------------------
        # if DEBUG is False, the DEBUG_LOG_FILE will not be used
        # if DEBUG is True, the LOG_FILE will not be used
        self.DEBUG = False
        self.DEBUG_LOG_FILE = 'Results/debug_log.txt'
        self.SIMULATE = True
        
        
        # the worst case task will cost, that means time allocated to the task
        # will be between INIT_TASK_TIME and WORST_CASE_EXECUTE_TIME
        # todo: not used
        self.WORST_CASE_EXECUTE_TIME = 20000 #HZ
        
        #------------------------------------------------------------
        ## Task Distribution settings
#        ((left_end, right_end), proportion),
        self.RUN_TIME_DISTRIBUTION = [
                  ((0, 200), 4),
                  ((200, 2000), 5),
                  ((2000, 20000), 12),
                  ((20000, 100000), 45),
                  ((100000, 200000), 28),
                  ((200000, 2000000), 4),
                  ((2000000, 4000000), 2),
                  ]
        
#        ((left_end, right_end), proportion),
        self.START_TIME_DISTRIBUTION = [
                  ((0, 4000000), 100),
                  ]
        
        self.STATIC_PRIORITY_DISTRIBUTION = [
                  ((100, 110), 5),
                  ((110, 120), 45),
                  ((120, 130), 35),
                  ((130, 140), 15),
                  ]
        
        
        self.NORMAL = 0
        self.CONSUME_CPU = 1
        self.CONSUME_MEMORY = 2
        self.INTERACTIVE = 3
#        (task_type, proportion),
        self.TASK_TYPE_DISTRIBUTION = [
                  (self.NORMAL, 10),
                  (self.CONSUME_CPU, 40),
                  (self.CONSUME_MEMORY, 20),
                  (self.INTERACTIVE, 10),
                  ]
        
#        ((init_cpu), proportion),
        self.INITIAL_CPU_DISTRIBUTION = [
                  (0, 20),
                  (1, 20),
                  (2, 20),
                  (3, 20),
                  ]

        # timer increment, every tick, HZ amount jiffies will increase 
#        self.TIME_INCREMET = 200 #HZ
        self.TIME_INCREMET = 20 #HZ
        
        # a new process has INIT_TASK_TIME millisecond
        self.INIT_TASK_TIME = 200 # HZ
        # used for 
        self.TOLERANT_JIFFIES = 200
        
        # todo: not used
        self.LASTET_START_TIME = 2000000 #HZ
        
        # todo: not used
        # the highest prioriy of a task, which means static_priority assigned to
        # the task will be  >=LOWEST_PRIORITY and <HIGHEST_PRIORITY
        self.LOWEST_PRIORITY = 100
        self.HIGHEST_PRIORITY = 140
        
        # todo: not used
        #CPU clock 1200*1000*1000 times every second
        self.CPU_FREQUENCY = 1200 * 1000 * 1000 
        self.JIFFIES_PER_MICROSECOND = 1
        
        # todo: not used
        # timer interrupt every TIMER_INTERRUPT_FREQUENCY clock
        self.TIMER_INTERRUPT_FREQUENCY = 1000 #ms, for convenience
        
        #-----------------------------------------------------
        # todo:
        # for update use
        self.REPORT_LANGUAGE = 'Chinese'
        self.SUPPORTED_LANGUAGE_LIST = [
                  'Chinese',
                  'English',
                  ]
        
        self.check_assert()
        return
    
    ## format configurations output
    def __str__(self):
        FMT = "%-30s \t %s"
        t = [
            (TRANS.C_CPU_AMOUNT, self.CPU_AMOUNT),
            (TRANS.C_TASK_AMOUNT, self.TASK_AMOUNT),
            (TRANS.C_SCHEDULER, self.SCHEDULER.__name__),
            ]
        t.append((TRANS.C_DEBUG, self.DEBUG))
        if self.DEBUG:t.append((TRANS.C_DEBUG_LOG_FILE, self.DEBUG_LOG_FILE))
        
        t.append((TRANS.C_LOAD_TASKS, self.LOAD_TASKS))
        if self.LOAD_TASKS:t.append((TRANS.C_TASKS_LOAD_FROM_FILE, self.TASKS_LOAD_FROM_FILE))
        
        t.append((TRANS.C_SAVE_TASKS, self.SAVE_TASKS))
        if self.SAVE_TASKS:t.append((TRANS.C_TASKS_SAVE_TO_FILE, self.TASKS_SAVE_TO_FILE))
        
        t.append((TRANS.C_LOG_FILE, self.LOG_FILE))
        t.append((TRANS.C_LOG_VERBOSE, self.LOG_VERBOSE))
        
        t.append((TRANS.C_RECORD_TASKS, self.RECORD_TASKS))
        if self.RECORD_TASKS:t.append((TRANS.C_TASKS_RECORD_FILE, self.TASKS_RECORD_FILE))
        
        t = [FMT % x for x in t]
        return '\n'.join(t)
    
    ## make sure all configurations are legal
    def check_assert(self):
        assert self.CPU_AMOUNT > 0
        assert self.TASK_AMOUNT > 0
        

#        ((left_end, right_end), proportion),
        for L in self.RUN_TIME_DISTRIBUTION:
            assert len(L) == 2
            assert len(L[0]) == 2
            left_end = L[0][0]
            assert left_end >= 0
            right_end = L[0][1]
            assert right_end > 0
            assert left_end <= right_end
            
            proportion = L[1]
            assert proportion >= 0
            pass
            
#        ((left_end, right_end), proportion),
        for L in self.START_TIME_DISTRIBUTION:
            assert len(L) == 2
            assert len(L[0]) == 2
            
            left_end = L[0][0]
            assert left_end >= 0
            
            right_end = L[0][1]
            assert right_end > 0
            assert left_end <= right_end
            
            proportion = L[1]
            assert proportion >= 0
            pass
        
        
        t = [self.NORMAL , self.CONSUME_CPU , self.CONSUME_MEMORY, self.INTERACTIVE, ]
        assert len(set(t)) == len(t)
        
#        (task_type, proportion),
        for L in self.TASK_TYPE_DISTRIBUTION:
            assert len(L) == 2
            
            proportion = L[1]
            assert proportion >= 0
            pass
        
        # if DEBUG is False, the DEBUG_LOG_FILE will not be used
        # if DEBUG is True, the LOG_FILE will not be used
        assert self.DEBUG is False or self.DEBUG is True
        assert self.SIMULATE  is False or self.SIMULATE is True
        
        #------------------------------------------------------------
        t = os.path.dirname(self.DEBUG_LOG_FILE)
        if self.DEBUG and t != "": assert os.path.exists(t)
        t = os.path.dirname(self.DEBUG_LOG_FILE)
        if self.DEBUG and t != "": assert os.path.exists(t)
        
        #------------------------------------------------------------
        assert self.LOG_VERBOSE is True or self.LOG_VERBOSE is False
        
        #------------------------------------------------------------
        t = os.path.dirname(self.LOG_FILE)
        if not self.DEBUG and t != "": assert os.path.exists(t)
        
      
        # TASKS_PICKLE_FILE is used to save task, and the with same tasks list,
        # they will be used for next compare
        assert self.SAVE_TASKS is True or self.SAVE_TASKS is False
        t = os.path.dirname(self.TASKS_SAVE_TO_FILE)
        if self.SAVE_TASKS and t != "": assert os.path.exists(t)
        
        assert self.LOAD_TASKS is True or self.LOAD_TASKS is False
        if self.LOAD_TASKS: assert os.path.exists(self.TASKS_LOAD_FROM_FILE)
        
        # timer increment, every tick, HZ amount jiffies will increase 
        assert self.TIME_INCREMET > 0 #HZ
        
        # a new process has INIT_TASK_TIME millisecond
        assert self.INIT_TASK_TIME > 0 # HZ
        
        # the worst case task will cost, that means time allocated to the task
        # will be between INIT_TASK_TIME and WORST_CASE_EXECUTE_TIME
        assert self.WORST_CASE_EXECUTE_TIME > 0 #HZ
        
        assert self.LASTET_START_TIME > 0 #HZ
        
        # the highest prioriy of a task, which means static_priority assigned to
        # the task will be between 0 and HIGHEST_PRIORITY
        assert self.HIGHEST_PRIORITY > 0
        assert self.LOWEST_PRIORITY > 0
        assert self.HIGHEST_PRIORITY > self.LOWEST_PRIORITY
        
        
        
        #CPU clock 1200*1000*1000 times every second
        assert self.CPU_FREQUENCY > 0
        
        
        # timer interrupt every TIMER_INTERRUPT_FREQUENCY clock
        assert self.TIMER_INTERRUPT_FREQUENCY > 0
        
        assert self.REPORT_LANGUAGE in self.SUPPORTED_LANGUAGE_LIST
        return

