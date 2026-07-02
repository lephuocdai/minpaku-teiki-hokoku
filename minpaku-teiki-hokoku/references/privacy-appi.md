# プライバシーと個人情報保護（APPI）ガイド

**最終確認日: 2026-07-02。** 本書に書かれた Anthropic のポリシー内容・PPC（個人情報保護委員会）の見解・法令の状況はすべてこの日時点のものです。ポリシーや法令は変わります。重要な判断の前にリンク先の原文を確認してください。

> **これは法的助言ではありません。**
> 本書は、このスキルの設計者（東京の民泊運営者）が「迷ったら保守的に倒す」という方針で整理した実務ガイダンスです。生成AIサービスへの個人データ入力が個人情報保護法上どう扱われるかについて、**確定した行政解釈や判例はまだ存在しません**。ここに書いた整理は「設計上の保守的な前提」であって、法的な結論ではありません。不安がある場合は弁護士・行政書士等の専門家に相談してください。
>
> また、このスキルは報告データを**準備する**道具です。届出・報告を行い、その内容に責任を負うのは常に**事業者（あなた）自身**です。

---

## 1. なぜこの文書を読む必要があるか

定期報告の作業では、ゲストの個人情報を扱います。

- **ゲストの氏名・住所・宿泊日は個人情報**です（個人情報保護法2条1項）。
- **旅券番号（パスポート番号）は「個人識別符号」**です（個人情報保護法施行令1条）。つまりパスポートの画像や番号は、氏名と紐づいていなくても**それ単体で個人情報**です。画像には顔写真も含まれます。
  - 出典: 施行令1条 / 解説: https://www.businesslawyers.jp/practices/274
- 一方で、**提出する定期報告そのものには個人データは一切含まれません**。報告項目は ①宿泊日数 ②宿泊者数 ③延べ宿泊者数 ④国籍別の宿泊者数の内訳 — すべて集計値です。
  - 出典: https://www.mlit.go.jp/kankocho/minpaku/business/host/index.html

つまり、**プライバシー上のリスクは「出力」ではなく「入力」（名簿・予約データ・パスポートの写し）の扱いに集中しています**。本書はその入力側の扱い方を定めます。

なお、国籍という情報それ自体は「要配慮個人情報」には該当しません（PPCガイドライン通則編:「単純な国籍や『外国人』という情報は法的地位であり、それだけでは人種には含まない」）。国籍の集計を作ること自体は特別扱いの必要な処理ではありませんが、入力データに含まれ得る他の情報（後述）には注意が必要です。

## 2. 民泊ホストと個人情報保護法 — このスキルの設計上の前提

以下は、このスキルが「なぜこういう慎重な作りになっているか」の説明です。**保守的な設計方針であり、確定した法解釈ではありません。**

1. **あなた（ホスト）は「個人情報取扱事業者」です。** 2017年5月30日の改正法施行で「5,000件要件」が撤廃されて以来、個人事業主でも、宿泊者名簿（法律上の保存義務があるので民泊ホストは必ず保有しています）を持つ時点で個人情報取扱事業者に該当し、安全管理措置・利用目的の特定・第三者提供の制限などの義務を負います。これは規模によらず該当します（高確度 — PPC FAQ: https://www.ppc.go.jp/all_faq_index/faq1-q1-50/ ）。

2. **PPCは2023年6月2日に生成AIサービス利用への注意喚起を出しています**（ https://www.ppc.go.jp/files/pdf/230602_alert_generative_AI_service.pdf ）。個人情報取扱事業者への要点は2つ:
   - 個人情報を含むプロンプトの入力は、**特定した利用目的の達成に必要な範囲内**であることを十分に確認すること。
   - 本人の同意なく個人データを入力し、それが**応答の生成以外の目的（例: 機械学習）で取り扱われる場合、法違反となる可能性**がある。提供事業者が当該データを「機械学習に利用しないこと等」を十分に確認すること。
   - このスキルの手順で「学習に使う設定をオフにする」「入力を必要最小限にする」ことを求めるのは、この注意喚起に沿うためです。

3. **外国にある第三者への提供（法28条）の論点。** Anthropic は米国の事業者です。日本の個人データを外国の事業者に「提供」する場合、原則として本人への情報提供（国名・その国の制度・講じられる措置）を伴う事前同意、または基準適合体制の確保が必要で、米国は指定国（EEA・英国のみ）ではありません。クラウドサービスへの入力が「提供」に当たらないとする、いわゆる**クラウド例外**（PPC Q&A 7-53 — 番号は二次資料での確認です）が使えるかどうかは、「提供事業者がそのデータを取り扱わない旨が契約で定められていること」が条件です。コンシューマー向け Claude の規約は安全性審査のためのスキャン・フラグされた内容の人間によるレビュー・（後述の）学習利用の留保を含むため、**このスキルはクラウド例外が使えない可能性がある、という保守的な前提で設計しています**。これは規約文言とPPCの条件を突き合わせた分析であって、**行政の判断や判例ではありません**。専門家の見解も分かれている論点です。

4. **2026年の個人情報保護法改正案（統計作成等・AI開発のための例外を含む）は、2026-07-02 時点で未成立です**（参議院で審議中）。成立していない以上、これに依拠することはできません。

この3.の前提から導かれる実務結論はシンプルです: **「同意やクラウド例外の議論に入らずに済むよう、Claude に読ませる個人データを最小にする」**。それが第3節以降の具体策です。

## 3. 具体的にやること（チェックリスト）

### 3-1. 最初に一度だけ

- [ ] **「Improve Claude（Claudeの改善）」設定をオフにする。**
  - クリック手順: Claude の **設定（Settings）→ プライバシー（Privacy）→「Improve Claude」をオフ**。日本語UIでは「Claudeの改善に協力する」等の表記の場合があります。画面の文言や場所は変更されることがあるので、見つからない場合は「privacy」設定内を探してください。
  - 注意: この設定は**オフにした後に開始・再開した会話にのみ**効きます。また、オフにしても例外が残ります（第4節参照）。
- [ ] **シークレット（Incognito）チャットが使える環境なら、その利用を検討する。** Incognito の会話は設定に関わらず学習に使われないとされています。ただし、**すべての利用環境でこの機能が使えるかは未確認**です（デスクトップのエージェント環境での可否は確認できていません）。使えない環境ではこの項目は飛ばして構いません。
- [ ] （選択肢として）**Team / Enterprise 等の法人向けプラン**は Commercial Terms が適用され、デフォルトで学習に使われません。業務データの扱いに慎重を期すなら検討の価値があります。

### 3-2. 毎回の運用ルール

- [ ] **ゲストのデータを公開の場に絶対に置かない。** 公開の GitHub リポジトリ、SNS投稿、スクリーンショット、質問サイト — どこにもです。このスキルの改善のために OTA エクスポートの**ヘッダー行**を共有してもらう仕組み（issueテンプレート）がありますが、共有してよいのは**列名の行だけ**です。ゲスト名や予約コードを含むデータ行は1行も貼らないでください。
- [ ] **作業フォルダは専用・最小にする。** Claude と共有するのは、その報告期間の予約データと名簿など**必要なファイルだけ**を入れた専用フォルダにしてください。名簿の全アーカイブやパスポート写しの保管庫を含む親フォルダごと共有しない。
- [ ] **要配慮個人情報を入れない。** 健康状態・宗教・犯罪歴などが書かれ得るアンケートの自由記述などは、Claude に読ませるファイルから除いてください（国籍そのものは要配慮個人情報ではありません）。
- [ ] **報告サイクルが終わったら、その会話（タスク）を削除する。** 削除された会話は履歴から即時消え、バックエンドからも30日以内に削除され、以後の学習には使われないとされています（2026-07-02時点のポリシー）。
- [ ] **過去期間の一括さかのぼり処理には慎重に。** 何期分もの実名入りの過去データをまとめて読ませるのは、入力する個人データ量を不必要に増やします。過去分はできるだけ第5節の最小化方式（国籍列のみ）で処理してください。

### 3-3. やってはいけないこと（重要）

- **パスポートの写しを「整理のため」に削除しない。** 外国人ゲスト（国内に住所のない方）のパスポートの写しは、宿泊者名簿とともに**作成の日から3年間保存する法律上の義務**があります（住宅宿泊事業法施行規則7条・ガイドライン）。「Claudeに読ませ終わったから消す」「プライバシーのために消す」は**法令違反の方向の間違い**です。このスキルはファイルの削除を提案しません。保存義務と「Claudeに読ませるかどうか」は別の問題です — 読ませない選択（第5節）はできますが、保存はやめられません。
- **提出物にゲスト名を書き足さない。** 定期報告は集計値のみです。何かの欄にゲスト情報を書く必要は一切ありません。

## 4. このスキルは何をどこに送るのか（正直な整理）

**スキル自体は何も送信しません。** このスキルは、あなたのセッションの中で動く手順書とローカルで実行される集計スクリプトの組み合わせです。スクリプトはフォルダ内のファイルを読み、フォルダ内に結果を書くだけで、ネットワーク送信を行いません。

ただし、**Claude に読ませたファイルの内容は Anthropic に送信されます**。これはスキルではなく Claude というサービス自体の仕組みです。2026-07-02 時点で確認したコンシューマー向けポリシー（現行ポリシーの表題は「Effective July 8, 2026」）の要点:

- Claude が読むファイル・会話・エージェント作業の内容は、ポリシー上の **「Inputs」** に該当します。フォルダ内のファイルが（Google Drive コネクタ経由のデータのように）学習除外扱いになるかは**公式に確認できていません — 本書は「Inputs として扱われる（学習対象になり得る）」という最悪ケースの前提**で書いています。
- 「Improve Claude」を**オフにすれば**、原則として Inputs は学習に使われず、保持期間は30日です（オンの場合は最長5年・非識別化）。
- **ただしオプトアウトは無条件ではありません。** ポリシーには明示的な例外（carve-out）があります: **(i) 会話が安全性審査（safety review）のためにフラグされた場合、または (ii) あなた自身がその内容を報告した場合には、オプトアウトしていても** Inputs/Outputs がモデル改善に使われ得ます。フラグされた入出力は**最長2年**、トラスト&セーフティの分類スコアは**最長7年**保持されます。何がフラグの引き金になるかは公表されておらず、フラグ時の通知の約束もありません。
- ポリシーは、法令遵守・重大な危害の防止・不正対応・規約執行のために**「誠実な信念（good-faith belief）」に基づき政府・法執行機関等へ個人データを共有し得る**とも定めています（裁判所命令を前提条件としていません）。PPC は2025年のDeepSeekに関する情報提供で、外国事業者の所在国・準拠法をリスク開示上の考慮要素として扱っており、米国法準拠である点は認識しておくべき事実です。

まとめると: **「オフ設定＋会話削除で通常は30日で消える。ただしフラグされた場合の例外が契約上残る」** — このスキルの手順が入力最小化にこだわるのは、この残余リスクを前提にしているからです。

出典（いずれも2026-07-02取得）: https://www.anthropic.com/legal/privacy / https://www.anthropic.com/news/updates-to-our-consumer-terms / https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-personal-data / https://privacy.claude.com/en/articles/10023580-is-my-data-used-for-model-training / https://support.claude.com/en/articles/13364135-use-claude-cowork-safely

## 5. より慎重な運用: PII最小化オプション（国籍列のみ方式）

パスポート写しのフォルダを国籍の情報源として使うのは、このスキルの**通常のサポート対象の手順**です（保存義務があるので、どの道あなたの手元にあります）。一方で、**パスポート画像を Claude に読ませたくない**という判断も十分に合理的です。Anthropic 自身も、エージェント作業に「個人の記録などの機微なファイル」へのアクセスを与えることには注意を促しています。その場合は次のようにしてください。

1. パスポート写しのフォルダは**共有フォルダの外**に置いたまま、保存義務どおり保管する。
2. 国籍は自分でスプレッドシート等に転記し、**予約確認コードと国籍だけの表**を作る。それを作業フォルダの `nationality-overrides.csv`（列: `confirmation_code,mode,nationalities`、`mode` は `fill`）として保存すれば、スキルはパスポート画像なしで国籍を確定できます。
3. 名簿ファイルを読ませる場合も、慎重にしたければ**氏名・住所・職業の列を消したコピー**を作って共有フォルダに入れれば足ります。集計に必要なのは宿泊日・人数・国籍だけです。

トレードオフは手作業の量です: パスポート方式は自動で速く、最小化方式は安全側だが転記の手間が増えます。**どちらでも最終的な報告書はまったく同じ**（集計値のみ）です。ゲスト数が少ない月や、特に慎重を期したい方には最小化方式を推奨します。

---

## English summary

**Verified as of 2026-07-02. Not legal advice.** This is the conservative design guidance this skill follows, written by its author (a Tokyo minpaku operator), not a settled legal ruling. The skill *prepares* your report; **you**, the operator, file it and are responsible for it.

**Why this matters.** Guest names/addresses are personal information under Japan's APPI; a passport number is an "individual identification code" (Cabinet Order Art. 1), so a passport image or number is personal information by itself. The report you submit contains **only aggregates** (nights occupied, guest counts, nationality breakdown) — the privacy risk lives entirely in the *inputs* (registry, reservation data, passport copies), not the output.

**Your APPI position (conservative reading).** Since the 5,000-record threshold was abolished (2017), even a single-property host holding the legally required guest registry is a 個人情報取扱事業者 (business operator handling personal information). The PPC's June 2023 generative-AI alert asks such operators to confirm inputs stay within the stated purpose of use and that the provider will not use the data for machine learning. Because Anthropic is a US company, APPI Art. 28 (transfers to third parties in foreign countries) is also in play; whether the PPC "cloud exception" covers a consumer AI service whose terms reserve safety scanning, human review and flagged-data training is **unsettled** — commentary is split, there is no ruling, and this skill conservatively assumes the exception may not apply. Hence: minimize what Claude reads.

**Do this:**
- Turn **OFF "Improve Claude"** (Settings → Privacy) before your first session; it only affects new/resumed chats. Consider Incognito chats where available (availability in agentic/desktop environments is unconfirmed).
- **Never put guest data anywhere public** — no repos, no social posts. When sharing OTA export formats via the issue template, share the **header row only**.
- Use a **dedicated, minimal working folder**; do not share your whole registry/passport archive.
- **Keep passport copies for 3 years** — that is a legal duty (施行規則 Art. 7). Never delete them to "clean up"; this skill will never suggest deleting them. Not sharing them with Claude (below) is fine; not keeping them is not.
- Delete the conversation/task after each reporting cycle (back-end purge within 30 days per current policy).
- Keep 要配慮個人情報 (health/religion/criminal-history, e.g. survey free text) out of shared files. Nationality itself is not in that category.

**What this skill sends where.** The skill itself transmits nothing; its script runs locally on files in your folder. But anything Claude reads becomes **"Inputs"** under Anthropic's consumer privacy policy (headed "Effective July 8, 2026"). Worst-case assumption stated plainly: folder files are treated as Inputs. With the opt-out OFF, retention is 30 days and no training — **except** the policy's explicit carve-out: conversations **flagged for safety review** (or content you yourself report) can be used for model improvement despite opt-out, with flagged inputs/outputs kept up to 2 years and classification scores up to 7 years. The policy also allows good-faith sharing with law enforcement under US law. The opt-out is real but conditional — which is why input minimization is the primary safeguard.

**PII-minimization option (for cautious users).** Passport folders are a supported, normal nationality source. If you prefer not to expose passport images to Claude: keep them outside the shared folder (still stored 3 years), transcribe nationalities yourself into `nationality-overrides.csv` (`confirmation_code,mode,nationalities`, mode `fill`), and optionally strip name/address/occupation columns from any registry copy you share — counting needs only dates, party sizes and nationalities. More manual work, identical final report.
