# Timbre_Attack

[実聴取前小括](実聴取前小括.md)：固定ゲイン・RMS補助比較をまとめ、device検証済みの関係と実聴取待ちの問いを整理する。

[第一音RMS一致の補助比較](第一音RMS一致_補助比較.md)：倍音追加版へ一定ゲインを掛け、固定ゲイン比較と並べる。知覚音量の一致は未確認。実装は `music_v02_timbre_attack_rms_control.py`。

[比較提示とPCM検査](比較提示とPCM検査.md)：既存4条件の単独音声、3対の正逆順提示、介入区間外の波形保存検査と実聴取記録。実装は `music_v02_timbre_attack_listening_pairs.py`。

同じpitch、onset、durationを保存したまま、attack envelope、harmonic profile、transient noiseを変えて、音色・発音状態候補の非同一性を検証するMusic v0.2領域。

音色 / attack 同一pitch-onset保存 最小ループ
: Music_v0.2_音色attack_同一pitch_onset保存_最小ループ.md / music_v02_timbre_attack_identity_probe.py。
  pitch、onset、duration、note orderを固定し、attack envelopeとharmonic profileを分けて実音化する。
