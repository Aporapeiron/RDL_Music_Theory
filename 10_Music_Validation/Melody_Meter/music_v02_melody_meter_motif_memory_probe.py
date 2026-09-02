"""Melody-meter motif memory probe for Music v0.2.

This fixture keeps a short motif identical while changing the return timing and
the absence interval and the intervening material before the motif reappears.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import math
from pathlib import Path
import wave

ROOT = Path(__file__).resolve().parents[2]
AUDIO_RELATIVE_PATH = "artifacts/audio/music_v02_melody_meter_motif_memory_probe.wav"
MANIFEST_RELATIVE_PATH = "artifacts/json/music_v02_melody_meter_motif_memory_probe.json"
SAMPLE_RATE = 44_100
BEAT_SECONDS = 0.42
PHRASE_GAP_SECONDS = 0.72
MOTIF = ("C4", "D4", "E4", "G4")
MOTIF_DURATIONS = (1, 1, 1, 1)
NOTE_DURATION_BEATS = 0.72
BEATS_PER_BAR = 4
DOWNBEAT_ORIGIN = 0

NOTE_FREQUENCIES = {
    "G3": 195.998,
    "A3": 220.000,
    "B3": 246.942,
    "C4": 261.626,
    "D4": 293.665,
    "E4": 329.628,
    "F4": 349.228,
    "G4": 391.995,
    "A4": 440.000,
}


@dataclass(frozen=True)
class MotifMemoryFrame:
    name: str
    first_motif_start_beat: int
    return_motif_start_beat: int
    intervening_material: tuple[str, ...]
    intervening_durations: tuple[int, ...]
    preserved_motif: tuple[str, ...]
    preserved_motif_contour: tuple[int, ...]
    primary_interventions: tuple[str, ...]
    return_relation: str
    derived_relations: tuple[str, ...]
    memory_condition: str
    derived_memory_candidate: str
    structural_prediction: str
    perceptual_hypothesis: str
    actual_listening_observation: str | None
    candidate_classification: str

    @property
    def return_gap_beats(self) -> int:
        return self.return_motif_start_beat - (self.first_motif_start_beat + sum(MOTIF_DURATIONS))

    @property
    def return_phase(self) -> int:
        return (self.return_motif_start_beat - DOWNBEAT_ORIGIN) % BEATS_PER_BAR

    @property
    def absence_interval_beats(self) -> int:
        return self.return_gap_beats

    @property
    def intervening_duration_beats(self) -> int:
        return sum(self.intervening_durations)


def contour(notes: tuple[str, ...]) -> tuple[int, ...]:
    values = [NOTE_FREQUENCIES[note] for note in notes]
    result: list[int] = []
    for before, after in zip(values, values[1:]):
        result.append(1 if after > before else -1 if after < before else 0)
    return tuple(result)


def build_frames() -> list[MotifMemoryFrame]:
    preserved_contour = contour(MOTIF)
    return [
        MotifMemoryFrame(
            name="immediate_return_bar_aligned",
            first_motif_start_beat=0,
            return_motif_start_beat=4,
            intervening_material=(),
            intervening_durations=(),
            preserved_motif=MOTIF,
            preserved_motif_contour=preserved_contour,
            primary_interventions=("set return_motif_start_beat to 4", "set intervening_material to empty"),
            return_relation="motif returns immediately at next bar downbeat",
            derived_relations=("return_gap_beats = 0", "return_phase = 0", "intervening_duration_beats = 0"),
            memory_condition="fresh return with no intervening material",
            derived_memory_candidate="direct repetition candidate before actual listening",
            structural_prediction="direct-repetition structural candidate",
            perceptual_hypothesis="listener may hear confirmation or simple echo",
            actual_listening_observation=None,
            candidate_classification="immediate_repetition_candidate",
        ),
        MotifMemoryFrame(
            name="delayed_return_after_filler",
            first_motif_start_beat=0,
            return_motif_start_beat=8,
            intervening_material=("G4", "F4", "E4", "D4"),
            intervening_durations=(1, 1, 1, 1),
            preserved_motif=MOTIF,
            preserved_motif_contour=preserved_contour,
            primary_interventions=("set return_motif_start_beat to 8", "set intervening_material to descending filler"),
            return_relation="motif returns after one intervening 4-beat filler",
            derived_relations=("return_gap_beats = 4", "return_phase = 0", "intervening_duration_beats = 4"),
            memory_condition="motif is absent for one bar before reentry",
            derived_memory_candidate="delayed return candidate after motif absence",
            structural_prediction="delayed-return structural candidate after sounding filler",
            perceptual_hypothesis="listener may hear refrain-like return or phrase answer",
            actual_listening_observation=None,
            candidate_classification="delayed_motif_return_candidate",
        ),
        MotifMemoryFrame(
            name="delayed_return_after_silence",
            first_motif_start_beat=0,
            return_motif_start_beat=8,
            intervening_material=(),
            intervening_durations=(),
            preserved_motif=MOTIF,
            preserved_motif_contour=preserved_contour,
            primary_interventions=("set return_motif_start_beat to 8", "set intervening_material to silence"),
            return_relation="motif returns at bar downbeat after four beats of silence",
            derived_relations=("return_gap_beats = 4", "return_phase = 0", "intervening_duration_beats = 0"),
            memory_condition="motif is absent for one bar with no sounding filler",
            derived_memory_candidate="silent-gap delayed return candidate before actual listening",
            structural_prediction="delayed-return structural candidate after silent gap",
            perceptual_hypothesis="listener may hear a cleaner return or weaker retained connection",
            actual_listening_observation=None,
            candidate_classification="silent_gap_delayed_return_candidate",
        ),
        MotifMemoryFrame(
            name="offphase_return_after_filler",
            first_motif_start_beat=0,
            return_motif_start_beat=6,
            intervening_material=("G4", "F4"),
            intervening_durations=(1, 1),
            preserved_motif=MOTIF,
            preserved_motif_contour=preserved_contour,
            primary_interventions=("set return_motif_start_beat to 6", "set intervening_material to two-beat filler"),
            return_relation="motif returns before the next bar downbeat after shorter filler",
            derived_relations=("return_gap_beats = 2", "return_phase = 2", "intervening_duration_beats = 2"),
            memory_condition="motif returns while bar phase is displaced",
            derived_memory_candidate="offphase return candidate derived from return start time",
            structural_prediction="offphase-return structural candidate",
            perceptual_hypothesis="listener may hear return plus interruption or compression",
            actual_listening_observation=None,
            candidate_classification="offphase_motif_return_candidate",
        ),
        MotifMemoryFrame(
            name="transformed_filler_then_return",
            first_motif_start_beat=0,
            return_motif_start_beat=8,
            intervening_material=("A4", "G4", "E4", "C4"),
            intervening_durations=(1, 1, 1, 1),
            preserved_motif=MOTIF,
            preserved_motif_contour=preserved_contour,
            primary_interventions=("set return_motif_start_beat to 8", "set intervening_material to contrasting contour"),
            return_relation="motif returns at bar downbeat after contrasting contour",
            derived_relations=("return_gap_beats = 4", "return_phase = 0", "intervening_duration_beats = 4"),
            memory_condition="intervening material changes contour direction before return",
            derived_memory_candidate="contrast-supported return candidate before actual listening",
            structural_prediction="contrast-supported return structural candidate",
            perceptual_hypothesis="listener may hear stronger return because contrast precedes it",
            actual_listening_observation=None,
            candidate_classification="contrast_supported_motif_return_candidate",
        ),
    ]


def sine_sample(frequency: float, index: int, duration: float) -> float:
    t = index / SAMPLE_RATE
    attack = min(t / 0.014, 1.0)
    release = min((duration - t) / 0.045, 1.0)
    envelope = max(0.0, min(attack, release))
    return math.sin(2.0 * math.pi * frequency * t) * envelope


def click_sample(index: int, duration: float, downbeat: bool) -> float:
    t = index / SAMPLE_RATE
    if t > duration:
        return 0.0
    frequency = 1550.0 if downbeat else 1050.0
    decay = math.exp(-t * 55.0)
    amp = 0.24 if downbeat else 0.13
    return amp * math.sin(2.0 * math.pi * frequency * t) * decay


def add_click(samples: list[float], start_frame: int, downbeat: bool) -> None:
    click_frames = int(SAMPLE_RATE * 0.055)
    for i in range(click_frames):
        pos = start_frame + i
        if pos < len(samples):
            samples[pos] += click_sample(i, 0.055, downbeat)


def add_note(samples: list[float], note: str, start_beat: int, accented: bool = False) -> None:
    duration = NOTE_DURATION_BEATS * BEAT_SECONDS
    frames = int(SAMPLE_RATE * duration)
    start_frame = int(start_beat * BEAT_SECONDS * SAMPLE_RATE)
    amp = 0.34 if accented else 0.22
    for i in range(frames):
        pos = start_frame + i
        if pos < len(samples):
            samples[pos] += amp * sine_sample(NOTE_FREQUENCIES[note], i, duration)


def render_frame(frame: MotifMemoryFrame) -> list[int]:
    total_beats = frame.return_motif_start_beat + sum(MOTIF_DURATIONS) + 1
    total_frames = int(SAMPLE_RATE * (total_beats * BEAT_SECONDS + PHRASE_GAP_SECONDS))
    values = [0.0] * total_frames

    for beat in range(total_beats):
        downbeat = (beat - DOWNBEAT_ORIGIN) % BEATS_PER_BAR == 0
        add_click(values, int(beat * BEAT_SECONDS * SAMPLE_RATE), downbeat)

    beat = frame.first_motif_start_beat
    for index, note in enumerate(frame.preserved_motif):
        add_note(values, note, beat + index, accented=index == 0)

    beat = frame.first_motif_start_beat + sum(MOTIF_DURATIONS)
    for note, duration in zip(frame.intervening_material, frame.intervening_durations):
        add_note(values, note, beat, accented=False)
        beat += duration

    beat = frame.return_motif_start_beat
    for index, note in enumerate(frame.preserved_motif):
        add_note(values, note, beat + index, accented=index == 0)

    return [int(max(-0.95, min(0.95, sample)) * 32767) for sample in values]


def frame_record(frame: MotifMemoryFrame) -> dict[str, object]:
    record = asdict(frame)
    record["return_gap_beats"] = frame.return_gap_beats
    record["absence_interval_beats"] = frame.absence_interval_beats
    record["return_phase"] = frame.return_phase
    record["intervening_duration_beats"] = frame.intervening_duration_beats
    return record


def write_wave(frames: list[MotifMemoryFrame], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    samples: list[int] = []
    for frame in frames:
        samples.extend(render_frame(frame))
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(b"".join(sample.to_bytes(2, "little", signed=True) for sample in samples))


def write_manifest(frames: list[MotifMemoryFrame], manifest_path: Path) -> None:
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema": "rdl_music_v02_melody_meter_motif_memory_probe_v0_1",
        "subject": "melody_meter_motif_memory_probe",
        "preserved_material": {
            "motif": list(MOTIF),
            "motif_durations": list(MOTIF_DURATIONS),
            "motif_contour": list(contour(MOTIF)),
            "meter_reference": "4/4 click grid with downbeat origin 0",
        },
        "frames": [frame_record(frame) for frame in frames],
        "device_audio_path": AUDIO_RELATIVE_PATH,
        "manifest_path": MANIFEST_RELATIVE_PATH,
        "stop_lines": [
            "same_motif_material_is_not_same_memory_candidate_state",
            "return_timing_is_not_identical_to_motif_identity",
            "return_phase_is_derived_from_return_start_time_under_fixed_meter",
            "return_gap_is_derived_from_return_start_time_and_motif_end",
            "return_start_time_entails_required_absence_interval_under_this_fixture",
            "absence_interval_is_not_identical_to_sounding_intervening_material",
            "motif_memory_candidate_state_is_conditioned_not_equated",
            "intervening_material_is_not_erasure_of_motif_memory",
            "motif_return_candidate_is_not_actual_refrain_perception",
            "click_track_is_device_fixture_not_human_meter_confirmation",
            "actual_listening_observation_remains_null_until_recorded",
        ],
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    frames = build_frames()
    expected_contour = contour(MOTIF)
    assert all(frame.preserved_motif == MOTIF for frame in frames)
    assert all(frame.preserved_motif_contour == expected_contour for frame in frames)
    assert frames[0].return_gap_beats == 0
    assert frames[1].return_gap_beats == 4
    assert frames[2].name == "delayed_return_after_silence"
    assert frames[2].return_gap_beats == 4
    assert frames[2].intervening_duration_beats == 0
    assert frames[3].return_phase == 2
    assert frames[4].return_gap_beats == 4
    assert all(frame.actual_listening_observation is None for frame in frames)
    audio_path = ROOT / AUDIO_RELATIVE_PATH
    manifest_path = ROOT / MANIFEST_RELATIVE_PATH
    write_wave(frames, audio_path)
    write_manifest(frames, manifest_path)
    print("music_v02_melody_meter_motif_memory_probe_observed")
    for frame in frames:
        print(
            f"frame={frame.name}; return_gap={frame.return_gap_beats}; "
            f"return_phase={frame.return_phase}; class={frame.candidate_classification}; "
            f"actual={frame.actual_listening_observation}"
        )
    print(f"device_audio_file={audio_path.name}")
    print(f"manifest_file={manifest_path.name}")


if __name__ == "__main__":
    main()
