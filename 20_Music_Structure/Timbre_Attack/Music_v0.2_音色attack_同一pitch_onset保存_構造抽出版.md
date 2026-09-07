# Music v0.2 音色 / attack 同一pitch-onset保存 構造抽出版

## 0. 抽出対象

```text
10_Music_Validation/Timbre_Attack/Music_v0.2_音色attack_同一pitch_onset保存_最小ループ.md
10_Music_Validation/Timbre_Attack/music_v02_timbre_attack_identity_probe.py
artifacts/json/music_v02_timbre_attack_identity_probe.json
```

## 1. 抽出主題

同じpitch、onset、durationを保存しても、attack envelopeとharmonic profileが変われば音色・発音状態候補は変わる。

```text
same pitch-onset-duration material
  ≠ same timbre-attack candidate state
```

## 2. 保存されるもの

```text
pitches:
  C4 E4 G4 C5

onsets:
  0 1 2 3

duration:
  0.82 beats

note_order:
  C4 E4 G4 C5
```

## 3. 変化するもの

```text
primary_interventions:
  attack envelope
  harmonic profile
  non-harmonic transient spectrum
  total rendered spectrum
  attack transient noise

derived_descriptors:
  attack slope proxy
  harmonic brightness proxy
  harmonic count
  plateau seconds
  encoded onset positions
```

## 4. 候補状態

```text
soft_sine_reference:
  soft_attack_low_brightness_candidate

sharp_attack_same_harmonic_profile:
  attack_changed_harmonic_profile_preserved_candidate

bright_harmonic_profile_same_attack:
  harmonic_profile_changed_attack_preserved_candidate

noise_only_same_attack_harmonic_profile:
  noise_changed_attack_harmonic_profile_preserved_candidate

transient_noise_attack:
  attack_and_harmonic_profile_changed_candidate
```

## 5. Music Core v0.2へ返す命題

```text
attack envelope
  ≠ encoded signal onset time
  may affect perceived / effective onset

harmonic profile
  ≠ pitch identity in this fixture

non-harmonic transient spectrum
  changes total rendered spectrum even when harmonic profile is held

total rendered spectrum
  ≠ harmonic profile alone

transient noise
  can be varied while attack duration and spectrum are held
  = attack color fixture
  ≠ actual listener confirmation
```

同じ音列でも、音の入り方と倍音分布が変わると、timbre-attack候補状態は変わる。ただし、encoded onset保存はperceived onset保存を意味しない。またattack duration変更は、同じ総duration内のplateau時間とエネルギー分布を派生的に変える。transient noiseを足すと、harmonic profileは保存されてもtotal rendered spectrumは変わる。現段階では聴取上の楽器感・硬さ・明るさを確定しない。

## 6. melody / meter 系列からの差分

```text
melody / meter:
  temporal placement relation
  onset / duration / return

timbre / attack:
  within-event formation relation
  attack envelope / harmonic profile / non-harmonic transient / total rendered spectrum
  encoded onset vs perceived onset
  plateau / energy distribution
```

ここで扱う関係は、音事象がいつ置かれるかではなく、置かれた音事象が開始直後にどのような形で形成されるかである。

## 7. 停止線

```text
same_pitch_onset_duration_is_not_same_timbre_attack_candidate_state
attack_envelope_is_not_identical_to_harmonic_profile
encoded_signal_onset_is_not_identical_to_perceived_onset
attack_duration_change_entails_energy_distribution_and_plateau_change
transient_noise_can_be_varied_without_attack_duration_or_harmonic_profile_change
transient_noise_changes_total_rendered_spectrum_even_when_harmonic_profile_is_held
harmonic_profile_change_is_not_pitch_change_in_this_fixture
transient_noise_is_attack_color_fixture_not_listener_confirmation
harmonic_brightness_proxy_describes_harmonic_profile_not_full_rendered_spectrum
harmonic_brightness_proxy_is_not_perceptual_brightness
device_audio_generation_is_not_actual_listening_observation
actual_listening_observation_remains_null_until_recorded
```

この抽出は、実聴取上の音色知覚を断定しない。現段階では、同一pitch-onset-durationを実聴取へ渡すためのtimbre / attack fixtureである。