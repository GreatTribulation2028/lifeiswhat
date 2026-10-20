# -*- coding: utf-8 -*-
"""
★ 生死記錄儀 — 英文版子頁生成器（通用）
  用法：python -X utf8 gen_en_pages.py [page_key ...]
  設計原則：
    1. 中文原檔唯讀，生成前後 SHA256 必須一致
    2. 翻譯表放 JSON（en_gen/<key>.json），Python 唔掂字串，零引號陷阱
    3. 關鍵字 array（match 中文標題嘅 pattern）一個字都唔准郁 → allow_chinese_js 白名單 + 反向驗證
    4. <style> 區 byte-identical
    5. 所有本地相對路徑加 ../
    6. HTML 可見中文 = 0；JS 非註解中文 ⊆ 白名單
"""
import hashlib
import io
import json
import os
import re
import shutil
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
GEN = os.path.join(BASE, "en_gen")
OUTDIR = os.path.join(BASE, "en")


def sha(p):
    return hashlib.sha256(io.open(p, "rb").read()).hexdigest()


def load_cfg(key):
    p = os.path.join(GEN, key + ".json")
    if not os.path.exists(p):
        return None
    return json.load(io.open(p, encoding="utf-8"))


def strip_comments(js):
    js = re.sub(r"/\*.*?\*/", "", js, flags=re.S)
    js = re.sub(r"^\s*//.*$", "", js, flags=re.M)
    return js


def apply_all(s, cfg, errs, counts):
    """★ html + js 翻譯表合併成一張 → 全域按 old 長度 DESC → 套用
       原因：同一句中文可能同時出現喺 HTML 同 JS（長度唔同），
       分表逐個替，短版會先拆爛長版 → 長版再也 match 唔到。"""
    table = []
    seen = {}
    for label in ("html", "js"):
        for pair in cfg.get(label, []):
            old, new = pair[0], pair[1]
            if old in seen:
                if seen[old][0] != new:
                    errs.append(f"[CONFLICT] 「{old[:50]}」喺 {seen[old][1]} 同 {label} 譯法唔同")
                continue          # ★ 完全相同嘅 pair 去重（避免第二次搵唔到）
            seen[old] = (new, label)
            table.append([old, new, label])
    for old, new, label in sorted(table, key=lambda p: -len(p[0])):
        n = s.count(old)
        if n == 0:
            errs.append(f"[{label}] 搵唔到：{old[:70]!r}")
            continue
        s = s.replace(old, new)
        counts[label] = counts.get(label, 0) + n
    return s


def add_prefix_paths(s, targets, errs, contains=()):
    """所有指向 targets 清單嘅本地檔案引用 → 加 ../
       覆蓋：href=/src= 屬性、JS 動態 .src、fetch()、window.location.href、純引號字串
       contains：引號字串內含呢啲子串 → 路徑開頭加 ../（處理 ?v= / ?cat= 查詢參數）"""
    n = 0
    for t in targets:
        # 1) 屬性
        for attr in ("href", "src"):
            for q in ('"', "'"):
                old = f"{attr}={q}{t}{q}"
                new = f"{attr}={q}../{t}{q}"
                c = s.count(old)
                if c:
                    s = s.replace(old, new)
                    n += c
        # 2) 通用引號字串（JS redirect / fetch / 動態 src）
        for q in ("'", '"'):
            old = f"{q}{t}{q}"
            new = f"{q}../{t}{q}"
            c = s.count(old)
            if c:
                s = s.replace(old, new)
                n += c
        # 3) .src=t?v=  /  fetch(t) 變體
        for q_ in ("'", '"'):
            for tmpl in (f".src={q_}{t}?v={q_}", f"fetch({q_}{t}{q_})",
                         f".src={q_}{t}{q_}", f"fetch({q_}{t}?v={q_})"):
                c = s.count(tmpl)
                if c:
                    s = s.replace(tmpl, tmpl.replace(f"{t}", f"../{t}"))
                    n += c
    # 4) 含查詢參數嘅路徑
    #    ★ 關鍵修正：字元類必須排除空白/尖括號/引號，否則 `[^"]*` 會跨過
    #      整段 CSS + script 搵到一個超長區間，令 "../" 插喺錯位
    #      （實測搞到 class="err"../>）。同時限制長度 ≤120。
    for sub in contains:
        for q in ("'", '"', "`"):
            pat = (re.escape(q) + r"([^" + q + r"<>\s]{0,120}" + re.escape(sub)
                   + r"[^" + q + r"<>\s]{0,120})" + re.escape(q))
            while True:
                m = re.search(pat, s)
                if not m:
                    break
                val = m.group(1)
                if val.startswith("../"):
                    break
                s = s.replace(m.group(0), f"{q}../{val}{q}")
                n += 1
    return s, n


def build(key):
    cfg = load_cfg(key)
    if not cfg:
        return None
    src = os.path.join(BASE, cfg["src"])
    out = os.path.join(OUTDIR, cfg["out"])
    errs = []
    counts = {}

    before = sha(src)
    s = io.open(src, encoding="utf-8").read()
    o = s
    style_blocks = re.findall(r"<style[^>]*>.*?</style>", s, flags=re.S)

    # 1b) ★ 先屏蔽所有 <style> 區塊（category.html 有 4 個）
    #     原因：path 嘅 regex 同文案替換都會誤傷 CSS 註解內嘅中文
    styles = []

    def _mask(m):
        styles.append(m.group(0))
        return f"@@__STYLE_BLOCK_{len(styles) - 1}__@@"

    s = re.sub(r"<style[^>]*>.*?</style>", _mask, s, flags=re.S)

    # 1) 路徑加 ../
    s, n_path = add_prefix_paths(s, cfg.get("path_prefix", []), errs,
                                 cfg.get("path_prefix_contains", []))
    counts["path"] = n_path

    # 2) HTML + JS 文案（合併、全域最長優先）
    s = apply_all(s, cfg, errs, counts)

    # 1c) 還原 <style> 區
    for i, blk in enumerate(styles):
        s = s.replace(f"@@__STYLE_BLOCK_{i}__@@", blk)

    # 4) 語言列
    lb = cfg.get("langbar")
    if lb:
        if s.count("<body>\n") != 1:
            errs.append("[langbar] <body> 定位失敗")
        else:
            s = s.replace("<body>\n", "<body>\n" + lb + "\n")

    # ===== 驗證 =====
    after = sha(src)
    if before != after:
        errs.append("[FATAL] 原檔被改動！")

    # <style> 區（用遮罩保證原封不動，逐個 block 比對）
    for i, blk in enumerate(style_blocks):
        if blk not in s:
            errs.append(f"[FATAL] <style> block {i} 被改動或遺失")

    # 本地路徑：預設要 ../；allow_same_dir 內嘅可以留喺同層（英文頁互連）
    allow_same = set(cfg.get("allow_same_dir", [])) | {"index.html"}
    leftover = []
    for m in re.finditer(r"""(?:href|src)\s*=\s*["']([^"']+)["']""", s):
        v = m.group(1)
        if v.startswith(("http", "data:", "#", "mailto:", "javascript:", "//")):
            continue
        if v.startswith("../") or v.split("?")[0] in allow_same or "${" in v:
            continue
        leftover.append(v)
    if leftover:
        errs.append(f"[FATAL] 仍有未加 ../ 的路徑：{sorted(set(leftover))}")

    # HTML 可見中文
    body = s[s.index("<body>"):] if "<body>" in s else s
    b = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    b = re.sub(r"<script.*?</script>", "", b, flags=re.S)
    b = re.sub(r"<style.*?</style>", "", b, flags=re.S)
    txt = re.sub(r"<[^>]+>", "\n", b)
    zh = sorted(set(x.strip() for x in txt.split("\n")
                    if x.strip() and re.search(r"[\u4e00-\u9fff]", x.strip())))
    if zh:
        errs.append(f"[FATAL] HTML 仍有可見中文 {len(zh)} 項：{zh[:12]}")

    # JS 非註解中文 vs 白名單
    allow = set(cfg.get("allow_chinese_js", []))
    js_all = "\n".join(re.findall(r"<script[^>]*>(.*?)</script>", s, flags=re.S))
    nc = strip_comments(js_all)
    found = set()
    for q in re.findall(r"'([^']{1,300})'|\"([^\"]{1,300})\"", nc):
        v = (q[0] or q[1]).strip()
        if re.search(r"[\u4e00-\u9fff]", v):
            for w in re.findall(r"[\u4e00-\u9fff]+", v):
                found.add(w)
    bad = sorted(found - allow)
    if bad:
        errs.append(f"[FATAL] JS 有非白名單中文：{bad[:25]}")
        for w in bad[:6]:
            for mm in re.finditer(re.escape(w), nc):
                a = max(0, mm.start() - 70)
                errs.append(f"        ↳ {w}: {nc[a:mm.end()+50]!r}")
                break
    # 反向：白名單每個詞都要仍然存在（證明關鍵字無被誤刪）
    lost = [w for w in allow if w not in js_all]
    if lost:
        errs.append(f"[FATAL] 白名單關鍵字消失（被誤改）：{lost}")
        for w in lost[:4]:
            errs.append(f"        ↳ {w} 原檔出現 {o.count(w)} 次")

    if errs:
        print(f"\n❌ {key} 失敗：")
        for e in errs:
            print("   ", e)
        return False

    os.makedirs(os.path.dirname(out), exist_ok=True)
    with io.open(out, "w", encoding="utf-8", newline="") as f:
        f.write(s)

    print(f"✅ {key:16s} → {cfg['out']:22s} "
          f"路徑{counts.get('path',0):3d} HTML{counts.get('html',0):4d} JS{counts.get('js',0):4d} "
          f"白名單{len(allow):3d}  {len(s):,} bytes")
    return True


def main():
    keys = sys.argv[1:] or [os.path.splitext(f)[0]
                            for f in sorted(os.listdir(GEN)) if f.endswith(".json")]
    ok = True
    for k in keys:
        if not build(k):
            ok = False
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
