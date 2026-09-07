# 70_T2_Extraction

Music検証から外へ出る汎用構造候補を置く領域。

旧整理では、ここに `T2候補`、`Metabolic Runtime`、`candidate lifecycle`、`selection controller` などを置いていた。新T0/T1基準では、それらをそのままT2へ昇格させない。

再分類責務:

```text
旧T2候補
  -> T1工程
  -> T2汎用検査道具
  -> Music固有Selection基準
  -> Music↔汎用fixture
  -> historical evidence
```

新T1/T2での暫定配置:

```text
T1:
  Probe
  Expansion
  Inspection
  Selection
  Reconstruction

T2:
  SelectionやInspectionに使う汎用検査道具候補

Music設計:
  Probeの具体実装
  Selection基準
  許容損失
  生成・再聴取fixture
```

したがって、`Metabolic Runtime` 全体や `selection -> commitment -> record` 系列を、丸ごと正式T2とは扱わない。非Music対象でも残るか、またT1工程とT2道具のどちらに属するかを再判定するまでは、このrepo内のExtraction Zoneとして保持する。
