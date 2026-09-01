# json

Music検証で生成した構造観測・再聴取slot・検証manifestを置く領域。

JSON記録は機械的な検証出力であり、人間聴取そのものではない。`actual_listening_observation` が未実施の場合は `null` として残す。
## C6 / Am7

```text
music_v02_c6_am7_rehearing_observation.json
  basic rehearing observation with actual_listening_observation = null

music_v02_c6_am7_intervention_separation.json
  separated context/register/bass/full-tilt intervention manifest
```

- music_v02_c6_am7_relation_weight_probe.json
  C6 / Am7関係重みプローブの構造圧・C中心抵抗・実聴取slot manifest。

- music_v02_c6_am7_temporal_context_probe.json
  C6 / Am7時間文脈実音化プローブのtarget同一性・前後文脈・実聴取slot manifest。

- music_v02_c6_am7_temporal_context_order_split.json
  C6 / Am7時間文脈提示順序分離の単独phrase・順序variant・実聴取slot manifest。

- music_v02_c6_am7_pre_listening_closure.json
  C6 / Am7実聴取前小括のCore返却候補・保留命題・actual listening slot集約manifest。

- music_v02_melody_meter_identity_probe.json
  旋律×拍節 輪郭保存アクセント変位プローブの構造予測・実聴取slot manifest。
