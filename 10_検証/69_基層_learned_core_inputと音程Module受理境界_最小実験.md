# 検証記録：基層-learned・core inputと音程Module受理境界

*対象：core module input candidateを、音程Module側の受理境界へ渡す条件*  
*状態：DRAFT v0.1 / 68 core module input adoption境界検証後のinterval module reception最小検証*  
*実装：`10_検証/base_to_interval_module_reception_boundary.py`*

---

## ■ 0. 検証目的

68では、core module bridge candidateだけでは中核Module入力にならず、`Γ_core_module_input_adoption`を与えた場合だけcore module input candidateが生じることを確認した。

69では、そのcore module input candidateを固定し、音程Module側の受理境界`B_interval_module_reception`と`Γ_interval_module_reception`を外部に与えたときだけ、interval module boundary input candidateが生じることを確認する。

```text
core module input candidate
  + B_interval_module_reception_fixture
  + Γ_interval_module_reception_fixture
  ↓
interval module boundary input candidate
  ↓
音程Module内部処理は未開始
```

ここで確認するのは、中核Module入力候補があることと、音程Module側の受理境界に入ったことを分けることである。

---

## ■ 1. 固定するcore module input candidate

68で得たfixture用のcore module input candidateを使う。

```text
core module input candidate:
  input_label = interval_module_pitch_relation_input_candidate
  module_name = 音程_Module
```

これは中核Module入力候補であり、まだ音程Module側のB/Γ境界を通っていない。

```text
core module input candidate
  ≠ interval module boundary input candidate
```

---

## ■ 2. 音程Module側の受理境界

今回はfixture用の受理境界を外部入力として置く。

```text
B_interval_module_reception_fixture:
  accepts module_name = 音程_Module
  receiver_family = pitch_relation_interpretation_receiver
```

これはCoreから来る一般入力境界ではなく、今回のfixture用境界である。

---

## ■ 3. 音程Module受理Γ

二つの経路を比較する。

```text
Γ_interval_module_reception = None
  → core module input candidate remains unreached by interval module
```

```text
Γ_interval_module_reception_fixture
  → module_nameとinput_labelを読み、
     interval module boundary input candidateを作る
```

このΓはfixture用であり、音程Module内部の一般処理規則ではない。

---

## ■ 4. 最小ケースの比較

### 4.1 reception Γなし

```text
core module input candidate
+ B_interval_module_reception_fixture
+ Γ_interval_module_reception = None
↓
status = core_input_not_received_without_gamma
interval module boundary input candidate = None
```

### 4.2 reception Γあり

```text
core module input candidate
+ B_interval_module_reception_fixture
+ Γ_interval_module_reception_fixture
↓
interval module boundary input candidate
  label = interval_module_received_pitch_relation_candidate
```

ただし、音程Module内部処理はまだ開始しない。

---

## ■ 5. 観測結果

| core module input | B_interval_reception | Γ_interval_reception | interval boundary input | interval processing started |
|---|---|---|---|---|
| interval input | same | None | `None` | `False` |
| interval input | same | fixture | `interval_module_received_pitch_relation_candidate` | `False` |

確認できたこと。

```text
same core module input candidate
same B_interval_module_reception
different Γ_interval_module_reception
↓
interval module boundary input appears / does not appear
```

さらに、

```text
interval module boundary input candidate
  ≠ 音程Module内部処理開始
  ≠ interval label generation
  ≠ B/Γ更新
```

である。

---

## ■ 6. Module責務の確認

今回の接続は、次のように分かれる。

```text
Γ_core_module_input_adoption:
  core module input candidateを作る

B_interval_module_reception:
  音程Moduleが受け取れる入力境界を置く

Γ_interval_module_reception:
  input candidateを音程Module側のboundary inputとして読む

音程Module内部処理:
  今回は未開始

Core:
  今回は未接続
```

したがって、receptionはModule内部処理開始ではない。

---

## ■ 7. まだ言えないこと

今回の検証から、次は言えない。

```text
interval module boundary input candidateが正しい音程Module入力であること
音程ModuleのB_chromatic / B_spelling / Γ_intervalが更新されたこと
generic intervalやqualityが生成されたこと
interval labelが生成されたこと
音程Module内部処理が開始されたこと
RDL Coreへ昇格できること
```

また、今回の`B_interval_module_reception`と`Γ_interval_module_reception`はfixture用であり、一般的な音程Module入力規則ではない。

---

## ■ 8. 暫定結論

69では、core module input candidateだけでは音程Module側の受理境界へ入らず、`B_interval_module_reception`と`Γ_interval_module_reception`を与えた場合だけinterval module boundary input candidateが生じることを確認した。

```text
core module input candidate
  + B_interval_module_reception_fixture
  + Γ_interval_module_reception_fixture
  ↓
interval module boundary input candidate
```

ただし、ここで停止する。

```text
interval module boundary input candidate
  ≠ 音程Module内部処理開始
  ≠ 音程ModuleのB/Γ更新
  ≠ interval label generation
  ≠ Core昇格
```

次に進むなら、interval module boundary input candidateを既存の音程Module内の`B_chromatic / B_spelling / Γ_interval`へ接続する境界を見る。
