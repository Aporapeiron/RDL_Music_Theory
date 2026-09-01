# C6_Am7

同一音集合 `{C,E,G,A}` を保存したまま、低音・配置・文脈の関係を変えて、C6 / Am7方向の状態候補を生成・再聴取するMusic v0.2最小ループ。

`F_device` 側の音声生成と、`F_human` 側の実聴取確認を同一視しない。
## 現在の検証

```text
保存・変化・生成・再聴取 最小ループ
  C6候補からAm7方向候補への基本遷移を作る。

介入分離 最小ループ
  context only / register only / bass primary / full tiltを分け、primary interventionとresidual changesを記録する。
```

関係重みプローブ 最小ループ
: Music_v0.2_C6_Am7_関係重みプローブ_最小ループ.md / music_v02_c6_am7_relation_weight_probe.py。
  同一音集合を保存したまま、bass / register / context がAm7方向の構造圧をどう変えるか比較する。
