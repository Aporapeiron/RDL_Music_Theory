# 検証記録：payload schema契約候補集合とinput contract adoption境界

*対象：複数payload schema候補から、最初に採用する入力受理契約を選ぶ境界*  
*状態：DRAFT v0.1*  
*実装：`10_検証/interval_module_input_contract_adoption.py`*

## ■ 0. 検証目的

payload schema contract候補集合を、採用済み入力契約と同一視しない。

```text
payload schema contract candidate set
+ external adoption controller
↓
adopted input reception contract candidate
↓
Module処理は未開始
Module本文は未変更
```

## ■ 1. 今回の採用

```text
selected payload schema:
  pitch_relation_payload
```

## ■ 2. 非同一性

```text
payload schema candidate set
≠ adopted input reception contract
≠ module processing start
≠ Module document mutation
```

## ■ 3. 暫定結論

121では、音程Moduleの入力受理契約として`pitch_relation_payload`を採用候補にした。

これはModule処理開始でも、Module計画本文の更新でもない。
