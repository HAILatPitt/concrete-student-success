# VSelect_v2.py
# Joao Gilberto and Caleb Finamore for RDS@Pitt

import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium", app_title="ConCReTE Student Success")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    """Configuration for all variable categories"""

    CATEGORY_CONFIG = {
        "financial": {
            "options": [
                {"label": "Include", "kind": "success", "value": "include"},
                {"label": "Exclude", "kind": "danger", "value": "exclude"},
                {"label": "Flag for Review", "kind": "warn", "value": "flag"},
            ],
            "emoji_map": {"include": "🟢", "exclude": "🔴", "flag": "🟡", None: "⚪️"},
            "text_map": {
                "include": "Include",
                "exclude": "Exclude",
                "flag": "Flag for Review",
                None: "no selection",
            },
        },
        "protected": {
            "options": [
                {"label": "Include as-is", "kind": "success", "value": "include_as_is"},
                {
                    "label": "Keep for Bias-Audit Only",
                    "kind": "warn",
                    "value": "audit_only",
                },
                {
                    "label": "Exclude Entirely",
                    "kind": "danger",
                    "value": "exclude_entirely",
                },
            ],
            "emoji_map": {
                "include_as_is": "🟢",
                "audit_only": "🟡",
                "exclude_entirely": "🔴",
                None: "⚪️",
            },
            "text_map": {
                "include_as_is": "Include as-is",
                "audit_only": "Keep for Bias-Audit Only",
                "exclude_entirely": "Exclude Entirely",
                None: "no selection",
            },
        },
        "reliability": {
            "options": [
                {"label": "Include as-is", "kind": "success", "value": "include_as_is"},
                {
                    "label": "Exclude (too unreliable)",
                    "kind": "danger",
                    "value": "exclude_unreliable",
                },
                {
                    "label": "Flag for Data-Quality Improvement",
                    "kind": "warn",
                    "value": "flag_improvement",
                },
            ],
            "emoji_map": {
                "include_as_is": "🟢",
                "exclude_unreliable": "🔴",
                "flag_improvement": "🟡",
                None: "⚪️",
            },
            "text_map": {
                "include_as_is": "Include as-is",
                "exclude_unreliable": "Exclude (too unreliable)",
                "flag_improvement": "Flag for Data-Quality Improvement",
                None: "no selection",
            },
        },
        "equity": {
            "options": [
                {"label": "Include as-is", "kind": "success", "value": "include_as_is"},
                {
                    "label": "Exclude (too unreliable)",
                    "kind": "danger",
                    "value": "exclude_unreliable",
                },
                {
                    "label": "Flag for Data-Quality Improvement",
                    "kind": "warn",
                    "value": "flag_improvement",
                },
            ],
            "emoji_map": {
                "include_as_is": "🟢",
                "exclude_unreliable": "🔴",
                "flag_improvement": "🟡",
                None: "⚪️",
            },
            "text_map": {
                "include_as_is": "Include as-is",
                "exclude_unreliable": "Exclude (too unreliable)",
                "flag_improvement": "Flag for Data-Quality Improvement",
                None: "no selection",
            },
        },
    }

    return (CATEGORY_CONFIG,)


@app.cell
def _():
    """Metadata for all variables"""

    META_DICT = {
        "pell": {
            "title": "Pell Status",
            "description": (
                "Whether a student receives a federal Pell Grant. "
                "New regulations restrict use of financial-aid data in predictive modeling."
            ),
            "category": "financial",
        },
        "efc": {
            "title": "Expected Family Contribution (EFC)",
            "description": (
                "Amount a family is expected to contribute to education costs "
                "(legacy FAFSA metric). Regulatory compliance requires excluding this sensitive financial information."
            ),
            "category": "financial",
        },
        "sai": {
            "title": "Student Aid Index (SAI)",
            "description": (
                "A new metric from recent FAFSA changes replacing EFC. "
                "Coverage may be inconsistent across historical data."
            ),
            "category": "financial",
        },
        "unmet_need": {
            "title": "Unmet Need",
            "description": (
                "Gap between cost of attendance and available resources. "
                "May be restricted due to new financial-data limitations."
            ),
            "category": "financial",
        },
        "merit_award": {
            "title": "Merit Award Amount",
            "description": (
                "Scholarship funding awarded for academic achievement. "
                "May inadvertently reflect socioeconomic background."
            ),
            "category": "financial",
        },
        "pell_plus": {
            "title": "Pell Plus",
            "description": (
                "Institutional matching funds tied to Pell eligibility. "
                "Likely subject to the same use restrictions as Pell Status."
            ),
            "category": "financial",
        },
    }

    return (META_DICT,)


@app.cell
def _(mo):
    """Story context and instructions"""

    context = """
    # ConCReTE: Student Success Model
    ---
    ## The Story So Far
    Over the past five years, the first-to-second-year retention rate at a prestigious research university has drifted downward. An internal mandate now calls for data-informed, proactive outreach so that support staff can offer help long before a student considers leaving. Within the Office of the Provost a small Student Success Analytics group has been established. This team combines institutional researchers, academic advisors, compliance officers, and data engineers. The analytics group is expected to respect privacy regulations such as FERPA and recent federal guidance that limits the use of individual financial-aid records in automated decision systems. It is also expected to uphold the university commitment to equity and transparency in every technical choice.


    ### Business Objective 
    The Student Success Analytics group has been asked to create an early warning intelligence tool that flags continuing undergraduates who appear at risk of stopping out or falling behind schedule. Advisors will then contact those students and connect them with tutoring, financial counseling, or mentoring. 

    ### Product
    Academic advisors need a concise, defensible list of candidate predictors that can drive a predictive model without violating regulations or undermining equitable treatment. Your deliverable for this scenario is a Variable Selection Brief. Working with colleagues you have assembled a data dictionary drawn from the university warehouse. The dictionary lists common student attributes in several categories, including academic, financial, and demographic. No raw records are available at this stage of the project; only the variable descriptions, their known limitations, and any red-flag notes provided by legal or ethical reviewers. In one page, your team will designate each variable as included, excluded, or flagged for additional discussion. For every decision you will provide a short rationale that links back to the goals of privacy protection, fairness, and practical usefulness. Advisors and compliance staff will review and sign this brief before any modelling work proceeds.

    ### Role   
    You are a compliance officer tasked with assessing which data points can and can not be a part of the Student Success group's model. Your work will inform the dataset on which the model will be trained. 

    ---
    ## Task 1 Regulatory Gate
    *For each variable choose **one** action:*
    """

    html = """
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

    mo.vstack([mo.md(context), mo.Html(html), mo.md("---")])
    return


@app.cell
def _(mo):
    """Create all state for financial variables - return getters"""

    financial_keys = ["pell", "efc", "sai", "unmet_need", "merit_award", "pell_plus"]

    financial_states = {}
    for _key in financial_keys:
        get_choice, set_choice = mo.state(None)
        get_justification, set_justification = mo.state("")

        financial_states[_key] = {
            "get_choice": get_choice,
            "set_choice": set_choice,
            "get_justification": get_justification,
            "set_justification": set_justification,
        }

    return financial_keys, financial_states


@app.cell
def _(
    CATEGORY_CONFIG,
    META_DICT,
    financial_keys,
    financial_states,
    mo,
):
    """Display financial variables - this cell re-runs when states change"""

    components = []

    for _key in financial_keys:
        _state = financial_states[_key]
        _meta = META_DICT[_key]
        _config = CATEGORY_CONFIG[_meta["category"]]

        # Read current state - this makes the cell reactive
        _choice = _state["get_choice"]()
        _justification =_state["get_justification"]()

        # Build buttons
        buttons = [
            mo.ui.button(
                label=opt["label"],
                kind=opt["kind"],
                on_click=lambda _, val=opt["value"], s=_state: s["set_choice"](val),
            )
            for opt in _config["options"]
        ]

        # Accordion with buttons
        accordion_content = mo.vstack([
            mo.md(_meta["description"]),
            mo.hstack(buttons, gap="1rem"),
        ])
        accordion = mo.accordion({_meta["title"]: accordion_content})

        # Feedback - based on current choice
        emoji = _config["emoji_map"][_choice]
        text = _config["text_map"][_choice]
        feedback = mo.md(f"You decided to {emoji} **{text}** the variable.")

        # Justification - only show after selection
        if _choice is None:
            justification_ui = mo.md("")
        else:
            justification_ui = mo.ui.text_area(
                label=f"Please briefly justify your reasoning for your {_meta['title']} choice",
                value=justification,
                on_change=lambda v, s=state: s["set_justification"](v),
                rows=4,
            )

        # Combine into component
        components.append(mo.vstack([
            accordion,
            feedback,
            justification_ui,
            mo.md("---"),
        ]))

    mo.vstack(components)
    return


@app.cell
def _(CATEGORY_CONFIG, META_DICT, financial_keys, financial_states, mo):
    """Summary table - re-runs when states change"""
    import pandas as pd

    rows = []
    for _key in financial_keys:
        _state = financial_states[_key]
        _meta = META_DICT[_key]
        _config = CATEGORY_CONFIG[_meta["category"]]

        # Read state
        _choice = _state["get_choice"]()
        _justification = _state["get_justification"]()

        # Convert to user-friendly text
        text_label = _config["text_map"][_choice]

        rows.append({
            "Variable": _meta["title"],
            "Decision": text_label,
            "Justification": _justification if _justification else "",
        })

    df = pd.DataFrame(rows)
    mo.ui.table(df)
    return


if __name__ == "__main__":
    app.run()
