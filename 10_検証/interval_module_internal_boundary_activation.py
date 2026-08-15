"""音程Module boundary inputと内部B/Gamma接続境界の最小検証。

69で得たinterval module boundary input candidateを固定し、外部payloadと
B_chromatic / B_spelling / Gamma_interval_processing_frameを与えた場合だけ
interval module processing frame candidateが生じることを確認する。

ここではgeneric interval、quality、interval labelは生成しない。

    interval module boundary input candidate
      + pitch relation payload fixture
      + B_chromatic_fixture
      + B_spelling_fixture
      + Gamma_interval_processing_frame_fixture
      -> interval module processing frame candidate
      -> interval label remains None
"""

from dataclasses import dataclass

from base_to_interval_module_reception_boundary import (
    IntervalModuleReceptionObservation,
    compare_interval_module_reception,
)


@dataclass(frozen=True)
class PitchRelationPayload:
    name: str
    lower_note: str
    upper_note: str
    chromatic_distance: int
    spelling_pair: tuple[str, str]
    generated_by_boundary_input: bool


@dataclass(frozen=True)
class IntervalInternalBoundary:
    name: str
    readable_field: str
    rule_scope: str


@dataclass(frozen=True)
class IntervalProcessingFrameGamma:
    name: str
    reads: tuple[str, str, str, str]
    rule_scope: str


@dataclass(frozen=True)
class IntervalModuleProcessingFrameCandidate:
    label: str
    source_boundary_input_label: str
    payload_name: str
    chromatic_distance_available: bool
    spelling_pair_available: bool
    generic_interval_generated: bool
    quality_generated: bool
    interval_label_generated: bool
    contextual_role_generated: bool


@dataclass(frozen=True)
class IntervalInternalActivationObservation:
    reception_observation: IntervalModuleReceptionObservation
    pitch_payload: PitchRelationPayload | None
    b_chromatic: IntervalInternalBoundary | None
    b_spelling: IntervalInternalBoundary | None
    processing_gamma: IntervalProcessingFrameGamma | None
    processing_frame: IntervalModuleProcessingFrameCandidate | None
    generic_interval_generated: bool
    quality_generated: bool
    interval_label_generated: bool
    contextual_role_generated: bool
    core_promoted: bool
    status: str
    activation_reason: str | None


@dataclass(frozen=True)
class IntervalInternalActivationComparison:
    without_gamma: IntervalInternalActivationObservation
    with_gamma: IntervalInternalActivationObservation
    same_boundary_input: bool
    same_pitch_payload: bool
    same_b_chromatic: bool
    same_b_spelling: bool
    same_processing_gamma: bool
    processing_frame_observed: bool
    generic_interval_generated: bool
    quality_generated: bool
    interval_label_generated: bool
    contextual_role_generated: bool
    core_promoted: bool


def interval_reception_observation() -> IntervalModuleReceptionObservation:
    return compare_interval_module_reception().with_gamma


def pitch_relation_payload_fixture() -> PitchRelationPayload:
    return PitchRelationPayload(
        name="pitch_relation_payload_C4_G4_fixture",
        lower_note="C4",
        upper_note="G4",
        chromatic_distance=7,
        spelling_pair=("C", "G"),
        generated_by_boundary_input=False,
    )


def b_chromatic_fixture() -> IntervalInternalBoundary:
    return IntervalInternalBoundary(
        name="B_chromatic_fixture",
        readable_field="chromatic_distance",
        rule_scope="fixture_limited_not_general_chromatic_boundary",
    )


def b_spelling_fixture() -> IntervalInternalBoundary:
    return IntervalInternalBoundary(
        name="B_spelling_fixture",
        readable_field="spelling_pair",
        rule_scope="fixture_limited_not_general_spelling_boundary",
    )


def interval_processing_frame_gamma() -> IntervalProcessingFrameGamma:
    return IntervalProcessingFrameGamma(
        name="Gamma_interval_processing_frame_fixture",
        reads=(
            "interval_module_boundary_input",
            "pitch_relation_payload",
            "B_chromatic",
            "B_spelling",
        ),
        rule_scope="fixture_limited_not_Gamma_generic_quality_or_label",
    )


def activate_interval_internal_frame(
    reception_observation: IntervalModuleReceptionObservation,
    pitch_payload: PitchRelationPayload | None,
    b_chromatic: IntervalInternalBoundary | None,
    b_spelling: IntervalInternalBoundary | None,
    processing_gamma: IntervalProcessingFrameGamma | None,
) -> IntervalInternalActivationObservation:
    boundary_input = reception_observation.interval_boundary_input
    if boundary_input is None:
        return IntervalInternalActivationObservation(
            reception_observation=reception_observation,
            pitch_payload=pitch_payload,
            b_chromatic=b_chromatic,
            b_spelling=b_spelling,
            processing_gamma=processing_gamma,
            processing_frame=None,
            generic_interval_generated=False,
            quality_generated=False,
            interval_label_generated=False,
            contextual_role_generated=False,
            core_promoted=False,
            status="no_interval_module_boundary_input",
            activation_reason=None,
        )

    if pitch_payload is None:
        return IntervalInternalActivationObservation(
            reception_observation=reception_observation,
            pitch_payload=None,
            b_chromatic=b_chromatic,
            b_spelling=b_spelling,
            processing_gamma=processing_gamma,
            processing_frame=None,
            generic_interval_generated=False,
            quality_generated=False,
            interval_label_generated=False,
            contextual_role_generated=False,
            core_promoted=False,
            status="boundary_input_not_connected_without_payload",
            activation_reason=None,
        )

    if b_chromatic is None or b_spelling is None:
        return IntervalInternalActivationObservation(
            reception_observation=reception_observation,
            pitch_payload=pitch_payload,
            b_chromatic=b_chromatic,
            b_spelling=b_spelling,
            processing_gamma=processing_gamma,
            processing_frame=None,
            generic_interval_generated=False,
            quality_generated=False,
            interval_label_generated=False,
            contextual_role_generated=False,
            core_promoted=False,
            status="boundary_input_not_connected_without_internal_boundary",
            activation_reason=None,
        )

    if processing_gamma is None:
        return IntervalInternalActivationObservation(
            reception_observation=reception_observation,
            pitch_payload=pitch_payload,
            b_chromatic=b_chromatic,
            b_spelling=b_spelling,
            processing_gamma=None,
            processing_frame=None,
            generic_interval_generated=False,
            quality_generated=False,
            interval_label_generated=False,
            contextual_role_generated=False,
            core_promoted=False,
            status="boundary_input_not_connected_without_processing_gamma",
            activation_reason=None,
        )

    if b_chromatic.readable_field != "chromatic_distance":
        status = "boundary_input_not_connected_without_chromatic_field"
    elif b_spelling.readable_field != "spelling_pair":
        status = "boundary_input_not_connected_without_spelling_field"
    else:
        status = ""

    if status:
        return IntervalInternalActivationObservation(
            reception_observation=reception_observation,
            pitch_payload=pitch_payload,
            b_chromatic=b_chromatic,
            b_spelling=b_spelling,
            processing_gamma=processing_gamma,
            processing_frame=None,
            generic_interval_generated=False,
            quality_generated=False,
            interval_label_generated=False,
            contextual_role_generated=False,
            core_promoted=False,
            status=status,
            activation_reason=None,
        )

    frame = IntervalModuleProcessingFrameCandidate(
        label="interval_processing_frame_C4_G4_candidate",
        source_boundary_input_label=boundary_input.label,
        payload_name=pitch_payload.name,
        chromatic_distance_available=True,
        spelling_pair_available=True,
        generic_interval_generated=False,
        quality_generated=False,
        interval_label_generated=False,
        contextual_role_generated=False,
    )
    return IntervalInternalActivationObservation(
        reception_observation=reception_observation,
        pitch_payload=pitch_payload,
        b_chromatic=b_chromatic,
        b_spelling=b_spelling,
        processing_gamma=processing_gamma,
        processing_frame=frame,
        generic_interval_generated=False,
        quality_generated=False,
        interval_label_generated=False,
        contextual_role_generated=False,
        core_promoted=False,
        status="interval_processing_frame_observed_not_labeled",
        activation_reason="boundary_input_payload_and_internal_boundaries_connected",
    )


def compare_interval_internal_activation() -> IntervalInternalActivationComparison:
    reception = interval_reception_observation()
    payload = pitch_relation_payload_fixture()
    b_chromatic = b_chromatic_fixture()
    b_spelling = b_spelling_fixture()
    without_gamma = activate_interval_internal_frame(
        reception_observation=reception,
        pitch_payload=payload,
        b_chromatic=b_chromatic,
        b_spelling=b_spelling,
        processing_gamma=None,
    )
    with_gamma = activate_interval_internal_frame(
        reception_observation=reception,
        pitch_payload=payload,
        b_chromatic=b_chromatic,
        b_spelling=b_spelling,
        processing_gamma=interval_processing_frame_gamma(),
    )
    return IntervalInternalActivationComparison(
        without_gamma=without_gamma,
        with_gamma=with_gamma,
        same_boundary_input=(
            without_gamma.reception_observation.interval_boundary_input
            == with_gamma.reception_observation.interval_boundary_input
        ),
        same_pitch_payload=without_gamma.pitch_payload == with_gamma.pitch_payload,
        same_b_chromatic=without_gamma.b_chromatic == with_gamma.b_chromatic,
        same_b_spelling=without_gamma.b_spelling == with_gamma.b_spelling,
        same_processing_gamma=(
            without_gamma.processing_gamma == with_gamma.processing_gamma
        ),
        processing_frame_observed=(
            with_gamma.status == "interval_processing_frame_observed_not_labeled"
        ),
        generic_interval_generated=with_gamma.generic_interval_generated,
        quality_generated=with_gamma.quality_generated,
        interval_label_generated=with_gamma.interval_label_generated,
        contextual_role_generated=with_gamma.contextual_role_generated,
        core_promoted=with_gamma.core_promoted,
    )


def run_checks() -> None:
    comparison = compare_interval_internal_activation()
    assert comparison.same_boundary_input is True
    assert comparison.same_pitch_payload is True
    assert comparison.same_b_chromatic is True
    assert comparison.same_b_spelling is True
    assert comparison.same_processing_gamma is False
    assert comparison.processing_frame_observed is True
    assert comparison.generic_interval_generated is False
    assert comparison.quality_generated is False
    assert comparison.interval_label_generated is False
    assert comparison.contextual_role_generated is False
    assert comparison.core_promoted is False

    assert (
        comparison.without_gamma.status
        == "boundary_input_not_connected_without_processing_gamma"
    )
    assert comparison.without_gamma.processing_frame is None

    assert comparison.with_gamma.status == "interval_processing_frame_observed_not_labeled"
    assert comparison.with_gamma.processing_frame is not None
    assert comparison.with_gamma.processing_frame.label == (
        "interval_processing_frame_C4_G4_candidate"
    )
    assert comparison.with_gamma.processing_frame.chromatic_distance_available is True
    assert comparison.with_gamma.processing_frame.spelling_pair_available is True
    assert comparison.with_gamma.processing_frame.generic_interval_generated is False
    assert comparison.with_gamma.processing_frame.quality_generated is False
    assert comparison.with_gamma.processing_frame.interval_label_generated is False
    assert comparison.with_gamma.pitch_payload is not None
    assert comparison.with_gamma.pitch_payload.generated_by_boundary_input is False
    assert comparison.with_gamma.activation_reason == (
        "boundary_input_payload_and_internal_boundaries_connected"
    )


def main() -> None:
    run_checks()
    comparison = compare_interval_internal_activation()
    with_gamma = comparison.with_gamma

    print("[pipeline]")
    print("  interval module boundary input candidate")
    print("  + pitch relation payload fixture")
    print("  + B_chromatic_fixture")
    print("  + B_spelling_fixture")
    print("  + Gamma_interval_processing_frame_fixture")
    print("  -> interval module processing frame candidate")
    print("  -> interval label remains None")
    print(f"  without_gamma_status={comparison.without_gamma.status}")
    print(f"  with_gamma_status={with_gamma.status}")
    print(f"  same_boundary_input={comparison.same_boundary_input}")
    print(f"  same_pitch_payload={comparison.same_pitch_payload}")
    print(f"  same_b_chromatic={comparison.same_b_chromatic}")
    print(f"  same_b_spelling={comparison.same_b_spelling}")
    print(f"  same_processing_gamma={comparison.same_processing_gamma}")
    print(f"  processing_frame_observed={comparison.processing_frame_observed}")
    print(
        "  interval_boundary_input="
        + (
            with_gamma.reception_observation.interval_boundary_input.label
            if with_gamma.reception_observation.interval_boundary_input
            else "None"
        )
    )
    print(
        "  processing_frame="
        + (with_gamma.processing_frame.label if with_gamma.processing_frame else "None")
    )
    print(f"  generic_interval_generated={comparison.generic_interval_generated}")
    print(f"  quality_generated={comparison.quality_generated}")
    print(f"  interval_label_generated={comparison.interval_label_generated}")
    print(f"  contextual_role_generated={comparison.contextual_role_generated}")
    print(f"  core_promoted={comparison.core_promoted}")


if __name__ == "__main__":
    main()
