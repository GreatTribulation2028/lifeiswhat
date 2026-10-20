# -*- coding: utf-8 -*-
"""
★ JS 語法驗證器（無 node → 用 headless Chrome）
  做法：頁面 inline JS 直接注入 probe.html 嘅 <script> 內
        → 真語法錯誤 = "Uncaught SyntaxError"（可區分）
        → 資源 404 = "Script error."（忽略）
  ★ 步驟 1 先用故意整壞嘅檔案驗證檢測器本身有效
"""
import io
import os
import re
import subprocess
import sys
import tempfile

BASE = os.path.dirname(os.path.abspath(__file__))
TMP = os.path.join(tempfile.gettempdir(), "js_syntax_check")
os.makedirs(TMP, exist_ok=True)

CHROME = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

HEAD = """<html><head><title>PENDING</title></head><body>
<script>
window.__errs=[];
window.onerror=function(m,s,l){window.__errs.push(String(m||'')+' @'+l);return false;};
window.addEventListener('error',function(e){
  var msg=String((e&&e.message)||'');
  if(msg && msg!=='Script error.') window.__errs.push(msg);
},true);
</script>
<script>
"""
TAIL = """
</script>
<script>
var se = window.__errs.filter(function(x){return /SyntaxError|Unexpected|Invalid or unexpected/i.test(x);});
var re_ = window.__errs.filter(function(x){return !/SyntaxError|Unexpected|Invalid or unexpected/i.test(x);});
document.title = se.length ? ('SYNTAX:: '+se.join(' | ')) : ('OK:: runtime-only:'+re_.length);
</script></body></html>"""


def check_js(js_text, tag=""):
    body = js_text.replace("</script>", "<\\/script>")
    with io.open(os.path.join(TMP, "probe.html"), "w", encoding="utf-8") as f:
        f.write(HEAD + body + TAIL)
    out = os.path.join(TMP, "out.html")
    uri = "file:///" + os.path.join(TMP, "probe.html").replace("\\", "/")
    try:
        r = subprocess.run(
            [CHROME, "--headless", "--disable-gpu", "--no-sandbox",
             "--virtual-time-budget=4000", "--dump-dom", uri],
            capture_output=True, text=True, timeout=90, errors="replace")
        html = r.stdout or ""
    except Exception as e:
        return False, f"chrome failed: {e}"
    m = re.search(r"<title>(.*?)</title>", html, flags=re.S)
    title = (m.group(1).strip() if m else "(no title)")
    if title.startswith("SYNTAX::"):
        return False, title[:300]
    if title.startswith("OK::"):
        return True, title
    return False, f"unexpected title: {title!r}"


def extract_inline_js(path):
    s = io.open(path, encoding="utf-8").read()
    return "\n;\n".join(m.group(1) for m in
                        re.finditer(r"<script[^>]*>(.*?)</script>", s, flags=re.S))


def main():
    print("=== 步驟 1：檢測器自我驗證 ===")
    ok, msg = check_js("var a = 1;\nfunction f( { return 2; }\nvar b = 'x;\n")
    print(f"  故意整壞 → {'❌ 檢測器漏報' if ok else '✅ 有效'}  {msg}")
    if ok:
        print("❌ 檢測器無效，停止"); sys.exit(1)
    ok, msg = check_js("var a = 1;\nfunction f(){ return 2; }\nnull.x;\n")
    print(f"  正常檔案 → {'✅ 通過' if ok else '❌ 誤報'}  {msg}")
    if not ok:
        print("❌ 檢測器誤報，停止"); sys.exit(1)

    print("\n=== 步驟 2：英文頁 inline JS 語法 ===")
    allok = True
    for p in ["index.html", "GoodNews.html", "timeline04.html",
              "index0203.html", "monitor03E.html", "category.html"]:
        f = os.path.join(BASE, "en", p)
        if not os.path.exists(f):
            print(f"  {p:20s} (未生成)"); continue
        js = extract_inline_js(f)
        ok, msg = check_js(js)
        print(f"  {p:20s} {'✅' if ok else '❌'}  {msg}  ({len(js):,} bytes JS)")
        if not ok:
            allok = False
    print("\n" + ("✅ 全部通過" if allok else "❌ 有頁面語法錯誤"))
    sys.exit(0 if allok else 1)


if __name__ == "__main__":
    main()