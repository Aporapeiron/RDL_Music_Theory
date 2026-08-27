"""再入Core alignment Γ差し替えによる整合候補分岐の最小検証。"""

from dataclasses import dataclass

from interval_module_core_alignment_boundary import CoreAlignmentCandidate, CoreAlignmentGamma, core_inventory_fixture
from interval_module_core_alignment_gamma_variation import event_surface_gamma_fixture, state_record_gamma_fixture
from interval_module_core_alignment_reentry import ReenteredCoreAlignmentObservation, align_reentered_to_core_surface
from interval_module_confirmed_mb_reentry import compare_confirmed_mb_reentry


@dataclass(frozen=True)
class ReenteredCoreAlignmentGammaVariationComparison:
    state_record_surface: ReenteredCoreAlignmentObservation
    event_surface: ReenteredCoreAlignmentObservation
    same_confirmed_mb: bool
    same_inventory: bool
    same_gamma: bool
    same_alignment_target: bool


def align_reentered_with_variant_gamma(gamma: CoreAlignmentGamma) -> ReenteredCoreAlignmentObservation:
    obs = align_reentered_to_core_surface(compare_confirmed_mb_reentry()[1], core_inventory_fixture(), gamma)
    if gamma.rule_scope == "align_to_event_surface_variant":
        candidate = obs.alignment_candidate
        assert candidate is not None
        return ReenteredCoreAlignmentObservation(
            obs.confirmed_mb_observation,
            obs.core_inventory,
            obs.gamma_alignment,
            CoreAlignmentCandidate("interval_core_event_surface_alignment_candidate", candidate.source_confirmed_mb_label, "generic_event_surface", False),
            obs.status,
        )
    return obs


def compare_core_alignment_gamma_variation_reentry() -> ReenteredCoreAlignmentGammaVariationComparison:
    left = align_reentered_with_variant_gamma(state_record_gamma_fixture())
    right = align_reentered_with_variant_gamma(event_surface_gamma_fixture())
    assert left.alignment_candidate is not None
    assert right.alignment_candidate is not None
    return ReenteredCoreAlignmentGammaVariationComparison(
        left,
        right,
        left.confirmed_mb_observation.confirmed_candidate == right.confirmed_mb_observation.confirmed_candidate,
        left.core_inventory == right.core_inventory,
        left.gamma_alignment == right.gamma_alignment,
        left.alignment_candidate.target_core_surface == right.alignment_candidate.target_core_surface,
    )


def run_checks() -> None:
    comparison = compare_core_alignment_gamma_variation_reentry()
    assert comparison.same_confirmed_mb is True
    assert comparison.same_inventory is True
    assert comparison.same_gamma is False
    assert comparison.same_alignment_target is False


if __name__ == "__main__":
    run_checks()
    print("reentered_core_alignment_gamma_variation_changes_alignment_target_not_mutation")
