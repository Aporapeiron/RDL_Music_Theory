# split candidate reintegration stress test 1699〜1748 最小実験

## 目的

1649〜1698でsplit zoneに入った候補が、後続文脈で再統合されうるか、あるいは独立候補として残るかを検査する。

reintegrationはforced unificationではない。split candidateはrejectionでも失敗でもなく、origin traceを持ったまま、文脈次第で戻れる候補として保持される。

## 50工程

1699. 1649〜1698のdrift accumulation thresholdを再入する。
1700. next ξ としてsplit_candidate_reintegration_stressを受け取る。
1701. threshold candidatesを再確認する。
1702. split candidate reintegration requestを作る。
1703. reintegrationをrejectionと同一視しない。
1704. reintegrationをforced unificationと同一視しない。
1705. reintegrationをorigin deletionと同一視しない。
1706. split reintegration policyを記録する。
1707. split candidate acceptance ruleを記録する。
1708. contextual reintegration permissionを記録する。
1709. independent retention permissionを記録する。
1710. boundary ambiguity preservation ruleを記録する。
1711. below threshold reintegration candidateを記録する。
1712. boundary zone reintegration candidateを記録する。
1713. split zone reintegration candidateを記録する。
1714. split traceをcarryする。
1715. origin traceをcarryする。
1716. forced unification falseを記録する。
1717. split rejection falseを記録する。
1718. contextual reintegration partitionを記録する。
1719. independent retention partitionを記録する。
1720. ambiguous reintegration partitionを記録する。
1721. partitionをfinal mergeと同一視しない。
1722. independent retentionをfailureと同一視しない。
1723. split candidate reintegration viewを作る。
1724. contextual merge viewを作る。
1725. independent candidate viewを作る。
1726. ambiguous reintegration viewを作る。
1727. split candidate reintegration bundleを作る。
1728. source bundleをcarryする。
1729. stop linesをcarryする。
1730. generated forced unification falseを記録する。
1731. generated split rejection falseを記録する。
1732. generated origin deletion falseを記録する。
1733. split and retained candidates carriedを確認する。
1734. contextual / independent pathsを確認する。
1735. split trace preservationを確認する。
1736. reintegration not forced unificationを確認する。
1737. no rejection / origin deletionを確認する。
1738. reintegrationとforced unificationを分離する。
1739. split candidateとrejectionを分離する。
1740. independent retentionとfailureを分離する。
1741. contextual mergeとfinal mergeを分離する。
1742. reintegrationをlater context recognitionとして保持する。
1743. split candidateをreturnable motifとして保持する。
1744. independent candidateをparallel memoryとして保持する。
1745. split candidate reintegration summaryを作る。
1746. no forced unification / no rejection summaryを作る。
1747. 次候補としてreintegration context pressureを立てる。
1748. next ξ として xi_reintegration_context_pressure_stress を選択する。

## 観測結果

```text
split_candidate_reintegration_1699_1748_observed_without_forced_unification_or_rejection
```

## 停止線

```text
reintegration ≠ rejection
reintegration ≠ forced unification
reintegration ≠ origin deletion
independent retention ≠ failure
contextual merge ≠ final merge
```

## 音楽的意味

driftによって別候補化した記憶は、捨てられるわけではない。

後続文脈が十分に近ければ再統合され、まだ曖昧なら保留され、別の聞こえとして強いなら独立候補として残る。ここで重要なのは、どの経路でもorigin traceを消さないことである。

## 次のξ

```text
reintegration_context_pressure_stress
```

