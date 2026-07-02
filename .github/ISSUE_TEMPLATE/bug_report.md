---
name: バグ報告 / Bug report
about: スキルが正しく動かなかったときの報告 / Report incorrect behavior of the skill
title: "[bug] "
labels: bug
---

<!--
⚠️ 個人情報を貼らないでください / DO NOT PASTE GUEST DATA
- ゲストの氏名・連絡先・予約確認コード・パスポート情報は絶対に含めないでください。
- 届出番号は必ずマスクしてください（例: 第M13xxxxxxx号）。
- CSVの内容を共有する場合は「ヘッダー行（1行目）のみ」にしてください。
- Never include guest names, contact info, confirmation codes, or passport data.
- Mask your 届出番号 (e.g. 第M13xxxxxxx号). If sharing CSV content, share the
  HEADER ROW ONLY.
-->

## 何が起きたか / What happened

（できるだけ具体的に。エラーメッセージがあればそのまま貼ってください）

## 期待した動作 / What you expected

## 実行環境 / Environment

- [ ] Claude Cowork（デスクトップアプリ）
- [ ] Claude Code
- [ ] claude.ai チャット
- OS: <!-- macOS / Windows / Linux -->
- インストール方法 / Install method: <!-- Releases ZIP / marketplace URL / Claude Code plugin -->

## どの段階で起きたか / At which step

- [ ] インストール / Install
- [ ] 初回セットアップ（物件・リスティングの質問）/ Onboarding interview
- [ ] 予約データの読み込み・変換 / Reading or normalizing reservation data
- [ ] 集計（スクリプト実行）/ Counting engine
- [ ] 出力（Excel / CSV / 入力ガイド）/ Outputs
- [ ] その他 / Other

## 対象期間 / Reporting period

<!-- 例 / e.g. 2026-04_2026-05 -->

## 入力データの種類 / Input data type

<!-- 例: Airbnb CSV（日本語版）、Booking.com エクスポート、宿泊者名簿xlsx など。
     必要ならヘッダー行（1行目）のみをコードブロックで貼ってください。
     e.g. Airbnb CSV (JP locale). If useful, paste the header row ONLY. -->

```
（ヘッダー行のみ / header row only）
```

## validation レポートの内容 / Contents of the validation report

<!-- 出力フォルダの validation_<期間>.md に警告が出ていた場合、個人情報を
     マスクした上で貼ってください。
     If validation_<period>.md showed warnings, paste them here with any
     personal data masked. -->

## 確認 / Confirmation

- [ ] ゲストの個人情報・実際の届出番号を含めていないことを確認しました /
      I confirm this issue contains no guest data and no real 届出番号
