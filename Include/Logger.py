#-*- coding: UTF-8 -*-

import pickle

import Translation as TRANS

class Logger:
    ## Constructor
    #  @param LogFile File to save log, default to None
    #  @param ToPrint Whether print the log on screen, default to True
    def __init__(self, LogFile=None, ToPrint=True):
        self.ToPrint = ToPrint
        self.LogFile = LogFile
        self.clear()
        return

    ## Clear all contents in the log file
    def clear(self):
        if self.LogFile:
            File = open(self.LogFile, "w")
            File.write('')
            File.close()
            pass
        return

    ## Log the specified String
    #  @param Str object to log
    #  @note if Str is list, it will be convert to a several lines<br/>
    #if Str is other type beside string like, it will be convert to sting.
    def __print(self, Str):
        if type(Str) == list:
            Str = "\n".join(Str)
        elif type(Str) == str:
            Str = Str
        else:
            Str = str(Str)
            pass
        
        if self.ToPrint:
            print Str
            pass
        if self.LogFile:
            File = open(self.LogFile, "a")
            File.write(Str + "\n")
            File.close()
            pass
        return
    
    def __str__(self):
        g = lambda name, data: "%-30s : %s" % (name, data)
        t = []
        
        return "\n".join(t)
        
    def log(self, s):
        self.__print(s)
    
    
    def log_start(self):
        self.__print(TRANS.L_START)
        return
    
    def log_end(self):
        self.__print(TRANS.L_END)
        return
    
    def log_section(self):
        self.__print(TRANS.L_SECTION)
        return
        
    def log_subsection(self):
        self.__print(TRANS.L_SUBSECTION)
        return
    
    def log_pickle(self, obj):
        if not self.LogFile:
            return
        File = open(self.LogFile, "w")
        pickle.dump(obj, File)
        File.close()
        
        return
    
    def load_pickle(self):
        return pickle.load(self.LogFile)
