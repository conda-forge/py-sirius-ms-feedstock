import os
import time
import sys

from PySirius import SiriusSDK, AlignedFeatureOptField, FragmentationTree, FormulaCandidate


path_to_project = "./testProject.sirius"
# start acceptance test for packages
api = SiriusSDK().attach_or_start_sirius(headless=True)
ps_info = api.projects().create_project("testProject", os.path.abspath(path_to_project))
try:
    path = os.getenv('RECIPE_DIR') + "/Kaempferol.ms"
    path = os.path.abspath(path)
    api.projects().import_preprocessed_data(ps_info.project_id, ignore_formulas=True, input_files=[path])

    feature_id = api.features().get_aligned_features(ps_info.project_id)[0].aligned_feature_id

    job_sub = api.jobs().get_default_job_config()
    job_sub.spectra_search_params.enabled = False
    job_sub.formula_id_params.enabled = True
    job_sub.fingerprint_prediction_params.enabled = False
    job_sub.structure_db_search_params.enabled = False
    job_sub.canopus_params.enabled = False
    job_sub.ms_novelist_params.enabled = False

    job = api.jobs().start_job(project_id=ps_info.project_id, job_submission=job_sub)

    while True:
        if api.jobs().get_job(ps_info.project_id, job.id).progress.state != 'DONE':
            time.sleep(10)
        else:
            break

    formula_candidate = api.features().get_aligned_feature(ps_info.project_id, feature_id, [AlignedFeatureOptField.TOPANNOTATIONS]).top_annotations.formula_annotation
    tree = api.features().get_frag_tree(ps_info.project_id, feature_id, formula_candidate.formula_id)

    print(tree.to_json())

    print("### [SIRIUS API] Test if formula candidate is non null and has correct type.")
    if not isinstance(formula_candidate, FormulaCandidate):
        print("Formula candidate is null or has wrong type. Test FAILED!")
        sys.exit(1)

    print("### [SIRIUS API] Test if tree is non null and has correct type.")
    if not isinstance(tree, FragmentationTree):
        print("Tree is null or has wrong type. Test FAILED!")
        sys.exit(1)

    print("### [SIRIUS API] Test if formula is correct.")
    if "C15H10O6" != formula_candidate.molecular_formula:
        print(f"Expected formula result to be C15H10O6 but found {formula_candidate.molecular_formula}. Test FAILED!")
        sys.exit(1)

finally:
    api.projects().close_project(ps_info.project_id)
    SiriusSDK().shutdown_sirius()
