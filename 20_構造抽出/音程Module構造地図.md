# 音程Module｜構造地図

*対象：音程Moduleで現在抽出済みの四構造*  
*状態：DRAFT v0.1 / 抽出版間の接続地図*

## ■ 0. 役割

本書は新しい検証結果を追加しない。音程Moduleの抽出版を、上流の物理関係から具体音実現、empty後の再探索、外部観測まで接続する地図である。各経路の詳しい条件は、対応する抽出版に残す。

## ■ 1. 全体地図

```text
物理音高・周波数関係
  ↓ ratio / cents / 12TET category
綴りを含む音楽ラベル
  ───────────────────────────────────────────┐
contextual role / learned tendency ───────────┼→ ξ_target_selection
                                                │       ↓
                                                └→ selected target degree
                                                          ↓
                                                    実現Module
                                                          ↓
                                             generated candidates
                                                          ↓
                                      range projection / voice relation
                                                          ↓
                                             candidate result
                                              ├─ remain → selection
                                              │             ↓
                                              │       concrete realization
                                              └─ empty
                                                   ↓
                                            reexploration actions
                                                   ↓
                                      action-set exhaustion / fallback
                                                   ↓
                                     structural state change (limited)
                                                   ↓
                                       candidate regeneration / ordinary search

Module固有state・record
  └─ Module固有projector → GenericDynamicEvent
```

## ■ 2. 四構造の担当

| 抽出版 | 担当する範囲 | 次の接続 |
|---|---|---|
| 物理音高から音楽ラベルへの分岐 | ratio、座標化、12TET、綴り、音程ラベル | `ξ_target_selection`の手前 |
| 音程実現 | 選択済みtarget degreeから候補生成・制約・選択 | concrete realization / empty |
| empty後再探索 | empty観測、action集合、fallback、三履歴 | structural state change / ordinary search |
| 動態Adapter候補 | Module固有state・recordの用途別観測とGeneric event投影 | Module外から読む観測境界 |

## ■ 3. 境界

```text
interval label
  ↓
ξ_target_selection
  ↓
selected target degree
```

target選択は未解決のまま残す。前段の音楽ラベルと後段の具体音実現を、仮の一意規則で直結しない。

また、GenericDynamicEventはこの経路を実行するcontrollerではない。Module固有recordの抽象観測であり、state再構成・候補再生成・fallback採用は音程Module内に残る。

## ■ 4. 現在の読み方

```text
物理関係 ≠ 音楽ラベル
音楽ラベル ≠ target選択
target degree ≠ concrete pitch
empty ≠ 探索全体の失敗
structural record ≠ concrete realization
Generic event ≠ Module状態の復元命令
```

途中にξが残っても、前後の接続は別々に検証・記述できる。この地図は各層を一つの因果法則へ圧縮しない。
