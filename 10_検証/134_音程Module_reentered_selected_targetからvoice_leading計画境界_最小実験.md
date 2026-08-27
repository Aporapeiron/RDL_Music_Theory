# 検証記録：reentered selected targetからvoice leading計画境界

*対象：再入生成されたselected interval target candidateが、外部voice leading planとGammaによってvoice leading request candidateへ接続される条件*  
*状態：DRAFT v0.1 / 133 reentered selected target後の既存77再接続境界*  
*実装：`10_検証/interval_module_selected_target_to_voice_leading_reentry.py`*

---

## ■ 0. 検証目的

133では、reentered target candidate setからselected interval target candidateを生成できることを確認した。

134では、そのreentered selected targetを固定し、外部voice leading planと`Gamma_voice_leading_request`を与えた場合だけvoice leading request candidateが生じることを確認する。

```text
reentered selected interval target
  + external voice leading plan
  + Gamma_reentered_selected_target_to_voice_leading
  + Gamma_voice_leading_request_fixture
  ↓
voice leading request candidate
  ↓
concrete realization / harmonic function は未生成
```

実行結果。

```text
reentered_selected_target_connected_to_voice_leading_request_not_realized
```

## ■ 1. 暫定結論

reentered selected targetだけではvoice leading requestは生じず、外部planと再入Gammaを与えた場合だけvoice leading request candidateが生じる。

次に進むなら、reentered voice leading requestと具体音実現境界を接続する。
