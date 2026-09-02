# Music v0.2 検証記録：音色 / attack 同一pitch-onset保存 最小ループ

*状態：DRAFT v0.1 / motif memory実聴取前小括後の次対象*
*実装：`10_Music_Validation/Timbre_Attack/music_v02_timbre_attack_identity_probe.py`*

## 0. 目的

C6 / Am7では和声関係、旋律×拍節では時間関係を扱った。今回は、同じ音高・開始時刻・長さを保存したまま、attack envelope と spectrum を変える。

```text
same pitch
+ same onset
+ same duration
  ≠ same timbre-attack candidate state
```

## 1. 境界B

```text
B_timbre_attack_identity_probe:
  preserved_pitches = C4 E4 G4 C5
  preserved_onsets = 0 1 2 3
  preserved_duration = 0.82 beats
  preserved_note_order = C4 E4 G4 C5
  primary_interventions:
    attack envelope
    harmonic spectrum
    attack transient noise
  derived_descriptors:
    attack slope proxy
    brightness proxy
    harmonic count
    plateau seconds
    encoded onset positions
```

ここで保存するのは、pitch / onset / duration / orderである。変えるのは音色を作るattack envelope、harmonic spectrum、attack transient noiseである。

## 2. 検証状態

### 2.1 soft_sine_reference

```text
attack_seconds = 0.09
harmonic_profile = fundamental only
transient_noise = 0
classification = soft_attack_low_brightness_candidate
```

基準状態。柔らかい立ち上がりと最小spectrumを持つ。

### 2.2 sharp_attack_same_spectrum

```text
attack_seconds = 0.008
harmonic_profile = fundamental only
transient_noise = 0
classification = attack_changed_spectrum_preserved_candidate
```

spectrumを保ったままattack envelopeだけを短くする。

### 2.3 bright_spectrum_same_attack

```text
attack_seconds = 0.09
harmonic_profile = upper harmonics added
transient_noise = 0
classification = spectrum_changed_attack_preserved_candidate
```

attack envelopeを保ったままspectrumだけを明るくする。

### 2.4 noise_only_same_attack_spectrum

```text
attack_seconds = 0.09
harmonic_profile = fundamental only
transient_noise > 0
classification = noise_changed_attack_spectrum_preserved_candidate
```

attack envelopeとspectrumを保ったまま、transient noiseだけを加える。noise単独の比較条件である。

### 2.5 transient_noise_attack

```text
attack_seconds = 0.008
harmonic_profile = upper harmonics added
transient_noise > 0
classification = attack_and_spectrum_changed_candidate
```

attack envelope、spectrum、transient noiseを同時に変えた複合条件である。noise-only controlとは異なり、noise単独の効果としては扱わない。

## 3. 生成artifact

```text
artifacts/audio/music_v02_timbre_attack_identity_probe.wav
artifacts/json/music_v02_timbre_attack_identity_probe.json
```

音声は5状態を順に鳴らすdevice-side fixtureである。

## 4. 実聴取slot

今回も `actual_listening_observation = null` として保持する。

```text
structural prediction
  ≠ perceptual hypothesis
  ≠ actual listening observation
```

実際に丸い、硬い、明るい、打撃的などとして聞こえるかは、actual listeningで別に記録する。

## 5. Music上の仮説

```text
same pitch-onset-duration material
+ changed attack envelope
+ changed harmonic spectrum
+ optional attack transient
+ derived plateau / energy distribution
-> different timbre-attack candidate state
```

attackはencoded signal onsetそのものではなく、開始直後のエネルギー形状である。ただし、perceived / effective onsetが同一に聞こえるとはまだ言わない。attack durationを変えると、同じ総duration内でplateau時間とエネルギー分布も派生的に変わる。spectrumはpitch変更ではなく、同じ基音に対する倍音分布の変更として扱う。

## 6. 停止線

```text
same_pitch_onset_duration_is_not_same_timbre_attack_candidate_state
attack_envelope_is_not_identical_to_spectrum
encoded_signal_onset_is_not_identical_to_perceived_onset
attack_duration_change_entails_energy_distribution_and_plateau_change
transient_noise_can_be_varied_without_attack_duration_or_spectrum_change
spectrum_change_is_not_pitch_change_in_this_fixture
transient_noise_is_attack_color_fixture_not_listener_confirmation
brightness_proxy_is_fixture_descriptor_not_universal_timbre_constant
device_audio_generation_is_not_actual_listening_observation
actual_listening_observation_remains_null_until_recorded
```