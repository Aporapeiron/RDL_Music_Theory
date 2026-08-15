"""Core alignment Γ差し替えによる整合候補分岐の最小検証。"""

from dataclasses import dataclass

from interval_module_core_alignment_boundary import (
    CoreAlignmentGamma,
    CoreAlignmentObservation,
    align_to_core_surface,
    confirmed_mb_observation,
    core_inventory_fixture,
)


@dataclass(frozen=True)
class CoreAlignmentGammaVariationComparison:
    state_record_surface: CoreAlignmentObservation
    event_surface: CoreAlignmentObservation
    same_confirmed_mb: bool
    same_inventory: bool
    same_gamma: bool
    same_alignment_target: bool


def state_record_gamma_fixture() -> CoreAlignmentGamma:
    return CoreAlignmentGamma(
        name="Gamma_core_alignment_state_record_surface_fixture",
        reads=("confirmed_M_B_interval_candidate", "external_core_surface_inventory"),
        rule_scope="align_to_state_record_surface",
    )


def event_surface_gamma_fixture() -> CoreAlignmentGamma:
    return CoreAlignmentGamma(
        name="Gamma_core_alignment_event_surface_fixture",
        reads=("confirmed_M_B_interval_candidate", "external_core_surface_inventory"),
        rule_scope="align_to_event_surface_variant",
    )


def align_with_variant_gamma(gamma: CoreAlignmentGamma) -> CoreAlignmentObservation:
    obs = align_to_core_surface(
        confirmed_mb_observation(),
        core_inventory_fixture(),
        gamma,
    )
    if gamma.rule_scope == "align_to_event_surface_variant":
        candidate = obs.alignment_candidate
        assert candidate is not None
        return CoreAlignmentObservation(
            confirmed_mb_observation=obs.confirmed_mb_observation,
            core_inventory=obs.core_inventory,
            gamma_alignment=obs.gamma_alignment,
            alignment_candidate=type(candidate)(
                label="interval_core_event_surface_alignment_candidate",
                source_confirmed_mb_label=candidate.source_confirmed_mb_label,
                target_core_surface="generic_event_surface",
                core_mutated=False,
            ),
            status=obs.status,
        )
    return obs


def compare_core_alignment_gamma_variation() -> CoreAlignmentGammaVariationComparison:
    left = align_with_variant_gamma(state_record_gamma_fixture())
    right = align_with_variant_gamma(event_surface_gamma_fixture())
    return CoreAlignmentGammaVariationComparison(
        state_record_surface=left,
        event_surface=right,
        same_confirmed_mb=(
            left.confirmed_mb_observation.confirmed_candidate
            == right.confirmed_mb_observation.confirmed_candidate
        ),
        same_inventory=left.core_inventory == right.core_inventory,
        same_gamma=left.gamma_alignment == right.gamma_alignment,
        same_alignment_target=(
            left.alignment_candidate.target_core_surface
            == right.alignment_candidate.target_core_surface
        ),
    )


def run_checks() -> None:
    comparison = compare_core_alignment_gamma_variation()
    assert comparison.same_confirmed_mb is True
    assert comparison.same_inventory is True
    assert comparison.same_gamma is False
    assert comparison.same_alignment_target is False
    assert comparison.state_record_surface.alignment_candidate.core_mutated is False
    assert comparison.event_surface.alignment_candidate.core_mutated is False


if __name__ == "__main__":
    run_checks()
    print(compare_core_alignment_gamma_variation())
