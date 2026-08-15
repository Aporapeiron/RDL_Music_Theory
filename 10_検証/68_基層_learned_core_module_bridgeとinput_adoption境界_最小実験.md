# 検証記録：基層-learned・core module bridgeとinput adoption境界

*対象：core module bridge candidateを、中核音楽理論Module入力候補として採用するcontroller境界*  
*状態：DRAFT v0.1 / 67 core module bridge境界検証後のinput adoption最小検証*  
*実装：`10_検証/base_to_core_music_module_input_adoption_boundary.py`*

---

## ■ 0. 検証目的

67では、selected musical interpretation candidateだけでは中核音楽理論Moduleへ接続されず、外部core module candidate setと`Γ_core_module_bridge`を与えた場合だけcore module bridge candidateが生じることを確認した。

68では、そのcore module bridge candidateを固定し、adoption controllerを外部に与えたときだけ、core module input candidateとして採用されることを確認する。

```text
core module bridge candidate
  + Γ_core_module_input_adoption_fixture
  ↓
core module input candidate
  ↓
中核Module内部処理は未開始
```

ここで確認するのは、core module bridge candidateがあることと、中核Module入力として採用済みであることを分けることである。

---

## ■ 1. 固定するcore module bridge candidate

67で得たfixture用のcore module bridge candidateを使う。

```text
core module bridge candidate:
  interpretation_label = pitch_relation_different_interpretation_candidate
  module_candidate = interval_module_pitch_relation_candidate
  module_name = 音程_Module
```

これは接続候補であり、まだ中核Module入力ではない。

```text
core module bridge candidate
  ≠ core module input candidate
```

---

## ■ 2. adoption controller

二つの経路を比較する。

```text
Γ_core_module_input_adoption = None
  → bridge candidate remains unadopted
```

```text
Γ_core_module_input_adoption_fixture
  → bridge candidateをcore module input candidateとして採用する
```

このcontrollerはfixture用であり、中核音楽理論Moduleへの一般入力採用規則ではない。

---

## ■ 3. 最小ケースの比較

### 3.1 adoption controllerなし

```text
core module bridge candidate
+ Γ_core_module_input_adoption = None
↓
status = core_module_bridge_candidate_unadopted
core module input candidate = None
```

### 3.2 adoption controllerあり

```text
core module bridge candidate
+ Γ_core_module_input_adoption_fixture
↓
core module input candidate
  module_name = 音程_Module
  input_label = interval_module_pitch_relation_input_candidate
```

ただし、中核Module内部処理はまだ開始しない。

---

## ■ 4. 観測結果

| core module bridge candidate | adoption controller | core module input candidate | module processing started | Core promotion |
|---|---|---|---|---|
| interval module bridge | None | `None` | `False` | `False` |
| interval module bridge | fixture | `interval_module_pitch_relation_input_candidate` | `False` | `False` |

確認できたこと。

```text
same core module bridge candidate
different Γ_core_module_input_adoption
↓
core module input candidate appears / does not appear
```

さらに、

```text
core module input candidate
  ≠ 中核Module内部処理開始
  ≠ Core昇格
```

である。

---

## ■ 5. Module責務の確認

今回の接続は、次のように分かれる。

```text
Γ_core_module_bridge:
  core module bridge candidateを作る

Γ_core_module_input_adoption:
  bridge candidateをcore module input candidateとして採用する

中核Module内部処理:
  今回は未開始

Core:
  今回は未接続
```

したがって、input adoptionはModule処理開始ではない。

---

## ■ 6. まだ言えないこと

今回の検証から、次は言えない。

```text
core module input candidateが正しいModule入力であること
音程ModuleのBやΓが更新されたこと
音程Module内部処理が開始されたこと
core module input adoption controllerの由来や採用条件が決まったこと
他の中核Module候補との競合が解決したこと
RDL Coreへ昇格できること
```

また、今回の`Γ_core_module_input_adoption`はfixture用であり、一般的な中核Module入力採用規則ではない。

---

## ■ 7. 暫定結論

68では、core module bridge candidateだけでは中核Module入力として採用されず、`Γ_core_module_input_adoption`を与えた場合だけcore module input candidateが生じることを確認した。

```text
core module bridge candidate
  + Γ_core_module_input_adoption_fixture
  ↓
core module input candidate
```

ただし、ここで停止する。

```text
core module input candidate
  ≠ 中核Module内部処理開始
  ≠ 中核ModuleのB/Γ更新
  ≠ Core昇格
```

次に進むなら、core module input candidateを実際に音程Module側のB/Γ境界へ渡す検証を見る。
