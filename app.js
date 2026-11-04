/* Local textbook UI. No external scripts, analytics or network uploads. */
'use strict';
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const KEY='da-beginner-book-v1';
let state={done:{},notes:{},codes:{},quiz:{},last:'start-01'},current=null,token='',runtime=null,busy=false,runId=0;
try { const old=JSON.parse(localStorage.getItem(KEY)||'null'); if(old&&typeof old==='object') state={...state,...old}; } catch(e){}
function save(){try{localStorage.setItem(KEY,JSON.stringify(state));}catch(e){toast('浏览器存储不可用，请导出学习记录。');}}
function toast(s){$('#toast').textContent=s;$('#toast').hidden=false;clearTimeout(toast.timer);toast.timer=setTimeout(()=>$('#toast').hidden=true,3500);}
function md(text){return text.split('\n').filter(x=>x.trim()).map(line=>line.startsWith('## ')?'<h2>'+esc(line.slice(3))+'</h2>':'<p>'+inline(line)+'</p>').join('');}
function inline(s){return esc(s).replace(/`([^`]+)`/g,'<code>$1</code>').replace(/\n/g,'<br>');}
function outline(){
 const search=$('#search').value.trim().toLowerCase(),core=$('#core-only').checked;
 $('#outline').innerHTML=BOOK.modules.map(m=>{
  const list=BOOK.lessons.filter(x=>x.module===m.id&&(!core||!x.advanced)&&(!search||(x.title+' '+x.body+' '+x.id).toLowerCase().includes(search)));
  if(!list.length)return '';
  return `<details ${search||current?.module===m.id?'open':''}><summary>${esc(m.title)} <small>(${list.length})</small></summary>${list.map(x=>`<a href="#${x.id}" ${current?.id===x.id?'class="active" aria-current="page"':''}><span class="tick">${state.done[x.id]?'✓':'○'}</span><span>${x.id.split('-')[1]} · ${esc(x.title)}</span></a>`).join('')}</details>`;
 }).join('')||'<p>没有找到相关章节，试试别的关键词。</p>';
 const n=BOOK.lessons.filter(x=>state.done[x.id]).length;
 $('#total-progress').textContent=`${n} / ${BOOK.lessons.length} 节`;
 $('#progress').max=BOOK.lessons.length;$('#progress').value=n;
}
function navigate(id,scroll=true){
 current=BOOK.lessons.find(x=>x.id===id)||BOOK.lessons[0];
 runId++; // Results from an earlier lesson must never appear in the new lesson.
 busy=false;$('#run').disabled=false;
 state.last=current.id;save();
 document.title=current.title+' · 数分起点';
 $('#module-name').textContent=BOOK.modules.find(m=>m.id===current.module).title+' / '+current.id;
 $('#level').textContent=current.advanced?'面试进阶 · 可第二轮学':'基础与核心';
 $('#lesson-title').textContent=current.title;
 $('#lesson-body').innerHTML=md(current.body);
 $('#engine').textContent=current.code?(current.engine==='sql'?'MySQL 8.0':'Python · Pandas'):'概念练习';
 $('#code-area').hidden=!current.code;$('#no-code').hidden=!!current.code;
 $('#editor').value=state.codes[current.id]??current.code;
 $('#editor').style.minHeight=Math.min(360,Math.max(200,(current.code.split('\n').length+2)*22))+'px';
 $('#output').innerHTML='<p>先运行默认代码，再修改一处。结果会显示在这里。</p>';
 $('#run').textContent='▶ 运行代码';
 $('#run-note').textContent=current.engine==='sql'?'每次运行都会恢复初始练习数据；同一次运行中的多条语句依次执行。':'已准备好练习用的数据表；用 print(...) 显示结果。';
 $('#expected').open=false;$('#expected').hidden=!current.expected;
 $('#expected-body').innerHTML=current.expected?'<p class="success-label">这是保存的验证结果，不是本次运行结果。</p>'+resultHTML(current.expected):'';
 const p=$('#practice');p.hidden=!current.task;
 p.innerHTML=current.task?`<h3>动手改一处</h3><p>${esc(current.task)}</p><details><summary>需要一点提示</summary><p>${esc(current.hint)}</p></details>${current.solution?`<details><summary>看参考改法</summary><pre>${esc(current.solution)}</pre></details>`:''}`:'';
 $('#note').value=state.notes[current.id]||'';$('#understood').checked=!!state.done[current.id];
 const ix=BOOK.lessons.indexOf(current);$('#previous').disabled=ix===0;$('#next').disabled=ix===BOOK.lessons.length-1;
 renderQuiz();renderLab();outline();
 if(scroll)window.scrollTo({top:0,behavior:'instant'});
}
function renderQuiz(){
 const q=current.quiz,saved=state.quiz[current.id];
 $('#quiz').innerHTML=`<span class="eyebrow">用一道小题确认理解</span><h2>${esc(q.q)}</h2>${q.options.map((s,i)=>`<button data-choice="${i}">${String.fromCharCode(65+i)}. ${esc(s)}</button>`).join('')}<p class="quiz-feedback" aria-live="polite"></p><button id="retry-quiz" class="quiet">清除作答，再想一次</button>`;
 $$('#quiz button[data-choice]').forEach(b=>b.onclick=()=>answerQuiz(Number(b.dataset.choice)));
 $('#retry-quiz').onclick=()=>{delete state.quiz[current.id];save();renderQuiz();};
 if(Number.isInteger(saved))showAnswer(saved);
}
function answerQuiz(i){state.quiz[current.id]=i;save();showAnswer(i);}
function showAnswer(i){
 const q=current.quiz;$$('#quiz button[data-choice]').forEach((b,j)=>{b.classList.toggle('correct',j===q.answer);b.classList.toggle('incorrect',j===i&&i!==q.answer);});
 $('#quiz .quiz-feedback').textContent=(i===q.answer?'理解对了。':'再想一步：')+q.explain;
}
function tableHTML(columns,rows){return `<div class="table-wrap"><table class="result-table"><thead><tr>${columns.map(c=>`<th>${esc(c)}</th>`).join('')}</tr></thead><tbody>${rows.map(r=>`<tr>${r.map(v=>v===null?'<td class="null">NULL</td>':`<td>${esc(v)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;}
function resultHTML(r){
 if(r.kind==='sql')return (r.results||[]).map((x,i)=>`<span class="success-label">结果 ${i+1} · ${x.total} 行${x.total>300?'（仅显示前 300 行）':''}</span>${x.rows.length?tableHTML(x.columns,x.rows):'<p>没有符合条件的行。</p>'}`).join('')+`<p>${esc(r.text||'执行完成。')}</p>`;
 return `<pre>${esc(r.text||'运行完成。')}</pre>`;
}
async function runCode(){
 if(busy)return;
 if(!token){$('#output').innerHTML='<div class="error">现在是阅读模式。请双击“启动讲义.cmd”，在自动打开的本地页面运行代码。预期输出仍可展开查看。</div>';return;}
 const active=current,id=++runId;
 busy=true;$('#run').disabled=true;$('#run').textContent='运行中…';$('#output').innerHTML='<p>正在执行你编辑的代码…</p>';
 try{
  const response=await fetch('/api/run',{method:'POST',headers:{'Content-Type':'application/json','X-Lecture-Key':token},body:JSON.stringify({engine:active.engine,code:$('#editor').value})});
  const result=await response.json();
  if(id!==runId)return;
  if(!response.ok)throw new Error(result.error||'执行失败');
  $('#output').innerHTML='<span class="success-label">✓ 本次代码已实际执行</span>'+resultHTML(result);
 }catch(e){if(id===runId)$('#output').innerHTML=`<div class="error"><strong>先读最后一行错误，再检查对应代码</strong><pre>${esc(e.message)}</pre><p>先核对列名、逗号和括号。可点“恢复示例”确认环境是否正常。</p></div>`;}
 finally{if(id===runId){busy=false;$('#run').disabled=false;$('#run').textContent='▶ 运行代码';}}
}
async function checkRuntime(attempt=0){
 if(location.protocol==='file:'){$('#connection').textContent='阅读模式 · 启动后可运行代码';return;}
 try{const r=await fetch('/api/status');const d=await r.json();if(d.app!=='da-beginner-textbook')throw Error('wrong server');runtime=d;token=d.token;
  $('#connection').textContent=d.ready?`MySQL 8.0 + Python ${d.python} 已连接`:(d.error==='尚未启动'?'正在准备 MySQL · Python 已可运行':`MySQL：${d.error||'准备中'} · Python 可运行`);
  $('#connection').classList.toggle('ready',d.ready);
  if(!d.ready&&attempt<45)setTimeout(()=>checkRuntime(attempt+1),1200);
 }catch(e){token='';$('#connection').classList.remove('ready');$('#connection').textContent='阅读模式 · 本地运行环境未连接';}
}
function slider(id,label,value,min,max,step,unit){return `<div class="slider-row"><label for="${id}">${label}<span id="${id}-value"></span></label><input type="range" id="${id}" value="${value}" min="${min}" max="${max}" step="${step}" data-unit="${unit}"></div>`;}
function renderLab(){
 const el=$('#visual-lab'),type=current.lab;el.hidden=!type;if(!type)return;
 const configs={
  bayes:{title:'动一下，看看基准率怎样改变结论',sliders:[['base','异常订单占比',1,.1,30,.1,'%'],['sensitivity','能检出多少异常',90,10,100,1,'%'],['falsep','正常订单误报率',5,.1,30,.1,'%']],footer:'深绿代表真告警，浅棕代表误报。保持检测能力不变，基准率越低，告警中误报占比越可能高。'},
  sample:{title:'样本量规划器 · 入门近似',sliders:[['base','基准转化率',10,1,80,1,'%'],['delta','希望检测的绝对差',1,.1,5,.1,' 个百分点']],footer:'固定双侧 α=0.05、功效 80%、两组等量、独立二元观测、近似相同方差。输出为每组样本；集群、长尾和比率指标不能直接套用。'},
  effect:{title:'观察效应大小与不确定性',sliders:[['pa','对照转化率',10,1,50,.5,'%'],['pb','实验转化率',12,1,50,.5,'%'],['n','每组独立用户',10000,500,30000,500,' 人']],footer:'图中竖线是差值 0，深绿线段是大样本近似 95% 区间，圆点是点估计。这里只演示区间，正式结论还要检查实验设计和护栏。'},
  gmv:{title:'把 GMV 拆成三个可解释的量',sliders:[['buyers','购买用户',1000,100,3000,100,' 人'],['frequency','人均订单数',2,1,8,.1,' 单'],['aov','客单价',80,10,200,5,' 元']],footer:'恒等式：GMV = 购买用户 × 人均订单数 × 客单价。保持其他因素不变是一种情景假设，不是已证实的因果关系。'}
 };
 const c=configs[type];el.innerHTML=`<h2>${c.title}</h2>${c.sliders.map(a=>slider(...a)).join('')}<div class="metric-output" id="lab-answer"></div><div id="lab-chart"></div><p>${c.footer}</p><p>参数演示与代码区相互独立。拖动不会自动改代码；想核对结果，可以手动把代码中的参数改成同一个值。</p>`;
 function update(){let v={};c.sliders.forEach(a=>{const s=$('#'+a[0]);v[a[0]]=Number(s.value);$('#'+a[0]+'-value').textContent=s.value+a[6];});let answer='',chart='';
  if(type==='bayes'){const t=v.base/100*v.sensitivity/100,f=(1-v.base/100)*v.falsep/100,posterior=t/(t+f);answer=`${(posterior*100).toFixed(1)}%<small>告警中真正异常的比例；每万单约 ${Math.round(t*10000)} 个真告警、${Math.round(f*10000)} 个误报</small>`;chart=`<div class="stackbar" aria-label="真告警占比 ${(posterior*100).toFixed(1)}%"><div style="width:${posterior*100}%"></div></div>`;}
  if(type==='sample'){const p=v.base/100,d=v.delta/100,n=Math.ceil(2*p*(1-p)*(1.959963984540054+0.8416212335729143)**2/d**2);answer=`${n.toLocaleString()} 人 / 组<small>两组合计约 ${(2*n).toLocaleString()} 人</small>`;}
  if(type==='gmv'){answer=`¥ ${(v.buyers*v.frequency*v.aov).toLocaleString(undefined,{maximumFractionDigits:0})}<small>${v.buyers} 人 × ${v.frequency} 单/人 × ${v.aov} 元/单</small>`;}
  if(type==='effect'){const a=v.pa/100,b=v.pb/100,d=b-a,se=Math.sqrt((a*(1-a)+b*(1-b))/v.n),lo=d-1.96*se,hi=d+1.96*se,bound=Math.max(Math.abs(lo),Math.abs(hi),.01)*1.15,pos=x=>50+50*x/bound;answer=`${(d*100).toFixed(2)} 个百分点<small>近似 95% 区间：[${(lo*100).toFixed(2)}, ${(hi*100).toFixed(2)}] 个百分点</small>`;chart=`<div class="interval"><i class="zero"></i><i class="ci" style="left:${pos(lo)}%;width:${pos(hi)-pos(lo)}%"></i><i class="point" style="left:${pos(d)}%"></i></div><p>区间${lo<=0&&hi>=0?'包含':'未包含'}零；未包含零也不自动意味着值得上线。</p>`;}
  $('#lab-answer').innerHTML=answer;$('#lab-chart').innerHTML=chart;
 }
 $$('#visual-lab input').forEach(s=>s.oninput=update);update();
}
const tableInfo={
 da_users:['用户表','每行是一位用户，记录用户编号、注册日期、来源渠道和城市。'],
 da_orders:['订单表','每行是一笔订单，记录订单编号、下单用户、时间、金额、状态和商品品类。同一用户可以有多笔订单。'],
 da_logins:['登录记录表','每行是一次登录。同一用户在同一天登录多次，会留下多行记录。'],
 da_events:['用户行为表','每行是一次行为：view 表示浏览商品，cart 表示加购，pay 表示支付。'],
 da_assignments:['实验分组表','每行记录一位用户被分到哪个实验组。arm 是组别，用于比较不同方案的效果。'],
 da_calendar:['日期表','每行是一个自然日。用它补齐没有订单的日期，后面才能按连续日期计算。']
};
function showTable(name){
 const item=BOOK.tables[name],key=name.replace('da_','');
 const columns=item.ddl.split(/,(?![^()]*\))/).map(x=>x.trim().split(/\s+/)[0]);
 $('#table-content').innerHTML=`<h3>${esc(key)}（${esc(tableInfo[name][0])}）· ${item.rows.length} 行</h3><p>${esc(tableInfo[name][1])}</p>${tableHTML(columns,item.rows)}<details><summary>查看字段类型和建表约束（进阶）</summary><pre>${esc(item.ddl)}</pre></details>`;
 $$('#table-tabs button').forEach(b=>b.classList.toggle('selected',b.dataset.table===name));
}
$('#table-button').onclick=()=>{$('#table-tabs').innerHTML=Object.keys(BOOK.tables).map(n=>`<button data-table="${n}">${n.replace('da_','')}（${esc(tableInfo[n][0])}）</button>`).join('');$$('#table-tabs button').forEach(b=>b.onclick=()=>showTable(b.dataset.table));showTable('da_users');$('#tables').showModal();};
$('#help-button').onclick=()=>$('#help').showModal();$$('dialog .close').forEach(b=>b.onclick=()=>b.closest('dialog').close());
$('#search').oninput=outline;$('#core-only').onchange=outline;
$('#note').oninput=()=>{state.notes[current.id]=$('#note').value;save();};
$('#editor').oninput=()=>{state.codes[current.id]=$('#editor').value;save();};
$('#understood').onchange=()=>{state.done[current.id]=$('#understood').checked;save();outline();};
$('#previous').onclick=()=>location.hash=BOOK.lessons[BOOK.lessons.indexOf(current)-1].id;
$('#next').onclick=()=>location.hash=BOOK.lessons[BOOK.lessons.indexOf(current)+1].id;
$('#reset-code').onclick=()=>{$('#editor').value=current.code;delete state.codes[current.id];save();toast('已恢复本节示例代码。');};
$('#run').onclick=runCode;
$('#editor').onkeydown=e=>{if((e.ctrlKey||e.metaKey)&&e.key==='Enter'){e.preventDefault();runCode();}if(e.key==='Tab'){e.preventDefault();const t=e.target,start=t.selectionStart,end=t.selectionEnd;t.value=t.value.slice(0,start)+'    '+t.value.slice(end);t.selectionStart=t.selectionEnd=start+4;t.dispatchEvent(new Event('input'));}};
$('#export-progress').onclick=()=>{const blob=new Blob([JSON.stringify({book:KEY,exportedAt:new Date().toISOString(),...state},null,2)],{type:'application/json'});const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='数分起点_学习记录_'+new Date().toISOString().slice(0,10)+'.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);toast('记录已下载，可移入 08_学习记录。');};
$('#import-progress').onclick=()=>$('#import-file').click();
$('#import-file').onchange=async e=>{const f=e.target.files[0];if(!f)return;try{if(f.size>2e6)throw Error('文件过大');const d=JSON.parse(await f.text());if(d.book!==KEY)throw Error('这不是本讲义的学习记录');for(const group of ['done','notes','codes','quiz']){if(!d[group]||typeof d[group]!=='object')continue;for(const x of BOOK.lessons){const v=d[group][x.id];if(group==='done'&&typeof v==='boolean')state[group][x.id]=v;if(['notes','codes'].includes(group)&&typeof v==='string'&&v.length<=50000)state[group][x.id]=v;if(group==='quiz'&&Number.isInteger(v)&&v>=0&&v<x.quiz.options.length)state[group][x.id]=v;}}save();navigate(current.id,false);toast('已合并记录，同课的导入内容覆盖现有记录。');}catch(err){toast('导入失败：'+err.message);}finally{e.target.value='';}};
$('#shutdown').onclick=async()=>{if(!token){$('#help-status').textContent='当前没有连接运行环境。';return;}try{await fetch('/api/shutdown',{method:'POST',headers:{'X-Lecture-Key':token}});token='';$('#connection').textContent='运行环境已停止 · 仍可阅读';$('#connection').classList.remove('ready');$('#help-status').textContent='已请求停止本地服务和本讲义 MySQL 实例；学习记录仍保存在浏览器。';}catch(e){$('#help-status').textContent='未连接到服务，可在启动窗口按 Ctrl+C。';}};
window.addEventListener('hashchange',()=>navigate(location.hash.slice(1)));
navigate(location.hash.slice(1)||state.last,false);checkRuntime();
