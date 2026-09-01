"""Melody-meter duration articulation probe for Music v0.2.

This fixture keeps melody, meter reference, onset positions, and note accent
schedule fixed while changing note duration / rest / overlap relations.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import math
from pathlib import Path
import wave

ROOT = Path(__file__).resolve().parents[2]
AUDIO_RELATIVE_PATH = "artifacts/audio/music_v02_melody_meter_duration_articulation_probe.wav"
MANIFEST_RELATIVE_PATH = "artifacts/json/music_v02_melody_meter_duration_articulation_probe.json"
SAMPLE_RATE = 44_100
BEAT_SECONDS = 0.42
PHRASE_GAP_SECONDS = 0.68
MELODY = ("C4", "D4", "E4", "G4", "E4", "D4", "C4", "G3")
ONSET_POSITIONS = tuple(float(index) for index in range(len(MELODY)))
NOTE_ACCENT_INDICES = (0, 4)
BEATS_PER_BAR = 4
DOWNBEAT_ORIGIN = 0

NOTE_FREQUENCIES = {
    "G3": 195.998,
    "C4": 261.626,
    "D4": 293.665,
    "E4": 329.628,
    "G4": 391.995,
}


@dataclass(frozen=True)
class DurationArticulationFrame:
    name: str
    note_duration_beats: float
    preserved_melody: tuple[str, ...]
    preserved_contour: tuple[int, ...]
    preserved_onset_positions: tuple[float, ...]
    preserved_note_accent_indices: tuple[int, ...]
    changed_relation: str
    structural_prediction: str
    perceptual_hypothesis: str
    actual_listening_observation: str | None
    candidate_classification: str

    @property
    def inter_onset_gap_beats(self) -> float:
        return 1.0 - self.note_duration_beats

    @property
    def articulation_kind(self) -> str:
        if self.note_duration_beats < 0.5:
            return "staccato_gap"
        if self.note_duration_beats < 1.0:
            return "detached_reference"
        if self.note_duration_beats == 1.0:
            return "connected_tenuto"
        return "overlap_legato"


def contour(notes: tuple[str, ...]) -> tuple[int, ...]:
    values = [NOTE_FREQUENCIES[note] for note in notes]
    result: list[int] = []
    for before, after in zip(values, values[1:]):
        result.append(1 if after > before else -1 if after < before else 0)
    return tuple(result)


def build_frames() -> list[DurationArticulationFrame]:
    preserved_contour = contour(MELODY)
    return [
        DurationArticulationFrame(
            name="detached_reference_same_onsets",
            note_duration_beats=0.72,
            preserved_melody=MELODY,
            preserved_contour=preserved_contour,
            preserved_onset_positions=ONSET_POSITIONS,
            preserved_note_accent_indices=NOTE_ACCENT_INDICES,
            changed_relation="reference detached duration with fixed onsets",
            structural_prediction="melody keeps clear onset identity while leaving short rests between notes",
            perceptual_hypothesis="listener may hear balanced articulation without strong gap or overlap pressure",
            actual_listening_observation=None,
            candidate_classification="duration_reference_candidate",
        ),
        DurationArticulationFrame(
            name="staccato_gap_same_onsets",
            note_duration_beats=0.36,
            preserved_melody=MELODY,
            preserved_contour=preserved_contour,
            preserved_onset_positions=ONSET_POSITIONS,
            preserved_note_accent_indices=NOTE_ACCENT_INDICES,
            changed_relation="short duration creates audible rest before next fixed onset",
            structural_prediction="same onset grid becomes segmented by inter-note silence",
            perceptual_hypothesis="listener may hear the melody as lighter or more fragmented",
            actual_listening_observation=None,
            candidate_classification="staccato_gap_candidate",
        ),
        DurationArticulationFrame(
            name="tenuto_connected_same_onsets",
            note_duration_beats=1.0,
            preserved_melody=MELODY,
            preserved_contour=preserved_contour,
            preserved_onset_positions=ONSET_POSITIONS,
            preserved_note_accent_indices=NOTE_ACCENT_INDICES,
            changed_relation="duration fills the inter-onset interval without changing onset grid",
            structural_prediction="same onset grid becomes connected without overlap",
            perceptual_hypothesis="listener may hear stronger melodic continuity",
            actual_listening_observation=None,
            candidate_classification="connected_tenuto_candidate",
        ),
        DurationArticulationFrame(
            name="overlap_legato_same_onsets",
            note_duration_beats=1.16,
            preserved_melody=MELODY,
            preserved_contour=preserved_contour,
            preserved_onset_positions=ONSET_POSITIONS,
            preserved_note_accent_indices=NOTE_ACCENT_INDICES,
            changed_relation="duration exceeds inter-onset interval and overlaps the next fixed onset",
            structural_prediction="same onset grid gains carry-over relation between neighboring notes",
            perceptual_hypothesis="listener may hear continuity or harmonic blur, pending actual observation",
            actual_listening_observation=None,
            candidate_classification="overlap_legato_candidate",
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


def add_note(
    samples: list[float],
    note: str,
    start_frame: int,
    duration_beats: float,
    accented: bool,
) -> None:
    duration = duration_beats * BEAT_SECONDS
    frames = int(SAMPLE_RATE * duration)
    amp = 0.33 if accented else 0.21
    for i in range(frames):
        pos = start_frame + i
        if pos < len(samples):
            samples[pos] += amp * sine_sample(NOTE_FREQUENCIES[note], i, duration)


def render_frame(frame: DurationArticulationFrame) -> list[int]:
    total_beats = len(frame.preserved_melody) + max(1.0, frame.note_duration_beats)
    total_frames = int(SAMPLE_RATE * (total_beats * BEAT_SECONDS + PHRASE_GAP_SECONDS))
    values = [0.0] * total_frames

    for beat in range(int(total_beats) + 1):
        downbeat = (beat - DOWNBEAT_ORIGIN) % BEATS_PER_BAR == 0
        add_click(values, int(beat * BEAT_SECONDS * SAMPLE_RATE), downbeat)

    for index, note in enumerate(frame.preserved_melody):
        start_frame = int(frame.preserved_onset_positions[index] * BEAT_SECONDS * SAMPLE_RATE)
        add_note(values, note, start_frame, frame.note_duration_beats, index in frame.preserved_note_accent_indices)

    return [int(max(-0.95, min(0.95, sample)) * 32767) for sample in values]


def frame_record(frame: DurationArticulationFrame) -> dict[str, object]:
    record = asdict(frame)
    record["articulation_kind"] = frame.articulation_kind
    record["inter_onset_gap_beats"] = frame.inter_onset_gap_beats
    return record


def write_wave(frames: list[DurationArticulationFrame], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    samples: list[int] = []
    for frame in frames:
        samples.extend(render_frame(frame))
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(b"".join(sample.to_bytes(2, "little", signed=True) for sample in samples))


def write_manifest(frames: list[DurationArticulationFrame], manifest_path: Path) -> None:
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema": "rdl_music_v02_melody_meter_duration_articulation_probe_v0_1",
        "subject": "melody_meter_duration_articulation_probe",
        "preserved_material": {
            "melody": list(MELODY),
            "contour": list(contour(MELODY)),
            "onset_positions": list(ONSET_POSITIONS),
            "note_accent_indices": list(NOTE_ACCENT_INDICES),
            "meter_reference": "4/4 click grid with downbeats at 0 and 4",
        },
        "frames": [frame_record(frame) for frame in frames],
        "device_audio_path": AUDIO_RELATIVE_PATH,
        "manifest_path": MANIFEST_RELATIVE_PATH,
        "stop_lines": [
            "duration_articulation_is_not_identical_to_onset_phase",
            "staccato_gap_is_not_deletion_of_melody_identity",
            "overlap_legato_is_not_harmonic_state_commitment",
            "click_track_is_device_fixture_not_human_meter_confirmation",
            "actual_listening_observation_remains_null_until_recorded",
        ],
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    frames = build_frames()
    expected_contour = contour(MELODY)
    assert all(frame.preserved_melody == MELODY for frame in frames)
    assert all(frame.preserved_contour == expected_contour for frame in frames)
    assert all(frame.preserved_onset_positions == ONSET_POSITIONS for frame in frames)
    assert all(frame.preserved_note_accent_indices == NOTE_ACCENT_INDICES for frame in frames)
    assert frames[1].inter_onset_gap_beats > frames[0].inter_onset_gap_beats
    assert frames[2].inter_onset_gap_beats == 0.0
    assert frames[3].inter_onset_gap_beats < 0.0
    assert all(frame.actual_listening_observation is None for frame in frames)
    audio_path = ROOT / AUDIO_RELATIVE_PATH
    manifest_path = ROOT / MANIFEST_RELATIVE_PATH
    write_wave(frames, audio_path)
    write_manifest(frames, manifest_path)
    print("music_v02_melody_meter_duration_articulation_probe_observed")
    for frame in frames:
        print(
            f"frame={frame.name}; duration={frame.note_duration_beats}; "
            f"gap={frame.inter_onset_gap_beats:.2f}; class={frame.candidate_classification}; "
            f"actual={frame.actual_listening_observation}"
        )
    print(f"device_audio_file={audio_path.name}")
    print(f"manifest_file={manifest_path.name}")


if __name__ == "__main__":
    main()
