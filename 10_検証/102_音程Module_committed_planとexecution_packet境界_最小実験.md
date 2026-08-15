# 検証記録：committed planとexecution packet境界

*実装：`10_検証/interval_module_execution_packet_boundary.py`*

```text
committed plan candidate
+ external execution scope boundary
↓
execution packet candidate
↓
未実行
```

execution packetは、構造圧縮を含む実行単位候補であり、実行結果ではない。
