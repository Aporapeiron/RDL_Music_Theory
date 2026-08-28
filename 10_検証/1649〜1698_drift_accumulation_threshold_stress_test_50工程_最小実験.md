# drift accumulation threshold stress test 1649〜1698 最小実験

## 目的

1599〜1648で観測したmemory driftが反復蓄積したとき、どこまで同一記憶の変形として扱い、どこから新しい候補として分けるべきかを検査する。

thresholdはtruthやforced selectionではない。ここでは、driftの蓄積圧力を観測し、同一性保持、境界曖昧性、新候補分岐を同時に残す。

## 50工程

1649. 1599〜1648のiterated reentry memory driftを再入する。
1650. next ξ としてdrift_accumulation_threshold_stressを受け取る。
1651. drift candidatesを再確認する。
1652. drift accumulation threshold requestを作る。
1653. thresholdをtruthと同一視しない。
1654. thresholdをforced selectionと同一視しない。
1655. thresholdをorigin deletionと同一視しない。
1656. drift threshold policyを記録する。
1657. soft threshold ruleを記録する。
1658. split threshold ruleを記録する。
1659. boundary ambiguity preservation ruleを記録する。
1660. forced selection false ruleを記録する。
1661. primary returned below thresholdを記録する。
1662. derivative returned boundary zoneを記録する。
1663. latent redeferred split zoneを記録する。
1664. identity anchorをcarryする。
1665. origin traceをcarryする。
1666. truth falseを記録する。
1667. forced selection falseを記録する。
1668. retained identity drift partitionを記録する。
1669. split candidate drift partitionを記録する。
1670. boundary zone drift partitionを記録する。
1671. partitionをdeletionと同一視しない。
1672. splitをrejectionと同一視しない。
1673. accumulation threshold viewを作る。
1674. identity retention viewを作る。
1675. candidate split viewを作る。
1676. boundary ambiguity viewを作る。
1677. drift accumulation threshold bundleを作る。
1678. source bundleをcarryする。
1679. stop linesをcarryする。
1680. generated forced selection falseを記録する。
1681. generated final truth falseを記録する。
1682. generated origin deletion falseを記録する。
1683. threshold candidates cover source driftsを確認する。
1684. retained / split pathsを確認する。
1685. boundary zone preservationを確認する。
1686. threshold not truth / selectionを確認する。
1687. origin trace across splitを確認する。
1688. thresholdとtruthを分離する。
1689. splitとrejectionを分離する。
1690. boundary zoneとdecisionを分離する。
1691. accumulationとresetを分離する。
1692. thresholdをrecognition pressureとして保持する。
1693. below thresholdをsame memory variationとして保持する。
1694. split zoneをnew musical candidateとして保持する。
1695. drift accumulation threshold summaryを作る。
1696. threshold without truth / forced selection summaryを作る。
1697. 次候補としてsplit candidate reintegrationを立てる。
1698. next ξ として xi_split_candidate_reintegration_stress を選択する。

## 観測結果

```text
drift_accumulation_threshold_1649_1698_observed_without_truth_or_forced_selection
```

## 停止線

```text
threshold ≠ truth
threshold ≠ forced selection
threshold ≠ origin deletion
split ≠ rejection
boundary zone ≠ decision
```

## 音楽的意味

driftが蓄積すると、同じ記憶の変形として聞き続けられる範囲と、別の音楽候補として立てるべき範囲が現れる。

ただし、その境界は真理判定ではない。境界曖昧性を残すことで、同一主題の変奏、別候補化、未確定の聞こえを同時に扱える。

## 次のξ

```text
split_candidate_reintegration_stress
```

