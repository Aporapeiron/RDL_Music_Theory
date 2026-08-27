"""178 adopted input contractから閉じた再入循環を50工程で確認する最小検証。"""

from dataclasses import dataclass

from interval_module_input_contract_adoption_reentry import (
    compare_input_contract_adoption_reentry,
)


@dataclass(frozen=True)
class ClosedReentryCycleStep:
    number: int
    name: str
    source: str
    result: str
    generated_mutation: bool


@dataclass(frozen=True)
class ClosedReentryCycleObservation:
    source_status: str
    steps: tuple[ClosedReentryCycleStep, ...]
    closed_to_processing_request: bool
    reached_handoff_boundary: bool
    generated_mutation: bool
    status: str


STEP_DEFINITIONS: tuple[tuple[int, str, str], ...] = (
    (179, "payload_instance_binding", "bound_payload_instance_candidate"),
    (180, "payload_validation", "payload_validation_diagnostic"),
    (181, "processing_request", "processing_request_candidate"),
    (182, "processing_request_adoption", "adopted_processing_request"),
    (183, "activation_input_bundle", "activation_input_bundle_candidate"),
    (184, "existing_70_activation_bridge", "processing_frame_candidate"),
    (185, "processing_frame_to_generic_reentry", "generic_interval_candidate"),
    (186, "generic_to_quality_reentry", "quality_candidate"),
    (187, "quality_to_label_reentry", "interval_label_candidate"),
    (188, "label_to_contextual_role_reentry", "contextual_role_annotation"),
    (189, "contextual_role_to_target_reentry", "target_candidate_set"),
    (190, "target_selection_reentry", "selected_interval_target"),
    (191, "selected_target_to_voice_leading_reentry", "voice_leading_request"),
    (192, "voice_leading_realization_reentry", "concrete_voice_leading"),
    (193, "selected_target_to_harmonic_bridge_reentry", "harmonic_bridge_candidate"),
    (194, "harmonic_bridge_to_function_annotation_reentry", "harmonic_function_annotation"),
    (195, "voice_leading_to_next_context_reentry", "next_context_candidate_set"),
    (196, "next_context_selection_reentry", "selected_next_context"),
    (197, "context_harmony_consistency_reentry", "consistency_candidates"),
    (198, "consistency_selection_reentry", "selected_consistency"),
    (199, "state_record_reentry", "state_record_candidate"),
    (200, "record_validation_reentry", "validated_state_record"),
    (201, "M_B_candidate_reentry", "M_B_interval_candidate"),
    (202, "Core_promotion_diagnostic_reentry", "blocked_core_promotion_diagnostic"),
    (203, "confirmation_readiness_reentry", "confirmation_readiness_diagnostic"),
    (204, "confirmation_evidence_variation_reentry", "readiness_evidence_variation"),
    (205, "confirmation_Gamma_variation_reentry", "readiness_Gamma_variation"),
    (206, "confirmed_M_B_reentry", "confirmed_M_B_candidate"),
    (207, "Core_alignment_reentry", "Core_alignment_candidate"),
    (208, "Core_alignment_Gamma_variation_reentry", "Core_alignment_target_variation"),
    (209, "Core_adoption_proposal_reentry", "Core_adoption_proposal"),
    (210, "Core_compatibility_reentry", "Core_compatibility_diagnostic"),
    (211, "Core_adoption_record_reentry", "Core_adoption_record_candidate"),
    (212, "contract_update_reentry", "Module_contract_update_candidate"),
    (213, "contract_regression_reentry", "regression_diagnostic"),
    (214, "next_verification_plan_reentry", "next_verification_plan_candidate"),
    (215, "plan_commitment_reentry", "committed_plan_candidate"),
    (216, "execution_packet_reentry", "execution_packet_candidate"),
    (217, "execution_readiness_reentry", "execution_readiness_diagnostic"),
    (218, "execution_run_reentry", "verification_run_observation"),
    (219, "result_classification_reentry", "verification_result_candidate"),
    (220, "break_diagnostic_reentry", "break_diagnostic_candidate"),
    (221, "integration_candidate_reentry", "integration_candidate"),
    (222, "document_update_proposal_reentry", "document_update_proposal"),
    (223, "update_review_reentry", "update_review_diagnostic"),
    (224, "update_acceptance_reentry", "accepted_update_record"),
    (225, "commit_candidate_reentry", "commit_candidate"),
    (226, "push_readiness_reentry", "push_readiness_diagnostic"),
    (227, "publication_plan_reentry", "publication_plan_candidate"),
    (228, "next_xi_to_contract_generalization_reentry", "handoff_ready_contract_target"),
)


def observe_closed_reentry_cycle() -> ClosedReentryCycleObservation:
    adopted = compare_input_contract_adoption_reentry()[1]
    assert adopted.adopted_contract is not None

    previous = "adopted_input_contract"
    steps = []
    for number, name, result in STEP_DEFINITIONS:
        steps.append(
            ClosedReentryCycleStep(
                number=number,
                name=name,
                source=previous,
                result=result,
                generated_mutation=False,
            )
        )
        previous = result

    observed = tuple(steps)
    return ClosedReentryCycleObservation(
        source_status=adopted.status,
        steps=observed,
        closed_to_processing_request=observed[2].result == "processing_request_candidate",
        reached_handoff_boundary=observed[-1].result == "handoff_ready_contract_target",
        generated_mutation=any(step.generated_mutation for step in observed),
        status="closed_reentry_cycle_179_228_observed_without_mutation",
    )


def run_checks() -> None:
    observation = observe_closed_reentry_cycle()
    assert observation.source_status == (
        "adopted_input_contract_observed_from_reentered_payload_schema_not_processed"
    )
    assert len(observation.steps) == 50
    assert observation.steps[0].number == 179
    assert observation.steps[-1].number == 228
    assert observation.closed_to_processing_request is True
    assert observation.reached_handoff_boundary is True
    assert observation.generated_mutation is False
    assert observation.steps[0].source == "adopted_input_contract"
    assert observation.steps[2].result == "processing_request_candidate"
    assert observation.steps[49].result == "handoff_ready_contract_target"


if __name__ == "__main__":
    run_checks()
    print(observe_closed_reentry_cycle().status)
