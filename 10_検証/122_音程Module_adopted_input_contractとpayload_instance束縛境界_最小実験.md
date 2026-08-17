# 検証記録：adopted input contractとpayload instance束縛境界

*対象：採用済み入力受理契約候補へ、実際のpayload instance候補を束縛する境界*  
*状態：DRAFT v0.1 / 音楽系優先*  
*実装：`10_検証/interval_module_input_payload_instance.py`*

## ■ 0. 検証目的

121で得たadopted input reception contractから、payload instanceを自動生成しない。

```text
adopted input reception contract candidate
+ external payload instance
+ Γ_payload_instance_binding
↓
bound payload instance candidate
↓
validationは未生成
Module処理は未開始
```

## ■ 1. 今回のpayload instance

```text
payload_schema = pitch_relation_payload
lower_note = C4
upper_note = G4
chromatic_distance = 7
spelling_pair = (C, G)
```

## ■ 2. 非同一性

```text
adopted input contract
≠ payload instance
≠ bound payload candidate
≠ validation
≠ module processing start
```

## ■ 3. 暫定結論

122では、採用済み入力契約に外部payload instanceを束縛できることだけを確認した。

payload instanceは契約から生成されない。
