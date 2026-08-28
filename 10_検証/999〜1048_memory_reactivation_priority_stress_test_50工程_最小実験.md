# 検証記録：memory reactivation priority stress test 50工程

## 目的

949〜998で compressed latent memory として保持された候補が、どの条件で active view へ戻るかを検査する。

ここでは、再活性化を selection、truth、deletion、単純反復へ同一視しない。特に、リフレイン的回帰を repetition ではなく、文脈変化を伴う memory return として扱う。

## 999〜1048 工程

999. 949〜998 memory limit bundle を再利用する。
1000. next ξ として memory_reactivation_priority_stress を受け取る。
1001. compressed memory が利用可能であることを再確認する。
1002. context shift trigger request を作る。
1003. B shift trigger request を作る。
1004. cadential return trigger request を作る。
1005. trigger の音楽的理由を記録する。
1006. trigger を truth と同一視しない。
1007. trigger を repetition と同一視しない。
1008. trigger を selection と同一視しない。
1009. reactivation priority request を作る。
1010. priority delta request を作る。
1011. compressed memory evaluation request を作る。
1012. altered B memory を評価する。
1013. policy audit memory を評価する。
1014. priority score を記録する。
1015. reactivation target を記録する。
1016. reinterpretation flag を記録する。
1017. selection=False を記録する。
1018. deletion=False を記録する。
1019. promoted memory view を作る。
1020. selectionなしのactive returnを記録する。
1021. refrain return を観測する。
1022. refrain と repetition の分離を確認する。
1023. remaining latent memory view を作る。
1024. latent remainder を rejection と同一視しない。
1025. latent remainder を deletion と同一視しない。
1026. reactivation priority bundle を作る。
1027. source bundle を保持する。
1028. stop lines を保持する。
1029. generated_selection=False を記録する。
1030. generated_repetition_identity=False を記録する。
1031. generated_deletion=False を記録する。
1032. compressed memory の再考を確認する。
1033. reactivation と selection の分離を確認する。
1034. refrain と repetition の分離を確認する。
1035. reinterpretation の保持を確認する。
1036. latent remainder の保持を確認する。
1037. reactivation と selection の非同一性を保持する。
1038. refrain と repetition の非同一性を保持する。
1039. priority と truth の非同一性を保持する。
1040. promotion と deletion の非同一性を保持する。
1041. return を refrain として保持する。
1042. latent memory を heard absence として保持する。
1043. contextual return difference を保持する。
1044. reactivation priority summary を作る。
1045. refrain non-repetition summary を作る。
1046. no selection / no deletion summary を作る。
1047. refrain_identity_boundary_next_candidate を次候補にする。
1048. next ξ として xi_refrain_identity_boundary_stress を選択する。

## 観測結果

実装：`memory_reactivation_priority_stress_999_1048.py`

観測結果：

```text
memory_reactivation_priority_999_1048_observed_without_selection_or_repetition_collapse
```

確認された保持条件：

- compressed memory は再考された。
- reactivation は selection ではない。
- refrain は repetition ではない。
- promoted memory は reinterpretation を保持する。
- remaining latent memory は削除されない。
- generated_selection / generated_repetition_identity / generated_deletion は発生していない。

## 意味

949〜998では、memory pressure によって一部候補を compressed latent memory へ回した。999〜1048では、その潜在memoryが B shift と cadential context によって再び active view へ戻る条件を観測した。

音楽的には、以前の読みが戻ってくることは、単純に同じものが反復されることではない。戻ってきた候補は、以前の状態を引きずりながら、現在の文脈によって再解釈される。このため、refrain は repetition ではなく、文脈差を持つ回帰として扱う。

## 停止線

```text
reactivation ≠ selection
refrain ≠ repetition
priority ≠ truth
promotion ≠ deletion
latent remainder ≠ rejection
```

## 次の ξ

```text
refrain_identity_boundary_stress
```
