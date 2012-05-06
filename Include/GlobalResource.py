#-*- coding: UTF-8 -*-
from Timer import Timer
from CPU import CPU

class GlobalResource:
    def __init__(self, conf):
        # gTASKS_EXPIRED and gTASKS_ACTIVE consist gTASKS_TO_RUN
        self.gTASKS_TO_RUN = []
        self.gTASKS_EXPIRED = []
        self.gTASKS_ACTIVE = []
        
        # when simulation done, gTASKS_FINISHED should be the same as 
        # gTASKS_TO_RUN before simulation
        self.gTASKS_FINISHED = []
        
        self.gCPUS = [CPU(i) for i in range(conf.CPU_AMOUNT)]
        
        self.gSCHEDULER = None
        
        self.gTIMER = Timer()
        self.conf = conf
        
        #------------------------------
        ## todo: 需要全部更改成gCONFIG
        self.gCONFIG = conf
        return
    
    
