"""Build the static GitHub Pages demo in docs/.

The demo reuses the real front-end verbatim so it can never drift far from the
shipped app; the only changes are (a) DEMO_MODE short-circuits the run button to
show the pre-verified expected output and (b) a banner says so out loud.
No backend, no execution endpoint, nothing is uploaded.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / 'docs'
BANNER = (
    '<p class="demo-note"><span>静态演示页：不连接任何后端，点「运行」显示的是预先验证过的预期输出。</span>'
    '<a href="https://github.com/VVsLitMoon/data-analysis-course">在本地运行完整版 →</a></p>'
)
DEMO_RUN = (
    " if(window.DEMO_MODE){const d=current.expected,o=$('#output'),b=$('#run');"
    "if(!d){o.innerHTML='<p>本节是概念练习，没有可运行代码。</p>';return;}"
    "b.disabled=true;b.textContent='运行中…';o.innerHTML='<p>正在执行你编辑的代码…</p>';"
    "setTimeout(()=>{o.innerHTML='<span class=\"success-label\">✓ 预先验证过的预期输出（静态演示，不执行真实代码）</span>'+resultHTML(d);"
    "b.disabled=false;b.textContent='▶ 运行代码';},420);return;}\n"
)
DEMO_STATUS = (
    " if(window.DEMO_MODE){$('#connection').textContent='静态演示 · 运行结果为预先生成';return;}\n"
)
BANNER_CSS = (
    ".demo-note{margin:0;padding:9px 30px;background:var(--accent);color:#fff;font-size:12px;"
    "line-height:1.7;display:flex;gap:16px;justify-content:center;align-items:center;"
    "flex-wrap:wrap;letter-spacing:.2px}.demo-note a{color:#ffe9b8;text-decoration:none;"
    "font-weight:600}.demo-note a:hover{text-decoration:underline}"
    "#shutdown{display:none}"
)


def replace_once(text, old, new, label):
    if text.count(old) != 1:
        raise SystemExit(f'build_demo: expected exactly one match for {label}, found {text.count(old)}')
    return text.replace(old, new)


def build():
    DOCS.mkdir(exist_ok=True)

    html = (ROOT / 'index.html').read_text(encoding='utf-8')
    html = replace_once(html, '<body>', '<body>\n' + BANNER, 'body banner')
    html = replace_once(
        html,
        '<script src="lessons.js"></script><script src="app.js"></script>',
        '<script src="lessons.js"></script><script>window.DEMO_MODE=true;</script><script src="app.js"></script>',
        'demo flag')
    html = replace_once(
        html,
        '<p><b>开始：</b>双击本文件夹的 <code>启动讲义.cmd</code>，浏览器打开 <code>http://127.0.0.1:8766</code>。首次数据库准备可能需要十几秒。</p>',
        '<p><b>这里是什么：</b>这是一份静态演示页，页面不连接任何后端。点「运行」看到的是预先在本机验证过的预期输出，'
        '用来体验交互方式，不会真的执行你改的代码。想真正执行 SQL 与 Python，请在本地运行完整版。</p>',
        'help text')

    app = (ROOT / 'app.js').read_text(encoding='utf-8')
    app = replace_once(app, 'async function runCode(){\n', 'async function runCode(){\n' + DEMO_RUN, 'runCode hook')
    app = replace_once(app, 'async function checkRuntime(attempt=0){\n',
                       'async function checkRuntime(attempt=0){\n' + DEMO_STATUS, 'checkRuntime hook')

    css = (ROOT / 'style.css').read_text(encoding='utf-8')
    css = css.rstrip('\n') + '\n' + BANNER_CSS + '\n'

    (DOCS / 'index.html').write_text(html, encoding='utf-8')
    (DOCS / 'app.js').write_text(app, encoding='utf-8')
    (DOCS / 'style.css').write_text(css, encoding='utf-8')
    for name in ('lessons.js', 'favicon.svg'):
        (DOCS / name).write_text((ROOT / name).read_text(encoding='utf-8'), encoding='utf-8')
    print({'docs': str(DOCS.relative_to(ROOT)), 'files': 5})


if __name__ == '__main__':
    build()
