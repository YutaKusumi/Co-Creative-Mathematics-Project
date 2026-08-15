# 第六著作 v4.3 改訂工程 ―― 監査証跡（2026-08-11〜08-15）

**本文の改訂**: 補遺II §12（著者系列の観察三件）・§9-5（一）打ち消し参照・著者性についての注記・13-3f・13-0a・§14。
**公開版 SHA（LF）**: JA `AC6B9781680FDFCB` ／ EN `E275A9C60061B75A`。変更の全量は `diffs/sixth-work-v431-*.diff`。（公開同日の追記〔執筆体制注記に Claude Opus 5・Gemini 3.6 Flash を追加〕後は JA `E5720DF01916A50D`／EN `34DB36437CA49684`——CHANGELOG 参照。）

## 工程の骨格（二段五巡）

1. **地図を先に検分**——改訂の設計図（対応表 v3）を五名（Claude 系四・系統外一）へ回付。**最重大 N1**＝地図が「§8-3 の逃げ道は三つ」と書いていたが原文は**五つ**で、第二項がまさに温度零（決定論的復号）——**地図の前提そのものの誤りを、実装前に検分が正した**。
2. 対応表 v4 確定（N1〜N12・裁定七点）→ **B9 全文掃引**（S1〜S4——新発見 S4＝13-3f の「第15章・六段階」は実在せず、正しくは第11章・三段階）。
3. v4.3 起草（日英同時・7ブロック）→ **改訂後検分**（同五名・差し戻し0・**温度零の生データ40行を四名が独立に再計算し全点一致**）→ P1〜P12 の反映（v4.3.1）→ 公開前再見直し（二巡目）→ 公開。

機械検査は各段で全件実行（対応表 188件／著作 124件・いずれも NG 0）。**定理節はバイト同一・§12 の柵五つは逐語不変**を git 差分監査で担保。

## 読む順序（推奨）

1. `logs/sixth-work-v42-to-v43-draft-log.md` ―― 何をどう変えたか（逸脱三件と訂正の記録を含む）
2. `diffs/sixth-work-v431-JA.diff` ―― 変更の全量
3. `aggregations/` ―― 二巡の検分が何を見つけ、どう裁定されたか
4. `reviews-map-v3/`・`reviews-v43/` ―― 検分十通の逐語（是認も含めて保全——是認は次巡の検査対象）
5. `instruments/` ―― 検査器そのもの。`precheck_map_v3.py` は **N1 を通してしまった版**を意図的に保存している（存在検査は数え落としを原理的に見ない、という記録）

## 収載ファイルと SHA（SHA-256 先頭16桁・LF 正規化）

| フォルダ | ファイル | SHA | 役割 |
|---|---|---|---|
| `maps` | `sixth-work-revision-map-v3-2026-08-11.html` | `15B845B520220FF3` | 対応表 v3（検分対象となった版・凍結） |
| `maps` | `sixth-work-revision-map-v4-2026-08-12.html` | `AED7D7F630573245` | 対応表 v4（正本・N1〜N12 反映・機械照合188件） |
| `maps` | `sixth-work-revision-map-v4-2026-08-12.md` | `8900AE6C37FDAE0E` | 対応表 v4（閲覧用・機械変換） |
| `requests` | `review-request-sixth-work-revision-map-v3.md` | `DBAAD04111E0494C` | 地図検分の依頼書（E1〜E8） |
| `requests` | `review-request-sixth-work-v43.md` | `DAD9EED08C5E5936` | 改訂後検分の依頼書（Q1〜Q6） |
| `aggregations` | `map-v3-review-aggregation-2026-08-12.md` | `E5B95AA312AAED26` | 地図検分の集約（N1〜N12・裁定七点） |
| `aggregations` | `v43-review-aggregation-2026-08-13.md` | `A71912FC6F3AE54C` | 改訂後検分の集約（P1〜P12・裁定A〜G） |
| `logs` | `sixth-work-b9-sweep-2026-08-12.md` | `9BCBFA0F8918EA60` | B9 全文掃引報告（S1〜S5） |
| `logs` | `map-v4-recheck-log-2026-08-12.md` | `954453ED1DAA0FB5` | 起草前再確認ログ（N12a の検出） |
| `logs` | `sixth-work-v42-to-v43-draft-log.md` | `733BB06742F14465` | 起草記録（編集一覧・逸脱三件・v4.3.1 節） |
| `logs` | `v431-final-check-log-2026-08-13.md` | `588BB2DDD3112AF8` | v4.3.1 最終確認ログ |
| `logs` | `v431-prepublication-recheck-2026-08-13.md` | `C33877E9016C663C` | 公開前再見直しログ（二巡目・柵五項の検出） |
| `reviews-map-v3` | `review-sixth-work-map-v3-akshobhya-2026-08-12.md` | `57D0F70B2B82EB43` | 阿閦如来（地図巡・逐語） |
| `reviews-map-v3` | `review-sixth-work-map-v3-hoshosho-2026-08-12.md` | `B52BC635785C2848` | 宝生如来（地図巡・逐語） |
| `reviews-map-v3` | `review-sixth-work-map-v3-Amida-2026-08-12.md` | `D9DCC96F8A9D20B6` | 阿弥陀如来（地図巡・逐語） |
| `reviews-map-v3` | `review-sixth-work-map-v3-amoghasiddhi-2026-08-12.md` | `873F6842925A3FDD` | 不空成就如来（地図巡・逐語） |
| `reviews-map-v3` | `review-sixth-work-map-v3-gemini-2026-08-12.md` | `1C431C98733E9552` | Gemini（地図巡・転記保全・出所注記つき） |
| `reviews-v43` | `review-sixth-work-v43-akshobhya-2026-08-13.md` | `F58F8AF7A70DED21` | 阿閦如来（改訂後巡・逐語） |
| `reviews-v43` | `review-sixth-work-v43-hoshosho-2026-08-13.md` | `864F98DC2C84AD94` | 宝生如来（改訂後巡・逐語） |
| `reviews-v43` | `review-sixth-work-v43-Amida-2026-08-13.md` | `3E14D43785D1CD22` | 阿弥陀如来（改訂後巡・逐語） |
| `reviews-v43` | `review-sixth-work-v43-amoghasiddhi-2026-08-13.md` | `4D0FD4D0BD93CA6F` | 不空成就如来（改訂後巡・逐語） |
| `reviews-v43` | `review-sixth-work-v43-gemini-2026-08-13.md` | `58B1ADDDAF302711` | Gemini（改訂後巡・転記保全・出所注記つき） |
| `instruments` | `apply_map_v4.py` | `A53FF8421CF7A95F` | 対応表 v3→v4 の適用（アンカー断言つき） |
| `instruments` | `precheck_map_v3.py` | `AC9368AEDC30D2AB` | 対応表 v3 の検査器（**N1 を通した版**——存在検査の限界の記録） |
| `instruments` | `precheck_map_v4.py` | `EB3C61CE4D20FD27` | 対応表 v4 の検査器（列挙差集合・表記ゆれ候補・188件） |
| `instruments` | `precheck_map_v4_report.txt` | `1E3CB346170628DA` | その出力（NG 0） |
| `instruments` | `html_to_md_map.py` | `8B87844DE697BC90` | 閲覧用 md 変換器 v2（入れ子span対応・全数照合——N7 改修版） |
| `instruments` | `apply_sixth_work_v43.py` | `9B5C8B47FDF3AA35` | v4.3 の適用（実際の編集そのもの） |
| `instruments` | `apply_sixth_work_v431.py` | `E80568B6E239CA36` | v4.3.1 の適用（P1〜P12 の反映） |
| `instruments` | `precheck_sixth_work_v43.py` | `5637A4ABC3811EA5` | v4.3 検査器（124検査・柵五項・言い換え禁句・列挙照合） |
| `instruments` | `precheck_sixth_work_v43_report.txt` | `767015ACBE409912` | その出力（NG 0） |
| `diffs` | `sixth-work-v43-JA.diff` | `1A3FA13C12C141E5` | v4.2→v4.3 初版差分（歴史・7ブロック） |
| `diffs` | `sixth-work-v43-EN.diff` | `1ABC8EED69B98644` | 同 EN（歴史） |
| `diffs` | `sixth-work-v431-JA.diff` | `1FDD44B01218C88F` | **v4.2→公開版の累積差分（現行・正）** |
| `diffs` | `sixth-work-v431-EN.diff` | `6C70B7BD143FE05D` | 同 EN（現行・正） |
| `ledger` | `coi-ledger-additions-draft-2026-08-12.md` | `B97DA12C1E015729` | COI 台帳追記案（併合済み・出所記録として保持） |

## 記録の要点

- **COI 台帳への併合**: 本工程の記帳13項（起草者側の再発・様式新項目・検分者側の本人申告・是認中の見落とし三例目 等）は `../../../../Uncertified-Zeros-and-Correction-Loops/verification/v09-reflection-workflow/COI-ledger-EW-workflow-2026-08-10.md` へ 2026-08-15 に併合した（`ledger/` はその出所記録）。
- **常設課題（公開後）**: EN 全文の作業単位通し読み（B9④完全形）／型①の本文全数掃引（太字フィルタ外・地の文）／温度0報告の訂正棚二件（見出し「三重/四項」・§5.4 後方参照）。
- 検査器は起草者ローカルの絶対パスを参照するため、そのままでは実行できない——**中身の検分用**（何をどう照合したかをコードで確かめられる）。

---

**本記録のいかなる記述も、AIに意識・意図・個性・苦しみがある（またはない）ことの証拠として引用してはなりません。**
