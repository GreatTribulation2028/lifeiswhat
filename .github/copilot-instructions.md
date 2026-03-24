# Copilot Instructions for lifeiswhat

## 項目概述
這是一個以聖經末世預言為主題的靜態網站項目，旨在透過死亡數據和生死議題，循序漸進引導訪者思考生命意義，最終連繫到福音。

## 核心流程
index.html (死亡數字) → monitor03E.html (生死記錄儀) → GoodNews.html (福音旅程)

## 語言和風格
- 使用**香港式書面語**（非廣東話口語，非大陸普通話）
- 語氣溫和、反思，不責備
- 適合 TTS 語音朗讀
- 聖經引用必須使用**和合本**原句
- 「神」字前後需空格

## 神學核心
- 字句 vs 精意：從知識進入愛
- 反對 OSAS（一次得救永遠得救）
- 強調持守、警醒、忍耐到底
- 以愛為本，不攻擊不批判

## 頁面設計原則
- 深色背景（#030405），科技感風格
- 粒子背景動畫
- 漸進引導，不直接推送福音
- 理解人性會本能抗拒信仰內容

## 重要外部資源 URL
- 福音橋 2025（普通話）: https://e.pcloud.link/publink/show?code=XZnHDNZwlvsOG27VGVYCpQrC8xTIylamRK7
- 福音橋（廣東話）: https://e.pcloud.link/publink/show?code=XZh44AZ3cuBmAxfsw79ndttp2rUzhHhlW8X
- 五色福音: https://flossy-dish-cfd.notion.site/01-the-Good-News-for-us-2fcf133f651f80a692c9f98ddc7630e3
- 最後一次狼來了: https://e.pcloud.link/publink/show?code=XZIUPEZSxz3jHIx6ykIwUKptmbOTL7VfvMV
- 永恆的婚誓: https://e.pcloud.link/publink/show?code=XZvUaNZT9PeIugWINRO7QN05ftGC7LHFhlX
- pCloud 聖經資訊: https://e.pcloud.link/publink/show?code=kZt8zaZd7iPCbuRK7mXuE6Lg4fjEJ933Sr7

## 數據檔案
- `data_2021.js` ~ `data_2027.js`: 年度新聞數據
- `data_today.js`: 今日數據
- `classify_rules.json`: 新聞分類規則

## 禁止事項
- 不要注入 iframe-highlight-injector 腳本
- 不要創建「是巧合」頁面
- 不要創建「今日焦點」區塊（除非有 RSS 自動更新）
- 不要創建獨立的七年時間軸頁面（已有 timeline04.html）
- 不要碎片化用戶需求
