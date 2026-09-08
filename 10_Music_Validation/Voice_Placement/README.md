# Voice Placement / Crossing：二声のオクターブ配置

状態：最初のdevice fixture。[初回会話聴取記録](初回会話聴取記録.md)を追加。混合音とB単独に関する自己報告あり。単独確認後の混合音再試行は未記録。

## 音楽的な問い

符号化された二声の一方だけをオクターブ移動し、音程列・音高クラス列・リズム・音列の系譜を保存したとき、各旋律を追うことや旋律の帰属がどう変わるか。声部ID A/Bは符号化された系譜として固定し、瞬間的な上声・下声とは分ける。「同じ旋律として聞こえるか」は実聴取の問いとして残す。

既存の声部実現検証が扱った声部IDと音高上下の区別を、今回は短い実音比較へ持ち込む。selected target生成や汎用Runtimeの追加は行わない。

## 材料と境界

今回用に作った8音のfixtureであり、既存曲の採譜ではない。12TET、A4=440Hz、1拍0.5秒、各音0.82拍、両声部同時発音、モノラル。

- A：C4 D4 F4 A4 C5 A4 F4 D4
- B基準：G3 G3 A3 G3 A3 G3 A3 G3
- B変更：G4 G4 A4 G4 A4 G4 A4 G4

Aは波形ごと同一。Bは全音を12半音上げ、音程列・音高クラス列・リズムを保存する。両声部は既存Timbre / Attackのsoft sine合成を使い、attack 0.09秒、release 0.08秒、noiseなし、声部ごとのゲインを固定する。絶対周波数と知覚上の音色の保存は主張しない。

## 確認する関係

| 条件 | A-Bの符号付き半音差 | 高い側の声部ID |
|---|---|---|
| 基準 | 5, 7, 8, 14, 15, 14, 8, 7 | A A A A A A A A |
| B+12 | -7, -5, -4, 2, 3, 2, -4, -5 | B B B A A A B B |

変更条件では、0始まりevent 3と6、すなわち第4音と第7音の開始で上下が逆転する。時刻は1.5秒と3.0秒。離散音の間の順序逆転であって、glissandoや同音での衝突ではない。

一次介入はBのオクターブ配置。Bの声域、垂直音程、周波数配置が伴って変わるため、交差だけの独立効果として扱わない。符号付き音程を12で割った剰余は保存するが、実際の同時音程や声部間距離は変わる。mix音量の正規化は行わない。

## 生成と検証

`music_voice_placement_crossing.py`を実行する。

音声は `artifacts/audio/voice_placement/`、manifestは `artifacts/json/music_voice_placement_crossing.json`。A単独、基準B単独、変更B単独、二声mix 2本、正逆順比較2本の計7本を生成する。

声部内音程列・音高クラス保存、順序逆転位置、Aの共通PCM、mixと声部の加算誤差、クリッピングなし、WAV読み戻しを検査する。PCM検査から声部の追いやすさを判定しない。

## 聴取

[聴取記録テンプレート](聴取記録テンプレート.md)で全8音の自己報告を記録し、その後でdevice上の反転位置と照合する。mixのみで選んだ旋律の声部IDが不明なら未確定とし、A/Bを推定で埋めない。

- [基準→交差条件](../../artifacts/audio/voice_placement/separated_then_crossing.wav)
- [交差条件→基準](../../artifacts/audio/voice_placement/crossing_then_separated.wav)
- [A単独](../../artifacts/audio/voice_placement/voice_A.wav)
- [基準B単独](../../artifacts/audio/voice_placement/separated_voice_B.wav)
- [変更B単独](../../artifacts/audio/voice_placement/crossing_voice_B.wav)

最初はmixでAまたはBを追い、どの位置で追いやすさが変わったか記録する。単独声部を聴いた後の再試行は、学習・提示履歴が変わった条件として別記録にする。

記録項目：日時、再生機器・音量、提示順、追った声部、単独音源を先に聴いたか、反復回数、追えなくなった位置、上下へ注意が移ったか、不明・差なしも含む自由記述。

生成manifestのactual_listening_observationは生成時点のnullを保持し、後続の人間報告は別の聴取記録へ保存する。構造上の上下逆転と人間の帰属切替を分離し、実聴取からEを扱う際は、どのM_Bの予測と後続解釈を比較したかを別途明示する。
