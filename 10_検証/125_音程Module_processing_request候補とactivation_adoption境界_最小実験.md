# 検証記録：processing request候補とactivation adoption境界

*対象：124のprocessing request候補を、processing frame activationへ採用する境界*  
*状態：DRAFT v0.1 / 音楽系優先*  
*実装：`10_検証/interval_module_processing_request_adoption.py`*

## ■ 0. 検証目的

processing request candidateを、Module処理開始と同一視しない。

```text
processing request candidate
+ external request adoption controller
↓
adopted processing request candidate
↓
activation input bundleは未生成
Module処理は未開始
```

## ■ 1. 今回の採用stage

```text
processing_frame_activation
```

## ■ 2. 非同一性

```text
processing request
≠ adopted processing request
≠ activation input bundle
≠ module processing start
```

## ■ 3. 暫定結論

125では、processing requestをactivationへ送る採用候補までを作る。

既存70のactivation処理はまだ走らせない。
