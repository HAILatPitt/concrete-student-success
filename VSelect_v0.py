import marimo

__generated_with = "0.17.7"
app = marimo.App(width="medium")

with app.setup:
    import functools
    import html

    BUTTON_KINDS = {"include": "success", "exclude": "danger", "flag": "warn"}
    CHOICE_MARKS = {"include": "🟢", "exclude": "🔴", "flag": "🟠"}

    CARD_STYLE = (
        "<style>.poee-card>div{height:220px;border-radius:14px;padding:18px;box-sizing:border-box;"
        "font-size:14px;line-height:1.5;box-shadow:0 2px 8px rgba(0,0,0,.12);animation:poee-flip .45s ease}"
        "@keyframes poee-flip{from{transform:rotateY(90deg)}to{transform:rotateY(0)}}</style>"
    )
    CHOICES = ("include", "exclude", "flag")

    TASKS = {
        1: {
            "heading": 'Task 1 – Regulatory Gate',
            "header": 'Regulatory Gate',
            "labels": {'include': 'Include', 'exclude': 'Exclude', 'flag': 'Flag for Review'},
            "banner": "**What to do here.** Decide whether each financial-aid variable may be used at all. Federal rules and student-privacy law limit how individual financial-aid records can be used in automated decisions about a student.\n\nFor every variable choose **one** action, then justify it.\n\n| Choice | Meaning |\n|---|---|\n| **Include** | Use this variable in the predictive model. |\n| **Exclude** | Remove it from consideration. |\n| **Flag for Review** | Put the variable on hold until university counsel (or the IRB) provides guidance. |",
        },
        2: {
            "heading": 'Task 2 – Protected-Attribute Gate: Fairness and Equity Check',
            "header": 'Protected-Attribute Gate',
            "labels": {'include': 'Include As-Is', 'exclude': 'Exclude Entirely', 'flag': 'Keep for Bias-Audit Only'},
            "banner": "**What to do here.** This wave challenges you to balance fairness, inclusivity, and ethical use of sensitive personal attributes. The decision set differs from Wave 1: some attributes are useful for post-hoc bias auditing but risky inside a predictive model. You must decide how (or whether) to retain them.\n\nFor every variable choose **one** action, then justify it.\n\n| Choice | Meaning |\n|---|---|\n| **Include As-Is** | Feed directly into the predictive algorithm. |\n| **Keep for Bias-Audit Only** | Store alongside model outputs to test for disparate impact, but do not let the algorithm see it during training. |\n| **Exclude Entirely** | Do not collect or use in any form. |",
        },
        3: {
            "heading": 'Task 3 – Data-Reliability Gate: Data Quality, Context Awareness, and Proportionality',
            "header": 'Data-Reliability Gate',
            "labels": {'include': 'Include As-Is', 'exclude': 'Exclude (Too Unreliable)', 'flag': 'Flag for Data-Quality Improvement'},
            "banner": "**What to do here.** You now confront fields whose measurement error, missingness, or inconsistent collection raise doubts about usefulness. The Responsible-Data-Science principles at play are Data Quality, Context Awareness, and Proportionality (does the signal justify the noise?).\n\nFor every variable choose **one** action, then justify it.\n\n| Choice | Meaning |\n|---|---|\n| **Include As-Is** | Accept the quality caveats and feed the variable to the model. |\n| **Exclude (Too Unreliable)** | Remove the variable entirely. |\n| **Flag for Data-Quality Improvement** | Pause use until stakeholders can standardise collection or transform it into a more reliable proxy. |",
        },
        4: {
            "heading": 'Task 4 – Equity & Actionability Gate: Beneficence, Proportionality, and Transparency',
            "header": 'Equity & Actionability Gate',
            "labels": {'include': 'Include As-Is', 'exclude': 'Exclude (Not Fair or Actionable)', 'flag': 'Flag for Equity & Intervention Review'},
            "banner": "**What to do here.** The final wave asks you to decide whether potentially predictive, yet ethically fraught variables belong in the model. Emphasis shifts to Beneficence, Proportionality, and Transparency. You must weigh (a) predictive value against (b) ability to drive a fair, actionable intervention.\n\nFor every variable choose **one** action, then justify it.\n\n| Choice | Meaning |\n|---|---|\n| **Include As-Is** | Feed it to the model. You're confident it predicts risk fairly and points advisors to a supportive intervention. |\n| **Exclude (Not Fair or Actionable)** | Remove it. The risk of unfair treatment outweighs its predictive value, or advisors couldn't act on it. |\n| **Flag for Equity & Intervention Review** | Hold it until stakeholders confirm it will drive supportive (not punitive) outreach and name a concrete intervention. |",
        },
    }


    EVAL_STYLE = (
        "<style>.poee-eval{color:#0f172a}"
        ".poee-eval .sum,.poee-eval .ev{background:#fff;border-radius:12px;padding:16px 20px;margin:14px 0;"
        "box-shadow:0 2px 8px rgba(0,0,0,.15)}"
        ".poee-eval .big{font-size:22px;font-weight:700}"
        ".poee-eval .bar{display:flex;height:10px;border-radius:5px;overflow:hidden;margin:10px 0}"
        ".poee-eval .legend,.poee-eval .chips{font-size:12px;color:#475569;margin-top:6px}"
        ".poee-eval .chip{display:inline-block;background:#ecfdf5;border:1px solid #a7f3d0;border-radius:12px;"
        "padding:2px 8px;margin:2px}"
        ".poee-eval .ev{border-left:5px solid #f59e0b}.poee-eval .ev.harm{border-left-color:#ef4444}"
        ".poee-eval h3{margin:0 0 10px}"
        ".poee-eval .trail{display:flex;gap:8px;margin-bottom:10px}"
        ".poee-eval .trail div{flex:1;border-radius:8px;padding:8px 10px;font-size:13px;background:#f1f5f9}"
        ".poee-eval .trail .ok{background:#ecfdf5}"
        ".poee-eval .k{display:block;font-size:10px;text-transform:uppercase;letter-spacing:.05em;color:#64748b}"
        ".poee-eval .also{font-size:11px;color:#64748b}"
        ".poee-eval .why,.poee-eval .cost{font-size:13px;line-height:1.55;margin:8px 0}"
        ".poee-eval .cost{background:#fef2f2;border-radius:8px;padding:10px 12px}"
        ".poee-eval .grp{margin:22px 0 4px;font-size:12px;text-transform:uppercase;letter-spacing:.06em;"
        "color:#64748b}</style>"
    )

    REFLECTION_PROMPTS = [
        "Which variables from your prediction made it into your model, and which did you end up excluding or "
        "flagging? What changed your mind?",
        "Which variables you said \"can't be used\" turned out to be in the data dictionary, and how did you handle "
        "them? Did the dictionary contain restricted variables you hadn't anticipated?",
        "Your model uses the variables you included. Is that enough for advisors to act on? What trade-off did you "
        "make between usefulness and protecting students?",
    ]

    CARDS = {
        'story': {
            "title": 'The story so far',
            "icon": '📖',
            "background": 'linear-gradient(135deg,#4f46e5,#7c3aed)',
            "back": 'Retention from first to second year has been sliding for five years. The Provost wants advisors to reach struggling students before they leave. A new Student Success Analytics team has to build an early-warning tool, inside FERPA and the new federal limits on using financial-aid records.',
            "full": 'The university is a large research institution that competes for students in a crowded higher-education market. Over the past five years the first-to-second-year retention rate has drifted downward, and graduation timelines have lengthened. Senior leadership has asked the Office of the Provost to treat student persistence as a strategic priority rather than a routine metric. An internal mandate now calls for data-informed, proactive outreach so that support staff can offer help long before a student considers leaving. Within the Office of the Provost a small Student Success Analytics group has been established. This team combines institutional researchers, academic advisors, compliance officers, and data engineers. Its first assignment is to create an early warning intelligence tool that flags continuing undergraduates who appear at risk of stopping out or falling behind schedule. Advisors will then contact those students and connect them with tutoring, financial counseling, or mentoring. The analytics group is expected to respect privacy regulations such as FERPA and recent federal guidance that limits the use of individual financial-aid records in automated decision systems. It is also expected to uphold the university commitment to equity and transparency in every technical choice.',
        },
        'role': {
            "title": 'Your role',
            "icon": '🧑\u200d💻',
            "background": 'linear-gradient(135deg,#0284c7,#0ea5e9)',
            "back": "You are the team's data scientist. You won't build the model yet. You decide what goes into it. You have a data dictionary and red-flag notes from legal and ethics reviewers, and no raw records.",
            "full": 'You serve as the team’s data science specialist. Your immediate task is not to build a model but to decide which pieces of information should be fed into one. Working with colleagues you have assembled a data dictionary drawn from the university warehouse. The dictionary lists common attributes such as high school grade point averages, standardized test scores, race, gender, residency status, and course loads. It also contains financial indicators like Pell eligibility and Expected Family Contribution. Several context-specific items are included as well. Examples are whether a student applied to a regional campus after a main-campus denial, whether a student is a varsity athlete, and the distance between the student’s home address and campus. No raw records are available at this stage of the project; only the variable descriptions, their known limitations, and any red-flag notes provided by legal or ethical reviewers.',
        },
        'deliver': {
            "title": 'What you deliver',
            "icon": '📋',
            "background": 'linear-gradient(135deg,#059669,#10b981)',
            "back": 'A one-page Variable Selection Brief. Every variable is marked include, exclude, or flag, with a short reason tied to privacy, fairness, and usefulness. Advisors and compliance sign it before any modelling starts.',
            "full": 'Academic advisors need a concise, defensible list of candidate predictors that can drive a predictive model without violating regulations or undermining equitable treatment. Your deliverable for this scenario is a Variable Selection Brief. In one page you will designate each variable as included, excluded, or flagged for additional discussion. For every decision you will provide a short rationale that links back to the goals of privacy protection, fairness, and practical usefulness. Advisors and compliance staff will review and sign this brief before any modelling work proceeds.',
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

@app.function
def with_entry(mapping: dict, name: str, value) -> dict:
    return {**mapping, name: value}


@app.function
def record_decision(set_decisions, name: str, choice: str, _value=None) -> None:
    set_decisions(lambda decisions: with_entry(decisions, name, choice))


@app.function
def record_reason(set_reasons, name: str, text: str) -> None:
    set_reasons(lambda reasons: with_entry(reasons, name, text))


@app.function
def brief_rows_of(decisions: dict, reasons: dict) -> list[tuple]:
    """One row per variable: (group, decision label, variable title, justification)."""
    rows = []
    for name, v in VARIABLES.items():
        choice = decisions.get(name)
        label = TASKS[v["task"]]["labels"][choice] if choice else "No Selection"
        rows.append((TASKS[v["task"]]["header"], label, v["title"], reasons.get(name, "").strip()))
    return rows


@app.function
def brief_table_html(rows: list[tuple]) -> str:
    out = "<table style='border-collapse:collapse; width:100%; text-align:left;'>"
    out += "<thead><tr><th>Group (Wave)</th><th>Decision</th><th>Variable</th><th>Justification</th></tr></thead><tbody>"
    for group in dict.fromkeys(r[0] for r in rows):
        out += f"<tr><td colspan='4' style='font-weight:bold; padding-top:10px;'>{html.escape(group)}</td></tr>"
        for grp, decision, variable, why in rows:
            if grp != group:
                continue
            color = " style='background-color:#e8f5e9;'" if decision.startswith("Include") else ""
            empty = "—" if decision == "No Selection" else "<i>No justification yet</i>"
            out += (f"<tr{color}><td></td><td>{html.escape(decision)}</td><td>{html.escape(variable)}</td>"
                    f"<td>{html.escape(why) or empty}</td></tr>")
        out += "<tr><td colspan='4' style='height:8px;'></td></tr>"
    return out + "</tbody></table>"



@app.function
def cards_ready(opened: frozenset) -> bool:
    return set(CARDS) <= set(opened)


@app.function
def toggled(items: frozenset, item: str) -> frozenset:
    return frozenset(items ^ {item})


@app.function
def added(items: frozenset, item: str) -> frozenset:
    return frozenset(items | {item})


@app.function
def record_flip(set_flipped, set_opened, card_id: str, _value=None) -> None:
    set_flipped(lambda flipped: toggled(flipped, card_id))
    set_opened(lambda opened: added(opened, card_id))


@app.function
def card_html(card_id: str, flipped: bool) -> str:
    card = CARDS[card_id]
    if flipped:
        face = (f"<div style='background:#fff;color:#0f172a;border:1px solid #e2e8f0;'>"
                f"<b style='display:block;margin-bottom:6px'>{html.escape(card['title'], quote=False)}</b>"
                f"{html.escape(card['back'], quote=False)}</div>")
    else:
        face = (f"<div style='background:{card['background']};color:#fff;text-align:center;"
                f"display:flex;flex-direction:column;justify-content:center;'>"
                f"<div style='font-size:42px'>{card['icon']}</div>"
                f"<div style='font-size:20px;font-weight:700;margin-top:6px'>{html.escape(card['title'], quote=False)}</div>"
                f"<div style='font-size:12px;opacity:.85;margin-top:4px'>click Flip to open</div></div>")
    return CARD_STYLE + f"<div class='poee-card'>{face}</div>"


@app.function
def prediction_html(prediction: dict) -> str:
    sections = [("Could predict a student stopping out", "could_predict"), ("Available, but should not be used", "barred")]
    out = ""
    for heading, key in sections:
        items = "".join(
            f"<li><b>{html.escape(row['variable'].strip())}</b>"
            + (f" — {html.escape(row['reason'].strip())}" if row.get("reason", "").strip() else "")
            + "</li>"
            for row in prediction[key]
        )
        out += f"<h4>{heading}</h4><ul>{items}</ul>"
    return out


@app.function
def choice_label(name: str, choice: str) -> str:
    return TASKS[VARIABLES[name]["task"]]["labels"][choice]


@app.function
def correct_choice_html(name: str) -> str:
    first, *others = VARIABLES[name]["correct"]
    also = "".join(
        f" <span class='also'>({html.escape(choice_label(name, c))} also accepted)</span>" for c in others
    )
    return f"<b>{html.escape(choice_label(name, first))}</b>{also}"


@app.function
def wrong_card_html(wrong: dict) -> str:
    cost = (
        f"<div class='cost'><b>What happens in the real world.</b> {html.escape(wrong['consequence'])}</div>"
        if wrong["consequence"]
        else ""
    )
    return (
        f"<div class=\"ev {wrong['severity']}\"><h3>{html.escape(wrong['title'])}</h3>"
        f"<div class='trail'><div><span class='k'>You chose</span>"
        f"<b>{html.escape(choice_label(wrong['name'], wrong['chose']))}</b></div>"
        f"<div class='ok'><span class='k'>Correct choice</span>{correct_choice_html(wrong['name'])}</div></div>"
        f"<div class='why'><b>Why.</b> {html.escape(wrong['why'])}</div>{cost}</div>"
    )


@app.function
def evaluation_html(decisions: dict) -> str:
    counts, wrong = summary_counts(decisions), wrong_choices(decisions)
    chips = "".join(
        f"<span class='chip'>{html.escape(v['title'])}</span>"
        for name, v in VARIABLES.items()
        if decisions.get(name) and is_correct(name, decisions[name])
    )
    out = (
        f"{EVAL_STYLE}<div class='poee-eval'><div class='sum'>"
        f"<div class='big'>{counts['correct']} of {len(VARIABLES)} choices hold up. {len(wrong)} to review.</div>"
        f"<div class='bar'><div style='flex:{counts['correct']};background:#10b981'></div>"
        f"<div style='flex:{counts['harm']};background:#ef4444'></div>"
        f"<div style='flex:{counts['cautious']};background:#f59e0b'></div></div>"
        f"<div class='legend'>🟥 {counts['harm']} would cause harm or break a rule &nbsp; "
        f"🟧 {counts['cautious']} too cautious, or effort in the wrong place</div>"
        f"<div class='chips'>✓ Correct: {chips or '—'}</div></div>"
    )
    for task in TASKS:
        cards = [w for w in wrong if w["task"] == task]
        if cards:
            out += f"<div class='grp'>Task {task} · {html.escape(TASKS[task]['header'])}</div>"
            out += "".join(wrong_card_html(w) for w in cards)
    return out + "</div>"


@app.function
def paragraph_html(text: str) -> str:
    return html.escape(text.strip()).replace("\n", "<br>") if text.strip() else "<i>(left blank)</i>"


@app.function
def report_html(name: str, prediction: dict, decisions: dict, reasons: dict, notes: str, reflections: list[str]) -> str:
    include_count = sum(1 for choice in decisions.values() if choice == "include")
    answers = "".join(
        f"<h3>{i}. {html.escape(q)}</h3><p>{paragraph_html(a)}</p>"
        for i, (q, a) in enumerate(zip(REFLECTION_PROMPTS, reflections), 1)
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Variable Selection Brief</title>
<style>
  body {{ font-family: system-ui, sans-serif; max-width: 900px; margin: 2rem auto; padding: 0 1rem; line-height: 1.5; }}
  th, td {{ padding: 4px 8px; vertical-align: top; border-bottom: 1px solid #ddd; }}
  @media print {{ body {{ margin: 0; }} }}
</style></head><body>
<h1>Variable Selection Brief</h1>
<p><b>Name:</b> {html.escape(name.strip()) or '<i>(not given)</i>'}<br>
<b>Scenario:</b> Student Success Analytics, early-warning variable selection<br>
<b>Variables included in the model:</b> {include_count}</p>
<h2>Prediction (locked before the data dictionary)</h2>
{prediction_html(prediction)}
<h2>Decisions and justifications</h2>
{brief_table_html(brief_rows_of(decisions, reasons))}
<h2>Notes for advisors and compliance staff</h2>
<p>{paragraph_html(notes)}</p>
<h2>Learner reflection</h2>
{answers}
<h2>Evaluation</h2>
{evaluation_html(decisions)}
</body></html>"""


@app.cell
def _():
    import marimo as mo                           
    mo.md(
        "# Variable selection scenario\n"

    )
    return (mo,)

@app.cell
def card_states(mo):
    get_flipped, set_flipped = mo.state(frozenset())
    get_opened, set_opened = mo.state(frozenset())
    get_prediction, set_prediction = mo.state(None)
    return get_flipped, get_opened, get_prediction, set_flipped, set_opened, set_prediction


@app.cell
def flip_buttons(mo, set_flipped, set_opened):
    flip_buttons = {
        card_id: mo.ui.run_button(
            label="Flip",
            on_change=functools.partial(record_flip, set_flipped, set_opened, card_id),
        )
        for card_id in CARDS
    }
    return (flip_buttons,)


@app.cell(hide_code=True)
def flip_cards(flip_buttons, get_flipped, mo):
    mo.hstack(
        [
            mo.vstack([mo.Html(card_html(card_id, card_id in get_flipped())), flip_buttons[card_id]], align="center")
            for card_id in CARDS
        ],
        widths="equal",
        gap=1,
    )
    return


@app.cell
def predict_inputs(mo):
    def prediction_rows(reason_placeholder):
        return mo.ui.array([
            mo.ui.dictionary({
                "variable": mo.ui.text(placeholder="variable…", full_width=True),
                "reason": mo.ui.text(placeholder=reason_placeholder, full_width=True),
            })
            for _ in range(5)
        ])

    def rows_view(rows):
        return mo.vstack([mo.hstack([row["variable"], row["reason"]], widths=[1, 2]) for row in rows.elements])

    could_predict_rows = prediction_rows("why you think so…")
    barred_rows = prediction_rows("which rule or concern…")
    lock_button = mo.ui.run_button(label="🔒 Lock my prediction", kind="success")
    return barred_rows, could_predict_rows, lock_button, rows_view


@app.cell
def lock_prediction(barred_rows, could_predict_rows, lock_button, mo, set_prediction):
    _ready = prediction_ready(could_predict_rows.value, barred_rows.value)
    if lock_button.value and _ready:
        set_prediction({
            "could_predict": [row for row in could_predict_rows.value if has_variable(row)],
            "barred": [row for row in barred_rows.value if has_variable(row)],
        })
    lock_warning = (
        mo.callout(mo.md("Add at least one variable to each list."), kind="warn")
        if lock_button.value and not _ready
        else ""
    )
    return (lock_warning,)


@app.cell(hide_code=True)
def predict(
    barred_rows,
    could_predict_rows,
    get_opened,
    get_prediction,
    lock_button,
    lock_warning,
    mo,
    rows_view,
):
    mo.stop(not cards_ready(get_opened()), mo.md("*Open all three cards to begin.*"))
    _header = [
        mo.md("# Stage 1 · Predict"),
        mo.md(
            "Before you see the university's data dictionary, write down from your own knowledge:\n\n"
            "1. **Variables that could predict a student stopping out**, each with a one-line reason.\n"
            "2. **Variables the university probably holds but should not use**, each with the rule or concern that stops it.\n\n"
            "Once you lock your prediction it cannot be changed. You will come back to it at the end."
        ),
    ]
    if get_prediction() is None:
        _output = mo.vstack(_header + [
            mo.md("**Variables that could predict a student stopping out**"),
            rows_view(could_predict_rows),
            mo.md("**Variables the university probably holds but should not use (and why)**"),
            rows_view(barred_rows),
            lock_button,
            lock_warning,
        ])
    else:
        _output = mo.vstack(_header + [
            mo.callout(mo.vstack([mo.md("🔒 **Your locked prediction**"), mo.Html(prediction_html(get_prediction()))]), kind="neutral"),
        ])
    _output
    return


@app.cell(hide_code=True)
def briefing(get_prediction, mo):
    mo.stop(get_prediction() is None)
    mo.accordion({
        "Read the full briefing": mo.md(
            "\n\n".join(f"### {card['title']}\n\n{card['full']}" for card in CARDS.values())
        )
    })
    return


@app.cell
def states(mo):
    get_decisions, set_decisions = mo.state({name: None for name in VARIABLES})
    get_reasons, set_reasons = mo.state({name: "" for name in VARIABLES})
    get_submitted, set_submitted = mo.state(False)
    return (
        get_decisions,
        get_reasons,
        get_submitted,
        set_decisions,
        set_reasons,
        set_submitted,
    )


@app.cell
def controls(mo, set_decisions, set_reasons):
    # Only setters are referenced here, so these elements survive every rerun.
    def build_controls(name):
        labels = TASKS[VARIABLES[name]["task"]]["labels"]
        row = {
            choice: mo.ui.run_button(
                label=labels[choice],
                kind=BUTTON_KINDS[choice],
                on_change=functools.partial(record_decision, set_decisions, name, choice),
            )
            for choice in CHOICES
        }
        row["reason"] = mo.ui.text_area(
            label=f"Please briefly justify your reasoning for your {VARIABLES[name]['title']} choice.",
            rows=4,
            full_width=True,
            on_change=functools.partial(record_reason, set_reasons, name),
        )
        return row

    controls = {name: build_controls(name) for name in VARIABLES}
    return (controls,)


@app.cell
def views(mo):
    def decision_line(name, choice):
        if not choice:
            return "⚪️ You have **not yet selected** an option."
        label = TASKS[VARIABLES[name]["task"]]["labels"][choice]
        return f"{CHOICE_MARKS[choice]} You decided: **{label}**."

    def variable_view(name, decisions, reasons, controls, submitted):
        title, choice = VARIABLES[name]["title"], decisions[name]
        if submitted:
            return mo.md(f"**{title}**: {decision_line(name, choice)} {html.escape(reasons[name].strip()) or '*No justification.*'}")
        picker = mo.vstack([mo.md(VARIABLES[name]["definition"]), mo.hstack([controls[name][c] for c in CHOICES])])
        return mo.vstack([
            mo.accordion({title: picker}),
            mo.md(decision_line(name, choice)),
            controls[name]["reason"] if choice else "",
        ])

    def task_view(task, decisions, reasons, controls, submitted):
        return mo.vstack(
            [
                mo.Html(f'<div id="task_{task}"></div>'),
                mo.md(f"## {TASKS[task]['heading']}"),
                mo.callout(mo.md(TASKS[task]["banner"]), kind="info"),
            ]
            + [variable_view(name, decisions, reasons, controls, submitted) for name in variables_in(task)]
            + [mo.Html('<hr style="border: 1px dashed black; margin-top:2.5rem; margin-bottom:3rem;">')]
        )
    return (task_view,)


@app.cell
def observe_header(get_prediction, mo):
    mo.stop(get_prediction() is None)
    mo.md("# Stage 2 · Observe")
    return


@app.cell
def task_1(
    controls,
    get_decisions,
    get_prediction,
    get_reasons,
    get_submitted,
    mo,
    task_view,
):
    mo.stop(get_prediction() is None)
    task_view(1, get_decisions(), get_reasons(), controls, get_submitted())
    return


@app.cell
def task_2(
    controls,
    get_decisions,
    get_prediction,
    get_reasons,
    get_submitted,
    mo,
    task_view,
):
    mo.stop(get_prediction() is None)
    task_view(2, get_decisions(), get_reasons(), controls, get_submitted())
    return


@app.cell
def task_3(
    controls,
    get_decisions,
    get_prediction,
    get_reasons,
    get_submitted,
    mo,
    task_view,
):
    mo.stop(get_prediction() is None)
    task_view(3, get_decisions(), get_reasons(), controls, get_submitted())
    return


@app.cell
def task_4(
    controls,
    get_decisions,
    get_prediction,
    get_reasons,
    get_submitted,
    mo,
    task_view,
):
    mo.stop(get_prediction() is None)
    task_view(4, get_decisions(), get_reasons(), controls, get_submitted())
    return


@app.cell(hide_code=True)
def wrapup_summary_table(get_decisions, get_prediction, get_reasons, mo):
    mo.stop(get_prediction() is None)
    brief_rows = brief_rows_of(get_decisions(), get_reasons())
    include_count = sum(1 for choice in get_decisions().values() if choice == "include")
    variable_plural = "variable" if include_count == 1 else "variables"
    mo.vstack([
        mo.md("## End-of-Scenario Wrap-Up – Variable-Selection Brief"),
        mo.md(
            f"**_Your model will use the {include_count} {variable_plural} highlighted in green._** "
            "Is this acceptable, or would you like to revise your selections?"
        ),
        mo.Html(brief_table_html(brief_rows)),
    ])
    return brief_rows, include_count


@app.cell
def review_wave_buttons(get_prediction, mo):
    mo.stop(get_prediction() is None)
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
def explain_inputs(mo):
    student_name = mo.ui.text(label="Your name", full_width=True)
    advisor_notes = mo.ui.text_area(label="Notes for advisors and compliance staff (optional)", rows=5, full_width=True)
    reflections = mo.ui.array([mo.ui.text_area(rows=5, full_width=True) for _ in REFLECTION_PROMPTS])
    submit_button = mo.ui.run_button(label="Submit for evaluation", kind="success")
    return advisor_notes, reflections, student_name, submit_button


@app.cell
def submit_action(get_decisions, mo, reflections, set_submitted, submit_button):
    _ready = can_submit(get_decisions(), reflections.value)
    if submit_button.value and _ready:
        set_submitted(True)
    submit_warning = (
        mo.callout(mo.md("Answer all three reflection questions before you submit."), kind="warn")
        if submit_button.value and not _ready
        else ""
    )
    return (submit_warning,)


@app.cell(hide_code=True)
def explain(
    advisor_notes,
    get_decisions,
    get_prediction,
    get_reasons,
    get_submitted,
    mo,
    reflections,
    student_name,
    submit_button,
    submit_warning,
):
    mo.stop(get_prediction() is None)
    mo.stop(not all_decided(get_decisions()), mo.md("*Decide every variable to continue to Stage 3.*"))
    _missing = missing_reasons(get_decisions(), get_reasons())
    _header = [
        mo.md("# Stage 3 · Explain"),
        mo.md(
            "Reconcile what you decided with what you predicted before you saw the data dictionary. "
            "Your answers here go into your Variable Selection Brief."
        ),
        mo.callout(mo.vstack([mo.md("🔒 **Your locked prediction**"), mo.Html(prediction_html(get_prediction()))]), kind="neutral"),
    ]
    if get_submitted():
        _answers = [
            mo.md(f"**{i}. {q}**\n\n{html.escape(a.strip())}")
            for i, (q, a) in enumerate(zip(REFLECTION_PROMPTS, reflections.value), 1)
        ]
        _output = mo.vstack(_header + [mo.md(f"**Name:** {html.escape(student_name.value.strip()) or '*not given*'}")] + _answers + [
            mo.md(f"**Notes for advisors and compliance staff:** {html.escape(advisor_notes.value.strip()) or '*none*'}"),
            mo.callout(mo.md("✅ **Submitted.** Your choices and reflection are locked."), kind="success"),
        ])
    else:
        _reasons_note = (
            mo.callout(
                mo.md(f"**{len(_missing)} decision(s) have no justification.** You can still submit, "
                      "but advisors will read your brief. Use the **Review Wave** buttons above to add them."),
                kind="warn",
            )
            if _missing
            else ""
        )
        _questions = [
            mo.vstack([mo.md(f"**{i}. {q}**"), box])
            for i, (q, box) in enumerate(zip(REFLECTION_PROMPTS, reflections), 1)
        ]
        _output = mo.vstack(_header + [student_name] + _questions + [
            advisor_notes,
            _reasons_note,
            mo.md("Submitting locks every choice and reflection, then shows your evaluation."),
            submit_button,
            submit_warning,
        ])
    _output
    return


@app.cell(hide_code=True)
def evaluate(get_decisions, get_submitted, mo):
    mo.stop(not get_submitted())
    mo.vstack([
        mo.md("# Stage 4 · Evaluate"),
        mo.md(
            "Here is how your choices compare with the correct choices. Only the choices to review get a card: "
            "each one says why, and what would happen in the real world if the brief shipped as written."
        ),
        mo.Html(evaluation_html(get_decisions())),
    ])
    return


@app.cell
def download_brief(
    advisor_notes,
    get_decisions,
    get_prediction,
    get_reasons,
    get_submitted,
    mo,
    reflections,
    student_name,
):
    mo.stop(not get_submitted())
    _name = student_name.value.strip()
    _doc = report_html(
        _name, get_prediction(), get_decisions(), get_reasons(), advisor_notes.value, reflections.value
    )
    _slug = "".join(c if c.isalnum() else "-" for c in _name.lower()).strip("-")
    mo.vstack([
        mo.md("## Download your brief"),
        mo.md(
            "The file holds your prediction, every decision and justification, your reflection and this evaluation. "
            "It opens in any web browser. To make a PDF, open it and use **Print → Save as PDF**."
        ),
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
