# 検証記録：音高調律から音程綴り境界 片方向stress test 10工程

*対象：279〜288で選ばれた音高調律→音程のdirected relationが、実データ列で差異を保存したまま通るか*  
*状態：DRAFT v0.1 / Module対stress test*  
*実装：`10_検証/tuning_to_interval_spelling_stress_289_298.py`*

---

## ■ 0. 検証目的

279〜288では、四Moduleの相互作用面を観測し、次のstress test候補を置いた。

```text
音高調律 → 音程:
  tuning categoryはspelling boundaryへ向かうが、interval nameを返さない
```

289〜298では、この片方向接続を実データ列で確認する。

ただし、確認するのは接続であって同一化ではない。

```text
12TET 7 semitones
  ≠ interval name
  ≠ spelling
  ≠ perfect fifth確定
```

---

## ■ 1. 既存検証の再利用

今回使う既存検証は次である。

```text
10 interval_fifth_decomposition.py
  3:2 frequency ratio
  → cents coordinate
  → 12TET 7 semitones

11 spelled_interval_divergence.py
  C4-G4
  → 7 semitones + generic fifth
  → 完全五度

  C#4-Ab4
  → 7 semitones + generic sixth
  → 減六度

  C4-A𝄫4
  → same physical pitch pair as C4-G4
  → 減六度
```

---

## ■ 2. 観測した10工程

```text
289 tuning_category_source
290 interval_spelling_boundary_request
291 unspelled_interval_label_block
292 C4_G4_spelling_application
293 Csharp4_Aflat4_spelling_application
294 same_12tet_category_comparison
295 directed_connection_check
296 reverse_determination_block
297 music_specific_difference_preservation
298 next_stress_target
```

---

## ■ 3. 実行結果

```text
tuning_to_interval_spelling_stress_289_298_observed_without_collapsing_12tet_category_into_interval_name
```

確認したこと。

```text
tuning_semitones_12tet = 7
spelling_labels = 完全五度 / 減六度 / 減六度
same_tuning_category = True
spelling_required_for_label = True
spelling_splits_interval_label = True
directed_connection_preserved = True
returns_interval_name_to_tuning = False
generated_mutation = False
```

---

## ■ 4. 暫定結論

289〜298では、音高調律Moduleから音程Moduleへの片方向接続が、差異を保存したまま通ることを確認した。

```text
3:2 frequency ratio
→ cents coordinate
→ 12TET 7 semitones
→ interval spelling boundary request
→ spellingありの場合だけ interval label candidate
```

同じ12TET 7半音でも、綴り境界により音程名は分岐する。

```text
C4-G4      → 完全五度
C#4-Ab4    → 減六度
C4-A𝄫4    → 減六度
```

したがって、音高調律から音程へ向かう接続は成立するが、12TETカテゴリーを音程名へ自動昇格しない。

---

## ■ 5. 相互作用面としての読み

今回のstress testは、279のdirected relationを実データ列で少し強くした。

```text
音高調律 → 音程
```

の向きは通る。

しかし、逆向きに、

```text
音程名 → 調律カテゴリー確定
```

は作らない。

つまり、この相互作用面は片方向接続であり、双方向同一性ではない。

---

## ■ 6. まだ言えないこと

```text
すべてのtuning categoryが音程綴り境界へ通ること
12TET 7半音が常に完全五度であること
綴り境界が常に一意に与えられること
音程名から調律体系を逆決定できること
人間の知覚上も同じ分岐になること
Core接続診断が不要になったこと
```

これらは未解決ξとして残す。
