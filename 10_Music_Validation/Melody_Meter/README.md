# Melody_Meter

旋律輪郭を保存したまま、拍節・アクセント配置を変えて、旋律同一性と拍節状態の非同一性を検証するMusic v0.2領域。

輪郭保存アクセント変位 最小ループ
: Music_v0.2_旋律拍節_輪郭保存アクセント変位_最小ループ.md / music_v02_melody_meter_identity_probe.py。

meter / accent / pickup 分離 最小ループ
: Music_v0.2_旋律拍節_meter_accent_pickup分離_最小ループ.md / music_v02_melody_meter_pickup_separation_probe.py。
  拍節参照、音符アクセント、弱起位置を分けて実音化する。

pre-roll付きpickup 最小ループ
: Music_v0.2_旋律拍節_preroll付きpickup_最小ループ.md / music_v02_melody_meter_preroll_pickup_probe.py。
  旋律開始前のmeter historyをclickで実音化し、local pickup offsetと分ける。

syncopation位相分離 最小ループ
: Music_v0.2_旋律拍節_syncopation位相分離_最小ループ.md / music_v02_melody_meter_syncopation_probe.py。
  meter referenceを固定したまま、note accent displacementとonset phase displacementを分ける。

duration articulation分離 最小ループ
: Music_v0.2_旋律拍節_duration_articulation分離_最小ループ.md / music_v02_melody_meter_duration_articulation_probe.py。
  onset位置、note accent、meter referenceを固定したまま、音価・余白・重なりを分ける。

duration articulation 実聴取前小括
: Music_v0.2_旋律拍節_duration_articulation_実聴取前小括.md。
  duration値を細分化せず、構造として返せる命題と実聴取まで保留する命題を分ける。

motif memory 最小ループ
: Music_v0.2_旋律拍節_motif_memory_最小ループ.md / music_v02_melody_meter_motif_memory_probe.py。
  同一motifの再帰時刻・拍節phase・介在材料を分け、motif-memory状態候補を検証する。
