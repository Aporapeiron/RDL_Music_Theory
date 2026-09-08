# Voice Placement / Crossing：最初の構造抽出

[少数聴取小括](../../10_Music_Validation/Voice_Placement/少数聴取小括.md)：指定Bへの注意指示後も別旋律が前景に出るとの報告あり。追跡自体は不確かなため、「追跡成功と別旋律の前景化が併存した」とは確定しない。

状態：device側の配置検証に加え、[初回会話聴取記録](../../10_Music_Validation/Voice_Placement/初回会話聴取記録.md)あり。混合と単独での聞こえに関する自己報告を保持するが、旋律帰属の切替位置・機序は未確定。

[二声の検証と音源](../../10_Music_Validation/Voice_Placement/README.md)では、Aを固定してB全体を12半音上げた。

保存したものは、声部ID、各声部の音程列・音高クラス列・onset・duration、合成パラメータ、AのPCM。変化したものは、Bの声域、垂直音程、瞬間の音高上下、絶対周波数配置である。

変更条件で上下が逆転するのは第4音と第7音。ここでも声部IDは再割当しない。

```text
voice ID
  != instantaneous upper/lower rank
pitch-order reversal
  != perceived melody attribution switch
preserved melodic intervals
  != preserved vertical intervals or register
```

オクターブ配置を変える比較は、交差だけを独立に操作した比較ではない。また同一合成設定も知覚音色の一致を保証しない。この連動を保持したまま、どの声部を追えるか、上下へ注意が移るかを聴取で記録する。

単独声部音源は材料確認に使えるが、それを聴くこと自体が後続の聴取履歴を変える。事前聴取の有無は別条件として残す。

現時点ではMusic CoreやC_relへの数値返却を行わない。Musicへ返す候補は、声部を音高順位で同定せず、旋律の系譜と現在の配置を別々に保持する記述である。

ここで保存した系譜は符号化された音列の系譜であり、知覚的な旋律同一性の保存は未確認である。聴取上の帰属が維持されたとしても、輪郭・隣接音程・提示履歴などが併存するため、関係履歴だけの効果と確定しない。

[聴取記録](../../10_Music_Validation/Voice_Placement/聴取記録テンプレート.md)では全イベントを同じ形式で記述する。反転位置以外の追跡困難や声部IDの対応未確定も残し、自己報告とdevice照合を分ける。
