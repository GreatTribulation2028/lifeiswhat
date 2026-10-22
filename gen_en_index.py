# -*- coding: utf-8 -*-
"""★ 2026-10-19：產生 en/index.html（生死記錄儀英文版首頁）
唯讀來源 index.html，只改：head title/meta、body 靜態文案、相對路徑加 ../
JS 一個字都唔改（已驗證 script 區 0 條中文）。
"""
import io
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
# ★ 語言列工具喺 build_news py（trilingual.py）—— 搵唔到就退化用舊 inline bar
_BUILD_NEWS_PY = os.path.join(os.path.dirname(_HERE), "build_news py")
if os.path.isdir(_BUILD_NEWS_PY) and _BUILD_NEWS_PY not in sys.path:
    sys.path.insert(0, _BUILD_NEWS_PY)
try:
    from trilingual import add_bar, strip_bars, LANG_CSS
except Exception:  # pragma: no cover
    add_bar = None
    strip_bars = None
    LANG_CSS = ""

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "en", "index.html")

# (舊字串, 新字串) 必須唯一，count != 1 即停
REPL = [
    # ---------- head ----------
    ('<html lang="zh-HK">', '<html lang="en">'),
    ('<title>STILL ALIVE? 還活著嗎?悲傷孤獨的世界裡，至少有人仍願意明白您，所以一直記錄著...</title>',
     '<title>STILL ALIVE? In a grieving, lonely world, someone still wanted to understand you &mdash; and kept recording...</title>'),
    ('<meta name="description" content="在你讀這句話的時間裡，有人永遠停止了呼吸。你還活著。">',
     '<meta name="description" content="In the time it took you to read this sentence, someone stopped breathing forever. You are still alive.">'),
    ('<meta property="og:title" content="STILL ALIVE? 還活著嗎?悲傷孤獨的世界裡，至少有人仍願意明白您，所以一直記錄著...">',
     '<meta property="og:title" content="STILL ALIVE? In a grieving, lonely world, someone still wanted to understand you &mdash; and kept recording...">'),
    ('<meta property="og:description" content="世界在變，人心依舊？">',
     '<meta property="og:description" content="The world is changing. Have people changed with it?">'),
    # ---------- top nav ----------
    ('id="data-date-title">2021 年 — 至今</div>',
     'id="data-date-title">2021 &ndash; today</div>'),
    ('<span class="catnav-label">災情報告分類</span>',
     '<span class="catnav-label">Disaster Report Categories</span>'),
    ('14 類 · 27,601 條 · rules', '14 categories &middot; 27,601 records &middot; rules'),
    ('<span class="cc-n">經濟</span>', '<span class="cc-n">Economy</span>'),
    ('<span class="cc-n">猝死</span>', '<span class="cc-n">Sudden Death</span>'),
    ('<span class="cc-n">醫藥</span>', '<span class="cc-n">Medical</span>'),
    ('<span class="cc-n">自殺</span>', '<span class="cc-n">Suicide</span>'),
    ('<span class="cc-n">治安</span>', '<span class="cc-n">Security</span>'),
    ('<span class="cc-n">交通</span>', '<span class="cc-n">Traffic</span>'),
    ('<span class="cc-n">火警</span>', '<span class="cc-n">Fire</span>'),
    ('<span class="cc-n">意外</span>', '<span class="cc-n">Accidents</span>'),
    ('<span class="cc-n">天災</span>', '<span class="cc-n">Natural Disasters</span>'),
    ('<span class="cc-n">遇溺</span>', '<span class="cc-n">Drowning</span>'),
    ('<span class="cc-n">AI安全</span>', '<span class="cc-n">AI Safety</span>'),
    ('<span class="cc-n">七年大災難</span>', '<span class="cc-n">Seven-Year Tribulation</span>'),
    ('<span class="cc-n">中暑昏迷</span>', '<span class="cc-n">Heatstroke</span>'),
    ('<span class="cc-n">宗教</span>', '<span class="cc-n">Religion</span>'),
    # ---------- top bar ----------
    ('人因心血管猝逝</div>', 'died of cardiovascular causes</div>'),
    ('<a href="timeline04.html">時代觀測</a>',
     '<a href="timeline04.html">Era Observatory</a>'),
    ('<a href="index0203.html">記錄儀</a>',
     '<a href="index0203.html">The Recorder</a>'),
    # ---------- splash ----------
    ('⚡ 死亡相關新聞 / 猝死</div>', '⚡ Death-related news / Sudden death</div>'),
    ('你打開後，全球估計已有 <span class="sgv" id="dc-since-sub">0</span> 人因心血管疾病猝逝</div>',
     'Since you opened this page, an estimated <span class="sgv" id="dc-since-sub">0</span> people worldwide have died of cardiovascular disease</div>'),
    ('<span class="ref-label">參考來源</span>',
     '<span class="ref-label">Sources</span>'),
    ('>WHO • 心血管</a>', '>WHO &bull; Cardiovascular</a>'),
    ('>AHA • 猝死</a>', '>AHA &bull; Sudden Death</a>'),
    ('>WHO • 交通</a>', '>WHO &bull; Road Traffic</a>'),
    ('>WHO • 自殺</a>', '>WHO &bull; Suicide</a>'),
    ('<div class="sudden-box-title">最新死亡記錄 <span class="hint">（向下滑＝更早）</span></div>',
     '<div class="sudden-box-title">Latest Death Records <span class="hint">(scroll down = earlier)</span></div>'),
    ('載入數年記錄中，請稍候…', 'Loading years of records, please wait&hellip;'),
    ('<div style="font-size:13px;margin-top:10px;color:rgba(255,255,255,.25)">資料量較大，首次載入需數秒</div>',
     '<div style="font-size:13px;margin-top:10px;color:rgba(255,255,255,.25)">Large dataset &mdash; first load takes a few seconds</div>'),
    # ---------- calendar stats ----------
    ('onclick="setCalMode(\'day\')">每日</button>', 'onclick="setCalMode(\'day\')">Daily</button>'),
    ('onclick="setCalMode(\'month\')">按月</button>', 'onclick="setCalMode(\'month\')">Monthly</button>'),
    ('onclick="setCalMode(\'year\')">按年</button>', 'onclick="setCalMode(\'year\')">Yearly</button>'),
    # ---------- SEC 1 ----------
    ('<div class="s-title">剩多少時間？</div>', '<div class="s-title">How much time is left?</div>'),
    ('<span class="age-label-txt">輸入年齡</span>', '<span class="age-label-txt">Enter age</span>'),
    ('<span class="age-unit">歲</span>', '<span class="age-unit">yrs</span>'),
    ('<span>出生</span><span id="d-pct">37.5% 已消耗</span><span>80 歲</span>',
     '<span>Birth</span><span id="d-pct">37.5% elapsed</span><span>Age 80</span>'),
    # ---------- SEC 2 ----------
    ('<div class="s-title">相同年齡，突發死亡多少?</div>',
     '<div class="s-title">At your age, how many sudden deaths?</div>'),
    ('<span id="p-range">25-35</span> 歲</div>', '<span id="p-range">25-35</span> yrs</div>'),
    ('本港新聞記錄中，同齡（±5年）突發死亡個案。<br>',
     'Sudden death cases among your age group (&plusmn;5 years) in Hong Kong news records.<br>'),
    ('上月 <strong id="p-lm" style="color:var(--gold)">—</strong> 宗',
     'Last month <strong id="p-lm" style="color:var(--gold)">—</strong> cases'),
    ('上年 <strong id="p-ly" style="color:var(--gold)">—</strong> 宗',
     'Last year <strong id="p-ly" style="color:var(--gold)">—</strong> cases'),
    ('<h4>本港突發死亡年齡分佈（新聞記錄）</h4>',
     '<h4>Age distribution of sudden deaths in Hong Kong (news records)</h4>'),
    # ---------- SEC 3 ----------
    ('<h4>📊 年度死亡時間曲線（2019 → 今日）</h4>',
     '<h4>📊 Annual Death Timeline (2019 &rarr; today)</h4>'),
    ('data-ycf="ALL" style="padding:4px 10px;cursor:pointer">全部</button>',
     'data-ycf="ALL" style="padding:4px 10px;cursor:pointer">All</button>'),
    ('<h4>📈 月度趨勢（猝死/暈倒）</h4>', '<h4>📈 Monthly trend (sudden death / collapse)</h4>'),
    ('>數據收集自 2021 年至今 · 每日更新 · 共 <span id="proof-total">—</span> 宗記錄</p>',
     '>Data collected from 2021 to today &middot; updated daily &middot; <span id="proof-total">&mdash;</span> records total</p>'),
    ('<div class="subkw-box"><h4>🔍 突發死亡關鍵詞分類統計</h4>',
     '<div class="subkw-box"><h4>🔍 Sudden death keyword classification</h4>'),
    # ---------- SEC 5 ----------
    ('style="line-height:2.2;font-size:clamp(1.6rem,5vw,2.4rem)">生命只如，<br>一滑而過？</div>',
     'style="line-height:2.2;font-size:clamp(1.6rem,5vw,2.4rem)">Life passes<br>in the blink of an eye?</div>'),
    ('<a class="cta-card" href="index0203.html">', '<a class="cta-card" href="index0203.html">'),
    ('<div class="cta-title">生死記錄儀</div><div class="cta-desc">完整記錄，每日更新</div>',
     '<div class="cta-title">STILL ALIVE Recorder</div><div class="cta-desc">The full record, updated daily</div>'),
    ('<a class="cta-card" href="timeline04.html">', '<a class="cta-card" href="timeline04.html">'),
    ('<div class="cta-title">時代觀測站</div><div class="cta-desc">六年，世界變了多少</div>',
     '<div class="cta-title">Era Observatory</div><div class="cta-desc">Six years &mdash; how much has changed</div>'),
    ('<a class="cta-card" href="GoodNews.html">', '<a class="cta-card" href="GoodNews.html">'),
    ('<div class="cta-title">如果下一個數字，是你…身邊人？</div><div class="cta-desc">給自己 3 分鐘</div>',
     '<div class="cta-title">What if the next number is someone you know?</div><div class="cta-desc">Give yourself 3 minutes</div>'),
    # ---------- footer ----------
    ('margin-bottom:8px">記錄的，不是數字。<br>是一份對人的記念。</div>',
     'margin-bottom:8px">What is recorded is not a number.<br>It is a remembrance of people.</div>'),
    ('全球每天約 <span class="btv">49,000</span> 人因心血管疾病猝逝 · 每年約 <span class="btv">1,790</span> 萬人',
     'Roughly <span class="btv">49,000</span> people worldwide die of cardiovascular disease every day &middot; about <span class="btv">17.9</span> million a year'),
]

# category.html 相對路徑加 ../
CAT_HREF = [
    'href="category.html?cat=economy"', 'href="category.html?cat=sudden"',
    'href="category.html?cat=medical"', 'href="category.html?cat=suicide"',
    'href="category.html?cat=security"', 'href="category.html?cat=traffic"',
    'href="category.html?cat=fire"', 'href="category.html?cat=accident"',
    'href="category.html?cat=disaster"', 'href="category.html?cat=drowning"',
    'href="category.html?cat=ai_safety"', 'href="category.html?cat=tribulation"',
    'href="category.html?cat=heatstroke"', 'href="category.html?cat=religion"',
]


# ===================================================================
# ★ JS 內 user-visible 字串（只有 en/index.html 副本會改，中文版一個字都唔郁）
#   唔改：分類關鍵字 array（kws:）、註解、變數名、邏輯
# ===================================================================
JS_REPL = [
    # ---- SUBKW 組名（只改 name，kws 保持中文做 match）----
    ("name:'猝死 / 暴斃 / 驟逝'", "name:'Sudden death / Collapse'"),
    ("name:'心臟驟停 / OHCA'", "name:'Cardiac arrest / OHCA'"),
    ("name:'心肌梗塞 / 心臟病發'", "name:'Heart attack / MI'"),
    ("name:'腦溢血 / 腦出血 / 腦梗塞'", "name:'Stroke / Brain haemorrhage'"),
    ("name:'過勞死 / 睡夢猝死'", "name:'Overwork death / Sleep death'"),
    ("name:'倒斃 / 路倒 / 當場不治'", "name:'Collapsed on scene / Pronounced dead'"),
    # ---- TAG_ZH 圖例 ----
    ("var TAG_ZH={sudden:'猝死',departure:'自殺離世',industry:'工業意外',traffic:'交通',fire:'火警',",
     "var TAG_ZH={sudden:'Sudden death',departure:'Suicide',industry:'Industrial accident',traffic:'Traffic',fire:'Fire',"),
    ("  tragedy:'遇溺悲劇',plague:'瘟疫醫藥',sidefx:'藥物副作用',econ:'經濟',disaster:'天災',",
     "  tragedy:'Drowning tragedy',plague:'Pandemic / Medical',sidefx:'Drug side effects',econ:'Economy',disaster:'Natural disaster',"),
    ("  war:'戰爭',social:'治安社會',food:'糧食',tech:'AI與科技',religion:'宗教',",
     "  war:'War',social:'Public safety',food:'Food',tech:'AI & Tech',religion:'Religion',"),
    ("  tribulation:'七年大災難',celestial:'天象',politics:'政治'};",
     "  tribulation:'Seven-Year Tribulation',celestial:'Celestial signs',politics:'Politics'};"),
    ("'　（全部類別）'", "' (All categories)'"),
    ("label:(YCF_CUR==='ALL'?'全部類別':tagZh(YCF_CUR))", "label:(YCF_CUR==='ALL'?'All categories':tagZh(YCF_CUR))"),
    # ---- 農曆：改用數字標記（M1..M12 / D1..D30 / Leap）----
    ("if(l.d===1)return (l.isLeap?'閏':'')+L_MONTH[l.m-1]+'月';",
     "if(l.d===1)return (l.isLeap?'Leap ':'')+'M'+l.m;"),
    # ---- 日曆 ----
    ("textContent=y+' 年 '+(m+1)+' 月'", "textContent=y+' / '+(m+1)"),
    ("textContent=y+' 年'", "textContent=y+''"),
    ("textContent=y+'年'+(m+1)+'月 死亡相關新聞共 '+monthTotal+' 宗 · 點任一日看當天記錄'",
     "textContent=y+' / '+(m+1)+' \\u2014 '+monthTotal+' death-related records \\u00b7 click any day'"),
    ("textContent=y+'年 死亡相關新聞共 '+yearTotal+' 宗 · 點任一月看當月記錄'",
     "textContent=y+' \\u2014 '+yearTotal+' death-related records \\u00b7 click any month'"),
    ("textContent='歷年總覽'", "textContent='All years'"),
    ("textContent='歷年死亡相關新聞共 '+grand.toLocaleString()+' 宗 · 點任一年看當年月份'",
     "textContent='All years: '+grand.toLocaleString()+' death-related records \\u00b7 click any year'"),
    ("：無記錄</div>", ": No records</div>"),
    # ---- 生命條 ----
    ("Math.min(100,pct)+'% 已消耗'", "Math.min(100,pct)+'% elapsed'"),
    # ---- 圖表 ----
    ("textContent='共 '+keys.length+' 個月（'+keys[0]+' 至 '+keys[keys.length-1]+'），X 軸顯示各年首月'",
     "textContent=keys.length+' months ('+keys[0]+' to '+keys[keys.length-1]+'), X axis shows first month of each year'"),
    ("textContent='暫無記錄'", "textContent='No records yet'"),
    ("textContent='↑ 上下瀏覽 · 向下滑動查看更早記錄 ↓'",
     "textContent='\\u2191 Scroll up / down to browse \\u00b7 swipe down for earlier records \\u2193'"),
    ("textContent='共 '+TL.total.toLocaleString()+' 條有真實日期　'",
     "textContent=TL.total.toLocaleString()+' records with a verified date'"),
    # ---- 錯誤訊息 ----
    ("'⚠ data_today.js 載入失敗（請 Ctrl+Shift+R 強制刷新）'",
     "'\\u26a0 data_today.js failed to load (press Ctrl+Shift+R to force refresh)'"),
    ("'⚠ data_today.js 內容為空'", "'\\u26a0 data_today.js is empty'"),
    # ---- data-date-title 動態日期 ----
    ("fp[0]+'年'+parseInt(fp[1])+'月'+parseInt(fp[2])+'日 — '+lp[0]+'年'+parseInt(lp[1])+'月'+parseInt(lp[2])+'日'",
     "fp[0]+'-'+fp[1]+'-'+fp[2]+' \\u2014 '+lp[0]+'-'+lp[1]+'-'+lp[2]"),
]


# ============ 第二輪：餘下 user-visible 字串 + data 路徑加 ../ ============
JS_REPL2 = [
    # ---- ★ data 路徑（英文版喺 en/ 子層，必須 ../ ）----
    ("s.src='data_today.js?v='", "s.src='../data_today.js?v='"),
    ("s.src='data_timeline.js?v='", "s.src='../data_timeline.js?v='"),
    ("fetch('classify_rules.json')", "fetch('../classify_rules.json')"),
    # ---- 日曆模式按鈕（定義 + 比對，必須一致）----
    ("var map={day:'每日',month:'按月',year:'按年'};",
     "var map={day:'Daily',month:'Monthly',year:'Yearly'};"),
    ("b.textContent.trim()==='每日'", "b.textContent.trim()==='Daily'"),
    ("b.textContent.trim()==='按月'", "b.textContent.trim()==='Monthly'"),
    # ---- 星期表頭 ----
    ("var wd=['日','一','二','三','四','五','六'];",
     "var wd=['Su','Mo','Tu','We','Th','Fr','Sa'];"),
    # ---- 月格 ----
    ("<div class=\"cal-d\">'+m+' 月</div>", "<div class=\"cal-d\">Month '+m+'</div>"),
    # ---- 日期格式：2026-03-14 ----
    ("var head=parts[0]+'年'+parseInt(parts[1])+'月'+parseInt(parts[2])+'日';",
     "var head=parts[0]+'-'+parts[1]+'-'+parts[2];"),
    ("'+head+' · '+dayEvents.length+' 宗</div>'",
     "'+head+' \\u00b7 '+dayEvents.length+' records</div>'"),
    # ---- 突發死亡按日 ----
    ("'+parts[0]+'年'+parseInt(parts[1])+'月'+parseInt(parts[2])+'日</span><br>突發死亡相關新聞 <span class=\"srv\">'+dates[d]+'</span> 宗<br>'",
     "'+parts[0]+'-'+parts[1]+'-'+parts[2]+'</span><br>Sudden-death records <span class=\"srv\">'+dates[d]+'</span><br>'"),
    ("'+date+'（'+groups[date].length+' 宗）</div>'",
     "'+date+' ('+groups[date].length+')</div>'"),
    # ---- 截斷提示（必須整句替換，唔可以拆細：拆咗會產生相鄰字串字面量 → SyntaxError）----
    (">另有 '+truncated.toLocaleString()+' 宗較早記錄 · 趨勢圖已包含全部數據</div>'",
     ">'+truncated.toLocaleString()+' earlier records · the trend chart includes them all</div>'"),
    # ---- 年度曲線圖 ----
    ("ctx.fillText('年度死亡新聞條數　最高 '+mx, 8, 14);",
     "ctx.fillText('Annual death records \\u00b7 peak '+mx, 8, 14);"),
    ("ctx.fillText('（Chart.js 未載入，用後備繪圖）', 8, h-4);",
     "ctx.fillText('(Chart.js not loaded \\u2014 fallback renderer)', 8, h-4);"),
    ("text:'新聞條數'", "text:'Records'"),
    ("text:'年份'", "text:'Year'"),
]

# ★ 正規化：作者手誤寫入嘅字面反斜線（\" 同 \'）必須還原成真字元，
#   否則 search string 會多兩個字而永遠 match 唔到（靜靜失敗）。
def _fix(t):
    return t.replace('\\"', '"').replace("\\'", "'")


JS_REPL2 = [(_fix(a), _fix(b)) for a, b in JS_REPL2]
JS_REPL = [(_fix(a), _fix(b)) for a, b in JS_REPL]


def main():
    o = io.open(SRC, encoding="utf-8").read()
    s = o
    orig_len = len(s)

    # 0) ★ 剝走來源檔已有嘅語言列。
    #    來源 index.html 嘅繁體 bar 入面 href="zh-cn/index.html" / "en/index.html"
    #    係相對 repo 根嘅，直接繼承落 en/index.html 會指錯層。
    #    同時舊 bar 嘅文字會令下面 REPL「出現次數 == 1」檢查計錯。
    if strip_bars:
        s, _n_inh = strip_bars(s)

    # 1) category.html 連結：★ 留喺同層（en/category.html = 英文版）
    #    只有共用資源（data_*.js / classify_rules.json）先加 ../
    for h in CAT_HREF:
        n = s.count(h)
        if n != 1:
            print(f"[STOP] {h} 出現 {n} 次（預期 1）")
            sys.exit(1)
        # 唔加 ../ — en/index.html → category.html 即 en/category.html（英文版）

    # 2) 文案替換
    applied = 0
    for old, new in REPL:
        n = s.count(old)
        if n != 1:
            print(f"[STOP] 「{old[:50]}」出現 {n} 次（預期 1）")
            sys.exit(1)
        s = s.replace(old, new)
        applied += 1

    # 3) JS user-visible 字串翻譯
    js_done = 0
    for old, new in JS_REPL:
        n = s.count(old)
        if n != 1:
            print(f"[STOP] JS「{old[:60]}」出現 {n} 次（預期 1）")
            sys.exit(1)
        s = s.replace(old, new)
        js_done += 1

    # 3b) 第二輪 JS 翻譯
    for old, new in JS_REPL2:
        n = s.count(old)
        if n != 1:
            print(f"[STOP] JS2「{old[:60]}」出現 {n} 次（預期 1）")
            sys.exit(1)
        s = s.replace(old, new)
        js_done += 1

    # 3) lunarLabel 剩餘行（用 regex，處理 \r\n）
    import re as _re
    pat_lunar = _re.compile(
        r"(?P<nl>\r?\n)var s;(?P=nl)"
        r"if\(l\.d===10\)s='初十';else if\(l\.d===20\)s='二十';else if\(l\.d===30\)s='三十';(?P=nl)"
        r"else s=\['初','十','廿','卅'\]\[Math\.floor\(l\.d/10\)\]\+L_NUM\[l\.d%10\];(?P=nl)"
        r"return s;"
    )
    s, n_lunar = pat_lunar.subn("", s, count=1)
    if n_lunar != 1:
        print(f"[STOP] lunarLabel 剩餘行匹配 {n_lunar} 次（預期 1）")
        sys.exit(1)

    # 4) 語言列：插喺 <body> 之後（統一用 trilingual 三語列：繁體 | 简体 | English）
    if add_bar:
        # en/index.html → 繁體 ../index.html、简体 ../zh-cn/index.html、英文自己
        s, _n_old = add_bar(s, "../index.html", "../zh-cn/index.html", "index.html", "en")
    else:
        # 退路：舊 inline bar（得兩語言）
        langbar = (
            '\n<div style="position:fixed;top:2px;left:50%;transform:translateX(-50%);'
            'z-index:1001;font-family:var(--f-mono);font-size:12px;'
            'background:rgba(6,10,18,.92);border:1px solid rgba(255,255,255,.08);'
            'padding:5px 14px;border-radius:20px">'
            '<a href="../index.html" style="color:var(--text-dim)">&#20013;&#25991;</a>'
            ' &nbsp;|&nbsp; <span style="color:var(--accent)">English</span></div>\n'
        )
        if s.count("<body>\n") != 1:
            print("[STOP] <body> 定位失敗")
            sys.exit(1)
        s = s.replace("<body>\n", "<body>\n" + langbar)

    # ===== 驗證 =====
    def inline_js(t):
        return t[t.rindex("<script>"):t.rindex("</script>")]

    def style_block(t):
        return t[t.index("<style>"):t.index("</style>") + len("</style>")]

    # 5) <style> 必須 byte-identical
    #    ★ 語言列 CSS（LANG_CSS）係 build_trilingual 加落嚟嘅，可以有；
    #    但原始頁面 CSS 一個字都唔准改 → 比較前先剝走 LANG_CSS。
    def norm_style(t):
        b = style_block(t)
        if LANG_CSS and LANG_CSS.strip() in b:
            b = b.replace(LANG_CSS.strip(), "", 1)
        return b

    if norm_style(o) != norm_style(s):
        print("[STOP] <style> 區被改動")
        sys.exit(1)

    import re
    # 6) 分類關鍵字必須一字不差（最關鍵：改咗全站分類死）
    for kwname in ["KW_CORE", "KW_CARDIAC", "KW_BRAIN", "KW_DEATH_CERTAIN",
                   "KW_NEED_CONFIRM", "KW_COLLAPSE", "CLASSIFY_MAP"]:
        po = re.search(kwname + r"\s*=\s*(\[[^;]*\]|\{[^;]*\});", o, re.S)
        ps = re.search(kwname + r"\s*=\s*(\[[^;]*\]|\{[^;]*\});", s, re.S)
        if po and po.group(1) != (ps.group(1) if ps else None):
            print(f"[STOP] {kwname} 被改動")
            sys.exit(1)
        if po:
            print(f"  ✓ {kwname} 未改動（{len(po.group(1)):,} 字元）")

    # 6b) SUBKW_GROUPS 嘅 kws array 必須原封不動
    for m_o in re.finditer(r"kws:(\[[^\]]*\])", o):
        if m_o.group(1) not in s:
            print(f"[STOP] SUBKW kws 被改動: {m_o.group(1)[:50]}")
            sys.exit(1)
    print(f"  ✓ SUBKW kws 全部未改動（{len(re.findall(r'kws:.', o))} 組）")

    # 7) JS 剩低中文只可以係註解
    js = inline_js(s)
    nocomment = re.sub(r"/\*.*?\*/", "", js, flags=re.S)
    nocomment = re.sub(r"^\s*//.*$", "", nocomment, flags=re.M)
    left = sorted(set(re.findall(r"[\u4e00-\u9fff]+", nocomment)))
    if left:
        print(f"[CHECK] 非註解區仍有中文: {left}")

    # 8) body 剩餘中文
    body = s[s.index("<body>"):s.rindex("<script>")]
    #    ★ 語言列嘅「繁體 | 简体」係刻意保留嘅中文標籤，唔算殘留
    body = re.sub(r'<div class="langbar">.*?</div>', "", body, flags=re.S)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    leftb = sorted(set(re.findall(r"[\u4e00-\u9fff]+", body)))
    if leftb:
        print(f"[CHECK] body 仍有中文: {leftb}")

    # 9) ★ 語言列自檢：只可以有一條，而且三語 link 齊全（唔准出現兩條重疊 bar）
    n_bar = s.count('class="langbar"')
    if n_bar != 1:
        print(f"[STOP] 語言列數量 {n_bar}（預期 1）")
        sys.exit(1)
    if '<div style="position:fixed;top:2px;left:50%' in s:
        print("[STOP] 舊 inline 語言列殘留")
        sys.exit(1)
    for need in ('href="../index.html"', 'href="../zh-cn/index.html"', 'href="index.html"'):
        if need not in s:
            print(f"[STOP] 語言列缺少 {need}")
            sys.exit(1)
    print("  ✓ 語言列 x1，三語 link 齊全")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with io.open(OUT, "w", encoding="utf-8", newline="") as f:
        f.write(s)

    print(f"\n[OK] {OUT}")
    print(f"     HTML 文案 {applied} 條 + category href {len(CAT_HREF)} 條 + JS 字串 {js_done} 條")
    print(f"     大小 {orig_len:,} → {len(s):,}  (+{len(s)-orig_len:,})")
    print(f"     <style> byte-identical ✓")


if __name__ == "__main__":
    main()