"""ASCII-named launcher: avoid non-ASCII commands inside Windows batch files."""
from pathlib import Path
from datetime import datetime
import runpy,sys,traceback

ROOT=Path(__file__).resolve().parent
class Tee:
    def __init__(self,console,log):self.console,self.log=console,log
    def write(self,message):
        self.console.write(message);self.log.write(message);return len(message)
    def flush(self):self.console.flush();self.log.flush()
    def isatty(self):return self.console.isatty()
    @property
    def encoding(self):return 'utf-8'

def main():
    for stream in (sys.stdout,sys.stderr):
        if hasattr(stream,'reconfigure'):stream.reconfigure(encoding='utf-8',errors='replace')
    logdir=ROOT/'runtime'/'logs';logdir.mkdir(parents=True,exist_ok=True)
    logfile=logdir/'启动诊断.log'
    original_out,original_err=sys.stdout,sys.stderr
    with logfile.open('a',encoding='utf-8',buffering=1) as log:
        sys.stdout,sys.stderr=Tee(original_out,log),Tee(original_err,log)
        try:
            print('\n'+ '='*48)
            print(datetime.now().isoformat(timespec='seconds')+' · 数分起点启动')
            print('讲义网址：http://127.0.0.1:8766')
            print('诊断日志：'+str(logfile))
            print('正在检查运行环境，请保留此窗口。\n',flush=True)
            runpy.run_path(str(ROOT/'程序/server.py'),run_name='__main__')
            print('\n本次启动检查完成。若已打开讲义，可以关闭这个提示窗口。',flush=True)
            return 0
        except KeyboardInterrupt:
            print('\n已停止本次启动。',flush=True);return 0
        except Exception:
            print('\n启动没有成功，错误详情如下（已保存到启动诊断日志）：',file=sys.stderr)
            traceback.print_exc();return 1
        finally:
            sys.stdout,sys.stderr=original_out,original_err

if __name__=='__main__':sys.exit(main())
