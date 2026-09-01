"""Split and reorder C6 / Am7 temporal-context fixtures.

The temporal-context probe puts four phrases in one WAV. This helper keeps the
same phrase definitions but exports each phrase separately and also creates two
order variants. The goal is to separate phrase-internal temporal context from
memory effects caused by the presentation order.
"""

from __future__ import annotations

from dataclasses import asdict
import importlib.util
import json
from pathlib import Path
import sys
from types import ModuleType

ROOT = Path(__file__).resolve().parents[2]
SOURCE_SCRIPT = Path(__file__).with_name("music_v02_c6_am7_temporal_context_probe.py")
MANIFEST_RELATIVE_PATH = "artifacts/json/music_v02_c6_am7_temporal_context_order_split.json"
AUDIO_DIR_RELATIVE_PATH = "artifacts/audio/c6_am7_temporal_context_order_split"

ORDER_VARIANTS = {
    "canonical_order": [
        "c_centered_frame",
        "a_centered_frame",
        "c_to_a_pivot_frame",
        "a_to_c_resistance_frame",
    ],
    "reversed_context_order": [
        "a_centered_frame",
        "c_centered_frame",
        "a_to_c_resistance_frame",
        "c_to_a_pivot_frame",
    ],
}


def load_temporal_probe() -> ModuleType:
    spec = importlib.util.spec_from_file_location("temporal_context_probe", SOURCE_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {SOURCE_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def phrase_by_name(phrases: list[object]) -> dict[str, object]:
    return {phrase.name: phrase for phrase in phrases}


def write_single_phrase_files(module: ModuleType, phrases: list[object], audio_dir: Path) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    audio_dir.mkdir(parents=True, exist_ok=True)
    for phrase in phrases:
        relative_path = f"{AUDIO_DIR_RELATIVE_PATH}/{phrase.name}.wav"
        module.write_wave([phrase], ROOT / relative_path)
        records.append(
            {
                "name": phrase.name,
                "audio_path": relative_path,
                "target_notes": list(phrase.target.notes),
                "changed_relation": phrase.changed_relation,
                "candidate_classification": phrase.candidate_classification,
                "actual_listening_observation": phrase.actual_listening_observation,
            }
        )
    return records


def write_order_variants(module: ModuleType, phrases: list[object]) -> list[dict[str, object]]:
    lookup = phrase_by_name(phrases)
    records: list[dict[str, object]] = []
    for variant_name, names in ORDER_VARIANTS.items():
        selected = [lookup[name] for name in names]
        relative_path = f"{AUDIO_DIR_RELATIVE_PATH}/{variant_name}.wav"
        module.write_wave(selected, ROOT / relative_path)
        records.append(
            {
                "name": variant_name,
                "phrase_order": names,
                "audio_path": relative_path,
                "presentation_memory_risk": "phrase order may affect the next phrase's listening context",
                "actual_listening_observation": None,
            }
        )
    return records


def write_manifest(single_files: list[dict[str, object]], order_variants: list[dict[str, object]]) -> None:
    manifest_path = ROOT / MANIFEST_RELATIVE_PATH
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema": "rdl_music_v02_c6_am7_temporal_context_order_split_v0_1",
        "subject": "C6_Am7_temporal_context_order_split",
        "source_probe": "10_Music_Validation/C6_Am7/music_v02_c6_am7_temporal_context_probe.py",
        "purpose": "separate phrase-internal temporal context from presentation-order memory effects",
        "single_phrase_files": single_files,
        "order_variants": order_variants,
        "manifest_path": MANIFEST_RELATIVE_PATH,
        "stop_lines": [
            "single_phrase_file_reduces_but_does_not_remove_listener_memory",
            "order_variant_tests_presentation_order_not_chord_truth",
            "actual_listening_observation_remains_null_until_recorded",
            "same_target_sonority_remains_identical_inside_each_phrase_definition",
        ],
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    module = load_temporal_probe()
    phrases = module.build_phrases()
    assert all(phrase.target.notes == module.TARGET_NOTES for phrase in phrases)
    assert all(phrase.actual_listening_observation is None for phrase in phrases)
    audio_dir = ROOT / AUDIO_DIR_RELATIVE_PATH
    single_files = write_single_phrase_files(module, phrases, audio_dir)
    order_variants = write_order_variants(module, phrases)
    write_manifest(single_files, order_variants)
    print("music_v02_c6_am7_temporal_context_order_split_observed")
    for record in single_files:
        print(f"single={record['name']}; audio={record['audio_path']}; actual={record['actual_listening_observation']}")
    for record in order_variants:
        print(f"variant={record['name']}; order={','.join(record['phrase_order'])}; audio={record['audio_path']}")
    print(f"manifest_file={Path(MANIFEST_RELATIVE_PATH).name}")


if __name__ == "__main__":
    main()
