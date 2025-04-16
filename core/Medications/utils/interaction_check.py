from .med_interactions import drug_interactions

def check_medication_interactions(new_med, user_meds):
    warnings = []

    for existing_med in user_meds:
        if new_med in drug_interactions and existing_med in drug_interactions[new_med]:
            warning = f"{new_med} + {existing_med}: {drug_interactions[new_med][existing_med]}"
            warnings.append(warning)
        if existing_med in drug_interactions and new_med in drug_interactions[existing_med]:
            warning = f"{existing_med} + {new_med}: {drug_interactions[existing_med][new_med]}"
            warnings.append(warning)

    return warnings
