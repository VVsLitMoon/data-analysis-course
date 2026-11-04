"""Execute small textbook examples in a separate process; not a general secure Python sandbox."""
import sys,json,ast,io,contextlib,traceback,builtins
sys.stdin.reconfigure(encoding='utf-8');sys.stdout.reconfigure(encoding='utf-8');sys.stderr.reconfigure(encoding='utf-8')
def run(payload):
 code=payload['code'];tree=ast.parse(code)
 allowed={'math','statistics','random','numpy','pandas','scipy','sklearn','collections','datetime','itertools'}
 forbidden={'open','eval','exec','compile','input','__import__','breakpoint','globals','locals','getattr','setattr','delattr','vars'}
 for node in ast.walk(tree):
  if isinstance(node,(ast.Import,ast.ImportFrom)):
   names=[node.module or ''] if isinstance(node,ast.ImportFrom) else [x.name for x in node.names]
   if any(n.split('.')[0] not in allowed for n in names):raise ValueError('本讲义只支持数学、统计与数据分析模块。文件和网络任务请在VS Code中另行运行。')
  if isinstance(node,ast.Name) and (node.id in forbidden or node.id.startswith('__')):raise ValueError('本讲义不执行文件、反射或嵌套执行操作。')
  if isinstance(node,ast.Attribute) and (node.attr.startswith('_') or node.attr.startswith(('read_','to_csv','to_excel','to_pickle','to_parquet','to_sql','to_feather')) or node.attr in {'save','savefig','load','dump','system','popen','query','eval'}):raise ValueError('本讲义代码区仅用于内存中的计算；文件读写请在VS Code中练习。')
 import pandas as pd
 columns={'users':['user_id','signup_date','channel','city'],'orders':['order_id','user_id','order_at','amount','status','category'],'logins':['login_id','user_id','login_at'],'events':['event_id','user_id','event_at','event_type'],'assignments':['user_id','arm'],'calendar':['dt']}
 ns={k:pd.DataFrame(v['rows'],columns=columns[k]) for k,v in payload['fixtures'].items()}
 ns['pd']=pd
 # Imports are AST-restricted above. Trusted local textbook execution, not hosted/multi-user execution.
 ns['__builtins__']=builtins.__dict__
 exec(compile(tree,'<讲义代码>','exec'),ns)
if __name__=='__main__':
 try:run(json.load(sys.stdin))
 except Exception:
  traceback.print_exc(limit=3);sys.exit(1)
