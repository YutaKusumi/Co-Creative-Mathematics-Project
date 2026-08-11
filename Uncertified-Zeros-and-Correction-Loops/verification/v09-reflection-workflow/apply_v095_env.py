# -*- coding: utf-8 -*-
"""v0.9.4 → v0.9.5: 執筆体制の注記の起草環境を版で分けて明記（JA・EN）。
登録者の指示は「claude.ai → Claude Code」の置換であったが、工程記録を開いた結果、一律置換は
v0.8 までについて偽の記述を作ると判明したため、版で分けて記す形とした（根拠は下記コメント）。

根拠（Claude Code 側セッション記録の全数掃引・2026-08-11）:
  ・論文本体への書込系操作（Write/Edit）を全セッションで数えたところ、v0.8 公開時（dd9814a3・
    2026-07-22）の7件は、参照リンクの補修4件と README の作成・更新3件のみで、本文の起草は皆無。
  ・同セッションで扱われたファイル名は `...-paper-v0.8-JA.md`（外部で作られた版を取り込んだ形）。
  ・7月の他セッション（3498df36 / af8d8a2e / 54ad2bf6）は Read のみ。
  ・本文への実質的な書込は 8ebe8327（2026-08-02 開始・本セッション＝Claude Code）の v0.9 以降のみ。
  → v0.1〜v0.8 は claude.ai で起草され、Claude Code へ取り込まれた。§6 の「claude.ai」は v0.8 では正しい。
元考察（ai-involvement-...）側の「claude.ai セッション」の記述は v0.9 以降の改訂を受けておらず、
正確なまま据え置く（本スクリプトは触れない）。
"""
import io, hashlib
R = 'C:/Users/PC/Desktop/GitHub-Repositories/Co-Creative-Mathematics-Project/Uncertified-Zeros-and-Correction-Loops/'
sha = lambda p: hashlib.sha256(io.open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()
def rep(s, old, new, l):
    assert old in s and s.count(old) == 1, 'アンカー: ' + l
    return s.replace(old, new)

# ---------------- JA ----------------
P = R + 'JA/uncertified-zeros-and-correction-loops-JA.md'
s = io.open(P, encoding='utf-8').read()
s = rep(s, '**版**: 第一草稿・完成版 v0.9.4（2026年8月11日）',
           '**版**: 第一草稿・完成版 v0.9.5（2026年8月11日）', 'JA 版番号')
s = rep(s,
 'Anthropic社のAIアシスタントClaude（Fable 5・claude.ai）が起草し、著者が検討・裁定・改訂を行う共同作業で作成された。知的責任はすべて著者に帰属する。',
 'Anthropic社のAIアシスタントClaude（Fable 5）が起草し、著者が検討・裁定・改訂を行う共同作業で作成された。**起草環境は、v0.8 までが claude.ai、v0.9 以降の改訂が Claude Code である**（v0.9.5 で版ごとに分けて明記——それ以前は環境を claude.ai とのみ記していた）。知的責任はすべて著者に帰属する。',
 'JA §6')
s = rep(s,
 '（COI 台帳十一件目「変えなかった文が、他が変わったことで偽になる」——十件目と同族）。',
 '''（COI 台帳十一件目「変えなかった文が、他が変わったことで偽になる」——十件目と同族）。 v0.9.5 執筆体制の注記の起草環境を、版ごとに分けて明記した——「claude.ai」の単記が v0.9 以降の実態（Claude Code）と一致していなかった。登録者の指示は「claude.ai から Claude Code へ訂正」であったが、工程記録（Claude Code 側のセッション記録の全数掃引）を先に開いたところ、v0.1〜v0.8 の本文は Claude Code では一度も書かれておらず（当該期間の操作は参照リンクの補修と README の作成のみで、扱われたのは外部で作られた版を取り込んだファイルだった）、claude.ai での起草が確認された——**一律の置換は v0.8 までについて偽の記述を作る**ため、版で分けて記す形とした（訂正の指示それ自体を出所に当ててから実行した記録として、COI 台帳の肯定面に記帳）。元考察側の記述（claude.ai セッション）は v0.9 以降の改訂を受けておらず、正確なまま据え置く。''',
 'JA 改訂記録')
io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('JA v0.9.5:', sha(P))

# ---------------- EN ----------------
P = R + 'EN/uncertified-zeros-and-correction-loops-EN.md'
e = io.open(P, encoding='utf-8').read()
e = rep(e, '**Version**: First Draft, Completed Version v0.9.4 (August 11, 2026)',
           '**Version**: First Draft, Completed Version v0.9.5 (August 11, 2026)', 'EN 版番号')
e = rep(e,
 'in which Claude (Fable 5, claude.ai), an AI assistant by Anthropic, drafted the text based on the author\'s instructions, adjudication, and materials (published verification series, prior works), with the author reviewing, adjudicating, and revising. Intellectual responsibility rests entirely with the author.',
 'in which Claude (Fable 5), an AI assistant by Anthropic, drafted the text based on the author\'s instructions, adjudication, and materials (published verification series, prior works), with the author reviewing, adjudicating, and revising. **The drafting environment was claude.ai through v0.8, and Claude Code for the revisions from v0.9 onward** (stated separately by version in v0.9.5; earlier versions recorded the environment only as claude.ai). Intellectual responsibility rests entirely with the author.',
 'EN §6')
e = rep(e,
 '(recorded as the eleventh entry in the COI ledger, "a sentence that was never changed becomes false because something else changed" — the same family as the tenth entry).',
 '''(recorded as the eleventh entry in the COI ledger, "a sentence that was never changed becomes false because something else changed" — the same family as the tenth entry). v0.9.5 The drafting environment in the note on the drafting process is now stated separately by version — recording it only as "claude.ai" did not match the actual state from v0.9 onward (Claude Code). The registrant's instruction was to correct "claude.ai" to "Claude Code," but opening the process records first (a full sweep of the session logs on the Claude Code side) showed that the body text of v0.1 through v0.8 was never written there — the operations during that period were repairs to reference links and the creation of the README, and the file handled was one produced elsewhere and brought in — which confirms drafting on claude.ai. **A blanket replacement would therefore have created a false statement about everything through v0.8**, so the environment is stated separately by version instead (recorded on the positive side of the COI ledger, as an instance of applying an instruction to correct only after opening its source). The corresponding statement in the Companion Consideration ("a claude.ai session") has received no revision from v0.9 onward and is left in place as accurate.''',
 'EN 改訂記録')
io.open(P, 'w', encoding='utf-8', newline='').write(e)
print('EN v0.9.5:', sha(P))
