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


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
