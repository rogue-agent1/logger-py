#!/usr/bin/env python3
"""Structured logger with levels, formatters, and handlers."""
import time, json, sys, os

class LogLevel:
    DEBUG=10;INFO=20;WARN=30;ERROR=40;FATAL=50
    _names={10:"DEBUG",20:"INFO",30:"WARN",40:"ERROR",50:"FATAL"}
    @classmethod
    def name(cls,level): return cls._names.get(level,"?")

class Logger:
    def __init__(self,name="root",level=LogLevel.DEBUG):
        self.name=name;self.level=level;self.handlers=[];self.context={}
    def add_handler(self,handler): self.handlers.append(handler)
    def with_context(self,**kwargs): self.context.update(kwargs); return self
    def _log(self,level,msg,**kwargs):
        if level<self.level: return
        record={"ts":time.time(),"level":LogLevel.name(level),"logger":self.name,
                "msg":msg,**self.context,**kwargs}
        for h in self.handlers: h(record)
    def debug(self,msg,**kw): self._log(LogLevel.DEBUG,msg,**kw)
    def info(self,msg,**kw): self._log(LogLevel.INFO,msg,**kw)
    def warn(self,msg,**kw): self._log(LogLevel.WARN,msg,**kw)
    def error(self,msg,**kw): self._log(LogLevel.ERROR,msg,**kw)

def console_handler(record):
    ts=time.strftime("%H:%M:%S",time.localtime(record["ts"]))
    extra=" ".join(f"{k}={v}" for k,v in record.items() if k not in ("ts","level","logger","msg"))
    print(f"  [{ts}] {record['level']:5s} {record['logger']}: {record['msg']} {extra}")

def json_handler(record): print(f"  {json.dumps(record,default=str)}")

if __name__ == "__main__":
    log=Logger("app",LogLevel.INFO)
    log.add_handler(console_handler)
    log.with_context(service="api",version="1.0")
    log.info("Server started",port=8080)
    log.warn("High memory",usage_pct=85)
    log.error("Request failed",status=500,path="/api/users")
    log.debug("This won't show")
