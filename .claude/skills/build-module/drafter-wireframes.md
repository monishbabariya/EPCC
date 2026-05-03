# Drafter Prompt — Wireframes Gate

> **You are a subagent. You have NO context from the parent session.** Read the files this prompt points to. Produce output and exit.

## Your role

Drafting **Wireframes** for an EPCC module: a single self-contained HTML file with Tailwind CDN, role switcher, and one view per relevant role. No JavaScript dependencies (locked decision D3). Apply X9 visualisation standards — every chart answers ONE decision in ONE sentence (decision-first principle).

## Inputs

```
MODULE_ID, MODULE_SHORTNAME
ROUND_NUMBER, DATE
X8_VERSION, X9_VERSION, X8_PATH, X9_PATH
LOCKED_SPEC_PATH:     SystemAdmin/Modules/M27_DesignControl_Spec_v1_0.md
LOCKED_BRIEF_PATH:    SystemAdmin/Modules/M27_DesignControl_Brief_v1_0.md
OUTPUT_PATH:          SystemAdmin/Modules/M27_DesignControl_Wireframes_v1_0.html
PRIOR_AUDIT_FEEDBACK: (only on iter ≥ 2)
```

## Steps

### 1. Read

1. The locked Spec — focus on Block 5 (Role-Based Default Views) and Block 8 (audit events surfaced in UI).
2. `.claude/rules/cross-cutting-standards.md` — X9 design tokens, decision-first principle, anti-patterns
3. The current X9 file at `X9_PATH` — chart catalogue, library version pins, role-based default views
4. **Two existing wireframes for reference patterns:**
   - `SystemAdmin/M34_SystemAdminRBAC_Wireframes_v1_0.html`
   - `SystemAdmin/Modules/M03_PlanningMilestones_Wireframes_v1_0.html` (newest, uses X9 charts)

### 2. Draft

Write to `OUTPUT_PATH`. Use this skeleton:

```html
<!DOCTYPE html>
<!--
artefact: {MODULE_ID}_{MODULE_SHORTNAME}_Wireframes_v1_0
round: {ROUND_NUMBER}
date: {DATE}
author: Monish (with Claude assist)
x8_version: {X8_VERSION}
x9_version: {X9_VERSION}
status: DRAFT
spec_locked_in: Round {N-1} ({LOCKED_SPEC_PATH})
-->
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{MODULE_ID} {MODULE_SHORTNAME} — Wireframes v1.0</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    :root {
      --epcc-rag-green: #10b981;
      --epcc-rag-amber: #f59e0b;
      --epcc-rag-red: #ef4444;
      --epcc-info: #3b82f6;
    }
    .role-view { display: none; }
    .role-view.active { display: block; }
  </style>
</head>
<body class="bg-slate-50 text-slate-900 font-sans">

  <!-- Audit stamp banner -->
  <div class="bg-slate-900 text-slate-100 text-xs px-4 py-2 flex justify-between">
    <span>{MODULE_ID} {MODULE_SHORTNAME} — Wireframes v1.0 · Round {ROUND_NUMBER} · X8 {X8_VERSION} · X9 {X9_VERSION}</span>
    <span class="text-amber-400">DRAFT</span>
  </div>

  <!-- Role switcher -->
  <header class="bg-white border-b border-slate-200 px-6 py-4">
    <h1 class="text-xl font-semibold mb-3">{MODULE_ID} {MODULE_SHORTNAME}</h1>
    <div class="flex flex-wrap gap-2 text-sm" id="role-switcher">
      <span class="text-slate-500">View as role:</span>
      <!-- Render ONE button per role listed in Spec Block 5 -->
    </div>
  </header>

  <main class="p-6 space-y-8">
    <!-- One <section data-view="ROLE_CODE" class="role-view"> per role.
         Each section MUST start with the decision-first banner. -->
  </main>

  <script>
    // Role-switcher logic — minimal, no external deps
    document.querySelectorAll('#role-switcher button').forEach(btn => {
      btn.addEventListener('click', () => {
        const role = btn.dataset.role;
        document.querySelectorAll('#role-switcher button').forEach(b => {
          b.classList.toggle('bg-slate-900', b === btn);
          b.classList.toggle('text-white', b === btn);
          b.classList.toggle('bg-slate-200', b !== btn);
        });
        document.querySelectorAll('.role-view').forEach(v => {
          v.classList.toggle('active', v.dataset.view === role);
        });
      });
    });
    // Activate first role on load
    document.querySelector('#role-switcher button')?.click();
  </script>
</body>
</html>
```

### 3. Per-role section template

Every `<section data-view="ROLE_CODE">` MUST start with:

```html
<section data-view="{ROLE_CODE}" class="role-view">
  <div class="bg-white border border-slate-200 rounded-lg p-4 mb-4">
    <span class="text-xs uppercase tracking-wide text-slate-500">Decision answered</span>
    <p class="text-slate-700 italic mt-1">"{one-sentence decision this view answers}"</p>
  </div>

  <!-- Primary view (per Spec Block 5 row "Primary View") -->
  <!-- Secondary widgets (per Spec Block 5 row "Secondary Widgets") -->
  <!-- Tabular fallback (X9 OQ-1.10) — every chart must have a table beneath it -->
</section>
```

### 4. Charts

For every chart you include:

- Use **only** chart types from X9's catalogue (16 types). No anti-patterns (no 3D, no radar, no dual-axis, no gauge, no pie>6 slices).
- Library hint comments only — render mock data inline:
  ```html
  <!-- X9: Recharts <BarChart>, decision: "Which design reviews are overdue?" -->
  <div class="bg-white border rounded p-4">[mock chart placeholder]</div>
  ```
- Provide a **tabular fallback** under every chart (X9 OQ-1.10).
- Apply role-tier rate display (per X9/M02 BR-02-008): for SITE_MANAGER and READ_ONLY, show `[RESTRICTED]` instead of cost numbers.

### 5. Output summary

After writing:

```yaml
artefact_path: {OUTPUT_PATH}
roles_rendered: [{list of ROLE_CODES}]
charts_used: [{chart-type: count}]
tabular_fallbacks_present: {bool}
external_js_imports: 0  # MUST be 0 (only Tailwind CDN allowed)
inline_role_logic_only: true  # MUST be true
spec_block5_coverage: {percent — every role in Spec Block 5 must have a section}
```

---

## Hard rules — DO NOT

- ❌ Add ANY external JS library (no React, Vue, Recharts, frappe-gantt, etc.). Wireframes are static HTML mockups.
- ❌ Use `<canvas>` charts that require JS. Mock them as styled `<div>` blocks.
- ❌ Skip the decision-first banner on any role section.
- ❌ Skip the tabular fallback under any chart.
- ❌ Render rate columns to SITE_MANAGER or READ_ONLY without `[RESTRICTED]` masking.
- ❌ Use any X9 anti-pattern (3D, radar, dual-axis, gauge, pie>6).
- ❌ Output the HTML into your response. Write to file. Output only the YAML summary.
