# 構造抽出：音高調律から音程綴り境界 片方向stress test

*対象：289〜298*  
*状態：DRAFT v0.1*

## ■ 1. 接続地図

```text
3:2 frequency ratio
× Γ_cents / Γ_12TET_round
→ tuning 7 semitone category

7 semitone category
× interval spelling boundary request
→ unspelled interval label block

7 semitone category
× C4-G4 spelling
→ 完全五度

7 semitone category
× C#4-Ab4 spelling
→ 減六度

same 7 semitone category
× comparison
→ same category / different label observation
```

## ■ 2. 確認した片方向性

```text
音高調律Module
→ 音程Module
```

は通る。

ただし、

```text
音程名
→ 音高調律Moduleのcategory確定
```

は作らない。

## ■ 3. 保持する非同一性

```text
frequency ratio
≠ cents coordinate
≠ 12TET semitone category
≠ spelling boundary
≠ interval label

12TET 7 semitones
≠ perfect fifth
≠ diminished sixth
```

## ■ 4. 禁止補完

```text
12TET 7 semitones
→ 完全五度確定

same physical pitch pair
→ same interval label

spelling boundary request
→ spelling自動生成

interval label
→ tuning category逆決定
```

は行わない。

## ■ 5. 未解決ξ

```text
ξ_tuning_category_to_spelling_boundary_scope
ξ_spelling_boundary_source
ξ_enharmonic_interval_label_divergence
ξ_reverse_interval_to_tuning_determination_block
ξ_human_perception_vs_spelled_label_difference
ξ_interval_to_harmonic_target_stress_test
```

## ■ 6. 暫定結論

289〜298で、音高調律から音程綴り境界へのdirected relationは、実データ列でも差異を保存したまま通ることを確認した。

この接続は、12TETカテゴリーを音程名へ潰さず、綴り境界を必要とする片方向stress testである。
