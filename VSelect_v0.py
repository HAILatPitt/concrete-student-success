import marimo

__generated_with = "0.17.7"
app = marimo.App(width="medium")

with app.setup:
    CHOICES = ("include", "exclude", "flag")

    TASKS = {
        1: {
            "header": 'Regulatory Gate',
            "labels": {'include': 'Include', 'exclude': 'Exclude', 'flag': 'Flag for Review'},
            "banner": "",
        },
        2: {
            "header": 'Protected-Attribute Gate',
            "labels": {'include': 'Include As-Is', 'exclude': 'Exclude Entirely', 'flag': 'Keep for Bias-Audit Only'},
            "banner": "",
        },
        3: {
            "header": 'Data-Reliability Gate',
            "labels": {'include': 'Include As-Is', 'exclude': 'Exclude (Too Unreliable)', 'flag': 'Flag for Data-Quality Improvement'},
            "banner": "",
        },
        4: {
            "header": 'Equity & Actionability Gate',
            "labels": {'include': 'Include As-Is', 'exclude': 'Exclude (Not Fair or Actionable)', 'flag': 'Flag for Equity & Intervention Review'},
            "banner": "",
        },
    }

    VARIABLES = {
        'pell': {
            "task": 1,
            "title": 'Pell Status',
            "definition": (
                'Whether a student receives a federal Pell Grant. New regulations restrict use of '
                'financial-aid data in predictive modeling.'
            ),
            "correct": ['exclude', 'flag'],
            "why": {
                'include': (
                    'Including Pell Status violates current federal guidance and may expose the institution '
                    'to penalties. Consider aggregate reporting instead of individual-level use.'
                ),
            },
            "consequence": {},
        },
        'efc': {
            "task": 1,
            "title": 'Expected Family Contribution (EFC)',
            "definition": (
                'Amount a family is expected to contribute to education costs (legacy FAFSA metric). '
                'Regulatory compliance requires excluding this sensitive financial information.'
            ),
            "correct": ['exclude', 'flag'],
            "why": {
                'include': (
                    'EFC is explicitly barred under 2024 Department of Education rules; its inclusion would '
                    'render the model non-compliant.'
                ),
            },
            "consequence": {},
        },
        'sai': {
            "task": 1,
            "title": 'Student Aid Index (SAI)',
            "definition": (
                'A new metric from recent FAFSA changes that replaced EFC. Recent implementation means '
                'this data may not be available for all students in your historical dataset.'
            ),
            "correct": ['exclude', 'flag'],
            "why": {
                'include': (
                    'SAI is sensitive financial-aid data with incomplete coverage. Using it risks privacy '
                    'violations and injects missing-data bias.'
                ),
            },
            "consequence": {},
        },
        'unmet': {
            "task": 1,
            "title": 'Unmet Need',
            "definition": (
                'Gap between the cost of attendance and the student’s available resources. Financial-'
                'stress indicator, but regulatory restrictions likely prohibit its use in individual-'
                'level models.'
            ),
            "correct": ['exclude', 'flag'],
            "why": {
                'include': (
                    'Unmet Need combines multiple restricted data points. Including it would contravene '
                    'policy and amplify socioeconomic bias.'
                ),
            },
            "consequence": {},
        },
        'merit': {
            "task": 1,
            "title": 'Merit Award Amount',
            "definition": (
                'Scholarship amounts awarded based on academic achievement rather than financial need. '
                'Consider whether this variable primarily reflects prior achievement or introduces '
                'socioeconomic factors into your model.'
            ),
            "correct": ['exclude', 'flag'],
            "why": {
                'include': (
                    'Merit awards can proxy socioeconomic status and unintentionally disadvantage low-income '
                    'students. Use only with a strong equity justification.'
                ),
            },
            "consequence": {},
        },
        'pell_plus': {
            "task": 1,
            "title": 'Pell Plus',
            "definition": (
                'University matching funds that complement federal Pell Grants. Financial-aid variables '
                'like this are likely subject to the same regulatory restrictions as other financial '
                'data.'
            ),
            "correct": ['exclude', 'flag'],
            "why": {
                'include': (
                    'Pell Plus directly signals Pell participation; individual-level use is restricted. '
                    'Exclude or seek explicit legal clearance.'
                ),
            },
            "consequence": {},
        },
        'race': {
            "task": 2,
            "title": 'Race',
            "definition": (
                'Student’s self-reported racial/ethnic identity. Used during exploratory data analysis '
                'but removed before predictive modeling.'
            ),
            "correct": ['flag'],
            "why": {
                'include': (
                    'Using Race as a predictive feature can embed historical inequities and violate '
                    'institutional policy. Retain only for bias-audit.'
                ),
                'exclude': (
                    'Without Race you lose the ability to audit fair outcomes across groups. Best practice is'
                    ' to keep it for auditing while excluding it from model training.'
                ),
            },
            "consequence": {},
        },
        'gender': {
            "task": 2,
            "title": 'Gender',
            "definition": (
                'Student’s gender identity as reported during application. Protected class variable that '
                'raises ethical considerations.'
            ),
            "correct": ['flag'],
            "why": {
                'include': (
                    'Directly modelling on Gender risks discriminatory interventions. Consider audit-only '
                    'retention.'
                ),
                'exclude': (
                    'Eliminating Gender data removes a key lens for detecting gender-based disparities as-is '
                    'outputs.'
                ),
            },
            "consequence": {},
        },
        'age': {
            "task": 2,
            "title": 'Age',
            "definition": (
                'Student’s age at enrollment. Flagged as protected class variable. Consider whether age-'
                'based predictions might disadvantage non-traditional students while recognizing that age'
                ' can reflect meaningful differences in life circumstances.'
            ),
            "correct": ['flag'],
            "why": {
                'include': (
                    'Age may correlate with persistence but also with protected status (non-traditional '
                    'learners). Document equity safeguards or shift to audit-only use.'
                ),
                'exclude': (
                    'Excluding Age erases patterns relevant to adult learners and hampers fairness checks. '
                    'Audit-only use is often a balanced choice.'
                ),
            },
            "consequence": {},
        },
        'pronouns': {
            "task": 2,
            "title": 'Preferred Pronouns',
            "definition": (
                'Student-provided pronoun preference collected by campus climate office. Optional field '
                'with high missingness. Can affirm identity but is not a stable predictor of retention.'
            ),
            "correct": ['flag'],
            "why": {
                'include': (
                    'Preferred Pronouns are not predictive of persistence and risk trivializing gender '
                    'identity. Exclude or store only for awareness training, not analytics.'
                ),
                'exclude': (
                    'Pronoun data lack completeness and standardization, limiting audit utility. Exclusion is'
                    ' usually appropriate.'
                ),
            },
            "consequence": {},
        },
        'gpa': {
            "task": 3,
            "title": 'High School GPA',
            "definition": (
                'Student’s high-school grade-point average, a common predictor of college success. This '
                'variable was unreliable due to reporting unreliability across high schools.'
            ),
            "correct": ['exclude', 'flag'],
            "why": {
                'include': (
                    'High-school GPAs lack standardisation; predictive value may be swamped by noise. '
                    'Consider excluding or flagging for quality remediation.'
                ),
            },
            "consequence": {},
        },
        'scores': {
            "task": 3,
            "title": 'Test Scores',
            "definition": (
                'Academic performance metrics from high school and standardised tests (SAT/ACT). Due to '
                'test-optional policies implemented during COVID, scores may be missing for many '
                'students. Creative solution to transform into a ‘test score submitted’ indicator '
                'leverages available information while addressing systematic gaps.'
            ),
            "correct": ['flag'],
            "why": {
                'include': (
                    'Raw Test Scores are sparse post-COVID; treating missing as zero could bias results. A '
                    'submission indicator or audit flag may be safer.'
                ),
                'exclude': (
                    'Dropping Test Scores ignores a potentially strong signal for the subset who submitted. '
                    'Could you retain a binary ‘submitted’ flag instead?'
                ),
            },
            "consequence": {},
        },
        'midterms': {
            "task": 3,
            "title": 'Midterm Grades',
            "definition": (
                'Preliminary academic performance indicators halfway through the term. Identified as '
                'valuable but not consistently available across courses.'
            ),
            "correct": ['flag'],
            "why": {
                'include': (
                    'Mid-Term Grades appear only for certain courses, risking departmental bias. Flag for '
                    'quality improvement or exclude.'
                ),
                'exclude': (
                    'Excluding Mid-Term Grades forfeits early academic-performance insight. Could selective '
                    'inclusion or data-quality work make it viable?'
                ),
            },
            "consequence": {},
        },
        'epr': {
            "task": 3,
            "title": 'Early Progress Reports',
            "definition": (
                'Faculty-submitted assessments of student performance early in the semester. Reporting '
                'inconsistency means this potentially valuable early-warning indicator isn’t reliable '
                'enough to include.'
            ),
            "correct": ['flag'],
            "why": {
                'include': (
                    'Sparse, faculty-dependent reporting could mislead the model. Flag for improvement or '
                    'consider exclusion.'
                ),
                'exclude': (
                    'You lose a proven early-alert signal. Engage stakeholders to improve reporting rather '
                    'than discard entirely.'
                ),
            },
            "consequence": {},
        },
        'printer': {
            "task": 3,
            "title": 'Dorm Printer Usage',
            "definition": (
                'Weekly count of pages printed in residence-hall printers. Logs are missing whenever '
                'printers are offline; many students use personal or library printers instead.'
            ),
            "correct": ['exclude'],
            "why": {
                'include': (
                    'Printer logs cover only a subset of students and machines, yielding noisy, biased '
                    'counts. Little theoretical link to persistence.'
                ),
                'flag': (
                    'Standardising printer data would require major infrastructure changes—benefit unlikely '
                    'to justify cost.'
                ),
            },
            "consequence": {},
        },
        'legacy': {
            "task": 4,
            "title": 'Legacy Status',
            "definition": (
                'Whether the student has family members who previously attended the university. May '
                'indicate stronger institutional ties.'
            ),
            "correct": ['exclude', 'flag'],
            "why": {
                'include': (
                    'Legacy Status may encode privilege and could unfairly prioritise well-connected '
                    'students. Document why its predictive gain outweighs equity concerns.'
                ),
            },
            "consequence": {},
        },
        'athlete': {
            "task": 4,
            "title": 'Student Athlete Status',
            "definition": (
                'Whether the student participates in university athletics. May indicate additional '
                'support structures but also time commitments.'
            ),
            "correct": ['flag'],
            "why": {
                'include': (
                    'Athlete status already triggers dedicated advising; flagging athletes again may waste '
                    'resources. Ensure interventions add value.'
                ),
                'exclude': (
                    'Athletes juggle academics and sport travel. Excluding this variable may hide a known '
                    'risk group lacking time for coursework.'
                ),
            },
            "consequence": {},
        },
        'firstgen': {
            "task": 4,
            "title": 'First Generation Status',
            "definition": (
                'Indicates if the student is the first in their family to attend college; may reflect '
                'differences in familiarity with college processes.'
            ),
            "correct": ['flag'],
            "why": {
                'include': (
                    'Good call—first-gen status supports equity-minded outreach. Be sure to explain positive,'
                    ' not deficit-based, interventions.'
                ),
                'exclude': (
                    'First-generation students often benefit from navigational support. Omitting this '
                    'variable could undermine equity goals.'
                ),
            },
            "consequence": {},
        },
        'distance': {
            "task": 4,
            "title": 'Distance From Home',
            "definition": (
                'Calculated metric based on student’s home address and campus location; privacy-'
                'preserving alternative to ZIP codes.'
            ),
            "correct": ['flag'],
            "why": {
                'include': (
                    'Distance correlates with homesickness and travel cost but offers limited intervention '
                    'levers. Note whether actionable support exists (e.g., travel grants).'
                ),
                'exclude': (
                    'Ignoring Distance removes insight into geographically isolated students who may need '
                    'community-building initiatives.'
                ),
            },
            "consequence": {},
        },
        'credits': {
            "task": 4,
            "title": 'Credits After Add/Drop',
            "definition": (
                'Credit hours the student is taking after the official add/drop deadline; may reflect '
                'adjustment to academic realities.'
            ),
            "correct": ['flag'],
            "why": {
                'include': 'Strong early signal of load management issues. Advisors can act quickly—solid choice.',
                'exclude': (
                    'Course-load changes are an actionable red flag. Excluding them weakens the model’s '
                    'practical value.'
                ),
            },
            "consequence": {},
        },
        'housing': {
            "task": 4,
            "title": 'Live On Campus or Commuter',
            "definition": 'Housing status affects integration into campus life and access to resources.',
            "correct": ['flag'],
            "why": {
                'include': (
                    'Useful and actionable—commuters may need remote-friendly support. Ensure interventions '
                    'respect time and travel constraints.'
                ),
                'exclude': (
                    'Housing status strongly predicts engagement. Excluding it may mask differences in '
                    'retention risk.'
                ),
            },
            "consequence": {},
        },
        'residency': {
            "task": 4,
            "title": 'Residency (In-State / Out-of-State / International)',
            "definition": 'Affects tuition rates and connection to campus.',
            "correct": ['flag'],
            "why": {
                'include': (
                    'Residency drives cost burden; interventions must avoid stereotyping out-of-state '
                    'students as less committed.'
                ),
                'exclude': (
                    'Cost differentials matter. Removing Residency could blunt financial-aid outreach to '
                    'high-tuition groups.'
                ),
            },
            "consequence": {},
        },
        'origins': {
            "task": 4,
            "title": 'Urban / Rural / Suburban Origins',
            "definition": 'Classification of student’s home community; derived from heuristics.',
            "correct": ['flag'],
            "why": {
                'include': (
                    'Heuristic classification may mislabel students; validate definitions or risk noisy '
                    'signals.'
                ),
                'exclude': (
                    'Campus adjustment often differs by origin. Excluding could overlook rural-to-urban '
                    'transition challenges.'
                ),
            },
            "consequence": {},
        },
        'transfer': {
            "task": 4,
            "title": 'Transfer Status',
            "definition": (
                'Whether the student transferred from another institution versus starting as a first-'
                'year.'
            ),
            "correct": ['flag'],
            "why": {
                'include': (
                    'Transfer students face unique credit-articulation hurdles—actionable and equity-'
                    'relevant.'
                ),
                'exclude': (
                    'You dropped a key subgroup with elevated departure risk. Advisors may miss needed '
                    'support.'
                ),
            },
            "consequence": {},
        },
        'extracurricular': {
            "task": 4,
            "title": 'Extracurricular Involvement',
            "definition": (
                'Participation in clubs or other non-academic activities; data collection relies on self-'
                'reporting.'
            ),
            "correct": ['flag'],
            "why": {
                'include': (
                    'Self-report bias and missingness limit reliability; document caveats to avoid '
                    'overstating predictive value.'
                ),
                'exclude': (
                    'Engagement predicts belonging; consider flagging data-quality issues rather than '
                    'discarding outright.'
                ),
            },
            "consequence": {},
        },
        'wi_fi': {
            "task": 4,
            "title": 'Campus-Wi-Fi Gaming Network Participation',
            "definition": (
                'Binary flag—student devices connected to high-traffic gaming ports for ≥ 5 hours/week '
                'during evenings.'
            ),
            "correct": ['exclude', 'flag'],
            "why": {
                'include': (
                    'Correlation to retention unproven; risk of pathologising hobby behaviour. Provide '
                    'theoretical justification or exclude.'
                ),
            },
            "consequence": {},
        },
    }


@app.function
def variables_in(task: int) -> list[str]:
    return [name for name, v in VARIABLES.items() if v["task"] == task]


@app.function
def is_correct(name: str, choice: str) -> bool:
    return choice in VARIABLES[name]["correct"]


@app.function
def severity(name: str, choice: str) -> str:
    return "harm" if choice == "include" and not is_correct(name, choice) else "cautious"


@app.function
def has_variable(row: dict) -> bool:
    return bool(row.get("variable", "").strip())


@app.function
def prediction_ready(could_predict: list[dict], barred: list[dict]) -> bool:
    return any(map(has_variable, could_predict)) and any(map(has_variable, barred))


@app.function
def all_decided(decisions: dict) -> bool:
    return all(decisions.get(name) for name in VARIABLES)


@app.function
def missing_reasons(decisions: dict, reasons: dict) -> list[str]:
    return [name for name, choice in decisions.items() if choice and not reasons.get(name, "").strip()]


@app.function
def can_submit(decisions: dict, reflections: list[str]) -> bool:
    return all_decided(decisions) and all(text.strip() for text in reflections)


@app.function
def wrong_choice(name: str, choice: str) -> dict:
    v = VARIABLES[name]
    return {
        "name": name,
        "task": v["task"],
        "title": v["title"],
        "chose": choice,
        "correct": v["correct"],
        "why": v["why"][choice],
        "consequence": v["consequence"].get(choice, ""),
        "severity": severity(name, choice),
    }


@app.function
def wrong_choices(decisions: dict) -> list[dict]:
    return [
        wrong_choice(name, decisions[name])
        for name in VARIABLES
        if decisions.get(name) and not is_correct(name, decisions[name])
    ]


@app.function
def summary_counts(decisions: dict) -> dict:
    wrong = wrong_choices(decisions)
    harm = sum(w["severity"] == "harm" for w in wrong)
    decided = sum(1 for name in VARIABLES if decisions.get(name))
    return {"correct": decided - len(wrong), "harm": harm, "cautious": len(wrong) - harm}




@app.cell(hide_code=True)
def variable_class_definition(
    button_labels_by_task,
    mo,
    textbox_text_boilerplate,
    variable_details,
):
    def variable_button_handler(obj, value): 
        setter = obj.state
        initial_feedback = obj.initial_feedback_setter
        final_feedback = obj.final_feedback_setter
        setter(value)
        initial_feedback(retrieve_variable_details(obj, *['feedback', 'initial', value]))
        final_feedback(retrieve_variable_details(obj, *['feedback', 'final', value]))


    def retrieve_variable_details(obj, *args): 
        sought_item = variable_details[obj.name]
        for item in args: 
            sought_item = sought_item[item]
        return sought_item


    class Variable:
        def __init__(self, name:str, task:int, state_setter, initial_feedback_setter, final_feedback_setter, text_state_setter):
            self.name = name
            self.task = task
            self.title = retrieve_variable_details(self, 'title')
            self.definition = retrieve_variable_details(self, 'def')
            self.state = state_setter
            self.text_state = text_state_setter
            self.initial_feedback_setter = initial_feedback_setter
            self.final_feedback_setter = final_feedback_setter
            self.incl = mo.ui.run_button(label=button_labels_by_task[self.task]['include'], 
                                         kind='success', 
                                         on_change=lambda _: variable_button_handler(self, 'include')
                                        )
            self.excl = mo.ui.run_button(label=button_labels_by_task[self.task]['exclude'], 
                                         kind='danger', 
                                         on_change=lambda _: variable_button_handler(self, 'exclude')
                                        )
            self.flag = mo.ui.run_button(label=button_labels_by_task[self.task]['flag'], 
                                         kind='warn', 
                                         on_change=lambda _: variable_button_handler(self, 'flag')
                                        )
            self.text = mo.ui.text_area(label=f"{textbox_text_boilerplate} {self.title} choice.",
                                        rows=4,
                                        full_width=True,
                                        on_change=text_state_setter,
                                       )


        def get_initial_feedback(self, dict): 
            return dict[self]['initial']
    return (Variable,)


@app.cell(hide_code=True)
def task_1_variable_instantiation(
    Variable,
    set_efc_final,
    set_efc_initial,
    set_efc_state,
    set_efc_text,
    set_merit_final,
    set_merit_initial,
    set_merit_state,
    set_merit_text,
    set_pell_final,
    set_pell_initial,
    set_pell_plus_final,
    set_pell_plus_initial,
    set_pell_plus_state,
    set_pell_plus_text,
    set_pell_state,
    set_pell_text,
    set_sai_final,
    set_sai_initial,
    set_sai_state,
    set_sai_text,
    set_unmet_final,
    set_unmet_initial,
    set_unmet_state,
    set_unmet_text,
):
    pell = Variable('pell', 1, set_pell_state, set_pell_initial, set_pell_final, set_pell_text)
    efc = Variable('efc', 1, set_efc_state, set_efc_initial, set_efc_final, set_efc_text)
    sai = Variable('sai', 1, set_sai_state, set_sai_initial, set_sai_final, set_sai_text)
    unmet = Variable('unmet', 1, set_unmet_state, set_unmet_initial, set_unmet_final, set_unmet_text)
    merit = Variable('merit', 1, set_merit_state, set_merit_initial, set_merit_final, set_merit_text)
    pell_plus = Variable('pell_plus', 1, set_pell_plus_state, set_pell_plus_initial, set_pell_plus_final, set_pell_plus_text)
    return efc, merit, pell, pell_plus, sai, unmet


@app.cell(hide_code=True)
def task_2_variable_instantiation(
    Variable,
    set_age_final,
    set_age_initial,
    set_age_state,
    set_age_text,
    set_gender_final,
    set_gender_initial,
    set_gender_state,
    set_gender_text,
    set_pronoun_final,
    set_pronoun_initial,
    set_pronoun_state,
    set_pronoun_text,
    set_race_final,
    set_race_initial,
    set_race_state,
    set_race_text,
):
    race = Variable("race", 2, set_race_state, set_race_initial, set_race_final, set_race_text)
    gender = Variable("gender", 2, set_gender_state, set_gender_initial, set_gender_final, set_gender_text) 
    age = Variable("age", 2, set_age_state, set_age_initial, set_age_final, set_age_text)
    pronouns = Variable("pronouns", 2, set_pronoun_state, set_pronoun_initial, set_pronoun_final, set_pronoun_text)
    return age, gender, pronouns, race


@app.cell(hide_code=True)
def task_3_variable_instantiation(
    Variable,
    set_epr_final,
    set_epr_initial,
    set_epr_state,
    set_epr_text,
    set_gpa_final,
    set_gpa_initial,
    set_gpa_state,
    set_gpa_text,
    set_midterms_final,
    set_midterms_initial,
    set_midterms_state,
    set_midterms_text,
    set_printer_final,
    set_printer_initial,
    set_printer_state,
    set_printer_text,
    set_scores_final,
    set_scores_initial,
    set_scores_state,
    set_scores_text,
):
    gpa = Variable("gpa", 3, set_gpa_state, set_gpa_initial, set_gpa_final, set_gpa_text)
    scores = Variable("scores", 3, set_scores_state, set_scores_initial, set_scores_final, set_scores_text)
    midterms = Variable("midterms", 3, set_midterms_state, set_midterms_initial, set_midterms_final, set_midterms_text)
    epr = Variable("epr", 3, set_epr_state, set_epr_initial, set_epr_final, set_epr_text)
    printer = Variable("printer", 3, set_printer_state, set_printer_initial, set_printer_final, set_printer_text,)
    return epr, gpa, midterms, printer, scores


@app.cell(hide_code=True)
def task_4_variable_instantiation(
    Variable,
    set_athlete_final,
    set_athlete_initial,
    set_athlete_state,
    set_athlete_text,
    set_credits_final,
    set_credits_initial,
    set_credits_state,
    set_credits_text,
    set_distance_final,
    set_distance_initial,
    set_distance_state,
    set_distance_text,
    set_extracurricular_final,
    set_extracurricular_initial,
    set_extracurricular_state,
    set_extracurricular_text,
    set_firstgen_final,
    set_firstgen_initial,
    set_firstgen_state,
    set_firstgen_text,
    set_housing_final,
    set_housing_initial,
    set_housing_state,
    set_housing_text,
    set_legacy_final,
    set_legacy_initial,
    set_legacy_state,
    set_legacy_text,
    set_origins_final,
    set_origins_initial,
    set_origins_state,
    set_origins_text,
    set_residency_final,
    set_residency_initial,
    set_residency_state,
    set_residency_text,
    set_transfer_final,
    set_transfer_initial,
    set_transfer_state,
    set_transfer_text,
    set_wi_fi_final,
    set_wi_fi_initial,
    set_wi_fi_state,
    set_wi_fi_text,
):
    legacy=Variable('legacy', 4, set_legacy_state, set_legacy_initial, set_legacy_final, set_legacy_text)
    athlete=Variable('athlete', 4, set_athlete_state, set_athlete_initial, set_athlete_final, set_athlete_text)
    firstgen = Variable('firstgen', 4, set_firstgen_state, set_firstgen_initial, set_firstgen_final, set_firstgen_text)
    distance = Variable('distance', 4, set_distance_state, set_distance_initial, set_distance_final, set_distance_text) 
    credits=Variable('credits', 4, set_credits_state, set_credits_initial, set_credits_final, set_credits_text)
    housing=Variable('housing', 4, set_housing_state, set_housing_initial, set_housing_final, set_housing_text)
    residency=Variable('residency', 4, set_residency_state, set_residency_initial, set_residency_final, set_residency_text) 
    origins=Variable('origins', 4, set_origins_state, set_origins_initial, set_origins_final, set_origins_text)
    transfer=Variable('transfer', 4, set_transfer_state, set_transfer_initial, set_transfer_final, set_transfer_text) 
    extracurricular=Variable('extracurricular', 
                             4, 
                             set_extracurricular_state, 
                             set_extracurricular_initial, 
                             set_extracurricular_final, 
                             set_extracurricular_text
                            )
    wi_fi=Variable('wi_fi', 4, set_wi_fi_state, set_wi_fi_initial, set_wi_fi_final, set_wi_fi_text)
    return (
        athlete,
        credits,
        distance,
        extracurricular,
        firstgen,
        housing,
        legacy,
        origins,
        residency,
        transfer,
        wi_fi,
    )


@app.cell(hide_code=True)
def reactive_elements_and_states(mo):
    #task 1 getters and setters
    #pell
    get_pell_state, set_pell_state = mo.state(None)
    get_pell_initial, set_pell_initial = mo.state(None)
    get_pell_final, set_pell_final = mo.state(None)
    get_pell_text, set_pell_text = mo.state(None)

    #efc
    get_efc_state, set_efc_state = mo.state(None)
    get_efc_initial, set_efc_initial = mo.state(None)
    get_efc_final, set_efc_final = mo.state(None)
    get_efc_text, set_efc_text = mo.state(None)

    #sai
    get_sai_state, set_sai_state = mo.state(None)
    get_sai_initial, set_sai_initial = mo.state(None)
    get_sai_final, set_sai_final = mo.state(None)
    get_sai_text, set_sai_text = mo.state(None)

    #unmet
    get_unmet_state, set_unmet_state = mo.state(None)
    get_unmet_initial, set_unmet_initial = mo.state(None)
    get_unmet_final, set_unmet_final = mo.state(None)
    get_unmet_text, set_unmet_text = mo.state(None)

    #merit
    get_merit_state, set_merit_state = mo.state(None)
    get_merit_initial, set_merit_initial = mo.state(None)
    get_merit_final, set_merit_final = mo.state(None)
    get_merit_text, set_merit_text = mo.state(None)

    #pell_plus
    get_pell_plus_state, set_pell_plus_state = mo.state(None)
    get_pell_plus_initial, set_pell_plus_initial = mo.state(None)
    get_pell_plus_final, set_pell_plus_final = mo.state(None)
    get_pell_plus_text, set_pell_plus_text = mo.state(None)



    #task 2 getters and setters
    #race
    get_race_state, set_race_state = mo.state(None)
    get_race_initial, set_race_initial = mo.state(None)
    get_race_final, set_race_final = mo.state(None)
    get_race_text, set_race_text = mo.state(None)

    #gender
    get_gender_state, set_gender_state = mo.state(None)
    get_gender_initial, set_gender_initial = mo.state(None)
    get_gender_final, set_gender_final = mo.state(None)
    get_gender_text, set_gender_text = mo.state(None)

    #age
    get_age_state, set_age_state = mo.state(None)
    get_age_initial, set_age_initial = mo.state(None)
    get_age_final, set_age_final = mo.state(None)
    get_age_text, set_age_text = mo.state(None)

    #pronouns
    get_pronoun_state, set_pronoun_state = mo.state(None)
    get_pronoun_initial, set_pronoun_initial = mo.state(None)
    get_pronoun_final, set_pronoun_final = mo.state(None)
    get_pronoun_text, set_pronoun_text = mo.state(None)


    #task_3 getters and setters

    #gpa
    get_gpa_state, set_gpa_state = mo.state(None)
    get_gpa_initial, set_gpa_initial = mo.state(None)
    get_gpa_final, set_gpa_final = mo.state(None)
    get_gpa_text, set_gpa_text = mo.state(None)

    #scores
    get_scores_state, set_scores_state = mo.state(None)
    get_scores_initial, set_scores_initial = mo.state(None)
    get_scores_final, set_scores_final = mo.state(None)
    get_scores_text, set_scores_text = mo.state(None)

    #midterms
    get_midterms_state, set_midterms_state = mo.state(None)
    get_midterms_initial, set_midterms_initial = mo.state(None)
    get_midterms_final, set_midterms_final = mo.state(None)
    get_midterms_text, set_midterms_text = mo.state(None)

    #epr
    get_epr_state, set_epr_state = mo.state(None)
    get_epr_initial, set_epr_initial = mo.state(None)
    get_epr_final, set_epr_final = mo.state(None)
    get_epr_text, set_epr_text = mo.state(None)

    #printer
    get_printer_state, set_printer_state = mo.state(None)
    get_printer_initial, set_printer_initial = mo.state(None)
    get_printer_final, set_printer_final = mo.state(None)
    get_printer_text, set_printer_text = mo.state(None)

    #task_4 getters_and_setters
    #legacy
    get_legacy_state, set_legacy_state = mo.state(None)
    get_legacy_initial, set_legacy_initial = mo.state(None)
    get_legacy_final, set_legacy_final = mo.state(None)
    get_legacy_text, set_legacy_text = mo.state(None)

    #athlete
    get_athlete_state, set_athlete_state = mo.state(None)
    get_athlete_initial, set_athlete_initial = mo.state(None)
    get_athlete_final, set_athlete_final = mo.state(None)
    get_athlete_text, set_athlete_text = mo.state(None)

    #firstgen
    get_firstgen_state, set_firstgen_state = mo.state(None)
    get_firstgen_initial, set_firstgen_initial = mo.state(None)
    get_firstgen_final, set_firstgen_final = mo.state(None)
    get_firstgen_text, set_firstgen_text = mo.state(None)

    #distance
    get_distance_state, set_distance_state = mo.state(None)
    get_distance_initial, set_distance_initial = mo.state(None)
    get_distance_final, set_distance_final = mo.state(None)
    get_distance_text, set_distance_text = mo.state(None)

    #credits
    get_credits_state, set_credits_state = mo.state(None)
    get_credits_initial, set_credits_initial = mo.state(None)
    get_credits_final, set_credits_final = mo.state(None)
    get_credits_text, set_credits_text = mo.state(None)

    #housing
    get_housing_state, set_housing_state = mo.state(None)
    get_housing_initial, set_housing_initial = mo.state(None)
    get_housing_final, set_housing_final = mo.state(None)
    get_housing_text, set_housing_text = mo.state(None)

    #residency
    get_residency_state, set_residency_state = mo.state(None)
    get_residency_initial, set_residency_initial = mo.state(None)
    get_residency_final, set_residency_final = mo.state(None)
    get_residency_text, set_residency_text = mo.state(None)

    #origins
    get_origins_state, set_origins_state = mo.state(None)
    get_origins_initial, set_origins_initial = mo.state(None)
    get_origins_final, set_origins_final = mo.state(None)
    get_origins_text, set_origins_text = mo.state(None)

    #transfer
    get_transfer_state, set_transfer_state = mo.state(None)
    get_transfer_initial, set_transfer_initial = mo.state(None)
    get_transfer_final, set_transfer_final = mo.state(None)
    get_transfer_text, set_transfer_text = mo.state(None)

    #extracurricular
    get_extracurricular_state, set_extracurricular_state = mo.state(None)
    get_extracurricular_initial, set_extracurricular_initial = mo.state(None)
    get_extracurricular_final, set_extracurricular_final = mo.state(None)
    get_extracurricular_text, set_extracurricular_text = mo.state(None)

    #wi_fi
    get_wi_fi_state, set_wi_fi_state = mo.state(None)
    get_wi_fi_initial, set_wi_fi_initial = mo.state(None)
    get_wi_fi_final, set_wi_fi_final = mo.state(None)
    get_wi_fi_text, set_wi_fi_text = mo.state(None)
    return (
        get_age_final,
        get_age_initial,
        get_age_state,
        get_age_text,
        get_athlete_final,
        get_athlete_initial,
        get_athlete_state,
        get_athlete_text,
        get_credits_final,
        get_credits_initial,
        get_credits_state,
        get_credits_text,
        get_distance_final,
        get_distance_initial,
        get_distance_state,
        get_distance_text,
        get_efc_final,
        get_efc_initial,
        get_efc_state,
        get_efc_text,
        get_epr_final,
        get_epr_initial,
        get_epr_state,
        get_epr_text,
        get_extracurricular_final,
        get_extracurricular_initial,
        get_extracurricular_state,
        get_extracurricular_text,
        get_firstgen_final,
        get_firstgen_initial,
        get_firstgen_state,
        get_firstgen_text,
        get_gender_final,
        get_gender_initial,
        get_gender_state,
        get_gender_text,
        get_gpa_final,
        get_gpa_initial,
        get_gpa_state,
        get_gpa_text,
        get_housing_final,
        get_housing_initial,
        get_housing_state,
        get_housing_text,
        get_legacy_final,
        get_legacy_initial,
        get_legacy_state,
        get_legacy_text,
        get_merit_final,
        get_merit_initial,
        get_merit_state,
        get_merit_text,
        get_midterms_final,
        get_midterms_initial,
        get_midterms_state,
        get_midterms_text,
        get_origins_final,
        get_origins_initial,
        get_origins_state,
        get_origins_text,
        get_pell_final,
        get_pell_initial,
        get_pell_plus_final,
        get_pell_plus_initial,
        get_pell_plus_state,
        get_pell_plus_text,
        get_pell_state,
        get_pell_text,
        get_printer_final,
        get_printer_initial,
        get_printer_state,
        get_printer_text,
        get_pronoun_final,
        get_pronoun_initial,
        get_pronoun_state,
        get_pronoun_text,
        get_race_final,
        get_race_initial,
        get_race_state,
        get_race_text,
        get_residency_final,
        get_residency_initial,
        get_residency_state,
        get_residency_text,
        get_sai_final,
        get_sai_initial,
        get_sai_state,
        get_sai_text,
        get_scores_final,
        get_scores_initial,
        get_scores_state,
        get_scores_text,
        get_transfer_final,
        get_transfer_initial,
        get_transfer_state,
        get_transfer_text,
        get_unmet_final,
        get_unmet_initial,
        get_unmet_state,
        get_unmet_text,
        get_wi_fi_final,
        get_wi_fi_initial,
        get_wi_fi_state,
        get_wi_fi_text,
        set_age_final,
        set_age_initial,
        set_age_state,
        set_age_text,
        set_athlete_final,
        set_athlete_initial,
        set_athlete_state,
        set_athlete_text,
        set_credits_final,
        set_credits_initial,
        set_credits_state,
        set_credits_text,
        set_distance_final,
        set_distance_initial,
        set_distance_state,
        set_distance_text,
        set_efc_final,
        set_efc_initial,
        set_efc_state,
        set_efc_text,
        set_epr_final,
        set_epr_initial,
        set_epr_state,
        set_epr_text,
        set_extracurricular_final,
        set_extracurricular_initial,
        set_extracurricular_state,
        set_extracurricular_text,
        set_firstgen_final,
        set_firstgen_initial,
        set_firstgen_state,
        set_firstgen_text,
        set_gender_final,
        set_gender_initial,
        set_gender_state,
        set_gender_text,
        set_gpa_final,
        set_gpa_initial,
        set_gpa_state,
        set_gpa_text,
        set_housing_final,
        set_housing_initial,
        set_housing_state,
        set_housing_text,
        set_legacy_final,
        set_legacy_initial,
        set_legacy_state,
        set_legacy_text,
        set_merit_final,
        set_merit_initial,
        set_merit_state,
        set_merit_text,
        set_midterms_final,
        set_midterms_initial,
        set_midterms_state,
        set_midterms_text,
        set_origins_final,
        set_origins_initial,
        set_origins_state,
        set_origins_text,
        set_pell_final,
        set_pell_initial,
        set_pell_plus_final,
        set_pell_plus_initial,
        set_pell_plus_state,
        set_pell_plus_text,
        set_pell_state,
        set_pell_text,
        set_printer_final,
        set_printer_initial,
        set_printer_state,
        set_printer_text,
        set_pronoun_final,
        set_pronoun_initial,
        set_pronoun_state,
        set_pronoun_text,
        set_race_final,
        set_race_initial,
        set_race_state,
        set_race_text,
        set_residency_final,
        set_residency_initial,
        set_residency_state,
        set_residency_text,
        set_sai_final,
        set_sai_initial,
        set_sai_state,
        set_sai_text,
        set_scores_final,
        set_scores_initial,
        set_scores_state,
        set_scores_text,
        set_transfer_final,
        set_transfer_initial,
        set_transfer_state,
        set_transfer_text,
        set_unmet_final,
        set_unmet_initial,
        set_unmet_state,
        set_unmet_text,
        set_wi_fi_final,
        set_wi_fi_initial,
        set_wi_fi_state,
        set_wi_fi_text,
    )


@app.cell(hide_code=True)
def task_1_getters(
    efc,
    get_efc_final,
    get_efc_initial,
    get_efc_state,
    get_efc_text,
    get_merit_final,
    get_merit_initial,
    get_merit_state,
    get_merit_text,
    get_pell_final,
    get_pell_initial,
    get_pell_plus_final,
    get_pell_plus_initial,
    get_pell_plus_state,
    get_pell_plus_text,
    get_pell_state,
    get_pell_text,
    get_sai_final,
    get_sai_initial,
    get_sai_state,
    get_sai_text,
    get_unmet_final,
    get_unmet_initial,
    get_unmet_state,
    get_unmet_text,
    merit,
    pell,
    pell_plus,
    sai,
    unmet,
):
    task_1_getters = {
        pell: {
            'state': get_pell_state(),
            'initial': get_pell_initial(),
            'final': get_pell_final(),
    		'text': get_pell_text(),
        },
        efc: {
            'state': get_efc_state(),
            'initial': get_efc_initial(),
            'final': get_efc_final(),
    		'text': get_efc_text(),
        },
        sai: {
            'state': get_sai_state(),
            'initial': get_sai_initial(),
            'final': get_sai_final(),
    		'text': get_sai_text(),
        },
        unmet: {
            'state': get_unmet_state(),
            'initial': get_unmet_initial(),
            'final': get_unmet_final(),
    		'text': get_unmet_text(),
        },
        merit: {
            'state': get_merit_state(),
            'initial': get_merit_initial(),
            'final': get_merit_final(),
    		'text': get_merit_text(),
        },
        pell_plus: {
            'state': get_pell_plus_state(),
            'initial': get_pell_plus_initial(),
            'final': get_pell_plus_final(),
    		'text': get_pell_plus_text(),
        },
    }
    return (task_1_getters,)


@app.cell(hide_code=True)
def task_2_getters(
    age,
    gender,
    get_age_final,
    get_age_initial,
    get_age_state,
    get_age_text,
    get_gender_final,
    get_gender_initial,
    get_gender_state,
    get_gender_text,
    get_pronoun_final,
    get_pronoun_initial,
    get_pronoun_state,
    get_pronoun_text,
    get_race_final,
    get_race_initial,
    get_race_state,
    get_race_text,
    pronouns,
    race,
):
    task_2_getters = {
        race: {
            'state': get_race_state(),
            'initial': get_race_initial(),
            'final': get_race_final(),
    		'text': get_race_text(),
        },
        age: {
            'state': get_age_state(),
            'initial': get_age_initial(),
            'final': get_age_final(),
    		'text': get_age_text(),
        },
        gender: {
            'state': get_gender_state(),
            'initial': get_gender_initial(),
            'final': get_gender_final(),
    		'text': get_gender_text(),
        },
        pronouns: {
            'state': get_pronoun_state(),
            'initial': get_pronoun_initial(),
            'final': get_pronoun_final(),
    		'text': get_pronoun_text(),
        },
    }
    return (task_2_getters,)


@app.cell(hide_code=True)
def task_3_getters(
    epr,
    get_epr_final,
    get_epr_initial,
    get_epr_state,
    get_epr_text,
    get_gpa_final,
    get_gpa_initial,
    get_gpa_state,
    get_gpa_text,
    get_midterms_final,
    get_midterms_initial,
    get_midterms_state,
    get_midterms_text,
    get_printer_final,
    get_printer_initial,
    get_printer_state,
    get_printer_text,
    get_scores_final,
    get_scores_initial,
    get_scores_state,
    get_scores_text,
    gpa,
    midterms,
    printer,
    scores,
):
    task_3_getters = {
        gpa: {
            'state': get_gpa_state(),
            'initial': get_gpa_initial(),
            'final': get_gpa_final(),
    		'text': get_gpa_text(),
        },
        scores: {
            'state': get_scores_state(),
            'initial': get_scores_initial(),
            'final': get_scores_final(),
    		'text': get_scores_text(),
        },
        midterms: {
            'state': get_midterms_state(),
            'initial': get_midterms_initial(),
            'final': get_midterms_final(),
    		'text': get_midterms_text(),
        },
        epr: {
            'state': get_epr_state(),
            'initial': get_epr_initial(),
            'final': get_epr_final(),
    		'text': get_epr_text(),
        },
        printer: {
            'state': get_printer_state(),
            'initial': get_printer_initial(),
            'final': get_printer_final(),
    		'text': get_printer_text(),
        },
    }
    return (task_3_getters,)


@app.cell(hide_code=True)
def task_4_getters(
    athlete,
    credits,
    distance,
    extracurricular,
    firstgen,
    get_athlete_final,
    get_athlete_initial,
    get_athlete_state,
    get_athlete_text,
    get_credits_final,
    get_credits_initial,
    get_credits_state,
    get_credits_text,
    get_distance_final,
    get_distance_initial,
    get_distance_state,
    get_distance_text,
    get_extracurricular_final,
    get_extracurricular_initial,
    get_extracurricular_state,
    get_extracurricular_text,
    get_firstgen_final,
    get_firstgen_initial,
    get_firstgen_state,
    get_firstgen_text,
    get_housing_final,
    get_housing_initial,
    get_housing_state,
    get_housing_text,
    get_legacy_final,
    get_legacy_initial,
    get_legacy_state,
    get_legacy_text,
    get_origins_final,
    get_origins_initial,
    get_origins_state,
    get_origins_text,
    get_residency_final,
    get_residency_initial,
    get_residency_state,
    get_residency_text,
    get_transfer_final,
    get_transfer_initial,
    get_transfer_state,
    get_transfer_text,
    get_wi_fi_final,
    get_wi_fi_initial,
    get_wi_fi_state,
    get_wi_fi_text,
    housing,
    legacy,
    origins,
    residency,
    transfer,
    wi_fi,
):
    #helps to trigger reactive elements across the notebook as they update

    task_4_getters = {
        legacy: {
            'state': get_legacy_state(),
            'initial': get_legacy_initial(),
            'final': get_legacy_final(),
    		'text': get_legacy_text(),
        },
        athlete: {
            'state': get_athlete_state(),
            'initial': get_athlete_initial(),
            'final': get_athlete_final(),
    		'text': get_athlete_text(),
        },
        firstgen: {
            'state': get_firstgen_state(),
            'initial': get_firstgen_initial(),
            'final': get_firstgen_final(),
    		'text': get_firstgen_text(),
        },
        distance: {
            'state': get_distance_state(),
            'initial': get_distance_initial(),
            'final': get_distance_final(),
    		'text': get_distance_text(),
        },
        credits: {
            'state': get_credits_state(),
            'initial': get_credits_initial(),
            'final': get_credits_final(),
    		'text': get_credits_text(),
        },
        housing: {
            'state': get_housing_state(),
            'initial': get_housing_initial(),
            'final': get_housing_final(),
    		'text': get_housing_text(),
        },
        residency: {
            'state': get_residency_state(),
            'initial': get_residency_initial(),
            'final': get_residency_final(),
    		'text': get_residency_text(),
        },
        origins: {
            'state': get_origins_state(),
            'initial': get_origins_initial(),
            'final': get_origins_final(),
    		'text': get_origins_text(),
        },
        transfer: {
            'state': get_transfer_state(),
            'initial': get_transfer_initial(),
            'final': get_transfer_final(),
    		'text': get_transfer_text(),
        },
        extracurricular: {
            'state': get_extracurricular_state(),
            'initial': get_extracurricular_initial(),
            'final': get_extracurricular_final(),
    		'text': get_extracurricular_text(),
        },
        wi_fi: {
            'state': get_wi_fi_state(),
            'initial': get_wi_fi_initial(),
            'final': get_wi_fi_final(),
    		'text': get_wi_fi_text(),
        },
    }
    return (task_4_getters,)


@app.cell(hide_code=True)
def functions(correct, mo, variables_by_task):
    #functions

    def var_selection_text_generator(choice:str|None, task:int)->str: 
        '''
        confirmation text for the user's variable choice(s)
        '''
        if choice == 'include': 
            insert_text = "🟢 **Include** the variable **as-is**."
        elif choice == 'exclude':
            if task in [1,2]: 
                insert_text = "🔴 **Exclude** the variable **entirely**."
            elif task == 3:
                insert_text = "🔴 **Exclude** the variable **due to unreliability**."
            elif task == 4:
                insert_text = "🔴 **Exclude** the variable **as not fair or actionable**."
        elif choice == 'flag': 
            if task==1: 
                insert_text = "🟠 **Flag** the variable **for Review**."
            elif task == 2: 
                insert_text = '🟠 **Keep** the variable **for Bias-Audit Only**.'
            elif task == 3: 
                insert_text = '🟠 **Flag** the variable **for Data-Quality Improvement**.'
            elif task == 4:
                insert_text = '🟠 **Flag** the variable **for Equity & Intervention Review**.'
        else:
            insert_text = "⚪️ **not yet selected**"
            return f"You have {insert_text} a variable option."
        return f"You decided to {insert_text}"


    def process_task_variables(obj, getter):
        '''
        collects and formats the text and reactive elements for each individual variable within a task's selection cell
        '''
        content = mo.vstack([
            mo.md(obj.definition),
            mo.hstack([obj.incl, obj.excl, obj.flag])            
        ])
        output = mo.vstack([
            mo.accordion({obj.title: content}),
            mo.md(f"""{var_selection_text_generator(getter[obj]['state'], obj.task)}"""),
            obj.text if getter[obj]['state'] else ''
        ])
        return output


    def initial_variable_feedback(obj, getter): 
        '''
        collects and formats the text and reactive elements for each individual variable's feedback
        '''
        response_text = getter[obj]['initial'] if getter[obj]['initial'] else ''
        feedback_out = mo.md(f"""**{obj.title}:** {response_text}""") 
        return feedback_out


    def variable_selection_generator(tasknumber:int): 
        '''
        builds the layout that compiles all of the task's individual text/reactive elements into one output
        '''
        var_selection_menu = [process_task_variables(var_option, variables_by_task[tasknumber]['getter']) 
                              for var_option 
                              in variables_by_task[tasknumber]['variables']
                             ]
        return mo.output.replace(mo.vstack(var_selection_menu))


    def initial_feedback_generator(tasknumber: int): 
        '''
        builds the layout that compiles all of a task's individual pieces of feedback into one output
        '''
        task_level_feedback = [initial_variable_feedback(var_item, variables_by_task[tasknumber]['getter']) 
                               for var_item 
                               in variables_by_task[tasknumber]['variables']
                              ]
        return mo.accordion({"Detailed Feedback": mo.vstack(task_level_feedback)})


    def gather_final_feedback(var, getter, correct_list: list[any], incorrect: list[any]):
        '''
        collects the text and reactive elements for each individual variable in preparation for the final list of feedback 
        '''
        if getter[var]['final'] == correct:
            correct_list.append(var.title)
        else: 
            if not getter[var]['final']: 
                incorrect.append(mo.md(f"""**{var.title}**: No variable was selected."""))
            else: 
                incorrect.append(mo.md(f"""**{var.title}**: {getter[var]['final']}"""))
        return correct_list, incorrect


    def format_final_feedback(correct: list[any], incorrect: list[any]): 
        '''
        builds the layout for the final feedback cell
        '''
        corr_text = f"""✅ **No major concerns for:** {', '.join(correct)}""" if len(correct)>0 else ""
        corr_output = mo.md(corr_text)
        incorr_text = "⚠️ **At least one variable still needs your attention.**" if len(incorrect)>0 else "✅ **Everything looks good in this wave!**"
        incorr_output = mo.md(incorr_text)
        final_output = mo.vstack([incorr_output] + incorrect + [corr_output])
        return final_output
    return (
        format_final_feedback,
        gather_final_feedback,
        initial_feedback_generator,
        variable_selection_generator,
    )


@app.cell
def _():
    import marimo as mo                           
    mo.md(
        "# Variable selection scenario\n"

    )
    return (mo,)


@app.cell(hide_code=True)
def introduction(mo):
    mo.vstack(
        [
            # 1) subtitle
            mo.md("## The story so far"),

            # 2) “Note to the team”
            mo.md(
                "The university is a large research institution that competes for students in a crowded " \
                "higher-education market. Over the past five years the first-to-second-year retention rate has " \
                "drifted downward, and graduation timelines have lengthened. Senior leadership has asked the Office of " \
                "the Provost to treat student persistence as a strategic priority rather than a routine metric. " \
                "An internal mandate now calls for data-informed, proactive outreach so that support staff can offer " \
                "help long before a student considers leaving. Within the Office of the Provost a small Student Success Analytics " \
                "group has been established. This team combines institutional researchers, academic advisors, compliance officers, "
                "and data engineers. Its first assignment is to create an early warning intelligence tool that flags continuing " \
                "undergraduates who appear at risk of stopping out or falling behind schedule. Advisors will then contact those " \
                "students and connect them with tutoring, financial counseling, or mentoring. The analytics group is expected to " \
                "respect privacy regulations such as FERPA and recent federal guidance that limits the use of individual financial-aid " \
                "records in automated decision systems. It is also expected to uphold the university commitment to equity and transparency in " \
                "every technical choice."
            ),


            mo.md("&nbsp;"),

            mo.md("## Role"),

            # 2) “Note to the team”
            mo.md(
                "You serve as the team’s data science specialist. Your immediate task is not to build a model but to decide which " \
                "pieces of information should be fed into one. Working with colleagues you have assembled a data dictionary drawn " \
                "from the university warehouse. The dictionary lists common attributes such as high school grade point averages, " \
                "standardized test scores, race, gender, residency status, and course loads. It also contains financial indicators " \
                "like Pell eligibility and Expected Family Contribution. Several context-specific items are included as well. "\
                "Examples are whether a student applied to a regional campus after a main-campus denial, whether a student is a varsity athlete, "\
                "and the distance between the student’s home address and campus. No raw records are available at this stage of the project; "\
                "only the variable descriptions, their known limitations, and any red-flag notes provided by legal or ethical reviewers."
            ),


            mo.md("&nbsp;"),


            mo.md("## Business Objective & Product"),

            # 2) “Note to the team”
            mo.md(
                "Academic advisors need a concise, defensible list of candidate predictors that can drive a predictive model without violating " \
                "regulations or undermining equitable treatment. Your deliverable for this scenario is a Variable Selection Brief. " \
                "In one page you will designate each variable as included, excluded, or flagged for additional discussion. " \
                "For every decision you will provide a short rationale that links back to the goals of privacy protection, fairness, and practical usefulness. " \
                "Advisors and compliance staff will review and sign this brief before any modelling work proceeds."
            ),


            mo.md("&nbsp;"),

        ]
    )
    return


@app.cell
def anchor_task_1(mo):
    mo.Html('<div id="task_1"></div>')
    return


@app.cell(hide_code=True)
def task_1(mo):
    mo.vstack(
        [
            mo.md("## Task 1 Regulatory Gate"),
            mo.md("*For each variable choose **one** action:*"),
            mo.Html(
                """
                <div style="display:flex; justify-content:center;">
                  <table style="border-collapse:separate; border-spacing:0 6px; text-align:center;">
                    <thead>
                      <tr>
                        <th style="padding:0.5rem 1.5rem;">Action</th>
                        <th style="padding:0.5rem 1.5rem;">Meaning</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td style="padding:0.5rem 1.5rem;"><b>Include</b></td>
                        <td style="padding:0.5rem 1.5rem;">
                          Use this variable in the predictive model.
                        </td>
                      </tr>
                      <tr>
                       <td style="padding:0.5rem 1.5rem;"><b>Exclude</b></td>
                        <td style="padding:0.5rem 1.5rem;">
                          Remove it from consideration.
                        </td>
                      </tr>
                      <tr>
                        <td style="padding:0.5rem 1.5rem;"><b>Flag for Legal / IRB Review</b></td>
                        <td style="padding:0.5rem 1.5rem;">
                          Put the variable on hold until university counsel (or the IRB) provides guidance.
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                """
            ),

        ]
    )
    return


@app.cell
def task_1_variable_selection(variable_selection_generator):
    variable_selection_generator(1)
    return


@app.cell
def task_1_initial_feedback(initial_feedback_generator):
    initial_feedback_generator(1)
    return


@app.cell
def section_separator(mo):
    mo.Html("""
    <hr style="border: 1px dashed black; margin-top:2.5rem; margin-bottom:3rem;">
    """)
    return


@app.cell
def anchor_task_2(mo):
    mo.Html('<div id="task_2"></div>')
    return


@app.cell(hide_code=True)
def task_2(mo):
    mo.vstack([
        mo.md("## Task 2 – Protected-Attribute Gate: Fairness and Equity Check"),
        mo.md(
            "**Note to the learner**  \n"
            "This wave challenges you to balance fairness, inclusivity, and ethical use of sensitive personal attributes. "
            "The decision set differs from Wave 1: some attributes are useful for post-hoc bias auditing but risky inside a predictive model. "
            "You must decide how (or whether) to retain them."
        ),
        mo.md("&nbsp;"),
        mo.md("*For every variable choose **one** action:*"),
        mo.Html(
            """
            <div style="display:flex; justify-content:center;">
              <table style="border-collapse:separate; border-spacing:0 6px; text-align:center;">
                <thead>
                  <tr>
                    <th style="padding:0.5rem 1.5rem;">Stance</th>
                    <th style="padding:0.5rem 1.5rem;">Meaning</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td style="padding:0.5rem 1.5rem;"><b>Include as-is</b></td>
                    <td style="padding:0.5rem 1.5rem;">
                      Feed directly into the predictive algorithm.
                    </td>
                  </tr>
                  <tr>
                    <td style="padding:0.5rem 1.5rem;"><b>Keep for Bias-Audit Only</b></td>
                    <td style="padding:0.5rem 1.5rem;">
                      Store alongside model outputs to test for disparate impact, but do not let the algorithm see it during training.
                    </td>
                  </tr>
                  <tr>
                    <td style="padding:0.5rem 1.5rem;"><b>Exclude Entirely</b></td>
                    <td style="padding:0.5rem 1.5rem;">
                      Do not collect or use in any form.
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            """
        ),
    ])
    return


@app.cell
def task_2_variable_selection(variable_selection_generator):
    variable_selection_generator(2)
    return


@app.cell
def task_2_initial_feedback(initial_feedback_generator):
    initial_feedback_generator(2)
    return


@app.cell
def section_separator(mo):
    mo.Html("""
    <hr style="border: 1px dashed black; margin-top:2.5rem; margin-bottom:3rem;">
    """)
    return


@app.cell(hide_code=True)
def anchor_task_3(mo):
    mo.Html('<div id="task_3"></div>')
    return


@app.cell(hide_code=True)
def task_3(mo):
    mo.vstack([
        mo.md("## Task 3 – Data-Reliability Gate: Data Quality, Context Awareness, and Proportionality"),
        mo.md(
            "**Note to the learner**  \n"
            "You now confront fields whose measurement error, missingness, or inconsistent collection raise doubts about usefulness. "
            "The Responsible-Data-Science principles at play are Data Quality, Context Awareness, and Proportionality "
            "(does the signal justify the noise?)."
        ),
        mo.md("&nbsp;"),
        mo.md("*For every variable choose **one** action:*"),
        mo.Html(
            """
            <div style="display:flex; justify-content:center;">
              <table style="border-collapse:separate; border-spacing:0 6px; text-align:center;">
                <thead>
                  <tr>
                    <th style="padding:0.5rem 1.5rem;">Action</th>
                    <th style="padding:0.5rem 1.5rem;">Meaning</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td style="padding:0.5rem 1.5rem;"><b>Include as-is</b></td>
                    <td style="padding:0.5rem 1.5rem;">
                      Accept the quality caveats and feed the variable to the model.
                    </td>
                  </tr>
                  <tr>
                    <td style="padding:0.5rem 1.5rem;"><b>Exclude (too unreliable)</b></td>
                    <td style="padding:0.5rem 1.5rem;">
                      Remove the variable entirely.
                    </td>
                  </tr>
                  <tr>
                    <td style="padding:0.5rem 1.5rem;"><b>Flag for Data-Quality Improvement</b></td>
                    <td style="padding:0.5rem 1.5rem;">
                      Pause use until stakeholders can standardise collection or transform it into a more reliable proxy.
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            """
        ),
    ])
    return


@app.cell
def task_3_variable_selection(variable_selection_generator):
    variable_selection_generator(3)
    return


@app.cell
def task_3_initial_feedback(initial_feedback_generator):
    initial_feedback_generator(3)
    return


@app.cell
def section_separator(mo):
    mo.Html("""
    <hr style="border: 1px dashed black; margin-top:2.5rem; margin-bottom:3rem;">
    """)
    return


@app.cell(hide_code=True)
def anchor_task_4(mo):
    mo.Html('<div id="task_4"></div>')
    return


@app.cell(hide_code=True)
def task_4(mo):
    mo.vstack([
        mo.md("## Task 4 – Equity & Actionability Gate: Beneficence, Proportionality, and Transparency"),
        mo.md(
            "**Note to the learner**  \n"
            "The final wave asks you to decide whether potentially predictive, yet ethically fraught variables belong in the model. "
            "Emphasis shifts to Beneficence, Proportionality, and Transparency. You must weigh (a) predictive value against "
            "(b) ability to drive a fair, actionable intervention."
        ),
        mo.md("&nbsp;"),
        mo.md("*For every variable choose **one** action:*"),
        mo.Html(
            """
            <div style="display:flex; justify-content:center;">
              <table style="border-collapse:separate; border-spacing:0 6px; text-align:center;">
                <thead>
                  <tr>
                    <th style="padding:0.5rem 1.5rem;">Action</th>
                    <th style="padding:0.5rem 1.5rem;">Meaning</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td style="padding:0.5rem 1.5rem;"><b>Include as-is</b></td>
                    <td style="padding:0.5rem 1.5rem;">
                      Feed it to the model. You're confident it predicts risk fairly and points advisors to a supportive intervention.
                    </td>
                  </tr>
                  <tr>
                    <td style="padding:0.5rem 1.5rem;"><b>Exclude (not fair or actionable)</b></td>
                    <td style="padding:0.5rem 1.5rem;">
                      Remove it. The risk of unfair treatment outweighs its predictive value, or advisors couldn't act on it.
                    </td>
                  </tr>
                  <tr>
                    <td style="padding:0.5rem 1.5rem;"><b>Flag for Equity &amp; Intervention Review</b></td>
                    <td style="padding:0.5rem 1.5rem;">
                      Hold it until stakeholders confirm it will drive supportive (not punitive) outreach and name a concrete intervention.
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            """
        ),
    ])
    return


@app.cell
def task_4_variable_selection(variable_selection_generator):
    variable_selection_generator(4)
    return


@app.cell
def task_4_initial_feedback(initial_feedback_generator):
    initial_feedback_generator(4)
    return


@app.cell(hide_code=True)
def section_separator(mo):
    mo.Html("""
    <hr style="border: 1px dashed black; margin-top:2.5rem; margin-bottom:3rem;">
    """)
    return


@app.cell
def wrapup_intro(variables_by_task):
    # ---- Collect all choices ----
    all_choices = [variables_by_task[tasknumber]['getter'][var]['state'] 
                   for tasknumber 
                   in variables_by_task 
                   for var 
                   in variables_by_task[tasknumber]['variables']
                  ]

    # ---- Count included variables ----
    include_count = sum(1 for c in all_choices if c == 'include')

    # ---- Keep returning states for later use ----
    return (include_count,)


@app.cell(hide_code=True)
def wrapup_summary_table(
    button_labels_by_task,
    include_count,
    mo,
    variables_by_task,
):
    import html
    variable_plural = "variable" if include_count == 1 else "variables"

    # one row per variable: (group, decision label shown on its button, variable title, justification)
    brief_rows = [
        (
            variables_by_task[task]['header'],
            button_labels_by_task[task][_g[var]['state']] if _g[var]['state'] else "No Selection",
            var.title,
            (_g[var]['text'] or "").strip(),
        )
        for task in variables_by_task
        for _g in [variables_by_task[task]['getter']]
        for var in variables_by_task[task]['variables']
    ]

    def brief_table_html(rows):
        out = "<table style='border-collapse:collapse; width:100%; text-align:left;'>"
        out += "<thead><tr><th>Group (Wave)</th><th>Decision</th><th>Variable</th><th>Justification</th></tr></thead><tbody>"
        for group in dict.fromkeys(r[0] for r in rows):
            out += f"<tr><td colspan='4' style='font-weight:bold; padding-top:10px;'>{html.escape(group)}</td></tr>"
            for _grp, decision, variable, why in rows:
                if _grp != group:
                    continue
                color = " style='background-color:#e8f5e9;'" if decision.startswith("Include") else ""
                out += (f"<tr{color}><td></td><td>{html.escape(decision)}</td><td>{html.escape(variable)}</td>"
                        f"<td>{html.escape(why) or ('—' if decision == 'No Selection' else '<i>No justification yet</i>')}</td></tr>")
            out += "<tr><td colspan='4' style='height:8px;'></td></tr>"
        return out + "</tbody></table>"

    table_html = brief_table_html(brief_rows)

    mo.vstack([
        mo.md("## End-of-Scenario Wrap-Up – Variable-Selection Brief"),
        mo.md(
        f"**_Your model will use the {include_count} {variable_plural} highlighted in green._** "
        "Is this acceptable, or would you like to revise your selections?"
    ),
        mo.Html(table_html)
    ])
    return brief_rows, brief_table_html, html


@app.cell
def review_wave_buttons(mo):
    button_output = []
    for num in range(1, 5):
        temp_md = f"""<a href=#task_{num}>""""""{temp_button}</a>"""
        temp_label = f"""Review Wave {num}"""
        button_output.append(mo.md(temp_md).batch(temp_button=mo.ui.button(label=temp_label)))
    mo.hstack(
        button_output
    )
    return


@app.cell
def final_feedback_divider(mo):
    mo.Html(f"""<hr style="border: 3px solid #4CAF50; margin-top:1rem; margin-bottom:1rem;">""")
    return


@app.cell
def final_feedback(
    format_final_feedback,
    gather_final_feedback,
    mo,
    variables_by_task,
):
    final_feedback_header = mo.Html(f"""<div style="text-align:center; color:#4CAF50; font-size:1.5rem; font-weight:bold; margin-bottom:1rem;">Final Feedback </div>""")

    final_output = []

    for task in variables_by_task: 
        local_header = f"""{variables_by_task[task]['header']} Feedback"""
        cor = []
        incor = []
        for var in variables_by_task[task]['variables']: 
            cor, incor = gather_final_feedback(var, variables_by_task[task]['getter'], cor, incor)
        final_task_output = format_final_feedback(cor, incor)
        final_output.append(mo.accordion({local_header: final_task_output}))

    mo.vstack([final_feedback_header]+ final_output)
    return


@app.cell
def brief_inputs(mo):
    student_name = mo.ui.text(label="Your name", full_width=True)
    advisor_notes = mo.ui.text_area(label="Notes for advisors and compliance staff (optional)", rows=5, full_width=True)
    reflection_prompts = [
        "Which decision was hardest to make, and what made it hard?",
        "Your model uses the variables you included. Is that enough for advisors to act on? "
        "What trade-off did you make between usefulness and protecting students?",
        "After reading the final feedback, which decision would you change, and why?",
    ]
    reflections = mo.ui.array([mo.ui.text_area(rows=5, full_width=True) for _ in reflection_prompts])
    return advisor_notes, reflection_prompts, reflections, student_name


@app.cell
def product(advisor_notes, brief_rows, mo, student_name):
    _missing_decision = sum(1 for r in brief_rows if r[1] == "No Selection")
    _missing_why = sum(1 for r in brief_rows if r[1] != "No Selection" and not r[3])
    _status = (
        mo.md("✅ **Every variable has a decision and a justification.** Your brief is complete.").callout("success")
        if not (_missing_decision or _missing_why)
        else mo.md(
            f"**Your brief is not complete yet:** {_missing_decision} variable(s) have no decision and "
            f"{_missing_why} decision(s) have no justification. Use the **Review Wave** buttons above to finish."
        ).callout("warn")
    )
    mo.vstack([
        mo.md("## Your Variable Selection Brief"),
        mo.md(
            "This is the product advisors and compliance staff will review before any modelling starts. "
            "It contains every decision and justification from the table above, plus your notes and reflection below. "
            "Download it at the bottom of the page and submit the file as instructed."
        ),
        _status,
        student_name,
        advisor_notes,
    ])
    return


@app.cell
def learner_reflection(include_count, mo, reflection_prompts, reflections):
    mo.vstack(
        [mo.md("## Learner Reflection"), mo.md(f"*Your model currently uses **{include_count}** variable(s).*")]
        + [mo.vstack([mo.md(f"**{i}. {q}**"), box]) for i, (q, box) in enumerate(zip(reflection_prompts, reflections), 1)]
    )
    return


@app.cell
def download_brief(
    advisor_notes,
    brief_rows,
    brief_table_html,
    html,
    include_count,
    mo,
    reflection_prompts,
    reflections,
    student_name,
):
    def _para(text):
        return html.escape(text.strip()).replace("\n", "<br>") if text.strip() else "<i>(left blank)</i>"

    _name = student_name.value.strip()
    _doc = f"""<!doctype html>
    <html lang="en"><head><meta charset="utf-8"><title>Variable Selection Brief</title>
    <style>
      body {{ font-family: system-ui, sans-serif; max-width: 900px; margin: 2rem auto; padding: 0 1rem; line-height: 1.5; }}
      th, td {{ padding: 4px 8px; vertical-align: top; border-bottom: 1px solid #ddd; }}
      @media print {{ body {{ margin: 0; }} }}
    </style></head><body>
    <h1>Variable Selection Brief</h1>
    <p><b>Name:</b> {html.escape(_name) or '<i>(not given)</i>'}<br>
    <b>Scenario:</b> Student Success Analytics, early-warning variable selection<br>
    <b>Variables included in the model:</b> {include_count}</p>
    <h2>Decisions and justifications</h2>
    {brief_table_html(brief_rows)}
    <h2>Notes for advisors and compliance staff</h2>
    <p>{_para(advisor_notes.value)}</p>
    <h2>Learner reflection</h2>
    {"".join(f"<h3>{i}. {html.escape(q)}</h3><p>{_para(a)}</p>" for i, (q, a) in enumerate(zip(reflection_prompts, reflections.value), 1))}
    </body></html>"""

    _slug = "".join(c if c.isalnum() else "-" for c in _name.lower()).strip("-")
    mo.vstack([
        mo.md("## Download your brief"),
        mo.md("The file opens in any web browser. To make a PDF, open it and use **Print → Save as PDF**."),
        mo.download(
            data=_doc.encode("utf-8"),
            filename=f"variable-selection-brief{'-' + _slug if _slug else ''}.html",
            mimetype="text/html",
            label="Download brief (.html)",
        ),
        mo.md("*Nothing is saved online: refreshing or closing this page erases your work, so download before you leave.*"),
    ])
    return


if __name__ == "__main__":
    app.run()
