# 検証記録：input source契約候補とpayload schema契約候補境界

*対象：入力source契約候補から、受け取れるpayload schema候補を生成する境界*  
*状態：DRAFT v0.1*  
*実装：`10_検証/interval_module_input_payload_schema_contract.py`*

## ■ 0. 検証目的

input source contract候補から、payload schemaを自動確定しない。

```text
input source contract candidates
+ external payload schema inventory
+ Γ_payload_schema_contract
↓
payload schema contract candidate set
↓
input contract adoptionは未生成
```

## ■ 1. 今回の限定Γ

今回のfixtureでは、`base_learned_core_input` だけを受理sourceとして読み、次のschema候補を作る。

```text
pitch_relation_payload
spelled_interval_payload
contextual_role_payload
```

## ■ 2. 非同一性

```text
input source contract
≠ payload schema inventory
≠ payload schema contract candidate set
≠ adopted input contract
```

## ■ 3. 暫定結論

120では、音程Moduleが受ける入力をsourceとpayload schemaへ分けた。

payload schema候補はまだ採用済み契約ではない。
