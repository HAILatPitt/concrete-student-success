# Student Success POEE Restructure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructure `VSelect_v0.py` into a gated Predict → Observe → Explain → Evaluate notebook. Feedback appears only at Evaluate, as cards for wrong choices that name real-world consequences, built on a corrected and fact-checked answer key.

**Architecture:** The notebook stays a single marimo file. The answer key and every rule that decides correctness, severity and gating move into the `app.setup` block and `@app.function` functions. A plain test script can then import and test them (verified to work on marimo 0.17.7). Reactive cells hold only UI. About 100 per-variable `mo.state` pairs and getter cells are replaced by five states: `decisions`, `reasons`, `flipped`/`opened` cards, `prediction`, `submitted`.

**Tech Stack:** Python 3.11+, marimo==0.17.7 (the only runtime dependency, Pyodide/WASM-safe), `uv`.

**Spec:** `/Users/qingchang/Library/CloudStorage/Dropbox/CONCRETE/docs/superpowers/specs/2026-10-20-student-success-poee-design.md`. Mockups referenced by the spec: `CONCRETE/.superpowers/brainstorm/25579-1792505670/content/{poee-flow-v2,evaluate-card-v2}.html`.

## Global Constraints

- Single notebook `VSelect_v0.py`. The only dependency is `marimo==0.17.7`. No new runtime packages: the published site runs under Pyodide.
- Published site: `docs/` is the GitHub Pages output of `marimo export html-wasm VSelect_v0.py -o docs --mode run`. Never hand-edit `docs/`, and never put plans or notes in it.
- No AI, no planted errors, no dataset, no backend. A refresh still erases work.
- No feedback of any kind before Evaluate. Nothing in Predict, Observe or Explain may reveal correctness: no "Right Choice" text and no colour keyed to correctness.
- Evaluate shows cards **only for wrong choices**. The label is **"Correct choice"**, never "Key". The prediction never appears in Evaluate.
- Flip-card backs name **no** dictionary variables.
- Coding standards (CONCRETE AGENTS.md §3): no function nested inside another function, one responsibility per function, intuitive names. Cell-level functions are fine.
- Real law only. Every cited instrument is fact-checked against a primary source and listed under **Sources** at the end of this plan before release.
- Work on branch `poee-restructure`. **Push, PR and Pages re-export need the maintainer's go-ahead.**
- Maintainer checkpoints (Tasks 6 and 8) are hard stops. Do not write consequences before the revised key is approved.

## Review Focus

1. **Whitespace-only Predict rows:** Lock must refuse. Test `test_prediction_ready_ignores_blank_rows` in Task 1.
2. **Learner switches a decision after writing a reason:** the reason is kept, and Evaluate grades the latest choice. Test `test_wrong_choices_uses_latest_decision` in Task 1.
3. **HTML in learner text** (`<script>`, `&`) reaching the download or on-screen cards must be escaped. Test `test_report_html_escapes_learner_text` in Task 5.
4. **Clicking Review Wave or a decision button after Submit** must change nothing, and Observe must render read-only. Browser check in Task 9.
5. **A card flipped open then closed again** still counts as opened for the Predict gate. Test `test_cards_ready_counts_ever_opened` in Task 3.

---

## File Structure

| Path | Responsibility |
|---|---|
| `VSelect_v0.py` | The notebook. The setup block holds `CHOICES`, `TASKS`, `VARIABLES` and copy. `@app.function`s hold the rules. Cells hold UI. |
| `test_vselect.py` | Plain-assert test script (ConCReTE convention: `__main__` runs every `test_*` and prints `ok <name>`). Imports `VSelect_v0`. |
| `plans/plan_01_poee_restructure.md` | This plan, including the Sources section filled in by Task 7. |

Run tests with `uv run --with marimo==0.17.7 python test_vselect.py`. Smoke-run the whole notebook headless with `uv run --with marimo==0.17.7 python VSelect_v0.py`; expected exit code 0 with no traceback.

---

### Task 1: Answer key and rules move into setup

**Files:**
- Modify: `VSelect_v0.py` (replace the `variable_details` cell at 937–1466 and the `variables_by_task` cell at 1467–1527 with the setup block and functions below)
- Create: `test_vselect.py`
- Commit: `plans/plan_01_poee_restructure.md`

**Interfaces:**
- Produces, in `with app.setup:`:
  - `CHOICES = ("include", "exclude", "flag")`.
  - `TASKS: dict[int, dict]`, with keys `header` (existing headers: "Regulatory Gate", "Protected-Attribute Gate", "Data-Reliability Gate", "Equity & Actionability Gate"), `labels` (existing `button_labels_by_task[t]`) and `banner` (filled in Task 2, `""` for now).
  - `VARIABLES: dict[str, dict]`, in existing task order, with keys `task: int`, `title: str`, `definition: str`, `correct: list[str]` (derived from current `final` entries equal to `"Right Choice"`), `why: dict[choice, str]` (current `final` text for each wrong choice) and `consequence: dict[choice, str]` (`{}` for now).
- Produces, as `@app.function`:
  - `variables_in(task: int) -> list[str]`
  - `is_correct(name: str, choice: str) -> bool`
  - `severity(name: str, choice: str) -> str`, which returns `"harm"` when `choice == "include"` and include is not correct, and `"cautious"` otherwise.
  - `prediction_ready(could_predict: list[dict], barred: list[dict]) -> bool`. Rows are `{"variable": str, "reason": str}`. It is true when each list has at least one row whose `variable` is non-blank after `strip()`.
  - `all_decided(decisions: dict[str, str | None]) -> bool`
  - `missing_reasons(decisions: dict, reasons: dict[str, str]) -> list[str]`, the names that have a decision and a blank reason.
  - `can_submit(decisions: dict, reflections: list[str]) -> bool`, true when `all_decided` holds and every reflection is non-blank.
  - `wrong_choices(decisions: dict) -> list[dict]`. Items have keys `name, task, title, chose, correct, why, consequence, severity`, ordered by task and then by `VARIABLES` order. Undecided variables are skipped.
  - `summary_counts(decisions: dict) -> dict`, returning `{"correct": int, "harm": int, "cautious": int}`.

- [ ] **Step 1: Create the branch.** `git checkout -b poee-restructure`. Expected: `Switched to a new branch`.
- [ ] **Step 2: Write the failing tests** in `test_vselect.py`:

```python
import VSelect_v0 as nb

def test_key_shape():
    assert len(nb.VARIABLES) == 26
    assert [len(nb.variables_in(t)) for t in (1, 2, 3, 4)] == [6, 4, 5, 11]
    for name, v in nb.VARIABLES.items():
        assert v["correct"] and set(v["correct"]) <= set(nb.CHOICES), name
        for c in set(nb.CHOICES) - set(v["correct"]):
            assert v["why"][c].strip(), (name, c)
        assert "Right Choice" not in " ".join(v["why"].values()), name

def test_severity():
    assert nb.severity("pell", "include") == "harm"
    assert nb.severity("race", "exclude") == "cautious"

def test_prediction_ready_ignores_blank_rows():
    row = lambda v: {"variable": v, "reason": ""}
    assert not nb.prediction_ready([row("  ")], [row("race")])
    assert not nb.prediction_ready([row("gpa")], [])
    assert nb.prediction_ready([row(""), row("gpa")], [row("race")])

def test_submit_gate():
    all_flag = {n: "flag" for n in nb.VARIABLES}
    assert nb.can_submit(all_flag, ["a", "b", "c"])
    assert not nb.can_submit(all_flag, ["a", " ", "c"])
    assert not nb.can_submit({**all_flag, "pell": None}, ["a", "b", "c"])
    assert nb.missing_reasons({"pell": "flag", "efc": None}, {"pell": " ", "efc": ""}) == ["pell"]

def test_wrong_choices_uses_latest_decision():
    d = {n: nb.VARIABLES[n]["correct"][0] for n in nb.VARIABLES}
    assert nb.wrong_choices(d) == [] and nb.summary_counts(d)["correct"] == 26
    d["pell"] = "include"
    [w] = nb.wrong_choices(d)
    assert (w["name"], w["chose"], w["severity"]) == ("pell", "include", "harm")
    d["pell"] = "exclude"
    assert nb.wrong_choices(d) == []
```

Add the `__main__` runner (`for name, fn in sorted(globals().items()): if name.startswith("test_"): fn(); print("ok", name)`).

- [ ] **Step 3: Run the tests and see them fail.** Expected: `AttributeError: module 'VSelect_v0' has no attribute 'VARIABLES'`.
- [ ] **Step 4: Implement the setup block and functions.** Build `VARIABLES` mechanically from the current `variable_details` (the extraction script used during design reads `feedback.final` and keeps the texts unchanged). Delete every `initial` entry and the `correct` sentinel. Existing cells that read `variable_details`, `variables_by_task` or `button_labels_by_task` will break; leave them broken until Task 2. Only the test script needs to pass in this task.
- [ ] **Step 5: Run the tests and see them pass.** Expected: five `ok` lines.
- [ ] **Step 6: Commit.** `git add VSelect_v0.py test_vselect.py plans/ && git commit -m "refactor: answer key and grading rules into app.setup"`

---

### Task 2: Five-state model and an Observe stage with no feedback

**Files:**
- Modify: `VSelect_v0.py`. Delete the `Variable` class cell (7–62), the four `task_N_variable_instantiation` cells (64–238), `reactive_elements_and_states` (240–616), the four `task_N_getters` cells (617–936), the `functions` cell (1528–1638), every `task_N_initial_feedback` cell and the `final_feedback` cell.

**Interfaces:**
- Consumes: Task 1 `VARIABLES`, `TASKS`, `variables_in`, `missing_reasons`.
- Produces, as cell outputs:
  - `get_decisions, set_decisions = mo.state({n: None for n in VARIABLES})`
  - `get_reasons, set_reasons = mo.state({n: "" for n in VARIABLES})`
  - `get_submitted, set_submitted = mo.state(False)`
  - `controls: dict[str, dict]`, holding `{"include"|"exclude"|"flag": mo.ui.run_button, "reason": mo.ui.text_area}` per variable. It is created in a cell that references **only setters**, so the elements survive reruns (the existing notebook's pattern). Use `functools.partial` for `on_change`; lambdas in a loop bind late.
  - A `task_view(task)` render cell per task, reading `get_decisions()`, `get_reasons()` and `get_submitted()`.

- [ ] **Step 1: Fill `TASKS[t]["banner"]`.** Each banner is markdown with one sentence on what to do in this task, followed by the existing "Note to the learner" text and the existing three-row action/stance table converted to a markdown table. Task 1 has no note: write one sentence about federal and privacy rules on financial-aid data. Render each banner with `mo.callout(..., kind="info")` above its task's variables.
- [ ] **Step 2: Replace the plumbing.** A `Stage 2 · Observe` header sits above Task 1. Each variable renders as: accordion(title → definition + three buttons); the existing "You decided to …" confirmation line; the reason box once a decision exists. After `get_submitted()` is true, render a read-only line (`**Title** — label — reason`) instead of buttons and boxes. Keep the brief table cell (`brief_table_html`) and the Review Wave buttons, rewired to read the dict states.
- [ ] **Step 3: Remove all feedback output.** `grep -n "Right Choice\|initial\|Detailed Feedback" VSelect_v0.py` must return nothing.
- [ ] **Step 4: Smoke-run.** `uv run --with marimo==0.17.7 python VSelect_v0.py` exits 0. `python test_vselect.py` is still green.
- [ ] **Step 5: Commit.** `git commit -am "refactor: dict state model; Observe gives no feedback"`

---

### Task 3: Opening flip cards and the Predict lock

**Files:**
- Modify: `VSelect_v0.py`. Replace the `introduction` cell. Add `flip_cards`, `predict` and `briefing` cells. Gate the four task cells.
- Test: `test_vselect.py`

**Interfaces:**
- Produces:
  - Setup constant `CARDS: dict[str, dict]`, with keys `story`, `role` and `deliver`. Each holds `title`, `icon` (📖 🧑‍💻 📋), `back` (exact back text from `poee-flow-v2.html`) and `full` (the original intro paragraph).
  - `@app.function card_html(card_id: str, flipped: bool) -> str`, which renders the front or back. On re-render it animates with a CSS `rotateY` keyframe; colours follow the mockup gradients.
  - `@app.function cards_ready(opened: frozenset) -> bool`
  - States `get_flipped/set_flipped = mo.state(frozenset())`, `get_opened/set_opened = mo.state(frozenset())` and `get_prediction/set_prediction = mo.state(None)`. When the prediction is locked it holds `{"could_predict": [rows], "barred": [rows]}`, keeping non-blank rows only.

- [ ] **Step 1: Write the failing test.**

```python
def test_cards_ready_counts_ever_opened():
    assert not nb.cards_ready(frozenset({"story", "role"}))
    assert nb.cards_ready(frozenset({"story", "role", "deliver"}))

def test_card_backs_name_no_variables():
    titles = [v["title"].lower() for v in nb.VARIABLES.values()]
    for c in nb.CARDS.values():
        assert not any(t in c["back"].lower() for t in titles), c["title"]
```

- [ ] **Step 2: Run the tests and see them fail.** Expected: `AttributeError: ... 'cards_ready'`.
- [ ] **Step 3: Implement the cards.** Each card is `mo.Html(card_html(...))` above a `mo.ui.button(label="Flip")`. A click toggles the card in `flipped` and adds it to `opened`. The `opened` set never shrinks.
- [ ] **Step 4: Implement Predict.** Use the heading `Stage 1 · Predict` and the spec §4.1 prompt text. Below it, two `mo.ui.array`s of 5 `mo.ui.dictionary({"variable": text, "reason": text})` rows, headed "Variables that could predict a student stopping out" and "Variables the university probably holds but should not use (and why)". Add a **🔒 Lock my prediction** `run_button`. On click, store the prediction if `prediction_ready`; otherwise show `mo.callout("Add at least one variable to each list.", kind="warn")`. Once locked, render the prediction read-only.
- [ ] **Step 5: Add gates.** The Predict cell calls `mo.stop(not cards_ready(get_opened()), mo.md("*Open all three cards to begin.*"))`. Every Observe cell and the `briefing` accordion ("Read the full briefing", containing the three `full` paragraphs) calls `mo.stop(get_prediction() is None, ...)`.
- [ ] **Step 6: Run the tests and see them pass, then smoke-run.**
- [ ] **Step 7: Commit.** `git commit -am "feat: flip-card opening and locked prediction"`

---

### Task 4: Explain and Submit

**Files:**
- Modify: `VSelect_v0.py`. The `brief_inputs`, `product` and `learner_reflection` cells become an Explain stage.

**Interfaces:**
- Consumes: `get_prediction`, `get_decisions`, `get_reasons`, `set_submitted`, `can_submit`, `missing_reasons`, `all_decided`.
- Produces: `REFLECTION_PROMPTS` (setup constant, exact text below), plus `reflections`, `student_name` and `advisor_notes` UI elements.

- [ ] **Step 1: Set `REFLECTION_PROMPTS` to exactly:**
  1. "Which variables from your prediction made it into your model, and which did you end up excluding or flagging? What changed your mind?"
  2. "Which variables you said \"can't be used\" turned out to be in the data dictionary, and how did you handle them? Did the dictionary contain restricted variables you hadn't anticipated?"
  3. "Your model uses the variables you included. Is that enough for advisors to act on? What trade-off did you make between usefulness and protecting students?"
- [ ] **Step 2: Build the stage.** `Stage 3 · Explain` stops on `not all_decided(get_decisions())` with "*Decide every variable to continue.*". Show the locked prediction read-only on top, then name, the three reflections and advisor notes. If `missing_reasons` is non-empty, warn with the count but don't block. Add a **Submit for evaluation** `run_button`: on click, call `set_submitted(True)` only if `can_submit(...)`; otherwise show a warn callout. After submit, render name, notes and reflections read-only.
- [ ] **Step 3: Smoke-run, run the tests, and commit.** `git commit -am "feat: Explain stage with reflection against the prediction and submit lock"`

---

### Task 5: Evaluate and download

**Files:**
- Modify: `VSelect_v0.py`. The `download_brief` cell, plus a new `evaluate` cell.
- Test: `test_vselect.py`

**Interfaces:**
- Produces:
  - `@app.function evaluation_html(decisions: dict) -> str`. It renders the summary bar and the wrong-choice cards, and is used both on screen (`mo.Html`) and in the download.
  - `@app.function report_html(name, prediction, decisions, reasons, notes, reflections) -> str`, the full downloadable document.

- [ ] **Step 1: Write the failing tests.**

```python
def test_evaluation_html_only_wrong_cards():
    d = {n: nb.VARIABLES[n]["correct"][0] for n in nb.VARIABLES}
    d["pell"] = "include"
    out = nb.evaluation_html(d)
    assert "25 of 26 choices hold up. 1 to review." in out
    assert out.count('class="ev') == 1 and "Correct choice" in out and "Key" not in out

def test_report_html_escapes_learner_text():
    d = {n: "flag" for n in nb.VARIABLES}
    r = {n: "<script>x</script> & y" for n in nb.VARIABLES}
    pred = {"could_predict": [{"variable": "<b>", "reason": ""}], "barred": []}
    out = nb.report_html("A&B", pred, d, r, "", ["", "", ""])
    assert "<script>" not in out and "&lt;script&gt;" in out
```

- [ ] **Step 2: Run the tests and see them fail.**
- [ ] **Step 3: Implement `evaluation_html`.**
  - Summary: `"{correct} of 26 choices hold up. {wrong} to review."`, a proportional bar (green, red, amber), the legend "🟥 Would cause harm or break a rule" / "🟧 Too cautious, or effort in the wrong place", and the correct titles as chips.
  - Cards are grouped under task headers. Each card shows the title; **You chose** (that task's button label); **Correct choice** (label of `correct[0]`, plus `(Label also accepted)` for each other correct choice); **Why.** with `why[chose]`; and **What happens in the real world.** with `consequence.get(chose, "")`, omitted when empty.
  - Styling follows `evaluate-card-v2.html`. Escape every string with `html.escape`.
- [ ] **Step 4: Implement `report_html`** from the existing `_doc` template, adding sections for Prediction, Decisions and justifications, Notes, Reflection and Evaluation (`evaluation_html`). Make the `evaluate` cell show `Stage 4 · Evaluate`, stop on `not get_submitted()`, render `mo.Html(evaluation_html(...))` and then the download button.
- [ ] **Step 5: Run the tests and see them pass, then smoke-run and commit.** `git commit -am "feat: Evaluate stage with wrong-choice cards and full-trail download"`

---

### Task 6: Revised answer key — MAINTAINER CHECKPOINT

**Files:**
- Modify: `VSelect_v0.py` (`VARIABLES[*]["correct"]` and `["why"]`)
- Test: `test_vselect.py`

- [ ] **Step 1: Draft the proposal.** Write a table in this plan under `## Key revision` with columns variable | current correct | proposed correct | one-line reason. Some variables must accept `include`. The design flagged first-gen, credits, housing, transfer and midterms as candidates. Pronouns Exclude and Midterm Exclude must also be resolved.
- [ ] **Step 2: STOP.** Send the table to the maintainer and wait for approval. Apply only the approved version.
- [ ] **Step 3: Add the failing test.** The flag ceiling of 18 is my call; the maintainer may change it at the checkpoint.

```python
def test_key_has_no_safe_default():
    assert any("include" in v["correct"] for v in nb.VARIABLES.values())
    for c in nb.CHOICES:
        assert sum(c in v["correct"] for v in nb.VARIABLES.values()) <= 18, c
```

- [ ] **Step 4: Apply the approved key.** Rewrite every `why` text that praises the choice it now sits under, so that each text explains why that choice is wrong. Run the tests and see them pass.
- [ ] **Step 5: Commit.** `git commit -am "content: revised answer key (maintainer-approved)"`

---

### Task 7: Fact-check the regulatory basis

**Files:**
- Modify: `VSelect_v0.py` (`definition` and `why` texts that state law), and the `## Sources` section of this plan.

- [ ] **Step 1: Find every legal claim.** `grep -n -i "federal\|regulat\|FERPA\|Title\|Department of Education\|ED \|law\|rule" VSelect_v0.py` lists every claim.
- [ ] **Step 2: Verify each claim against a primary source.** Candidates: FERPA (34 CFR Part 99); the FAFSA Simplification Act (SAI replacing EFC from award year 2024–25); the FUTURE Act and IRC §6103(l)(13) limits on FAFSA and FTI data use; HEA §483(a)(3)(E); Title VI; Title IX; ED Office for Civil Rights guidance. Record each claim with its instrument, section, URL and verdict (accurate / corrected / removed) in `## Sources`.
- [ ] **Step 3: Correct the texts.** Any text resting on a non-existent rule (for example "2024 Department of Education rules" barring EFC) is rewritten to the real basis. Run the tests and smoke-run.
- [ ] **Step 4: Commit.** `git commit -am "content: regulatory claims fact-checked against primary sources"`

---

### Task 8: Real-world consequences — MAINTAINER CHECKPOINT

**Files:**
- Modify: `VSelect_v0.py` (`VARIABLES[*]["consequence"]`)
- Test: `test_vselect.py`

- [ ] **Step 1: Write the failing test.**

```python
def test_every_wrong_choice_has_consequence():
    for name, v in nb.VARIABLES.items():
        for c in set(nb.CHOICES) - set(v["correct"]):
            assert v["consequence"].get(c, "").strip(), (name, c)
```

- [ ] **Step 2: Draft the consequences.** One or two sentences for each wrong (variable, choice) under the approved key. Cover both the university side (compliance, legal exposure, project stalled) and the student side (who gets flagged, who gets missed). Cite only instruments listed in `## Sources`.
- [ ] **Step 3: STOP.** Send the full list to the maintainer for review. Apply edits. Run the tests and see them pass.
- [ ] **Step 4: Commit.** `git commit -am "content: real-world consequences for every wrong choice"`

---

### Task 9: Browser walkthrough and WASM export

- [ ] **Step 1: Run the notebook.** `uv run --with marimo==0.17.7 marimo run VSelect_v0.py --port 2718 --headless`. Walk it in the browser pane:
  - Predict is hidden until all three cards have been opened. Closing a card again doesn't re-hide it.
  - Lock refuses blank rows.
  - No correctness signal appears anywhere before Submit.
  - Explain appears after all 26 decisions.
  - After Submit, Observe and Explain are read-only, and Review Wave changes nothing.
  - Evaluate shows only wrong cards.
  - The download opens, and HTML typed into a reason shows as text.

  Screenshot each stage.
- [ ] **Step 2: Export.** `uv run --with marimo==0.17.7 marimo export html-wasm VSelect_v0.py -o docs --mode run`. Serve with `python -m http.server -d docs 8000` and repeat the Predict → Evaluate path once in the WASM build.
- [ ] **Step 3: Commit.** `git add docs && git commit -m "build: re-export Pages site"`
- [ ] **Step 4: STOP.** Ask the maintainer before `git push` or opening a PR to `HAILatPitt/concrete-student-success`.

---

## Key revision

*Draft by Claude, 2026-10-20. Waiting for maintainer approval (Task 6, Step 2).*

**Principle.** **Include** is correct when a variable is reliable, actionable, lawful and not a protected attribute. **Flag** is correct only where a real open question remains. **Exclude** is correct where use is barred or worthless. A variable accepts a second answer only when that answer is also defensible.

| Variable | Current correct | Proposed correct | Reason |
|---|---|---|---|
| First Generation Status | flag | **include** | Not protected; the intervention (navigational support) is known. The current Include text already says "Good call". |
| Credits After Add/Drop | flag | **include** | Registrar data: reliable and actionable. The current Include text says "solid choice". |
| Live On Campus or Commuter | flag | **include** | Reliable and actionable (commuter-friendly support). The current Include text says "Useful and actionable". |
| Transfer Status | flag | **include** | Known higher-risk group with a concrete intervention (credit articulation). The current Include text says "actionable". |
| Expected Family Contribution (EFC) | exclude, flag | **exclude** | FAFSA-derived and retired; a review adds nothing (the original initial feedback said so). Law to be confirmed in Task 7. |
| Student Aid Index (SAI) | exclude, flag | **exclude** | FAFSA-derived, with incomplete history. Law to be confirmed in Task 7. |
| Unmet Need | exclude, flag | **exclude** | Built from FAFSA-derived inputs. Law to be confirmed in Task 7. |
| Preferred Pronouns | flag | **exclude** | Not predictive, high missingness, weak audit value. The current Exclude text already says "usually appropriate". |
| Campus Wi-Fi Gaming | exclude, flag | **exclude** | Network-surveillance data with no theory linking it to persistence. Nothing for a review to rescue. |
| Midterm Grades | flag | flag (unchanged) | Rewrite the Include "why" text, which currently says "flag … or exclude" though Exclude is graded wrong. |
| Early Progress Reports | flag | flag (unchanged) | Rewrite the Include "why" text, which currently says "or consider exclusion". |
| All other 15 | — | unchanged | — |

**Effect.** Flagging everything drops from 25/26 to 16/26. Excluding everything scores 11/26, and including everything scores 4/26. A defensible model now has four inputs. New "why" texts are needed for the newly wrong choices: Flag on the four Include variables, Flag on EFC, SAI, Unmet Need and Wi-Fi, and Flag on Pronouns.

## Sources

*Task 7, checked 2026-10-20 against primary sources. The eCFR returned a bot check, so 34 CFR was read on law.cornell.edu; re-check against the eCFR before release. No 2026 revision of GEN-25-08 was found, but confirm in the ED library before release.*

| Claim in the scenario | Verdict | Now says | Source |
|---|---|---|---|
| "Recent federal guidance limits individual financial-aid records in automated decision systems" (story, Task 1 banner, Pell definition) | Partly accurate | Federal law limits **FAFSA data**, and the FTI inside it, to awarding and administering aid and to de-identified research. The school's own aid records fall under FERPA. No rule mentions automated decisions. | [20 U.S.C. 1090(a)(3)](https://www.law.cornell.edu/uscode/text/20/1090); [26 U.S.C. 6103(l)(13)](https://www.law.cornell.edu/uscode/text/26/6103); [GEN-25-08](https://fsapartners.ed.gov/knowledge-center/library/dear-colleague-letters/2025-09-30/guidance-use-federal-tax-information-fti-free-application-federal-student-aid-fafsar-data-and-non-fafsa-data) |
| "EFC is explicitly barred under 2024 Department of Education rules" | Inaccurate | EFC is FAFSA data, replaced by SAI from 2024–25. Restricted as FAFSA data; no rule bars it by name. | [20 U.S.C. 1087mm](https://www.law.cornell.edu/uscode/text/20/1087mm); [GEN-23-11](https://fsapartners.ed.gov/knowledge-center/library/dear-colleague-letters/2023-08-04/fafsa-simplification-act-changes-implementation-2024-25) |
| "Including Pell Status violates federal guidance and may expose the institution to penalties" | Partly accurate | The ISIR Pell eligibility flag is FAFSA data; disbursed Pell is school data under FERPA. Penalties attach mainly to FTI misuse. | GEN-25-08, "Types of Information" and "FERPA and the Use of Non-FAFSA or Institutional Data" |
| Unmet Need "regulatory restrictions likely prohibit its use" | Inaccurate | ED lists unmet need as school data (FERPA). It is built on SAI and may allow SAI to be reverse-calculated. | GEN-25-08 |
| Pell Plus "likely subject to the same regulatory restrictions" | Inaccurate as stated | An institutional award is school data under FERPA, but it reveals Pell receipt. | GEN-25-08 |
| FERPA permits internal use by school officials | Accurate (not previously stated) | Allowed for school officials with a legitimate educational interest, under the criteria in the school's annual notice. | [34 CFR 99.31(a)(1)](https://www.law.cornell.edu/cfr/text/34/99.31); [34 CFR 99.7(a)(3)(iii)](https://www.law.cornell.edu/cfr/text/34/99.7) |

**Open interpretation.** Neither the statute nor ED defines whether retention outreach counts as "administering aid". The scenario takes the conservative reading: a model that flags named students is not aid administration.

**Raised for the Task 8 checkpoint.** The approved key marks Unmet Need as Exclude-only on the premise that it is FAFSA-restricted. ED instead treats it as school data. Exclude still rests on equity grounds (it flags students for being poor) and on the risk of revealing SAI, but Flag for legal review is now also defensible. The maintainer decides whether to accept Flag again.
