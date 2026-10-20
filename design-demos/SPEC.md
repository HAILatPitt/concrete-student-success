# Design spec: Student Success opening + Predict (three-direction gate)

## What this is
ConCReTE's Student Success scenario is a marimo notebook that university students work through in a browser (also published as a static WASM site on GitHub Pages). The learner plays the data scientist on a university "Student Success Analytics" team. Their job is to decide which student variables may feed an early-warning model that flags students at risk of dropping out. The notebook runs four gated stages: Predict → Observe → Explain → Evaluate. This spec covers only the **first screen**: the opening (three flip cards), the **Stage 1 · Predict** section, and the **stage header** pattern that all four stages reuse.

## Audience and setting
- Data-science and social-science students, undergraduate and graduate.
- They open it on a laptop at about 1m distance, alone or in class, for a 45–60 minute exercise.
- Many are not coders. The subject is serious (student welfare, privacy law, fairness), but the opening should invite people in. It reads like a case-study briefing, not a SaaS dashboard.

## Emotional tone
Calm, credible, a little curious. Think "a well-made case file handed to you on day one". Not playful-gamified, not corporate, not "AI product".

## Content (use exactly; no lorem, no invented stats)
Page title: **Variable selection scenario**

Three cards. Each card has a front and a back.
1. Front title **The story so far**. Back text: "Retention from first to second year has been sliding for five years. The Provost wants advisors to reach struggling students before they leave. A new Student Success Analytics team has to build an early-warning tool, inside FERPA and the federal limits on using FAFSA data."
2. Front title **Your role**. Back text: "You are the team's data scientist. You won't build the model yet. You decide what goes into it. You have a data dictionary and red-flag notes from legal and ethics reviewers, and no raw records."
3. Front title **What you deliver**. Back text: "A one-page Variable Selection Brief. Every variable is marked include, exclude, or flag, with a short reason tied to privacy, fairness, and usefulness. Advisors and compliance sign it before any modelling starts."

Fronts carry a small affordance line: "click to open". In the mockup, show card 1 **flipped** (back face) and cards 2–3 as fronts. Below the cards, a muted line: "Open all three cards to begin."

Predict section:
- Stage header: "Stage 1 · Predict".
- Prompt: "Before you see the university's data dictionary, write down from your own knowledge: (1) variables that could predict a student stopping out, each with a one-line reason; (2) variables the university probably holds but should not use, each with the rule or concern that stops it. Once you lock your prediction it cannot be changed. You will come back to it at the end."
- Two labelled writable boxes, one per list: "Variables that could predict a student stopping out" and "Variables the university probably holds but should not use (and why)".
- A button: "Lock my prediction".

## Hard technical constraints (marimo; the design must be buildable)
- **Page.** marimo light theme: white page, one centred content column about **740px** wide. Mock it as a 1440×900 page with that column. You may style only inside your own blocks. The page background stays white (no global body styles).
- **Cards.** The three cards sit in one row, **identical size**, about 224×272px each, with equal gaps. Each whole card is clickable (it is rendered as the label of a marimo button). Card HTML must use **inline styles plus one `<style>` block**, with no JavaScript. The flip is a CSS keyframe that plays when the face re-renders (e.g. rotateY 90°→0°, ~400ms), so show the keyframe in CSS. Both faces must fit the same box. Back text is 13–14px and must fit without scrolling.
- **Textareas and the button are marimo-native and can't be restyled.** Render them as a plain `<textarea>` (1px #d4d4d8 border, 6px radius, system sans 14px, ~5 rows) and a small green "success" button (#16a34a background, white 13px text, 6px radius). Design only what surrounds them: labels, framing, spacing, header.
- Fonts: marimo's defaults are PT Sans (body) and Lora (headings). You may load Google Fonts via `<link>`. Avoid Fraunces, Inter as display, Space Grotesk and Playfair Display.
- Readability floor: body ≥14px, labels ≥12px, contrast ≥4.5:1.

## Brand and colour inputs
ConCReTE is a HAIL @ University of Pittsburgh project. Its decks use Pitt gold **#FFB81C** and navy **#003594** / **#003163**. Derive the palette (sample → converge to 2–3 chromatic colours plus one neutral series in oklch → justify in one sentence). No purple gradients, no emoji icons, no rounded card with a coloured left-border accent, no SVG illustrations of people.

## Visual motif
Find one motif that grows from this content and no other (a case file? index cards in a records drawer? a data-dictionary entry? a sealed envelope?). Say in one sentence where the form comes from.

## Deliverable per direction
One self-contained HTML file at `design-demos/<file>.html`, viewport 1440×900, containing in order: the page title, the three cards (card 1 flipped), the "Open all three cards" line, and the Predict section. At the top of the file put an HTML comment with: the logic used and its anchor (style, reference or designer), the palette with the one-sentence justification, the fonts, and "form comes from: …". Real content only.
