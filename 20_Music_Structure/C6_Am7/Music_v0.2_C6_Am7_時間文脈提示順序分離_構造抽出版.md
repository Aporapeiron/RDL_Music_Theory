# Music v0.2 C6 / Am7 時間文脈提示順序分離 構造抽出版

## 0. 抽出対象

```text
10_Music_Validation/C6_Am7/Music_v0.2_C6_Am7_時間文脈提示順序分離_最小ループ.md
10_Music_Validation/C6_Am7/music_v02_c6_am7_temporal_context_order_split.py
artifacts/json/music_v02_c6_am7_temporal_context_order_split.json
```

## 1. 抽出主題

時間文脈実音化では、phrase内の前後関係を鳴らした。

今回抽出するのは、その聴取提示に含まれる二つの層の分離である。

```text
phrase-internal temporal context
  = preceding chord -> identical target -> following chord

presentation-order memory
  = previous phrase -> current phrase listening condition
```

この二つを混ぜると、「targetがどう読まれたか」と「直前に何を聞いたからそう読まれたか」が区別しにくくなる。

## 2. 分離方法

```text
single_phrase_files:
  each phrase exported as its own WAV

order_variants:
  canonical_order
  reversed_context_order
```

単独phrase fileはphrase内contextを見やすくし、order variantは提示順序memoryを観測対象として明示する。

## 3. 保存されるもの

```text
target_notes:
  C3 E3 G3 A3

target_is_identical_inside_each_phrase_definition:
  true
```

提示順序を変えても、各phrase定義内のtargetは同一である。

## 4. 追加された観測軸

```text
presentation_order:
  canonical_order
  reversed_context_order

listening_scope:
  single_phrase
  ordered_sequence

memory_risk:
  phrase order may affect the next phrase's listening context
```

`memory_risk` は欠陥ではなく、聴取条件として明示的に保持する。

## 5. Music Core v0.2へ返す命題

```text
時間文脈は二重である。

1. 作品内・phrase内の前後関係
2. 検証提示上の聴取順序関係
```

C6 / Am7の状態候補を実聴取へ接続するには、この二つを分けて記録する必要がある。

## 6. 停止線

```text
single_phrase_file_reduces_but_does_not_remove_listener_memory
order_variant_tests_presentation_order_not_chord_truth
actual_listening_observation_remains_null_until_recorded
same_target_sonority_remains_identical_inside_each_phrase_definition
```

この抽出は、C6 / Am7の解決ではなく、実聴取前に提示条件を分解するMusic fixtureである。