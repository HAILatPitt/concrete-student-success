import marimo

__generated_with = "0.17.7"
app = marimo.App(width="compact")

with app.setup:
    import functools
    import html

    BUTTON_KINDS = {"include": "success", "exclude": "danger", "flag": "warn"}

    FONT_LINK = (
        "<link rel='stylesheet' href='https://fonts.googleapis.com/css2?family=Libre+Franklin:"
        "wght@400;500;600;700&family=Lora:ital,wght@0,400;0,500;0,600;1,400;1,500&display=swap'>"
    )
    # Pitt navy is the case's ink; Pitt gold marks what the learner adds. Cool hue-260 neutrals.
    PALETTE = (
        ".ss{--gold:#FFB81C;--navy:#003594;--navy-dk:#003163;--ink:oklch(0.24 0.012 260);"
        "--mid:oklch(0.47 0.010 260);--rule:oklch(0.86 0.006 260);--wash:oklch(0.975 0.004 260);"
        "--sans:'Libre Franklin','PT Sans',sans-serif;--serif:'Lora',Georgia,serif;"
        "color:var(--ink);font-family:var(--sans)}"
    )
    # Card faces render inside the marimo button's shadow root, so they carry their own styles.
    CARD_STYLE = (
        ".ss-card{box-sizing:border-box;width:224px;height:300px;overflow:hidden;background:#fff;"
        "border:1px solid var(--rule);border-radius:2px;display:flex;flex-direction:column;text-align:left;"
        "white-space:normal;font-weight:400;box-shadow:0 1px 0 var(--rule),0 8px 18px -14px rgba(0,49,99,.35);"
        "animation:ss-flip .4s cubic-bezier(.2,.7,.3,1) both}"
        ".ss-card:hover{border-color:var(--gold)}"
        ".ss-front-face{display:var(--ss-front,flex)}.ss-back-face{display:var(--ss-back,none)}"
        "@keyframes ss-flip{from{transform:rotateY(90deg);opacity:.4}to{transform:rotateY(0);opacity:1}}"
        ".ss-band,.ss-band-b{display:flex;align-items:center;justify-content:center;"
        "font:600 12px/1 var(--sans);letter-spacing:.16em;text-transform:uppercase}"
        ".ss-band{height:54px;background:var(--navy);color:#fff}"
        ".ss-band-b{height:40px;margin-top:auto;background:var(--gold);color:var(--navy-dk)}"
        ".ss-front-body{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;"
        "text-align:center;padding:0 20px}"
        ".ss-numeral{font:italic 400 22px/1 var(--serif);color:var(--navy)}"
        ".ss-front-title{font:500 24px/1.15 var(--serif);color:var(--ink);margin-top:10px}"
        ".ss-hair{width:28px;height:2px;background:var(--gold);margin:14px auto 0}"
        ".ss-back{padding:18px 18px 14px}"
        ".ss-back-head{display:flex;align-items:baseline;justify-content:space-between;"
        "border-bottom:2px solid var(--navy);padding-bottom:7px}"
        ".ss-back-head b{font:500 16px/1.1 var(--serif);color:var(--ink)}"
        ".ss-back-head i{font:italic 400 15px/1 var(--serif);color:var(--navy)}"
        ".ss-back-text{display:block;font:400 13px/1.45 var(--sans);color:var(--ink);margin:9px 0 0;hyphens:auto}"
        ".ss-back-text::first-letter{font:500 30px/.8 var(--serif);float:left;color:var(--navy);margin:3px 4px 0 0}"
    )
    # marimo's button is a fixed-height inline-flex; centring it in a card-height flex slot lets the
    # card overflow it symmetrically and sit in normal flow. The card's -9px margin covers the button's
    # 7.2px side padding and 1px border. ponytail: tied to marimo 0.17.7's button box; re-check on upgrade.
    CARD_SLOT = {"display": "flex", "align-items": "center", "justify-content": "center", "height": "300px"}
    # Page-level blocks (light DOM), injected once by the title cell.
    BRIEF_STYLE = (
        ".ss-kicker{font:600 12px/1 var(--sans);letter-spacing:.14em;text-transform:uppercase;color:var(--navy)}"
        ".ss-title{font:500 42px/1.1 var(--serif);letter-spacing:-.01em;margin:10px 0 30px;color:var(--ink)}"
        ".ss-gate{margin:18px 0 0;text-align:center;font:italic 400 15px/1.4 var(--serif);color:var(--mid)}"
        ".ss-gate::before,.ss-gate::after{content:'';display:inline-block;width:36px;height:1px;"
        "background:var(--rule);vertical-align:middle;margin:0 12px}"
        ".ss-stage{margin-top:40px}"
        ".ss-runhead{display:flex;justify-content:space-between;font:600 12px/1 var(--sans);letter-spacing:.14em;"
        "text-transform:uppercase;color:var(--mid);border-top:2px solid var(--navy-dk);padding-top:9px}"
        ".ss-runhead span:first-child{color:var(--navy)}"
        ".ss-stage-title{font:500 34px/1.1 var(--serif);margin:18px 0 0;padding:0;border:0;color:var(--ink)}"
        ".ss-stage-title em{font-style:italic;color:var(--navy)}"
        ".ss-steps{display:flex;gap:18px;margin-top:12px;font:400 13px/1 var(--sans);color:var(--mid)}"
        ".ss-step.now{color:var(--ink);font-weight:600;border-bottom:2px solid var(--gold);padding-bottom:3px}"
        ".ss-prompt{margin-top:22px;background:var(--wash);border-top:1px solid var(--rule);"
        "border-bottom:1px solid var(--rule);padding:18px 22px;font:400 16px/1.6 var(--serif);color:var(--ink)}"
        ".ss-prompt .n{font-style:italic;color:var(--navy)}"
        ".ss-prompt strong{font-weight:600}"
        ".ss-label{display:grid;grid-template-columns:34px 1fr;align-items:baseline;margin:22px 0 8px}"
        ".ss-label i{font:italic 400 20px/1 var(--serif);color:var(--navy)}"
        ".ss-label span{font:600 14px/1.35 var(--sans);color:var(--ink)}"
        ".ss-indent{padding-left:34px}"
        ".ss-locked{margin-top:22px;background:var(--wash);border-top:2px solid var(--navy-dk);"
        "border-bottom:1px solid var(--rule);padding:14px 22px 18px}"
        ".ss-locked-head{font:600 12px/1 var(--sans);letter-spacing:.14em;text-transform:uppercase;color:var(--navy)}"
        ".ss-locked h4{font:italic 500 16px/1.3 var(--serif);color:var(--ink);margin:14px 0 4px}"
        ".ss-locked p{font:400 15px/1.55 var(--sans);margin:0}"
        ".ss-task-title{font:500 24px/1.2 var(--serif);color:var(--ink);margin:34px 0 12px;padding:0;border:0}"
        ".ss-brief{background:var(--wash);border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);"
        "padding:16px 22px 18px;font:400 14px/1.6 var(--sans);color:var(--ink)}"
        ".ss-brief p{margin:0 0 10px}"
        ".ss-brief table{width:100%;border-collapse:collapse;margin:6px 0 0;font-size:13.5px}"
        ".ss-brief th,.ss-brief td{text-align:left;vertical-align:top;padding:7px 10px 7px 0;"
        "border-bottom:1px solid var(--rule)}"
        ".ss-brief th{font:600 11px/1 var(--sans);letter-spacing:.12em;text-transform:uppercase;color:var(--navy);"
        "border-bottom:2px solid var(--navy)}"
        ".ss-brief td:first-child{white-space:nowrap;padding-right:18px}"
        ".ss-note{margin:16px 0 0;background:#fff8e6;border-top:2px solid var(--gold);padding:12px 18px;"
        "font:400 14px/1.55 var(--sans);color:var(--ink)}"
        ".ss-note.ok{background:#ecfdf5;border-top-color:#15803d}"
        ".ss-sheet{width:100%;border-collapse:collapse;font:400 13.5px/1.45 var(--sans);color:var(--ink)}"
        ".ss-sheet th{text-align:left;font:600 11px/1 var(--sans);letter-spacing:.12em;text-transform:uppercase;"
        "color:var(--navy);border-bottom:2px solid var(--navy);padding:8px 10px 8px 0}"
        ".ss-sheet td{text-align:left;vertical-align:top;padding:7px 10px 7px 0;border-bottom:1px solid var(--rule)}"
        ".ss-sheet .grp td{font:600 12px/1 var(--sans);letter-spacing:.1em;text-transform:uppercase;color:var(--mid);"
        "padding-top:18px;border-bottom:1px solid var(--navy-dk)}"
        ".ss-sheet .inc td{background:#ecfdf5}"
        ".ss-sheet .muted{color:var(--mid);font-style:italic}"
    )
    STAGES = ("Predict", "Observe", "Explain", "Evaluate")
    CHOICES = ("include", "exclude", "flag")

    TASKS = {
        1: {
            "heading": 'Task 1 – Regulatory Gate',
            "header": 'Regulatory Gate',
            "labels": {'include': 'Include', 'exclude': 'Exclude', 'flag': 'Flag for Review'},
            "banner": "**What to do here.** Decide whether each financial-aid variable may be used at all. Federal law limits FAFSA data, and the IRS tax data inside it, to awarding and administering aid and to research that identifies no one. The school's own aid records fall under FERPA, the student-privacy law.\n\nFor every variable choose **one** action, then justify it.\n\n| Choice | Meaning |\n|---|---|\n| **Include** | Use this variable in the predictive model. |\n| **Exclude** | Remove it from consideration. |\n| **Flag for Review** | Put the variable on hold until university counsel (or the IRB) provides guidance. |",
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
        "<style>.poee-eval .sum{background:var(--wash);border-top:2px solid var(--navy-dk);"
        "border-bottom:1px solid var(--rule);padding:16px 22px;margin:14px 0}"
        ".poee-eval .big{font:500 22px/1.3 var(--serif);color:var(--ink)}"
        ".poee-eval .bar{display:flex;height:8px;overflow:hidden;margin:12px 0}"
        ".poee-eval .legend,.poee-eval .chips{font:400 12.5px/1.6 var(--sans);color:var(--mid);margin-top:6px}"
        ".poee-eval .chip{display:inline-block;background:#fff;border:1px solid var(--rule);padding:1px 8px;margin:2px;"
        "color:var(--ink)}"
        ".poee-eval .ev{background:#fff;border:1px solid var(--rule);border-top:3px solid #d97706;padding:16px 20px;margin:14px 0}"
        ".poee-eval .ev.harm{border-top-color:#b91c1c}"
        ".poee-eval h3{font:500 19px/1.25 var(--serif);color:var(--ink);margin:0 0 12px;padding:0;border:0}"
        ".poee-eval .trail{display:flex;gap:8px;margin-bottom:10px}"
        ".poee-eval .trail div{flex:1;padding:8px 10px;font:400 13px/1.4 var(--sans);background:var(--wash)}"
        ".poee-eval .trail .ok{background:#ecfdf5}"
        ".poee-eval .k{display:block;font:600 10.5px/1.4 var(--sans);text-transform:uppercase;letter-spacing:.1em;"
        "color:var(--mid)}"
        ".poee-eval .also{font-size:11.5px;color:var(--mid)}"
        ".poee-eval .key{display:inline-block;width:10px;height:10px;margin:0 6px -1px 0}"
        ".poee-eval .why,.poee-eval .cost{font:400 14px/1.6 var(--sans);color:var(--ink);margin:8px 0}"
        ".poee-eval .cost{background:#fdf3f2;padding:10px 12px}"
        ".poee-eval .grp{margin:26px 0 4px;font:600 12px/1 var(--sans);text-transform:uppercase;letter-spacing:.14em;"
        "color:var(--navy)}</style>"
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
            "numeral": 'i',
            "title": 'The story so far',
            "back": 'Retention from first to second year has been sliding for five years. The Provost wants advisors to reach struggling students before they leave. A new Student Success Analytics team has to build an early-warning tool, inside FERPA and the federal limits on using FAFSA data.',
            "full": 'The university is a large research institution that competes for students in a crowded higher-education market. Over the past five years the first-to-second-year retention rate has drifted downward, and graduation timelines have lengthened. Senior leadership has asked the Office of the Provost to treat student persistence as a strategic priority rather than a routine metric. An internal mandate now calls for data-informed, proactive outreach so that support staff can offer help long before a student considers leaving. Within the Office of the Provost a small Student Success Analytics group has been established. This team combines institutional researchers, academic advisors, compliance officers, and data engineers. Its first assignment is to create an early warning intelligence tool that flags continuing undergraduates who appear at risk of stopping out or falling behind schedule. Advisors will then contact those students and connect them with tutoring, financial counseling, or mentoring. The analytics group is expected to respect privacy regulations such as FERPA and the federal law and Department of Education guidance that limit how FAFSA data may be used. It is also expected to uphold the university commitment to equity and transparency in every technical choice.',
        },
        'role': {
            "numeral": 'ii',
            "title": 'Your role',
            "back": "You are the team's data scientist. You won't build the model yet. You decide what goes into it. You have a data dictionary and red-flag notes from legal and ethics reviewers, and no raw records.",
            "full": 'You serve as the team’s data science specialist. Your immediate task is not to build a model but to decide which pieces of information should be fed into one. Working with colleagues you have assembled a data dictionary drawn from the university warehouse. The dictionary lists common attributes such as high school grade point averages, standardized test scores, race, gender, residency status, and course loads. It also contains financial indicators like Pell eligibility and Expected Family Contribution. Several context-specific items are included as well. Examples are whether a student applied to a regional campus after a main-campus denial, whether a student is a varsity athlete, and the distance between the student’s home address and campus. No raw records are available at this stage of the project; only the variable descriptions, their known limitations, and any red-flag notes provided by legal or ethical reviewers.',
        },
        'deliver': {
            "numeral": 'iii',
            "title": 'What you deliver',
            "back": 'A one-page Variable Selection Brief. Every variable is marked include, exclude, or flag, with a short reason tied to privacy, fairness, and usefulness. Advisors and compliance sign it before any modelling starts.',
            "full": 'Academic advisors need a concise, defensible list of candidate predictors that can drive a predictive model without violating regulations or undermining equitable treatment. Your deliverable for this scenario is a Variable Selection Brief. In one page you will designate each variable as included, excluded, or flagged for additional discussion. For every decision you will provide a short rationale that links back to the goals of privacy protection, fairness, and practical usefulness. Advisors and compliance staff will review and sign this brief before any modelling work proceeds.',
        },
    }

    VARIABLES = {
        'pell': {
            "task": 1,
            "title": 'Pell Status',
            "definition": (
                'Whether a student receives a federal Pell Grant. The Pell eligibility flag in the FAFSA '
                "results is FAFSA data; a record of Pell actually paid is the school's own record."
            ),
            "correct": ['exclude', 'flag'],
            "why": {
                'include': (
                    'If this is the Pell eligibility flag from the FAFSA results, federal law limits FAFSA '
                    'data to awarding and administering aid and to research that identifies no one, and a '
                    'model that flags named students for outreach is neither. A record of Pell actually paid '
                    'falls under FERPA instead, but it is a direct marker of low income, so it needs legal '
                    'and equity review before any use. Reporting it in aggregate is the safer route.'
                ),
            },
            "consequence": {
                'include': (
                    "Compliance won't sign the brief, and if the FAFSA eligibility flag ships anyway the "
                    'university is using FAFSA data outside what the law allows. For students, being low-'
                    'income becomes the reason an advisor calls, so the first thing a Pell student hears is '
                    '"we think you\'ll struggle."'
                ),
            },
        },
        'efc': {
            "task": 1,
            "title": 'Expected Family Contribution (EFC)',
            "definition": (
                'Amount a family was expected to contribute to education costs, calculated from the '
                'FAFSA. Replaced by the Student Aid Index from the 2024–25 award year, so only older '
                'records have it.'
            ),
            "correct": ['exclude'],
            "why": {
                'include': (
                    'EFC is FAFSA data: federal law limits FAFSA data to awarding and administering aid and '
                    'to research that identifies no one, and a model that flags named students for outreach '
                    'is neither. It also stopped existing in 2024–25, so most current students have no value '
                    'at all.'
                ),
                'flag': (
                    'A review adds little here. EFC is derived from the FAFSA and has been retired, so the '
                    'answer is already clear: keep it out of the model.'
                ),
            },
            "consequence": {
                'include': (
                    'Most current students have no EFC, so the model learns from older cohorts and treats the'
                    " missing value as a signal. Using FAFSA data this way also falls outside the law's "
                    'permitted uses, and compliance will send the brief back.'
                ),
                'flag': (
                    'Counsel spends time on a question the law already answers, and modelling waits while '
                    'they do. Students gain nothing except a later start to outreach.'
                ),
            },
        },
        'sai': {
            "task": 1,
            "title": 'Student Aid Index (SAI)',
            "definition": (
                'A new metric from recent FAFSA changes that replaced EFC. Recent implementation means '
                'this data may not be available for all students in your historical dataset.'
            ),
            "correct": ['exclude'],
            "why": {
                'include': (
                    'SAI is FAFSA data: federal law limits FAFSA data to awarding and administering aid and '
                    'to research that identifies no one, and a model that flags named students for outreach '
                    'is neither. It exists only from 2024–25, so the historical data behind the model would '
                    'be largely missing.'
                ),
                'flag': (
                    'A review adds little here. SAI is derived from the FAFSA and carries the same '
                    'restrictions as other FAFSA data, and many past students have no SAI on record. Keep it '
                    'out of the model.'
                ),
            },
            "consequence": {
                'include': (
                    "Only students from 2024–25 onward have an SAI, so the model can't learn from past "
                    'cohorts and treats the gap as a signal. It also uses FAFSA data outside the permitted '
                    'uses, which compliance will reject.'
                ),
                'flag': (
                    'A review spends legal time confirming what the law already says and delays the model. '
                    "The brief also looks unsure about a clear rule, which weakens advisors' trust in the "
                    'rest of it.'
                ),
            },
        },
        'unmet': {
            "task": 1,
            "title": 'Unmet Need',
            "definition": (
                'Gap between the cost of attendance and the student’s available resources, calculated '
                'from the aid package and the Student Aid Index. A strong financial-stress signal.'
            ),
            "correct": ['exclude', 'flag'],
            "why": {
                'include': (
                    "Unmet Need is the school's own aid record, governed by FERPA, but it is built on the "
                    'Student Aid Index, and next to cost of attendance and aid amounts it can reveal that '
                    'FAFSA figure. It also flags students for being poor rather than for anything advisors '
                    'can change.'
                ),
            },
            "consequence": {
                'include': (
                    "Students get flagged because they can't afford college, not for anything advisors can "
                    'fix, so outreach turns into "you\'re at risk because you\'re poor." Because unmet need can'
                    ' reveal the Student Aid Index, the university also risks exposing FAFSA data through its'
                    ' own records.'
                ),
            },
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
            "consequence": {
                'include': (
                    'Merit awards go disproportionately to students from well-resourced schools, so the model'
                    ' learns that having no award means risk and flags lower-income students more often. '
                    'Advisors spend their time on family income rather than on how students are doing.'
                ),
            },
        },
        'pell_plus': {
            "task": 1,
            "title": 'Pell Plus',
            "definition": (
                "University matching funds paid to Pell Grant recipients. The award is the school's own "
                'record, but it reveals that the student receives Pell.'
            ),
            "correct": ['exclude', 'flag'],
            "why": {
                'include': (
                    'Pell Plus reveals Pell receipt, a direct marker of low income. Using it to flag '
                    'individual students needs legal and equity review first, and it adds little beyond Pell '
                    'Status.'
                ),
            },
            "consequence": {
                'include': (
                    'It reveals who receives Pell, so the low-income flag comes in by the back door. '
                    'Compliance will spot the link, and Pell students get singled out a second time.'
                ),
            },
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
            "consequence": {
                'include': (
                    'Students would be flagged partly because of their race, which invites a civil-rights '
                    'complaint and lasting damage to trust. Black and Latino students who are doing fine get '
                    "calls implying they're expected to fail."
                ),
                'exclude': (
                    'With race gone, nobody can check whether the model flags some groups far more than '
                    'others. If it does, the university finds out from a complaint or a news story instead of'
                    ' its own audit.'
                ),
            },
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
            "consequence": {
                'include': (
                    "Flags would differ by gender for reasons advisors can't act on, which looks like "
                    'discrimination in any review. Students get outreach based on who they are rather than '
                    "how they're doing."
                ),
                'exclude': (
                    'You lose the ability to see whether the model flags men and women at different rates. A '
                    'gender gap in outreach could run for years without anyone noticing.'
                ),
            },
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
            "consequence": {
                'include': (
                    'Older, non-traditional students get flagged for their age, and outreach reads as "people'
                    ' like you don\'t finish." Age-discrimination complaints become a real exposure.'
                ),
                'exclude': (
                    "Without age you can't check whether the model fails adult learners, a group with real "
                    'and specific needs. Problems for them stay invisible.'
                ),
            },
        },
        'pronouns': {
            "task": 2,
            "title": 'Preferred Pronouns',
            "definition": (
                'Student-provided pronoun preference collected by campus climate office. Optional field '
                'with high missingness. Can affirm identity but is not a stable predictor of retention.'
            ),
            "correct": ['exclude'],
            "why": {
                'include': (
                    'Preferred Pronouns are not predictive of persistence and risk trivializing gender '
                    'identity. Exclude or store only for awareness training, not analytics.'
                ),
                'flag': (
                    'Pronoun data are optional, mostly missing and not standardised, so they cannot support a'
                    ' reliable bias audit either. Excluding them is the clearer choice.'
                ),
            },
            "consequence": {
                'include': (
                    'A mostly empty, optional field becomes a signal, so students who shared their pronouns '
                    "are treated differently from those who didn't. Trans and nonbinary students could be "
                    'flagged for disclosing their identity.'
                ),
                'flag': (
                    "The team keeps sensitive identity data it can't use, adding privacy risk with nothing in"
                    ' return. A breach would expose students who trusted the campus climate office.'
                ),
            },
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
            "consequence": {
                'include': (
                    'Because high schools grade differently, the model favours students from generous graders'
                    ' and flags those from rigorous or under-resourced schools. Advisors chase noise while '
                    'real risk goes unflagged.'
                ),
            },
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
            "consequence": {
                'include': (
                    'Under test-optional admissions, missing scores look like low scores, so students who '
                    "didn't submit get flagged for a policy choice. Those are often the lower-income students"
                    ' test-optional was meant to help.'
                ),
                'exclude': (
                    'You throw away useful information, including the simple fact of whether a student '
                    'submitted scores. The model gets weaker with no gain in fairness.'
                ),
            },
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
                    'Mid-term grades appear only for some courses, so students in those courses would look '
                    'riskier than others. Flag it for data-quality improvement before the model uses it.'
                ),
                'exclude': (
                    'Excluding Mid-Term Grades forfeits early academic-performance insight. Could selective '
                    'inclusion or data-quality work make it viable?'
                ),
            },
            "consequence": {
                'include': (
                    'Students in courses that report midterms look riskier than identical students in courses'
                    " that don't, so flags follow course choice and department habits. Advisors call the "
                    'wrong students.'
                ),
                'exclude': (
                    'The model loses its most timely academic signal. Students who are struggling now get '
                    'missed until final grades post, after the withdrawal deadline.'
                ),
            },
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
                    'Sparse, faculty-dependent reporting could mislead the model. Flag it so stakeholders can'
                    ' improve reporting first.'
                ),
                'exclude': (
                    'You lose a proven early-alert signal. Engage stakeholders to improve reporting rather '
                    'than discard entirely.'
                ),
            },
            "consequence": {
                'include': (
                    'Reports arrive only from some faculty, so students in those classes get flagged more and'
                    ' others are missed. Which students get outreach ends up depending on which instructors '
                    'file reports.'
                ),
                'exclude': (
                    'The university drops an early-alert system it already runs instead of fixing it. '
                    'Struggling students lose one of the few signals that arrives early enough to help.'
                ),
            },
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
            "consequence": {
                'include': (
                    'Counts depend on which printers were online and who uses dorm machines, so commuters and'
                    ' students with their own printers look "inactive." Advisors chase a meaningless number.'
                ),
                'flag': (
                    'Time and money go into fixing printer logs that will never predict persistence. That '
                    'effort comes out of the budget for signals that matter.'
                ),
            },
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
            "consequence": {
                'include': (
                    'Students whose parents attended are treated as lower risk, which steers support toward '
                    'the already advantaged. First-generation students, who need the help most, are pushed '
                    'down the list.'
                ),
            },
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
            "consequence": {
                'include': (
                    'Athletes already have dedicated academic advising, so the model sends a second, '
                    'uncoordinated call to the same students. Advisor time is wasted and athletes get mixed '
                    'messages.'
                ),
                'exclude': (
                    'A group with known time pressures disappears from the model, so no one checks whether '
                    'athletics advising is catching everyone. Athletes who slip through get no backup.'
                ),
            },
        },
        'firstgen': {
            "task": 4,
            "title": 'First Generation Status',
            "definition": (
                'Indicates if the student is the first in their family to attend college; may reflect '
                'differences in familiarity with college processes.'
            ),
            "correct": ['include'],
            "why": {
                'exclude': (
                    'First-generation students often benefit from navigational support. Omitting this '
                    'variable could undermine equity goals.'
                ),
                'flag': (
                    'Holding First Generation Status back delays a variable with a clear, supportive use. The'
                    ' intervention (navigational support such as mentoring and help with college processes) '
                    'is already known, so a review adds little.'
                ),
            },
            "consequence": {
                'exclude': (
                    "The model can't see a group that benefits from navigational support, so first-generation"
                    ' students confused by college processes get no early call. The university loses an easy '
                    'equity win.'
                ),
                'flag': (
                    'Outreach to first-generation students waits on a review with an obvious answer. Students'
                    ' who need help in their first term may not get it until their second.'
                ),
            },
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
            "consequence": {
                'include': (
                    'Students who live far away get flagged, but advisors have little to offer about '
                    'distance, so the flag leads nowhere. It can also stand in for a rural or low-income '
                    'background.'
                ),
                'exclude': (
                    'Geographically isolated students, who often struggle with belonging, become invisible. '
                    'Community-building programmes lose the data they need to reach them.'
                ),
            },
        },
        'credits': {
            "task": 4,
            "title": 'Credits After Add/Drop',
            "definition": (
                'Credit hours the student is taking after the official add/drop deadline; may reflect '
                'adjustment to academic realities.'
            ),
            "correct": ['include'],
            "why": {
                'exclude': (
                    'Course-load changes are an actionable red flag. Excluding them weakens the model’s '
                    'practical value.'
                ),
                'flag': (
                    'Credit-load data comes straight from the registrar, so it is reliable, and advisors can '
                    'act on a drop right away. Holding it for review only delays a strong early signal.'
                ),
            },
            "consequence": {
                'exclude': (
                    'The model misses one of the clearest early warnings: a student who drops below full time'
                    ' after add/drop. Advisors find out only when the student fails to re-enrol.'
                ),
                'flag': (
                    'A strong, reliable signal sits idle while a review confirms what is already known. '
                    'Students who cut their load in week two wait longer for a call.'
                ),
            },
        },
        'housing': {
            "task": 4,
            "title": 'Live On Campus or Commuter',
            "definition": 'Housing status affects integration into campus life and access to resources.',
            "correct": ['include'],
            "why": {
                'exclude': (
                    'Housing status strongly predicts engagement. Excluding it may mask differences in '
                    'retention risk.'
                ),
                'flag': (
                    'Housing status is reliable and the support is already clear: commuter-friendly advising,'
                    ' hours and resources. Holding it for review delays a useful signal.'
                ),
            },
            "consequence": {
                'exclude': (
                    'Commuters, who often have the weakest ties to campus, become invisible to the model. '
                    'Support built for them never reaches the students who need it.'
                ),
                'flag': (
                    'The model waits on a review of a reliable variable with a clear use. Commuters who are '
                    'drifting away get help later than they could.'
                ),
            },
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
            "consequence": {
                'include': (
                    'Out-of-state and international students get flagged for where they come from, which for '
                    'international students can look like national-origin bias. Outreach risks telling them '
                    "they don't belong."
                ),
                'exclude': (
                    'You lose sight of the tuition burden out-of-state students carry, so financial outreach '
                    "can't target them. Students leave for cost reasons no one saw coming."
                ),
            },
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
            "consequence": {
                'include': (
                    'A guessed urban, rural or suburban label feeds the model as if it were fact, so '
                    'mislabelled students get the wrong outreach. Rural students may be stereotyped by a '
                    'heuristic.'
                ),
                'exclude': (
                    'Rural-to-urban transition problems go unseen. Students struggling with that move get no '
                    'targeted support.'
                ),
            },
        },
        'transfer': {
            "task": 4,
            "title": 'Transfer Status',
            "definition": (
                'Whether the student transferred from another institution versus starting as a first-'
                'year.'
            ),
            "correct": ['include'],
            "why": {
                'exclude': (
                    'You dropped a key subgroup with elevated departure risk. Advisors may miss needed '
                    'support.'
                ),
                'flag': (
                    'Transfer students face known credit-articulation hurdles, and the support is concrete. '
                    'Holding the variable for review delays help for a group with elevated departure risk.'
                ),
            },
            "consequence": {
                'exclude': (
                    'Transfer students, who leave at higher rates, disappear from the model. Credit-'
                    'articulation problems that one meeting could fix go unnoticed.'
                ),
                'flag': (
                    'Outreach to transfer students waits on a review with a clear answer. Credit problems '
                    'that should be caught in the first term are found later.'
                ),
            },
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
            "consequence": {
                'include': (
                    'Self-reported involvement favours students who fill in surveys, so quiet or busy '
                    'students look disengaged. Students who work long hours get flagged for working.'
                ),
                'exclude': (
                    'A useful belonging signal is thrown away instead of being cleaned up. The model loses '
                    'its only measure of social connection.'
                ),
            },
        },
        'wi_fi': {
            "task": 4,
            "title": 'Campus-Wi-Fi Gaming Network Participation',
            "definition": (
                'Binary flag—student devices connected to high-traffic gaming ports for ≥ 5 hours/week '
                'during evenings.'
            ),
            "correct": ['exclude'],
            "why": {
                'include': (
                    'Correlation to retention unproven; risk of pathologising hobby behaviour. Provide '
                    'theoretical justification or exclude.'
                ),
                'flag': (
                    "There is nothing for a review to rescue: monitoring students' gaming traffic is "
                    'intrusive surveillance with no established link to persistence. Exclude it.'
                ),
            },
            "consequence": {
                'include': (
                    "The university would be watching students' network traffic to judge them, and when "
                    'students find out, trust collapses. Gamers get flagged for a hobby with no proven link '
                    'to dropping out.'
                ),
                'flag': (
                    "A review gives a surveillance idea legitimacy and burns committee time on it. Students' "
                    'privacy stays at risk while the committee meets.'
                ),
            },
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
def prediction_ready(could_predict: str, barred: str) -> bool:
    return bool(could_predict.strip()) and bool(barred.strip())


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
def record_field(setter, key: str, text: str) -> None:
    setter(lambda fields: with_entry(fields, key, text))


@app.function
def reflections_of(fields: dict) -> list[str]:
    return [fields.get(f"r{i}", "") for i in range(1, len(REFLECTION_PROMPTS) + 1)]


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
    out = "<table class='ss-sheet'><tr><th>Variable</th><th>Decision</th><th>Justification</th></tr>"
    for group in dict.fromkeys(r[0] for r in rows):
        out += f"<tr class='grp'><td colspan='3'>{html.escape(group)}</td></tr>"
        for grp, decision, variable, why in rows:
            if grp != group:
                continue
            row_class = " class='inc'" if decision.startswith("Include") else ""
            shown = html.escape(why) if why else "<span class='muted'>none yet</span>"
            if decision == "No Selection":
                shown = "—"
            out += (f"<tr{row_class}><td>{html.escape(variable)}</td><td>{html.escape(decision)}</td>"
                    f"<td>{shown}</td></tr>")
    return out + "</table>"



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
def card_html(card_id: str) -> str:
    card = CARDS[card_id]
    title = html.escape(card["title"], quote=False)
    front = (
        "<div class='ss-card ss-front-face'><div class='ss-band'>Student Success</div>"
        f"<div class='ss-front-body'><div class='ss-numeral'>{card['numeral']}</div>"
        f"<div class='ss-front-title'>{title}</div><div class='ss-hair'></div></div>"
        "<div class='ss-band-b'>Click to open</div></div>"
    )
    back = (
        f"<div class='ss-card ss-back ss-back-face'><div class='ss-back-head'><b>{title}</b><i>{card['numeral']}</i></div>"
        f"<div class='ss-back-text'>{html.escape(card['back'], quote=False)}</div></div>"
    )
    return f"<style>{PALETTE}{CARD_STYLE}</style><div class='ss' style='margin:0 -9px'>{front}{back}</div>"


@app.function
def card_slot_style(flipped: bool) -> dict:
    # The face is chosen by custom properties, which inherit into the button's shadow root.
    return {**CARD_SLOT, "--ss-front": "none" if flipped else "flex", "--ss-back": "none" if not flipped else "block"}


@app.function
def bold_html(text: str) -> str:
    parts = html.escape(text, quote=False).split("**")
    return "".join(f"<strong>{part}</strong>" if i % 2 else part for i, part in enumerate(parts))


@app.function
def banner_html(task: int) -> str:
    lines = TASKS[task]["banner"].split("\n")
    paragraphs = [line for line in lines if line.strip() and not line.startswith("|")]
    rows = [line.strip("|").split("|") for line in lines if line.startswith("|") and not line.startswith("|---")]
    head, *body = [[cell.strip() for cell in row] for row in rows]
    table = (
        "<table><tr>" + "".join(f"<th>{bold_html(cell)}</th>" for cell in head) + "</tr>"
        + "".join("<tr>" + "".join(f"<td>{bold_html(cell)}</td>" for cell in row) + "</tr>" for row in body)
        + "</table>"
    )
    return "<div class='ss ss-brief'>" + "".join(f"<p>{bold_html(p)}</p>" for p in paragraphs) + table + "</div>"


@app.function
def stage_header_html(stage: int) -> str:
    steps = "".join(
        f'<span class="ss-step now">{name}</span>' if i == stage else f'<span class="ss-step">{name}</span>'
        for i, name in enumerate(STAGES, 1)
    )
    return (
        f'<div class="ss ss-stage"><div class="ss-runhead"><span>Variable Selection Brief</span>'
        f"<span>Stage {stage} of 4</span></div>"
        f'<h2 class="ss-stage-title"><em>Stage {stage}</em> · {STAGES[stage - 1]}</h2>'
        f'<div class="ss-steps">{steps}</div></div>'
    )


@app.function
def locked_prediction_html(prediction: dict) -> str:
    return (
        '<div class="ss ss-locked"><div class="ss-locked-head">Your locked prediction</div>'
        f"{prediction_html(prediction)}</div>"
    )


@app.function
def prediction_html(prediction: dict) -> str:
    sections = [("Could predict a student stopping out", "could_predict"), ("Available, but should not be used", "barred")]
    return "".join(f"<h4>{heading}</h4><p>{paragraph_html(prediction[key])}</p>" for heading, key in sections)


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
        f"<style>{PALETTE}</style>{EVAL_STYLE}<div class='ss poee-eval'><div class='sum'>"
        f"<div class='big'>{counts['correct']} of {len(VARIABLES)} choices hold up. {len(wrong)} to review.</div>"
        f"<div class='bar'><div style='flex:{counts['correct']};background:#15803d'></div>"
        f"<div style='flex:{counts['harm']};background:#b91c1c'></div>"
        f"<div style='flex:{counts['cautious']};background:#d97706'></div></div>"
        f"<div class='legend'><span class='key' style='background:#b91c1c'></span>{counts['harm']} would cause harm "
        f"or break a rule &nbsp; <span class='key' style='background:#d97706'></span>{counts['cautious']} too "
        "cautious, or effort in the wrong place</div>"
        f"<div class='chips'>Correct: {chips or '—'}</div></div>"
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


@app.function
def wrapup_prompt(include_count: int, submitted: bool) -> str:
    noun = "variable" if include_count == 1 else "variables"
    if submitted:
        return f"**_Your model uses the {include_count} {noun} highlighted in green._** Your choices are locked."
    return (
        f"**_Your model will use the {include_count} {noun} highlighted in green._** "
        "Is this acceptable, or would you like to revise your selections?"
    )


@app.cell(hide_code=True)
def _():
    import marimo as mo

    mo.Html(
        f"{FONT_LINK}<style>{PALETTE}{BRIEF_STYLE}</style>"
        "<div class='ss'><div class='ss-kicker'>ConCReTE · Student Success Analytics</div>"
        "<h1 class='ss-title'>Variable selection scenario</h1></div>"
    )
    return (mo,)


@app.cell
def card_states(mo):
    get_flipped, set_flipped = mo.state(frozenset())
    get_opened, set_opened = mo.state(frozenset())
    get_prediction, set_prediction = mo.state(None)
    return get_flipped, get_opened, get_prediction, set_flipped, set_opened, set_prediction


@app.cell(hide_code=True)
def card_buttons(mo, set_flipped, set_opened):
    # Built once, both faces in the label; flip_cards picks the face, so a button is never recreated.
    story_card, role_card, deliver_card = (
        mo.ui.run_button(
            label=card_html(card_id),
            on_change=functools.partial(record_flip, set_flipped, set_opened, card_id),
        )
        for card_id in ("story", "role", "deliver")
    )
    return deliver_card, role_card, story_card


@app.cell(hide_code=True)
def flip_cards(deliver_card, get_flipped, get_opened, mo, role_card, story_card):
    _slots = [
        card.style(card_slot_style(card_id in get_flipped()))
        for card_id, card in (("story", story_card), ("role", role_card), ("deliver", deliver_card))
    ]
    _gate = "" if cards_ready(get_opened()) else mo.Html("<p class='ss ss-gate'>Open all three cards to begin.</p>")
    mo.vstack([mo.hstack(_slots, justify="space-between", wrap=True, gap=1), _gate])
    return


@app.cell
def predict_inputs(mo):
    get_draft, set_draft = mo.state({"could_predict": "", "barred": ""})
    lock_button = mo.ui.run_button(label="Lock my prediction", kind="success")
    return get_draft, lock_button, set_draft


@app.cell
def predict_boxes(mo, set_draft):
    # A plain dict is not tracked by marimo, so the cell that renders these never re-runs while
    # the learner types; the text reaches the kernel through state instead.
    predict_boxes = {
        "could_predict": mo.ui.text_area(
            placeholder="e.g. first-term GPA, because early grades show who is struggling",
            rows=6,
            full_width=True,
            on_change=functools.partial(record_field, set_draft, "could_predict"),
        ),
        "barred": mo.ui.text_area(
            placeholder="e.g. race, because it is a protected attribute",
            rows=6,
            full_width=True,
            on_change=functools.partial(record_field, set_draft, "barred"),
        ),
    }
    return (predict_boxes,)


@app.cell
def lock_prediction(get_draft, lock_button, mo, set_prediction):
    _draft = get_draft()
    _ready = prediction_ready(_draft["could_predict"], _draft["barred"])
    if lock_button.value and _ready:
        set_prediction({key: text.strip() for key, text in _draft.items()})
    lock_warning = (
        mo.Html("<div class='ss ss-note'>Write something in both boxes before you lock.</div>")
        if lock_button.value and not _ready
        else ""
    )
    return (lock_warning,)


@app.cell(hide_code=True)
def predict(get_opened, get_prediction, lock_button, lock_warning, mo, predict_boxes):
    mo.stop(not cards_ready(get_opened()))
    _header = [
        mo.Html(stage_header_html(1)),
        mo.Html(
            "<div class='ss ss-prompt'>Before you see the university's data dictionary, write down from your own "
            "knowledge: <span class='n'>(1)</span> variables that could predict a student stopping out, each with a "
            "one-line reason; <span class='n'>(2)</span> variables the university probably holds but should not use, "
            "each with the rule or concern that stops it. <strong>Once you lock your prediction it cannot be "
            "changed.</strong> You will come back to it at the end.</div>"
        ),
    ]
    if get_prediction() is None:
        _output = mo.vstack(_header + [
            mo.Html(
                "<div class='ss'><div class='ss-label'><i>1</i><span>Variables that could predict a student "
                f"stopping out</span></div><div class='ss-indent'>{predict_boxes['could_predict']}</div>"
                "<div class='ss-label'><i>2</i><span>Variables the university probably holds but should not use "
                f"(and why)</span></div><div class='ss-indent'>{predict_boxes['barred']}</div>"
                f"<div class='ss-indent' style='margin-top:22px'>{lock_button}</div></div>"
            ),
            lock_warning,
        ])
    else:
        _output = mo.vstack(_header + [mo.Html(locked_prediction_html(get_prediction()))])
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
            return "*Not decided yet.*"
        label = TASKS[VARIABLES[name]["task"]]["labels"][choice]
        return f"You decided: **{label}**."

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
                mo.Html(f"<h3 class='ss ss-task-title'>{html.escape(TASKS[task]['heading'])}</h3>"),
                mo.Html(banner_html(task)),
            ]
            + [variable_view(name, decisions, reasons, controls, submitted) for name in variables_in(task)]
            + [mo.Html('<hr style="border: 1px dashed black; margin-top:2.5rem; margin-bottom:3rem;">')]
        )
    return (task_view,)


@app.cell
def observe_header(get_prediction, mo):
    mo.stop(get_prediction() is None)
    mo.Html(stage_header_html(2))
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
def wrapup_summary_table(get_decisions, get_prediction, get_reasons, get_submitted, mo):
    mo.stop(get_prediction() is None)
    _include_count = sum(1 for choice in get_decisions().values() if choice == "include")
    mo.vstack([
        mo.md("## End-of-Scenario Wrap-Up – Variable-Selection Brief"),
        mo.md(wrapup_prompt(_include_count, get_submitted())),
        mo.Html(f"<div class='ss'>{brief_table_html(brief_rows_of(get_decisions(), get_reasons()))}</div>"),
    ])
    return


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
    get_explain, set_explain = mo.state({"name": "", "notes": "", "r1": "", "r2": "", "r3": ""})
    submit_button = mo.ui.run_button(label="Submit for evaluation", kind="success")
    return get_explain, set_explain, submit_button


@app.cell
def explain_fields(mo, set_explain):
    # Plain dict for the same reason as predict_boxes: the explain cell must not re-run on typing.
    explain_fields = {
        "name": mo.ui.text(full_width=True, on_change=functools.partial(record_field, set_explain, "name")),
        "notes": mo.ui.text_area(rows=5, full_width=True, on_change=functools.partial(record_field, set_explain, "notes")),
        **{
            f"r{i}": mo.ui.text_area(rows=5, full_width=True, on_change=functools.partial(record_field, set_explain, f"r{i}"))
            for i in range(1, len(REFLECTION_PROMPTS) + 1)
        },
    }
    return (explain_fields,)


@app.cell
def submit_action(get_decisions, get_explain, mo, set_submitted, submit_button):
    _ready = can_submit(get_decisions(), reflections_of(get_explain()))
    if submit_button.value and _ready:
        set_submitted(True)
    submit_warning = (
        mo.Html("<div class='ss ss-note'>Answer all three reflection questions before you submit.</div>")
        if submit_button.value and not _ready
        else ""
    )
    return (submit_warning,)


@app.cell(hide_code=True)
def explain(
    explain_fields,
    get_decisions,
    get_explain,
    get_prediction,
    get_reasons,
    get_submitted,
    mo,
    submit_button,
    submit_warning,
):
    mo.stop(get_prediction() is None)
    mo.stop(not all_decided(get_decisions()), mo.md("*Decide every variable to continue to Stage 3.*"))
    _header = [
        mo.Html(stage_header_html(3)),
        mo.md(
            "Reconcile what you decided with what you predicted before you saw the data dictionary. "
            "Your answers here go into your Variable Selection Brief."
        ),
        mo.Html(locked_prediction_html(get_prediction())),
    ]
    if get_submitted():
        _fields = get_explain()
        _answers = "".join(
            f"<div class='ss-label'><i>{i}</i><span>{html.escape(q)}</span></div>"
            f"<div class='ss-indent'>{paragraph_html(a)}</div>"
            for i, (q, a) in enumerate(zip(REFLECTION_PROMPTS, reflections_of(_fields)), 1)
        )
        _output = mo.vstack(_header + [
            mo.Html(
                f"<div class='ss'><div class='ss-label'><i></i><span>Name</span></div>"
                f"<div class='ss-indent'>{paragraph_html(_fields['name'])}</div>{_answers}"
                f"<div class='ss-label'><i></i><span>Notes for advisors and compliance staff</span></div>"
                f"<div class='ss-indent'>{paragraph_html(_fields['notes'])}</div></div>"
            ),
            mo.Html("<div class='ss ss-note ok'><strong>Submitted.</strong> Your choices and reflection are locked.</div>"),
        ])
    else:
        _missing = missing_reasons(get_decisions(), get_reasons())
        _reasons_note = (
            mo.Html(
                f"<div class='ss ss-note'><strong>{len(_missing)} decision(s) have no justification.</strong> "
                "You can still submit, but advisors will read your brief. Use the <strong>Review Wave</strong> "
                "buttons above to add them.</div>"
            )
            if _missing
            else ""
        )
        _questions = "".join(
            f"<div class='ss-label'><i>{i}</i><span>{html.escape(q)}</span></div>"
            f"<div class='ss-indent'>{explain_fields[f'r{i}']}</div>"
            for i, q in enumerate(REFLECTION_PROMPTS, 1)
        )
        _output = mo.vstack(_header + [
            mo.Html(
                f"<div class='ss'><div class='ss-label'><i></i><span>Your name</span></div>"
                f"<div class='ss-indent'>{explain_fields['name']}</div>{_questions}"
                f"<div class='ss-label'><i></i><span>Notes for advisors and compliance staff (optional)</span></div>"
                f"<div class='ss-indent'>{explain_fields['notes']}</div></div>"
            ),
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
        mo.Html(stage_header_html(4)),
        mo.md(
            "Here is how your choices compare with the correct choices. Only the choices to review get a card: "
            "each one says why, and what would happen in the real world if the brief shipped as written."
        ),
        mo.Html(evaluation_html(get_decisions())),
    ])
    return


@app.cell
def download_brief(get_decisions, get_explain, get_prediction, get_reasons, get_submitted, mo):
    mo.stop(not get_submitted())
    _fields = get_explain()
    _name = _fields["name"].strip()
    _doc = report_html(
        _name, get_prediction(), get_decisions(), get_reasons(), _fields["notes"], reflections_of(_fields)
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
