"""Plain-assert tests for the notebook's setup block and @app.function rules.

Run: uv run --with marimo==0.17.7 python test_vselect.py
"""
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


def blank_row(variable):
    return {"variable": variable, "reason": ""}


def test_prediction_ready_ignores_blank_rows():
    assert not nb.prediction_ready([blank_row("  ")], [blank_row("race")])
    assert not nb.prediction_ready([blank_row("gpa")], [])
    assert nb.prediction_ready([blank_row(""), blank_row("gpa")], [blank_row("race")])


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


def test_record_decision_passes_a_plain_function_updater():
    # marimo's state setter treats only plain functions as updaters; a
    # functools.partial would be stored as the new state value.
    import types
    seen = []
    nb.record_decision(seen.append, "pell", "flag")
    nb.record_reason(seen.append, "pell", "because")
    assert all(isinstance(u, types.FunctionType) for u in seen)
    assert seen[0]({"pell": None}) == {"pell": "flag"}
    assert seen[1]({"pell": ""}) == {"pell": "because"}


def test_cards_ready_counts_ever_opened():
    assert not nb.cards_ready(frozenset({"story", "role"}))
    assert nb.cards_ready(frozenset({"story", "role", "deliver"}))


def test_card_backs_name_no_variables():
    import re
    titles = [v["title"].lower() for v in nb.VARIABLES.values()]
    for c in nb.CARDS.values():
        named = [t for t in titles if re.search(rf"\b{re.escape(t)}\b", c["back"].lower())]
        assert not named, (c["title"], named)


def test_card_html_shows_one_face():
    front, back = nb.card_html("role", False), nb.card_html("role", True)
    assert "Your role" in front and nb.CARDS["role"]["back"] not in front
    assert nb.CARDS["role"]["back"] in back


def test_record_flip_toggles_face_and_remembers_opened():
    import types
    flips, opens = [], []
    nb.record_flip(flips.append, opens.append, "story")
    assert isinstance(flips[0], types.FunctionType) and isinstance(opens[0], types.FunctionType)
    assert flips[0](frozenset()) == {"story"} and flips[0](frozenset({"story"})) == frozenset()
    assert opens[0](frozenset({"story"})) == {"story"}


def test_reflection_prompts_reconcile_with_prediction():
    assert len(nb.REFLECTION_PROMPTS) == 3
    assert "prediction" in nb.REFLECTION_PROMPTS[0]
    assert not any("feedback" in p for p in nb.REFLECTION_PROMPTS)


def test_evaluation_html_only_wrong_cards():
    d = {n: nb.VARIABLES[n]["correct"][0] for n in nb.VARIABLES}
    d["pell"] = "include"
    out = nb.evaluation_html(d)
    assert "25 of 26 choices hold up. 1 to review." in out
    assert out.count('class="ev') == 1 and "Correct choice" in out and "Key" not in out


def test_evaluation_html_names_also_accepted_choice():
    d = {n: nb.VARIABLES[n]["correct"][0] for n in nb.VARIABLES}
    d["pell"] = "include"
    assert "(Flag for Review also accepted)" in nb.evaluation_html(d)


def test_report_html_escapes_learner_text():
    d = {n: "flag" for n in nb.VARIABLES}
    r = {n: "<script>x</script> & y" for n in nb.VARIABLES}
    pred = {"could_predict": [{"variable": "<b>", "reason": ""}], "barred": []}
    out = nb.report_html("A&B", pred, d, r, "", ["", "", ""])
    assert "<script>" not in out and "&lt;script&gt;" in out


def test_key_has_no_safe_default():
    assert any("include" in v["correct"] for v in nb.VARIABLES.values())
    for c in nb.CHOICES:
        assert sum(c in v["correct"] for v in nb.VARIABLES.values()) <= 18, c


def test_approved_key_revision():
    approved = {
        "firstgen": ["include"], "credits": ["include"], "housing": ["include"], "transfer": ["include"],
        "efc": ["exclude"], "sai": ["exclude"], "unmet": ["exclude", "flag"], "pronouns": ["exclude"], "wi_fi": ["exclude"],
    }
    for name, correct in approved.items():
        assert nb.VARIABLES[name]["correct"] == correct, name


def test_why_texts_do_not_praise_wrong_choices():
    praise = ("good call", "solid choice", "useful and actionable", "usually appropriate", "flag for quality improvement or exclude", "consider exclusion")
    for name, v in nb.VARIABLES.items():
        for choice, text in v["why"].items():
            assert not any(p in text.lower() for p in praise), (name, choice)


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
