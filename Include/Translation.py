#-*- coding: UTF-8 -*-
#-------------------------------
## Chinese
## M_ means the variable is used in main.py
M_GENERATION_START = "*正在生成任务..."
M_LOAD_TASKS = "*正在载入任务..."
M_SAVE_TASKS = "*正在保存任务..."
M_SIMULATION_START = "*正在模拟..."
M_SIMULATION_END = "*模拟结束 "
M_COLLECT_TASK = "*正在收集任务..."
M_COLLECT_REPORT = "*正在收集报告..."

#--------------
## L_ means the variable used in Logger.py
L_START = "＝【开始】%s" % (30 * "＝")
L_END = "%s【结束】＝" % (30 * "＝")
L_SECTION = "＝" * 35
L_SUBSECTION = "━" * 35

#--------------
# RC_ means the variable used in ReportCollector.py
RC_CPU_AMOUNT =             "*处理器数量　　　　　　　　　"
RC_TASK_AMOUNT =            "*任务数量　　　　　　　　　　"
RC_EXCEED_DEADLINE_AMOUNT = "*不在期望时间内完成的任务数量"
RC_WITHIN_DEADLINE_AMOUNT = "*在期望时间内完成的任务数量　"
RC_IN_TIME_AMOUNT =         "*及时完成的任务数量　　　　　"
RC_NOT_IN_TIME_AMOUNT =     "*没有及时完成的任务数量　　　"
RC_TASK_TYPE =              "*任务类型数量　　　　　　　　"
RC_CPUS_INIT_CPU =          "*初始处理器数量　　　　　　　"
RC_TOTAL_ALLOCATED_JIFFIES ="*分配的总任务基频数　　　　　"
M_START_TIME =              "*开始时间　　　　　　　　　　"
M_END_TIME =                "*结束时间　　　　　　　　　　"
M_TOTAL_TIME =              "*耗费的时间　　　　　　　　　"
M_START_JIFFIES =           "*开始基频数　　　　　　　　　"
M_END_JIFFIES =             "*结束基频数　　　　　　　　　"
M_TOTAL_JIFFIES =           "*耗费的基频数　　　　　　　　"

#--------------
# T_ means the variable used in Task.py
T_PID =                     "任务标识　　　"
T_INITIAL_CPU =             "初始处理器　　"
T_ALLOCATED_JIFFIES =       "分配的基频数　"
T_START_JIFFIES =           "开始基频数　　"
T_DEADLINE =                "期望截止基频数"
T_ACTUAL_JIFFIES =          "实际耗费基频数"
T_ACTUAL_STATRT_JIFFIES =   "实际开始基频数"
T_FINISH_JIFFIES =          "实际结束基频数"
T_START_TIME =              "实际开始时间　"
T_FINISH_TIME =             "实际结束时间　"
T_ACTUAL_TIME =             "实际耗费时间　"
T_PRIORITY =                "优先级　　　　"
T_COUNTER =                 "基频计数器　　"
T_TASK_COUNTER =            "任务基频计数器"

#--------------
## C_ means the variable used in Config.py
C_CPU_AMOUNT =              "*处理器数量　　　　"
C_SCHEDULER =               "*调度器　　　　　　"
C_TASK_AMOUNT =             "*任务数量　　　　　"
C_DEBUG =                   "*是否调试　　　　　"
C_DEBUG_LOG_FILE =          "*调试信息文件　　　"
C_TASKS_PICKLE_FILE =       "*任务持久文件　　　"
C_LOG_FILE =                "*日志文件　　　　　"
C_LOG =                     "*是否保存日志　　　"
C_LOG_VERBOSE =             "*是否输出显示日志　"

C_SAVE_TASKS =              "*是否保存任务　　　"
C_TASKS_SAVE_TO_FILE =      "*任务保存文件　　　"
C_LOAD_TASKS =              "*是否载入任务　　　"
C_TASKS_LOAD_FROM_FILE =    "*任务载入文件　　　"
C_RECORD_TASKS =            "*是否记录任务　　　"
C_TASKS_RECORD_FILE =       "*任务记录文件　　　"
