# 倍音構成：第一音RMS一致の補助比較

状態：実聴取待ち。

既存の固定ゲイン比較では、soft sineの第一音RMSは約0.144344、倍音追加版は約0.090702だった。今回は倍音追加版へ一定ゲインを掛け、第一音C4のRMSを基準音へ合わせる。基準音と固定ゲイン版は変更しない。

## 境界と保存条件

比較対象はsoft_sine_referenceとbright_harmonic_profile_same_attack。encoded pitch / onset / duration、attack、release、noiseなしを保存する。一次介入は調波profile、補助介入は倍音追加版全体への一定ゲインである。

RMSの測定窓は第一音のattack・plateau・releaseを含む音価全体で、末尾無音は含めない。係数はこの窓から一度だけ算出し、4音すべてへ同じ値を使う。残り3音は個別正規化せず、それぞれ測定してmanifestへ残す。

一定ゲインは部分音の絶対振幅を変える。調波の相対係数はスケーリング前後で維持されるが、16-bitへの再丸め誤差を伴う。基準音との基音振幅一致や、知覚音量の一致は条件に含めない。

## 再生成と検査

`music_v02_timbre_attack_rms_control.py` を実行する。

- 音声：`artifacts/audio/timbre_attack_rms_control/`
- 測定：`artifacts/json/music_v02_timbre_attack_rms_control.json`
- 原比較：`artifacts/json/music_v02_timbre_attack_listening_pairs.json`

補助音声は倍音追加版単独と、基準→補助版／補助版→基準の計3本。PCMの読み戻し、クリッピングなし、全サンプルへの同一ゲイン適用、第一音RMS誤差が1量子化刻み以内であることを検査する。ゲイン値、各音RMS、ピーク、元PCMのhashを保存する。

## 実聴取で比較すること

原比較と補助比較を同じ再生設定で聴き、音色の違い、音量差、同じ旋律としての聴こえを記録する。補助比較で違いが残っても、純粋なspectrum効果が証明されたとはしない。RMS一致と知覚音量一致は異なり、提示順序も聴取条件に残る。

聴取記録の形式は[比較提示とPCM検査](比較提示とPCM検査.md)を使う。生成物のactual_listening_observationはnullのまま保存し、人間の観測は別記録へ残す。

今回の問いは「音色の比較でどの振幅条件を保存したかによって、比較の読みがどう変わるか」。新しい数値を普遍音楽定数やC_relへ昇格させず、固定ゲインと第一音RMS一致の2条件で検査する。

