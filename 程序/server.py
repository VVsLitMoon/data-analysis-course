"""Local interactive textbook. Bind only to loopback; no cloud publication."""
from pathlib import Path
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse,unquote
import json,os,sys,subprocess,time,threading,secrets,socket,webbrowser,mimetypes,atexit,signal,xml.etree.ElementTree as ET
import urllib.request
ROOT=Path(__file__).resolve().parent.parent
RUNTIME=ROOT/'runtime'
LOGDIR=RUNTIME/'logs'
LOGDIR.mkdir(parents=True,exist_ok=True)
MYSQL=Path(os.environ.get('MYSQL_BIN',r'C:\Program Files\MySQL\MySQL Server 8.0\bin'))
PORT=8766
DBPORT=33318
DBNAME='da_beginner_lab'
TOKEN=secrets.token_urlsafe(24)
FLAGS=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0
lock=threading.RLock()
dbproc=None
db_error='尚未启动'
ready=False
fixtures=json.loads((ROOT/'data/fixtures.json').read_text(encoding='utf-8'))
fixture_tables={k.removeprefix('da_'):v for k,v in fixtures.items()}
def call(sql,user='root',xml=False,timeout=10):
 args=[str(MYSQL/'mysql.exe'),'--no-defaults','--host=127.0.0.1',f'--port={DBPORT}',f'--user={user}','--default-character-set=utf8mb4','--connect-timeout=3']
 if xml:args+=['--xml']
 else:args+=['--batch','--skip-column-names','--raw']
 env=os.environ.copy()
 if user=='student':env['MYSQL_PWD']=student_password
 p=subprocess.run(args,input=sql,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=timeout,creationflags=FLAGS,env=env)
 if p.returncode:raise RuntimeError(p.stderr.strip() or 'SQL没有成功执行')
 return p.stdout
def lit(x):
 if x is None:return 'NULL'
 if isinstance(x,(int,float)):return str(x)
 return "'"+str(x).replace("'","''")+"'"
def seed():
 statements=[f'USE {DBNAME};']
 for name,v in fixture_tables.items():
  statements.extend([f'DROP TABLE IF EXISTS `{name}`;',f'CREATE TABLE `{name}` ({v["ddl"]});',f'INSERT INTO `{name}` VALUES '+','.join('('+','.join(map(lit,r))+')' for r in v['rows'])+';'])
 statements+=['DROP TABLE IF EXISTS scratch;', 'CREATE TABLE scratch (id INT PRIMARY KEY, amount DECIMAL(12,2));','INSERT INTO scratch VALUES (1,10),(2,20);']
 call('\n'.join(statements))
def stop_db():
 global dbproc
 if dbproc is not None and dbproc.poll() is None:
  try:call('SHUTDOWN;',timeout=5)
  except Exception:pass
  try:dbproc.wait(timeout=10)
  except subprocess.TimeoutExpired:dbproc.terminate();dbproc.wait(timeout=5)
 dbproc=None
def start_db():
 global dbproc,ready,db_error,student_password
 try:
  if not (MYSQL/'mysqld.exe').exists():raise RuntimeError(f'未找到 MySQL 8.0 的 mysqld 可执行文件（当前路径 {MYSQL}）。可先阅读讲义与预期结果；如需执行 SQL，请安装 MySQL 8.0 并用环境变量 MYSQL_BIN 指向其 bin 目录。')
  with socket.socket() as s:
   if s.connect_ex(('127.0.0.1',DBPORT))==0:raise RuntimeError('讲义数据库端口已占用。请关闭此前启动的讲义后重试；不会连接其他数据库。')
  data=RUNTIME/'mysql';marker=data/'textbook-owned.json'
  if data.exists() and not marker.exists():raise RuntimeError('运行数据目录没有本讲义标记，拒绝覆盖。')
  if not data.exists():
   data.mkdir(parents=True)
   marker.write_text(json.dumps({'owner':'da-beginner-textbook','version':1}),encoding='utf-8')
  # Marker stays in the parent; initialize the separate empty engine child.
  actual=data/'engine'
  actual.mkdir(exist_ok=True)
  if not (actual/'mysql.ibd').exists():
   init=subprocess.run([str(MYSQL/'mysqld.exe'),'--no-defaults','--initialize-insecure','--datadir=.','--console'],cwd=actual,capture_output=True,text=True,encoding='utf-8',errors='replace',creationflags=FLAGS,timeout=60)
   (LOGDIR/'mysql-init.log').write_text(init.stdout+init.stderr,encoding='utf-8')
   if init.returncode:raise RuntimeError('讲义数据库初始化未成功，详情见 runtime/logs/mysql-init.log。')
  log=(LOGDIR/'mysql.log').open('a',encoding='utf-8')
  dbproc=subprocess.Popen([str(MYSQL/'mysqld.exe'),'--no-defaults','--datadir=.','--port=33318','--bind-address=127.0.0.1','--mysqlx=OFF','--skip-log-bin','--console'],cwd=actual,stdout=log,stderr=log,creationflags=FLAGS)
  for _ in range(50):
   if dbproc.poll() is not None:raise RuntimeError('讲义数据库启动失败，详情见 runtime/logs/mysql.log。')
   try:call('SELECT 1;',timeout=3);break
   except Exception:time.sleep(.25)
  else:raise RuntimeError('讲义数据库启动超时')
  student_password=secrets.token_hex(20)
  call(f"CREATE DATABASE IF NOT EXISTS {DBNAME} CHARACTER SET utf8mb4; CREATE USER IF NOT EXISTS 'student'@'127.0.0.1' IDENTIFIED BY '{student_password}'; ALTER USER 'student'@'127.0.0.1' IDENTIFIED BY '{student_password}'; GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP,ALTER,INDEX,CREATE TEMPORARY TABLES ON {DBNAME}.* TO 'student'@'127.0.0.1';")
  with lock:seed()
  ready=True;db_error=''
 except Exception as e:
  db_error=str(e);stop_db()
def parse_xml(raw):
 import re
 documents=re.findall(r'<resultset\b[^>]*(?:/>|>[\s\S]*?</resultset>)',raw)
 result=[]
 for text in documents:
  doc=ET.fromstring(text);rows=[];cols=[]
  for row in doc.findall('row'):
   if not cols:cols=[x.attrib['name'] for x in row.findall('field')]
   rows.append([None if x.attrib.get('{http://www.w3.org/2001/XMLSchema-instance}nil')=='true' else (x.text or '') for x in row.findall('field')])
  result.append({'columns':cols,'rows':rows[:300],'total':len(rows)})
 return result
def execute_sql(code):
 if not ready:raise RuntimeError(db_error or 'MySQL仍在准备中，请稍后再点运行。')
 # Each run recreates only this lecture's tables. Student account cannot access other databases.
 with lock:
  seed()
  raw=call(f'USE {DBNAME}; SET SESSION MAX_EXECUTION_TIME=4000; SET SESSION innodb_lock_wait_timeout=2;\n'+code,user='student',xml=True,timeout=8)
  return {'kind':'sql','results':parse_xml(raw),'text':'执行成功。每次运行均使用一份新数据；本轮多条语句可连续操作。'}
def execute_python(code):
 payload=json.dumps({'code':code,'fixtures':fixture_tables},ensure_ascii=False)
 p=subprocess.run([sys.executable,str(ROOT/'程序/python_runner.py')],input=payload,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=12,cwd=RUNTIME,creationflags=FLAGS)
 if p.returncode:raise RuntimeError(p.stderr.strip()[-6000:] or 'Python执行失败')
 return {'kind':'python','text':p.stdout[:20000] or '执行完成。用 print(...) 显示结果。'}
def execute(engine,code):return execute_sql(code) if engine=='sql' else execute_python(code)
class Handler(BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def headers_out(self,status,kind='application/json; charset=utf-8'):
  self.send_response(status);self.send_header('Content-Type',kind);self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.end_headers()
 def send_json(self,data,status=200):self.headers_out(status);self.wfile.write(json.dumps(data,ensure_ascii=False).encode())
 def do_GET(self):
  path=urlparse(self.path).path
  if path=='/api/status':return self.send_json({'app':'da-beginner-textbook','ready':ready,'error':db_error,'token':TOKEN,'python':sys.version.split()[0],'mysql':'8.0','port':PORT})
  if path=='/api/tables':return self.send_json(fixture_tables)
  # Static serving only explicitly public lecture files, never runtime or source server credentials.
  name=unquote(path).lstrip('/') or 'index.html'
  if name not in ['index.html','app.js','style.css','lessons.js','favicon.svg']:
   return self.send_json({'error':'不存在的资源'},404)
  p=ROOT/name
  if not p.exists():return self.send_json({'error':'讲义尚未生成'},404)
  mime=mimetypes.guess_type(p.name)[0] or 'text/plain'
  self.headers_out(200,mime+'; charset=utf-8');self.wfile.write(p.read_bytes())
 def do_POST(self):
  origin=self.headers.get('Origin','')
  if self.headers.get('X-Lecture-Key')!=TOKEN or (origin and origin not in [f'http://127.0.0.1:{PORT}',f'http://localhost:{PORT}']):return self.send_json({'error':'请从本机讲义页面运行。'},403)
  size=int(self.headers.get('Content-Length','0'))
  if size>50000:return self.send_json({'error':'代码过长'},413)
  try:data=json.loads(self.rfile.read(size) or '{}')
  except Exception:return self.send_json({'error':'请求格式错误'},400)
  if self.path=='/api/shutdown':
   self.send_json({'ok':True});threading.Thread(target=self.server.shutdown,daemon=True).start();return
  if self.path!='/api/run':return self.send_json({'error':'不存在的接口'},404)
  engine=data.get('engine');code=data.get('code','')
  if engine not in ['sql','python'] or not isinstance(code,str):return self.send_json({'error':'请选择SQL或Python代码'},400)
  try:return self.send_json(execute(engine,code))
  except subprocess.TimeoutExpired:return self.send_json({'error':'运行超时。先缩小数据量，检查循环或笛卡尔积。'},400)
  except Exception as e:return self.send_json({'error':str(e)},400)
def open_lecture_page():
 url=f'http://127.0.0.1:{PORT}'
 if '--no-browser' in sys.argv:return
 try:opened=webbrowser.open(url,new=2)
 except Exception as e:
  print(f'默认浏览器未能打开：{e}',flush=True);opened=False
 if opened:print('已请求默认浏览器打开讲义。若没有弹出窗口，请复制下面的网址到浏览器。',flush=True)
 else:print('请在浏览器地址栏手动输入下面的网址。',flush=True)
 print(url,flush=True)
class LectureHTTPServer(ThreadingHTTPServer):
 # On Windows SO_REUSEADDR can allow duplicate listeners; keep this port exclusive.
 allow_reuse_address=False
 def server_bind(self):
  if os.name=='nt':self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_EXCLUSIVEADDRUSE,1)
  super().server_bind()
def existing_lecture():
 try:
  with urllib.request.urlopen(f'http://127.0.0.1:{PORT}/api/status',timeout=3) as response:return json.load(response)
 except Exception:return {}
def reopen_existing():
 if existing_lecture().get('app')!='da-beginner-textbook':return False
 print('讲义已经在运行，正在为你重新打开。无需重复启动数据库。',flush=True)
 open_lecture_page();return True
def main():
 RUNTIME.mkdir(exist_ok=True)
 if reopen_existing():return
 try:server=LectureHTTPServer(('127.0.0.1',PORT),Handler)
 except OSError as bind_error:
  # Reopen only a verified instance of this textbook, never take over another service.
  if reopen_existing():return
  raise RuntimeError('讲义无法监听8766端口，且该端口不是可识别的讲义服务。请查看启动诊断日志；程序没有关闭其他服务。') from bind_error
 atexit.register(stop_db)
 threading.Thread(target=start_db,daemon=True).start()
 print(f'讲义已启动：http://127.0.0.1:{PORT}  （Ctrl+C关闭）',flush=True)
 open_lecture_page()
 try:server.serve_forever()
 except KeyboardInterrupt:pass
 finally:server.server_close();stop_db()
if __name__=='__main__':main()
