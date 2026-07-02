# 民泊 定期報告スキル（minpaku-teiki-hokoku）

**Minpaku Teiki-Hokoku — an Agent Skill that prepares Japan's bi-monthly vacation-rental report (住宅宿泊事業法14条) from your reservation data. You review, you file.**

住宅宿泊事業（新法民泊）の**隔月の定期報告**を、データ集めから提出用ファイルまで丸ごと準備するAgent Skillです。Claude（Cowork / Claude Code / claude.ai）にフォルダを共有して「定期報告を作って」と話しかけると、スキルがあなたの物件・予約データについて1問ずつインタビューし、Airbnbなど各サイトの予約データを集計して、**確認用Excel（物件ごと）**、**民泊制度運営システムの一括アップロード用CSV**、**画面入力用のクリックガイド**を生成します。国籍の分類は自動で行い、**どの根拠で分類したか（名簿／フォーム／パスポート／住所ルール／推定）を一人ずつ表示**するので、提出前に自分の目で確認できます。

> **大事なこと**: このスキルは報告の「準備」をするだけです。数字を確認して提出するのは事業者であるあなた自身です。行政書士サービスでも法律助言でもありません。

---

## 目次

- [こんな方のためのスキルです](#こんな方のためのスキルです)
- [なぜ作ったか（費用と時間の話）](#なぜ作ったか費用と時間の話)
- [法的背景（1分で）](#法的背景1分で)
- [インストール](#インストール)
- [クイックスタート](#クイックスタート)
- [必要なデータ](#必要なデータ)
- [出力されるもの](#出力されるもの)
- [プライバシーと個人情報の扱い（必読）](#プライバシーと個人情報の扱い必読)
- [他の方法との比較](#他の方法との比較)
- [作者について](#作者について)
- [免責事項と未確認事項](#免責事項と未確認事項)
- [スクリーンショット](#スクリーンショット)
- [コントリビュート](#コントリビュート)
- [リポジトリ構成（開発者向け）](#リポジトリ構成開発者向け)
- [English](#english)

---

## こんな方のためのスキルです

**対象になる方:**

- **届出番号（第M＋数字9桁＋号）を持つ住宅宿泊事業者**で、偶数月15日の定期報告を自分（または家族・スタッフ）で提出している方
- 複数のOTAアカウント・複数物件を運営していて、集計が毎回つらい方
- Macユーザー（国土交通省の無料ソフトはWindows専用です）
- 管理会社に運営を委託していても、定期報告だけは自分でやっている方

**このスキルが不要な方:**

- **旅館業許可**（ホテル・旅館・簡易宿所）のみで運営している方 — 旅館業にこの隔月報告義務はありません
- **特区民泊（国家戦略特区の認定）**のみの方 — 特区民泊はこのMLIT定期報告の対象外です（自治体からの求めに応じた報告など、別の制度に従います）
- PMSや管理会社が定期報告の作成・提出まで完全に代行してくれている方（ただし、委託しても報告義務そのものは事業者に残ります。また、主要PMSに「ワンクリック定期報告出力」があるかは未確認です）

届出住宅が1件もない場合、スキルは最初の質問の段階（初回セットアップ中）で正直にそう伝えて停止します。旅館業・特区民泊が混ざっている場合でも、届出済証や自治体の公表一覧での確認を挟みながら報告対象の物件を選別します — スキルが物件の制度区分を推測で決めることはありません。

## なぜ作ったか（費用と時間の話）

定期報告を行政書士に依頼すると、相場は**1報告・1物件あたり33,000円**です。年6回の報告なので、例えば物件6件なら**年間およそ119万円**。自分でやれば無料ですが、複数アカウントのCSVを集めて、キャンセルを除き、期間をまたぐ予約を按分して、ゲスト一人ずつの国籍を22分類に振り分けて…という作業が2ヶ月ごとに発生します。

このスキルは、その「毎回同じなのに毎回つらい」部分を肩代わりします。あなたに残るのは、**出来上がった数字を確認して、ポータルに提出する**ことだけです。

## 法的背景（1分で）

- 住宅宿泊事業者は、**届出住宅ごとに**、宿泊させた日数などを定期的に都道府県知事等へ報告する義務があります（**住宅宿泊事業法第14条**、報告事項と期限は**施行規則第12条**）。
- **期限は偶数月の15日**。直前の2ヶ月分を報告します:

  | 提出期限 | 対象期間 |
  |---|---|
  | 2月15日 | 12月・1月 |
  | 4月15日 | 2月・3月 |
  | 6月15日 | 4月・5月 |
  | 8月15日 | 6月・7月 |
  | 10月15日 | 8月・9月 |
  | 12月15日 | 10月・11月 |

- 報告する項目は4つ: **①宿泊日数 ②宿泊者数 ③延べ宿泊者数 ④国籍別の宿泊者数の内訳**（22の固定分類）。
- 宿泊実績がゼロの期間も**0件報告が必要**です（届出が受理された日から）。
- 報告をしない、または虚偽の報告をした場合は**30万円以下の罰金**の対象です（法第76条第3号）。だからこそ、このスキルは推定した値に必ず「推定」と印を付け、提出前の本人確認をワークフローの必須ステップにしています。
- 京都市など、**条例で報告項目を上乗せしている自治体**があります（京都市: 苦情の件数・日時・内容・対応状況）。スキルは京都市に対応済み。その他の自治体は[観光庁の自治体窓口一覧](https://www.mlit.go.jp/kankocho/minpaku/municipality.html)で確認するよう案内します。

## インストール

### 前提

- **Claude Cowork**（推奨）: 有料プラン（Pro / Max / Team / Enterprise）＋ Claude Desktopアプリ（macOS / Windows、Linuxはベータ）が必要です。
- claude.aiのチャットやClaude Codeでも動作します。
- 設定の **Capabilities → 「Code execution and file creation」（コード実行とファイル作成）** がオンになっていること（通常は初期状態でオン）。

> ⚠️ **やってはいけないインストール方法**: スキルのフォルダをパソコンの `~/.claude/skills/` にコピーする方法は**Coworkやclaude.aiチャットでは動きません**（Claude Code専用の方法です）。必ず下のいずれかの方法を使ってください。

### 方法0（いちばん簡単・おすすめ）: リポジトリURLを貼るだけ（動作確認中）

> 🧪 **この方法はCoworkでの動作確認中です。** うまくいかない場合は方法Aを使ってください。

1. Claude デスクトップアプリで Cowork を開き、作業用フォルダ（例: `書類/民泊報告`）を選びます。
2. 次の1行を貼り付けて送信します:

   > 「https://github.com/lephuocdai/minpaku-teiki-hokoku の内容をこのフォルダに取り込んで（ZIPを取得して展開）、minpaku-teiki-hokoku/SKILL.md の手順に従って民泊の定期報告の準備を始めてください。」

3. あとは質問に答えるだけです。次回以降はフォルダにファイルが残っているので、「定期報告の続きをやって」と言うだけでOKです。

この方法では何も「インストール」されません — Claudeが作業フォルダに置かれた手順書（`minpaku-teiki-hokoku/SKILL.md`）に従うだけなので、スキルのセッション内インストールにまつわる既知の問題も避けられます。スキルを毎回のセッションで自動的に使えるようにしたい方は、下の方法A・Bを使ってください。

### 方法A: ZIPをアップロード（スキルとして常設したい方向け・確実）

1. このリポジトリの **[Releases](../../releases)** ページを開き、**「Assets」欄**にある `minpaku-teiki-hokoku.zip` をダウンロードします（「Assets」が折りたたまれている場合はクリックして開いてください）。
   - ⚠️ **間違えやすいダウンロードが2つあります。** ①リポジトリのトップにある緑色の **「Code」ボタン →「Download ZIP」は使わないでください**。②Releasesページの「Assets」欄に自動表示される **「Source code (zip)」「Source code (tar.gz)」もダウンロードしないでください**。どちらもリポジトリ全体を包んだZIPで、**スキルとして認識されず、アップロード時にエラーになります**。正解は `minpaku-teiki-hokoku.zip` という名前のファイルだけです。
2. Claude Desktop（またはclaude.ai）を開き、左サイドバーの **「Customize（カスタマイズ）」** をクリックします。
3. **「Skills（スキル）」** タブ → **「＋」** → **「Upload a skill（スキルをアップロード）」** を選びます。
4. ダウンロードしたZIPファイルを選択します。
5. 確認: アップロード完了後、同じ **Customize → Skills の一覧に `minpaku-teiki-hokoku` が表示されていれば成功**です（いま開いている画面で確認できます）。チャットの入力欄で「/」と入力して一覧に出るかどうかでも確認できますが、この表示は環境により異なる可能性があります（動作確認中）。

> 📦 ZIPを自分で作り直す場合の注意: ZIPの**直下**に `minpaku-teiki-hokoku` フォルダ（中に `SKILL.md`）が来るように圧縮してください。**フォルダ名とスキル名が一致していないとアップロードに失敗します。** Releasesに置いてあるZIPはこの形になっています。

### 方法B: マーケットプレイスURLを追加（動作確認中）

> 🧪 **この方法はCoworkでの動作確認中です。** うまくいかない場合は方法Aを使ってください。

1. Coworkの **「Customize（カスタマイズ）」** → **「Plugins（プラグイン）」** タブを開きます。
2. **「＋」→「Add marketplace（マーケットプレイスを追加）」** を選びます。
3. `https://github.com/lephuocdai/minpaku-teiki-hokoku` を貼り付けて追加します。
4. 一覧から `minpaku-teiki-hokoku` をインストールします。

### Claude Codeを使っている方

```
/plugin marketplace add lephuocdai/minpaku-teiki-hokoku
/plugin install minpaku-teiki-hokoku@minpaku-teiki-hokoku
```

## クイックスタート

1. パソコンに**作業用フォルダ**を1つ作ります（例: `定期報告`）。
2. Coworkでそのフォルダを共有し（「フォルダで作業」）、こう話しかけます:

   > **「定期報告を作って」**

3. あとはスキルがインタビューしてくれます。初回だけ、物件の届出番号・自治体・OTAアカウントなどを1問ずつ聞かれます（回答はフォルダ内の設定ファイルに保存され、**2回目以降はデータの確認だけ**になります）。
4. 案内に従って、各OTAの予約エクスポートや宿泊者名簿をフォルダに入れます。
5. スキルが集計し、**確認用Excel**を出し、ゲストごとの国籍判定根拠の一覧を**チャットに表示**します。数字と根拠を**自分の目で確認**してください。
6. 問題なければ、**アップロード用CSV**と**画面入力ガイド**が出来上がります。[民泊制度運営システム](https://www.mlit.go.jp/kankocho/minpaku/)にご自身のIDでログインして提出してください（CSVの場合は、まず1行だけのテストアップロードを推奨 — 理由は[未確認事項](#免責事項と未確認事項)参照）。

## 必要なデータ

すべて**ファイルとして作業フォルダに入れる**だけです（スキル側が取りに行くことはありません）。

| データ | 必須? | 備考 |
|---|---|---|
| OTAの予約エクスポート（Airbnb CSVなど） | ✅ | Airbnbの取得手順は同梱ガイドに記載。Booking.com・楽天バケーションステイ・Agoda・PMSのエクスポートも読み込みます（列構成は初回に確認ゲートあり） |
| 宿泊者名簿（Excel / スプレッドシートからダウンロードした.xlsx） | 推奨 | 国籍の最優先ソース。**名簿がない方には法定様式のテンプレートを同梱**しています（3年保存義務があります） |
| パスポート写しのフォルダ | 任意 | 外国人非居住者ゲストについては法律上保存が義務。国籍判定の通常ソースの一つとして扱います |
| チェックインフォーム等の回答 | 任意 | 国籍ソースとして利用 |
| 苦情ログ（京都市のみ） | 京都市は✅ | ない場合はスキルがログの雛形を作ります |
| Gmailの予約確認メール | 代替 | CSVが取れない共同ホストなどの最終手段。メールを転送・保存してフォルダへ |

## 出力されるもの

各報告期間ごとに、作業フォルダ内へ:

- **確認用Excel（届出住宅ごとに1ファイル）** — カレンダー形式の宿泊日、22分類の国籍表、明細（ゲストごとの国籍と、その値がどの入力から来たかの記録）、集計サマリー。**どの根拠で国籍を判定したか（名簿／フォーム／パスポート／住所ルール／推定）の一人ずつの一覧は、確認ステップでチャットに表示**されます
- **一括アップロード用CSV**（Shift-JIS・CRLF、民泊制度運営システムの仕様）
- **画面入力用クリックガイド** — Web画面に手入力する場合の、画面の並び順どおりの数字一覧と注意点（期間プルダウンの初期値の罠など）
- **検証レポート** — 合計の整合チェック、重複予約の検出、180日ルールの進捗（120泊・170泊で警告）など

## プライバシーと個人情報の扱い（必読）

宿泊者名簿とパスポート写しは**個人情報**です。特に**旅券番号は個人情報保護法上の「個人識別符号」**にあたります。詳細は同梱の `minpaku-teiki-hokoku/references/privacy-appi.md` にまとめてありますが、最低限:

1. **Claudeの設定で「Improve Claude」（モデル改善へのデータ提供）をオフ**にしてください（Settings → Privacy）。ゲストデータをAIの学習に提供しない設定です（安全性審査でフラグされた会話等の例外あり。詳細は `minpaku-teiki-hokoku/references/privacy-appi.md`）。
2. **ゲストデータをGitHubなどに絶対にアップロードしない**でください（このリポジトリへのIssueにも貼らない — テンプレートが「ヘッダー行のみ」と念を押すのはこのためです）。
3. 名簿・パスポート写しには**3年間の保存義務**があります（名簿は施行規則第7条、パスポート写しはガイドライン〔施行要領〕により名簿とともに保存）。報告が終わっても削除しないでください。
4. 海外事業者のサービスに個人データを扱わせることは、個人情報保護法の**外国にある第三者への提供（法28条）**の論点に関わります。個人情報保護委員会の2023年の生成AIに関する注意喚起も含め、`privacy-appi.md` を一読の上、ご自身の判断で利用してください。

## 他の方法との比較

正直な比較です。それぞれに合理的な選択の場面があります。

| 方法 | 費用 | 得意なこと | 弱点 |
|---|---|---|---|
| **国交省の電子宿泊者名簿ソフト** | 無料 | 公式。名簿から報告CSVを生成 | **Windows 10/11専用（Mac不可）**。名簿をこのソフトの中で管理し続ける前提 |
| **Beds24の無料スプレッドシート** | 無料 | Airbnb CSV→アップロード用CSV変換の実績あるツール | **国籍は全ゲスト手動確認**。1リスティングずつ処理、キャンセルは手動削除、Shift-JIS変換も手動、計18ステップの手順 |
| **行政書士に依頼** | **33,000円／報告／物件** | 作業をおまかせできる専門家 | 費用。物件×年6回で積み上がる。**報告義務そのものは事業者に残り**、提出も事業者本人のID・名義で行う運用（MLIT公式） |
| **PMS・運営代行** | 月額1万〜10万円超 | 運営全体を委託できる | ワンクリックの定期報告出力を持つ主要PMSは**未確認**。委託しても報告義務は事業者に残る |
| **このスキル** | 無料（Claudeの有料プランは必要） | Mac/Windows両対応、複数アカウント・複数物件、キャンセル・期間またぎ・ゼロ報告のルールを実装済み、国籍を自動分類し**根拠つきで提示** | 最終確認と提出はあなた自身。AIの推定は必ず検証が必要 |

## 作者について

東京で6件の届出住宅を運営し、毎回この定期報告を提出している民泊オーナーが作りました。このスキルの集計ロジックは、作者自身が毎回の提出に使っているものと同じです。

## 免責事項と未確認事項

**免責事項:**

- このスキルは**法律助言でも行政書士サービスでもありません**。報告データの「準備」を支援するツールです。
- **提出前にすべての数字を確認する責任は事業者にあります。** 虚偽報告は罰則の対象であり、AIの出力には誤りが含まれえます。スキルが「推定」と印を付けた国籍は特に確認してください。
- 提出（ポータルへのログインとアップロード／入力）は事業者本人が行います。管理を委託していても報告義務は事業者に残ります。

**未確認事項（正直に書きます）:**

- **Airbnb以外のOTAエクスポートの列構成**は公開資料がなく、完全には検証できていません。未知の形式に出会ったときは、スキルが列の対応づけを提示して**あなたの確認を待ってから**処理します。[ヘッダー行の提供](../../issues/new?template=ota_header_donation.md)にご協力いただけると精度が上がります。
- **一括アップロードCSVの正確な仕様は、公式マニュアル2冊の間で記述が矛盾しています。** スキルは操作手順書v1.7の形式を既定とし、もう一方の形式も選べますが、**初回は必ず1行だけのテストアップロード**をしてください（行ごとにエラーが返るので安全に試せます）。
- **京都市以外の自治体の上乗せ条例**は網羅調査していません（千代田区などにも独自の記録義務があります）。必ず[自治体窓口一覧](https://www.mlit.go.jp/kankocho/minpaku/municipality.html)から自分の自治体のルールを確認してください。
- **方法0（リポジトリURLの取り込み）と方法B（マーケットプレイスURL）のCoworkでの動作**は確認中です。確認が取れ次第このREADMEを更新します。

## スクリーンショット

<!-- TODO(post-cowork-test): capture and embed the following screenshots after the hands-on Cowork test.
  1. Customize > Skills > Upload a skill (方法AのZIPアップロード画面)
  2. Cowork で「/」を入力してスキルが一覧に出ている画面
  3. 「定期報告を作って」のインタビュー会話例（synthetic data のみ！）
  4. 確認用Excel（国籍の根拠列が見える状態、synthetic data）
  5. クリックガイドの例
-->

📷 準備中です（Coworkでの動作確認後に追加します）。

## コントリビュート

- **バグ報告**: [バグ報告テンプレート](../../issues/new?template=bug_report.md)からお願いします。**ゲストの個人情報や実際の届出番号は絶対に含めないでください。**
- **OTAエクスポートのヘッダー提供**: あなたの使っているOTAのエクスポートが認識されなかったら、[ヘッダー行だけを共有](../../issues/new?template=ota_header_donation.md)してください（データ行は1行も不要です）。対応フォーマットを増やす一番の近道です。
- Pull Request歓迎です。`examples/` に入れてよいのは合成データのみです。

## リポジトリ構成（開発者向け）

```
minpaku-teiki-hokoku/            # スキル本体（Releases ZIPのルート）
├── SKILL.md                     # オンボーディングと実行手順
├── scripts/
│   ├── generate_report.py       # 決定論的な集計エンジン
│   └── nationality_map.py       # 国籍文字列 → 22分類
├── references/                  # 法的根拠・OTA手順・ポータル操作・京都市・プライバシー
└── assets/
    └── guest-registry-template.xlsx  # 宿泊者名簿テンプレート
examples/                        # 合成データのサンプル一式
.claude-plugin/marketplace.json  # プラグインマーケットプレイス定義
```

集計エンジンは単体でも実行できます（依存はopenpyxlのみ）:

```
python3 scripts/generate_report.py <作業フォルダ> <期間>
# 期間の形式: YYYY-MM_YYYY-MM（連続する2ヶ月, 例 2026-04_2026-05）
```

（このコマンドはスキルフォルダ `minpaku-teiki-hokoku/` の中で実行する想定です。リポジトリ直下からは `python3 minpaku-teiki-hokoku/scripts/generate_report.py examples 2026-04_2026-05` のように実行してください — `examples/README.md` と同じ形です。）

入力は `<作業フォルダ>/minpaku-config.yaml` と `<作業フォルダ>/<期間>/normalized_reservations.csv`（任意で `nationality-overrides.csv`・`kujo-log.csv`）。出力は `<作業フォルダ>/<期間>/output/` に `report_data.json`、届出番号ごとの確認用xlsx、`teiki-hokoku-upload_<期間>.csv`（Shift-JIS・CRLF）、`click-guide_<期間>.md`、`validation_<期間>.md` が生成されます。LLMは判断が必要な部分（列の対応づけ・国籍推定・対話）だけを担当し、**数を数えるのはすべてこのスクリプト**です。

## ライセンス

[MIT](LICENSE)

---

# English

## What this is

**Minpaku Teiki-Hokoku** is an Agent Skill that prepares Japan's **bi-monthly vacation-rental report** (定期報告) required of notified minpaku operators under the Private Lodging Business Act (住宅宿泊事業法, Art. 14). Share a folder with Claude (Cowork / Claude Code / claude.ai), say **"定期報告を作って"** (or "prepare my minpaku report"), and the skill interviews you step by step, aggregates your reservation exports (Airbnb and other OTAs), and produces: a **review Excel workbook per property**, a **bulk-upload CSV** for the official 民泊制度運営システム portal, and a **click-by-click guide** for the portal's web form. Nationality classification is automatic, and the skill presents a **per-guest provenance table** (registry / check-in form / passport copy / residence rule / inferred) in the chat review step — the review workbook records each guest's nationality and which input it came from — so you can verify everything before filing.

> **Important**: this skill PREPARES the report. **You** — the notified operator — review the figures and file them. It is not a legal service and not an administrative-scrivener (行政書士) service.

## Who it's for — and who doesn't need it

**For you if:**

- You hold a 届出番号 (notification number, format 第M+9 digits+号) and file the bi-monthly 定期報告 yourself
- You juggle multiple OTA accounts and/or multiple properties
- You use a Mac (MLIT's free desktop tool is Windows-only)

**Not for you if:**

- You operate only under a **ryokan-gyo license** (旅館業) — no bi-monthly MLIT report applies
- You operate only **tokku minpaku** (特区民泊, National Strategic Zone certification) — a different reporting regime applies
- Your PMS or management company already prepares and files the report end-to-end (note: the legal duty still stays with the operator even when management is delegated, and we could not confirm any major PMS ships a one-click 定期報告 export)

If you have zero M-number properties, the skill says so honestly during onboarding and stops. Mixed portfolios (M-number + ryokan-gyo + tokku) are sorted through a confirmation gate (M-number check, 届出済証 verification) — the skill never guesses a property's regime.

## Why it exists

Outsourcing this report to a 行政書士 (administrative scrivener) costs around **¥33,000 per report per property**. With six filings a year, a six-property operator pays roughly ¥1.19M/year. Doing it yourself is free but means, every two months: merging CSVs across accounts, dropping cancellations, splitting stays that straddle the reporting period, and classifying every guest into 22 fixed nationality categories. This skill takes over that repetitive part and leaves you the part that must stay human: **verifying and filing**.

## Legal background in one minute

- Notified operators must report, **per notified property**, under **Art. 14 of the Act**; the items and schedule are set by **Art. 12 of the Enforcement Regulations** (施行規則).
- **Deadline: the 15th of every even month**, covering the preceding two months (e.g. June 15 → April + May).
- Four items: **① 宿泊日数 (days occupied) ② 宿泊者数 (number of guests) ③ 延べ宿泊者数 (guest-nights) ④ nationality breakdown** across 22 fixed categories.
- Periods with zero stays still require a **zero report**, starting from the date your notification was accepted.
- Failing to file, or filing falsely, is punishable by a **fine of up to ¥300,000** (Art. 76 item 3). This is exactly why the skill labels every inferred value as inferred and makes pre-submission review a mandatory workflow step.
- Some municipalities **add report items by ordinance** — Kyoto City (complaints log: count, date/time, content, handling) is fully supported; for others the skill points you to the [MLIT municipality directory](https://www.mlit.go.jp/kankocho/minpaku/municipality.html).

## Install

### Prerequisites

- **Claude Cowork** (recommended): paid plan (Pro / Max / Team / Enterprise) + Claude Desktop app (macOS / Windows; Linux beta). The skill also works in claude.ai chat and Claude Code.
- Settings → Capabilities → **"Code execution and file creation"** enabled (default on).

> ⚠️ **Anti-pattern**: copying the skill folder into `~/.claude/skills/` does **NOT** work in Cowork or claude.ai chat — that path is Claude Code-only. Use one of the paths below.

### Path 0 — Paste the repo URL (simplest, recommended; being verified)

> 🧪 **This path is still being verified on Cowork.** If it fails, use Path A.

1. Open Cowork in the Claude desktop app and pick a working folder (e.g. `Documents/minpaku-report`).
2. Paste this one line and send it:

   > "Download https://github.com/lephuocdai/minpaku-teiki-hokoku into this folder (fetch the ZIP and extract), then follow minpaku-teiki-hokoku/SKILL.md to prepare my minpaku bi-monthly report."

3. Answer the questions. On later runs the files are already in the folder — just say "continue my 定期報告".

Nothing gets "installed" with this path — Claude simply follows the instruction file placed in your folder, which also sidesteps the known rough edges of in-session skill installation. If you want the skill auto-available in every session instead, use Path A or B below.

### Path A — Upload the ZIP (reliable; makes the skill available in every session)

1. On the **[Releases](../../releases)** page, download `minpaku-teiki-hokoku.zip` from the **Assets** section (click "Assets" open if it is collapsed).
   - ⚠️ **Two look-alike downloads will NOT work.** Do not use the green **"Code" → "Download ZIP"** button on the repo top page, and do not download the auto-generated **"Source code (zip)" / "Source code (tar.gz)"** entries listed under Assets. Both wrap the whole repository and are **rejected by the skill upload with a confusing error**. The only correct file is the one literally named `minpaku-teiki-hokoku.zip`.
2. In Claude Desktop (or claude.ai), open **Customize** in the left sidebar.
3. **Skills** tab → **"+"** → **"Upload a skill"**.
4. Select the downloaded ZIP.
5. Verify: after the upload, `minpaku-teiki-hokoku` should be **listed on the same Customize → Skills screen** — that is the success signal. (Typing "/" in the chat box may also list it, but that UI is still being verified.)

> 📦 If you re-zip it yourself: the `minpaku-teiki-hokoku` folder (containing `SKILL.md`) must sit at the **root of the ZIP**, and the **folder name must equal the skill name** or the upload fails. The Releases ZIP is already packaged correctly.

### Path B — Add the marketplace URL (being verified)

> 🧪 **This path is still being verified on Cowork.** If it fails, use Path A.

1. Cowork → **Customize** → **Plugins** tab.
2. **"+" → "Add marketplace"**.
3. Paste `https://github.com/lephuocdai/minpaku-teiki-hokoku`.
4. Install `minpaku-teiki-hokoku` from the list.

### Claude Code users

```
/plugin marketplace add lephuocdai/minpaku-teiki-hokoku
/plugin install minpaku-teiki-hokoku@minpaku-teiki-hokoku
```

## Quick start

1. Create one **working folder** on your computer.
2. Share it with Cowork ("Work in a folder") and say: **"定期報告を作って"** — or ask in English; the skill converses in your language.
3. First run only: the skill interviews you (notification numbers, municipality, OTA accounts…), one question at a time, and saves your answers to a config file in the folder. **Later runs skip straight to the data.**
4. Drop your OTA reservation exports and guest registry into the folder as instructed.
5. The skill computes everything, produces a **review Excel**, and shows a per-guest nationality provenance table in the chat — check the figures and the provenance **yourself**.
6. Once you're satisfied, take the **upload CSV** and/or **click guide** and file at the [民泊制度運営システム portal](https://www.mlit.go.jp/kankocho/minpaku/) with your own login. For CSV, do a **1-row test upload first** (see [Unverified items](#disclaimer--unverified-items)).

## What data it needs

Everything enters as **files you place in the shared folder** (the skill never fetches your accounts):

- OTA reservation exports (Airbnb CSV first-class; Booking.com / Rakuten Vacation Stay / Agoda / PMS exports with a confirm-the-mapping gate on first contact)
- Guest registry (宿泊者名簿) as .xlsx — the top nationality source; **a legally compliant template is bundled** if you don't keep one (3-year retention duty applies)
- Passport-copy folder (legally required for foreign non-resident guests; a normal nationality source here)
- Check-in form/survey answers (optional)
- Complaints log (Kyoto City only; the skill scaffolds one if missing)
- Gmail booking confirmations as a fallback when no CSV export is available

## What you get

Per reporting period: a **review .xlsx per notified property** (calendar of occupied dates, 22-category nationality table, a detail sheet recording each guest's nationality and its input source, summary), the **portal bulk-upload CSV** (Shift-JIS, CRLF), a **click guide** for manual web-form entry (in exact on-screen order, including the period-pulldown default trap), and a **validation report** (consistency checks, duplicate detection, 180-day cap progress with 120/170-night warnings). The per-guest provenance table (registry / form / passport / residence rule / inferred) is shown in the chat review step.

## Privacy (read this)

Guest registries and passport copies are personal data; **passport numbers are 個人識別符号 (individual identification codes) under Japan's APPI**. Full guidance lives in `minpaku-teiki-hokoku/references/privacy-appi.md`. Minimum rules:

1. **Turn OFF "Improve Claude"** in Claude's privacy settings so guest data is not used for model training (the opt-out has narrow carve-outs — e.g. safety-flagged conversations may still be used; see `minpaku-teiki-hokoku/references/privacy-appi.md`).
2. **Never upload guest data to GitHub** — including issues on this repo (our templates insist on header rows only).
3. Registries and passport copies carry a **3-year retention duty** (the registry under Enforcement Regulations Art. 7; passport copies kept with the registry per the MLIT guideline / 施行要領) — do not delete them after filing.
4. Processing personal data through a foreign provider touches APPI's **cross-border transfer rules (Art. 28)** and the PPC's 2023 cautionary statement on generative AI — read the appendix and decide for yourself.

## Honest comparison

| Option | Cost | Strong at | Weak at |
|---|---|---|---|
| MLIT's free 電子宿泊者名簿 desktop tool | Free | Official; generates the report CSV from its registry | **Windows 10/11 only — no Mac**; registry must live inside the tool |
| Beds24's free Google Sheets generator | Free | Proven Airbnb-CSV→upload-CSV conversion | **Nationality is 100% manual per guest**; one listing at a time; manual cancellation deletion and Shift-JIS conversion; ~18 manual steps |
| 行政書士 (scrivener) | **¥33,000 / report / property** | A professional does the work for you | Cost compounds: properties × 6 filings/year; **the legal duty still stays with the operator**, and submission uses the operator's own portal ID per MLIT |
| PMS / management company | ¥10k–100k+/month | Full operational delegation | One-click 定期報告 export **unconfirmed** for major PMSs; the legal duty stays with you |
| **This skill** | Free (paid Claude plan required) | Mac/Windows, multi-account & multi-property, cancellation / period-straddling / zero-report rules encoded, automatic nationality classification **with provenance** | You still verify and file; AI inference must be checked |

## About the author

Built by a Tokyo minpaku operator who runs six notified properties and files this exact report every cycle. The counting logic in this repo is the same logic the author uses for their own filings.

## Disclaimer & unverified items

- **Not legal advice, not a scrivener service.** The skill prepares data; the operator verifies every figure and files. False reporting is criminally sanctioned, and AI output can contain errors — check anything labeled "inferred".
- **Unverified, stated honestly:**
  - **Non-Airbnb OTA export schemas** are publicly undocumented; on an unfamiliar format the skill proposes a column mapping and **waits for your confirmation**. [Donating header rows](../../issues/new?template=ota_header_donation.md) hardens the parsers.
  - **The exact bulk-upload CSV serialization conflicts between two official manuals.** The skill defaults to the 操作手順書 v1.7 format (the other is selectable) — **always do a 1-row test upload first**; the portal returns per-row errors, so this is safe.
  - **Municipal add-on ordinances beyond Kyoto** have not been exhaustively surveyed (Chiyoda-ku has extra record duties, others may too) — check your municipality via the [MLIT directory](https://www.mlit.go.jp/kankocho/minpaku/municipality.html).
  - **Path 0 (repo-URL import) and Path B (marketplace URL) are still being verified on Cowork**; this README will be updated once tested hands-on.

## Screenshots

📷 Coming after the hands-on Cowork test. <!-- TODO(post-cowork-test): same capture list as the Japanese section. -->

## Contributing

Bug reports via the [bug template](../../issues/new?template=bug_report.md) (no guest data, mask your 届出番号). Unrecognized OTA export? [Share the header row only](../../issues/new?template=ota_header_donation.md). PRs welcome — synthetic data only in `examples/`.

## For developers

The deterministic engine runs standalone (openpyxl is the only dependency):

```
python3 scripts/generate_report.py <workdir> <period>   # period: YYYY-MM_YYYY-MM, e.g. 2026-04_2026-05
```

(Run this from inside the `minpaku-teiki-hokoku/` skill folder. From the repo root, use the full path instead: `python3 minpaku-teiki-hokoku/scripts/generate_report.py examples 2026-04_2026-05` — same form as `examples/README.md`.)

It reads `<workdir>/minpaku-config.yaml` and `<workdir>/<period>/normalized_reservations.csv` (plus optional `nationality-overrides.csv` and `kujo-log.csv`) and writes into `<workdir>/<period>/output/`: `report_data.json`, one review xlsx per notification number, `teiki-hokoku-upload_<period>.csv` (Shift-JIS/CRLF), `click-guide_<period>.md`, and `validation_<period>.md`. The LLM handles judgment only (column mapping, nationality inference, dialogue); **all counting is done by the audited script**.

## License

[MIT](LICENSE)
