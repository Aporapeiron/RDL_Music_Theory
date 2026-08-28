# 検証記録：alternative memory limit stress test 50工程

## 目的

899〜948で保持された alternative memory に対して、保持数が増えた場合の制限境界を検査する。

ここでは、memoryを無制限にactive保持し続けるのではなく、active view と compressed latent memory へ分ける。ただし、制限は削除・棄却・真理順位確定ではない。

## 949〜998 工程

949. 899〜948 update memory bundle を再利用する。
950. next ξ として alternative_memory_limit_stress を受け取る。
951. alternative memory が利用可能であることを再確認する。
952. memory expansion request を作る。
953. future context variant memory を追加する。
954. B shift variant memory を追加する。
955. policy comparison variant memory を追加する。
956. memory pressure を観測する。
957. limit policy request を作る。
958. limit を deletion と同一視しない。
959. limit を truth と同一視しない。
960. limit を final ranking と同一視しない。
961. max active entries を記録する。
962. active selection rule を記録する。
963. overflow handling を記録する。
964. inactive memory preservation を記録する。
965. reactivation permission を記録する。
966. deletes_overflow=False を記録する。
967. asserts_final_ranking=False を記録する。
968. active memory view を作る。
969. active memory count が上限内であることを確認する。
970. active memory reason を記録する。
971. compressed memory view を作る。
972. compressed memory がlabelを保持することを確認する。
973. compressed memory がreactivation targetを保持することを確認する。
974. compressed memory をerrorと同一視しない。
975. compressed memory をdeleted candidateと同一視しない。
976. limit bundle を作る。
977. source bundle を保持する。
978. stop lines を保持する。
979. generated_resolution=False を記録する。
980. generated_deletion=False を記録する。
981. limit と deletion の分離を確認する。
982. compression と reactivation の両立を確認する。
983. active memory がboundedであることを確認する。
984. inactive memory が保持されていることを確認する。
985. ranking と truth の分離を確認する。
986. limit と deletion の非同一性を保持する。
987. compression と rejection の非同一性を保持する。
988. priority と truth の非同一性を保持する。
989. active view と total memory の非同一性を保持する。
990. memory pressure を音楽的密度として保持する。
991. low priority をlatent readingとして保持する。
992. future reentry route を保持する。
993. limit policy summary を作る。
994. compression summary を作る。
995. no deletion summary を作る。
996. no truth summary を作る。
997. memory_reactivation_priority_next_candidate を次候補にする。
998. next ξ として xi_memory_reactivation_priority_stress を選択する。

## 観測結果

実装：`alternative_memory_limit_stress_949_998.py`

観測結果：

```text
alternative_memory_limit_949_998_observed_without_deleting_or_finalizing_memory
```

確認された保持条件：

- expanded memory は4件に増えた。
- active memory は2件に制限された。
- compressed memory は2件保持された。
- limit は deletion ではない。
- compression は reactivation target を保持する。
- ranking は truth assertion ではない。
- generated_deletion は発生していない。

## 意味

899〜948では、未選択候補をalternative memoryとして残せることを確認した。949〜998では、そのmemoryが増えたとき、すべてをactiveに置き続けるのではなく、active view と compressed latent memory に分ける境界を置いた。

音楽的には、現在の文脈で強く参照する候補と、後の文脈・B変化・policy比較で再活性化できる候補を分ける。これは候補削除ではなく、音楽的な読みの密度を管理する操作である。

## 停止線

```text
limit ≠ deletion
compression ≠ rejection
priority ≠ truth
active view ≠ total memory
inactive memory ≠ erased memory
```

## 次の ξ

```text
memory_reactivation_priority_stress
```
