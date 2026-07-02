---
name: OTAエクスポートのヘッダー提供 / OTA export header donation
about: 認識されなかった予約エクスポートの「ヘッダー行だけ」を共有して、対応フォーマットを増やすための協力 / Share ONLY the header row of an unrecognized OTA export so we can support more formats
title: "[ota-header] "
labels: ota-header, enhancement
---

<!--
ご協力ありがとうございます！ Booking.com・楽天バケーションステイ・Agoda・PMS
などのエクスポート列構成は公開資料がなく、皆さんのヘッダー提供が対応精度を
直接向上させます。

⚠️ 絶対ルール / HARD RULE:
貼ってよいのは「ヘッダー行（1行目）だけ」です。2行目以降（ゲスト氏名・
予約番号・金額などの実データ）は1行たりとも貼らないでください。
Paste ONLY the header row (line 1). Never paste any data rows — no guest
names, confirmation codes, or amounts, not even one sample row.
-->

## OTA / システム名 / OTA or system name

<!-- 例: Booking.com エクストラネット, 楽天バケーションステイ, Agoda(YCS), Beds24, AirHost など -->

## エクスポートまでの画面操作 / How you exported it (click path)

<!-- 例: エクストラネット > 予約 > 「ダウンロード」ボタン > CSV を選択 -->

## ファイル形式・言語 / File format & locale

- 形式 / Format: <!-- csv / xlsx / tsv -->
- 画面の言語設定 / Account language: <!-- 日本語 / English / ... -->
- 文字コード・改行（わかれば）/ Encoding & line endings (if known): <!-- UTF-8, Shift-JIS, CRLF... -->

## ヘッダー行（1行目のみ！）/ Header row (line 1 ONLY!)

```
（ここにヘッダー行だけを貼り付け / paste the header row only）
```

## 列の意味の補足（任意）/ Notes on ambiguous columns (optional)

<!-- 例: 「人数」列は大人+子どもの合計、乳幼児は別列がない、日付は YYYY/M/D など。
     e.g. the "Guests" column is adults+children combined; dates are YYYY/M/D. -->

## 確認 / Confirmation

- [ ] ヘッダー行（1行目）のみで、ゲストの実データを1行も含めていません /
      I pasted the header row only — zero data rows, zero guest data
