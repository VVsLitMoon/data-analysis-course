"""Run every default example through the same local API used by the browser."""
from pathlib import Path
import json,time,urllib.request,urllib.error,urllib.parse,datetime,decimal,re,ast,sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parent.parent
BASE='http://127.0.0.1:8766'
def get(path):
 with urllib.request.urlopen(BASE+urllib.parse.quote(path),timeout=20) as r:return json.load(r)
status=get('/api/status')
if not status['ready']:raise RuntimeError(status['error'])
def run(engine,code,token=status['token']):
 req=urllib.request.Request(BASE+'/api/run',json.dumps({'engine':engine,'code':code}).encode(),{'Content-Type':'application/json','X-Lecture-Key':token},method='POST')
 with urllib.request.urlopen(req,timeout=30) as r:return json.load(r)
book=json.loads((ROOT/'程序/curriculum.json').read_text(encoding='utf-8'))
checks_only='--checks-only' in sys.argv
sql_only='--sql-only' in sys.argv
changed='--changed' in sys.argv
changed_python={'python-07','python-08','python-10'}
reuse=checks_only or sql_only or changed
results=json.loads((ROOT/'runtime/自动验证报告.json').read_text(encoding='utf-8'))['examples'] if reuse else []
if sql_only:results=[r for r in results if r['engine']!='sql']
if changed:results=[r for r in results if r['engine']!='sql' and r['id'] not in changed_python]
outputs=json.loads((ROOT/'data/default_outputs.json').read_text(encoding='utf-8')) if reuse else {}
for item in ([] if checks_only else book['lessons']):
 if not item['code']:continue
 if sql_only and item['engine']!='sql':continue
 if changed and item['engine']!='sql' and item['id'] not in changed_python:continue
 t=time.monotonic()
 try:
  outputs[item['id']]=run(item['engine'],item['code'])
  results.append({'id':item['id'],'engine':item['engine'],'ok':True,'seconds':round(time.monotonic()-t,2)})
 except Exception as e:
  msg=e.read().decode() if isinstance(e,urllib.error.HTTPError) else str(e)
  results.append({'id':item['id'],'engine':item['engine'],'ok':False,'error':msg})
 print(item['id'],results[-1]['ok'],flush=True)
checks=[]
def check(name,fn):
 try:fn();checks.append({'name':name,'ok':True})
 except Exception as e:checks.append({'name':name,'ok':False,'error':str(e)})
def require(v,msg='assertion failed'):
 if not v:raise AssertionError(msg)
def rows(i,k=0):return outputs[i]['results'][k]['rows']
fixture=json.loads((ROOT/'data/fixtures.json').read_text(encoding='utf-8'))
paid=[x for x in fixture['da_orders']['rows'] if x[4]=='paid']
check('聚合金额、订单数、购买人数与独立Python手算一致',lambda:require(int(rows('sql-06')[0][0])==len(paid) and int(rows('sql-06')[0][1])==len({x[1] for x in paid}) and decimal.Decimal(rows('sql-06')[0][2])==sum(decimal.Decimal(str(x[3])) for x in paid)))
check('LEFT JOIN保留7位用户，零订单用户数为0',lambda:require(len(rows('sql-10'))==7 and all(int(r[1])==0 for r in rows('sql-10') if r[0] in ['5','6'])))
def streak_check():
 expected=[]
 for user in fixture['da_users']['rows']:
  dates=sorted({datetime.date.fromisoformat(x[2][:10]) for x in fixture['da_logins']['rows'] if x[1]==user[0]})
  groups=[]
  for dt in dates:
   if not groups or (dt-groups[-1][-1]).days!=1:groups.append([dt])
   else:groups[-1].append(dt)
  expected.extend([str(user[0]),str(g[0]),str(g[-1]),str(len(g))] for g in groups if len(g)>=3)
 require(rows('sql-20')==expected,repr((rows('sql-20'),expected)))
check('连续登录与按用户日期逐天扫描算法一致',streak_check)
def rolling_check():
 for row in rows('sql-24'):
  dt=datetime.date.fromisoformat(row[0]);lo=dt-datetime.timedelta(days=6)
  total=sum(decimal.Decimal(str(x[3])) for x in paid if lo<=datetime.date.fromisoformat(x[2][:10])<=dt)
  require(decimal.Decimal(row[2])==total,repr(row))
check('七日滚动与独立日期区间求和一致',rolling_check)
check('事务修改后回滚恢复',lambda:require(rows('sql-26',0)==rows('sql-26',2) and rows('sql-26',0)!=rows('sql-26',1)))
check('贝叶斯后验为2/13',lambda:require(abs(float(outputs['stats-05']['text'].split('：')[-1])-2/13)<1e-10))
def rejection():
 try:run('sql','SELECT 1;','wrong-token')
 except urllib.error.HTTPError as e:require(e.code==403);return
 raise AssertionError('missing token accepted')
check('缺少正确本地请求令牌时拒绝执行',rejection)
def error_recovery():
 try:run('sql','SELECT missing_column FROM users;')
 except urllib.error.HTTPError as e:require(e.code==400)
 else:raise AssertionError('invalid SQL unexpectedly succeeded')
 require(run('sql','SELECT COUNT(*) AS n FROM users;')['results'][0]['rows']==[['7']])
check('SQL错误有反馈且下一次运行恢复正常',error_recovery)
def reset_check():
 run('sql','UPDATE scratch SET amount=777 WHERE id=1; SELECT * FROM scratch;')
 require(run('sql','SELECT amount FROM scratch WHERE id=1;')['results'][0]['rows']==[['10.00']])
check('每次运行恢复教学数据',reset_check)
def deny_static():
 try:get('/程序/server.py')
 except urllib.error.HTTPError as e:require(e.code==404);return
 raise AssertionError('private static path exposed')
check('静态服务不提供程序源码和运行数据',deny_static)
def files_check():
 for f in (ROOT/'程序').glob('*.py'):ast.parse(f.read_text(encoding='utf-8'))
 for f in (ROOT/'代码示例').glob('*.py'):ast.parse(f.read_text(encoding='utf-8'))
 for f in (ROOT/'代码示例').glob('*.ipynb'):
  nb=json.loads(f.read_text(encoding='utf-8'))
  require(nb['nbformat']==4)
  for cell in nb['cells']:
   if cell['cell_type']=='code':ast.parse(''.join(cell['source']))
 ids=[x['id'] for x in book['lessons']];require(len(ids)==len(set(ids)))
 require(all(x['quiz']['options'] and 0<=x['quiz']['answer']<len(x['quiz']['options']) for x in book['lessons']))
check('全部Python导出和Notebook语法、课号和题目配置完整',files_check)
report={'date':datetime.datetime.now().isoformat(timespec='seconds'),'lessons':len(book['lessons']),'examples':results,'checks':checks,'note':'默认代码逐条通过真实HTTP运行；附加检查覆盖关键口径与恢复路径。执行成功不等于对任意用户改写代码提供判题。'}
(ROOT/'data/default_outputs.json').write_text(json.dumps(outputs,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'runtime/自动验证报告.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
summary={'examples_passed':sum(x['ok'] for x in results),'examples_total':len(results),'checks_passed':sum(x['ok'] for x in checks),'checks_total':len(checks),'failed':[x for x in results+checks if not x['ok']]}
print(json.dumps(summary,ensure_ascii=False,indent=2))
sys.exit(0 if all(x['ok'] for x in results+checks) else 1)
