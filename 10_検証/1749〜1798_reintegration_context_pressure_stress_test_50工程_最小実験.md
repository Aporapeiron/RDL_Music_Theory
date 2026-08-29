# reintegration context pressure stress test 1749〜1798 最小実験

## 目的

1699〜1748で保持したsplit candidate reintegrationに対して、後続文脈がどの程度再統合を促すかを検査する。

context pressureはdecisionでもtruthでもない。弱・中・強の圧力を観測しつつ、forced reintegration、context truth、independent path deletionを止める。

## 50工程

1749. 1699〜1748のsplit candidate reintegrationを再入する。
1750. next ξ としてreintegration_context_pressure_stressを受け取る。
1751. reintegration candidatesを再確認する。
1752. reintegration context pressure requestを作る。
1753. pressureをforced reintegrationと同一視しない。
1754. pressureをcontext truthと同一視しない。
1755. pressureをindependent deletionと同一視しない。
1756. context pressure policyを記録する。
1757. weak pressure acceptance ruleを記録する。
1758. medium pressure acceptance ruleを記録する。
1759. strong pressure acceptance ruleを記録する。
1760. ambiguity under pressure preservation ruleを記録する。
1761. contextual reintegration weak pressureを記録する。
1762. ambiguous reintegration medium pressureを記録する。
1763. independent candidate strong pressureを記録する。
1764. candidate traceをcarryする。
1765. context traceをcarryする。
1766. forced reintegration falseを記録する。
1767. independent deletion falseを記録する。
1768. weak pressure partitionを記録する。
1769. medium pressure partitionを記録する。
1770. strong pressure partitionを記録する。
1771. partitionをdecisionと同一視しない。
1772. strong pressureをforced mergeと同一視しない。
1773. context pressure viewを作る。
1774. weak context viewを作る。
1775. medium ambiguity viewを作る。
1776. strong parallel path viewを作る。
1777. reintegration context pressure bundleを作る。
1778. source bundleをcarryする。
1779. stop linesをcarryする。
1780. generated forced reintegration falseを記録する。
1781. generated independent path deletion falseを記録する。
1782. generated context truth falseを記録する。
1783. pressure candidates coverを確認する。
1784. pressure levels preservationを確認する。
1785. candidate / context traceを確認する。
1786. pressure not forced reintegrationを確認する。
1787. no deletion / context truthを確認する。
1788. pressureとdecisionを分離する。
1789. strong pressureとforced mergeを分離する。
1790. context traceとtruthを分離する。
1791. independent pathとdeletionを分離する。
1792. pressureをcontextual pullとして保持する。
1793. medium pressureをambiguous hearingとして保持する。
1794. strong pressureをreturn invitationとして保持する。
1795. reintegration context pressure summaryを作る。
1796. pressure without forced merge summaryを作る。
1797. 次候補としてcontext pressure selection delayを立てる。
1798. next ξ として xi_context_pressure_selection_delay_stress を選択する。

## 観測結果

```text
reintegration_context_pressure_1749_1798_observed_without_forced_merge_or_context_truth
```

## 停止線

```text
pressure ≠ forced reintegration
pressure ≠ context truth
pressure ≠ independent path deletion
strong pressure ≠ forced merge
context trace ≠ truth
```

## 音楽的意味

後続文脈は、候補を再統合へ引く力を持つ。ただし、その力は決定そのものではない。

弱い圧力は同一文脈内の継続として残り、中程度の圧力は曖昧な聞こえを保留し、強い圧力は戻りを促す。しかし強く促しても、独立候補を削除したり、強制的に統合したりはしない。

## 次のξ

```text
context_pressure_selection_delay_stress
```

