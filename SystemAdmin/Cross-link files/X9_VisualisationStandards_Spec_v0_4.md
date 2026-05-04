# X9 — Visualisation Standards
## Spec v0.4 (LIVING)
**Status:** Locked v0.4
**Type:** Cross-Cutting LIVING Document
**Author:** Monish (with Claude assist)
**Created:** 2026-05-03 (v0.1) | **Updated:** 2026-05-04 (v0.4)
**Last Audited:** v0.4 on 2026-05-04
**Reference Standards:** X8_GlossaryENUMs_v0_6.md, M34_SystemAdminRBAC_Spec_v1_0.md, M01_ProjectRegistry_Spec_v1_0.md (+ v1_1_CascadeNote + v1_2_CascadeNote + v1_3_CascadeNote), M02_StructureWBS_Spec_v1_0.md, M03_PlanningMilestones_Spec_v1_1.md (+ v1_2_CascadeNote), M04_ExecutionCapture_Spec_v1_0.md, M06_FinancialControl_Spec_v1_0.md (v1.0a), M06_FinancialControl_Wireframes_v1_0.html
**Folder:** SystemAdmin/Cross-link files/ (per Round 18 audit canonical placement)

> **X9 governs how data becomes visual artefacts in EPCC** — chart types, libraries, design tokens, composition rules, role-tiered behaviour, role-based default views. Living document — versioned per cross-cutting changes.

---

## CHANGE LOG

| Version | Date | Change Summary |
|---|---|---|
| v0.1 | 2026-05-03 | Initial spec lock. 16 chart types catalogued. Decision-first principle (§3). Composition rules (§7). Module-by-module chart matrix (§8). Pipeline Funnel deep spec (§9). Role-based default views (§13). All Round 13 OQ-1 + OQ-2 decisions embedded. |
| v0.2 | 2026-05-03 | M03 lock cascade. §13.3.3 updated per OQ-1.11=B: PROJECT_DIRECTOR adds PV S-curve as secondary widget; PLANNING_ENGINEER adds PV roll-up shape (no values, just curve) as secondary widget. Audit log: ROLE_DEFAULT_VIEW_CHANGED for both roles. No other sections changed. Catalogue + composition rules + design tokens unchanged. |
| v0.3 | 2026-05-03 | M04 lock cascade (Round 20). §13.3.4 rewritten per M04 Brief OQ-1.8 + Spec Block 5: scope-decomposition cleanup (HSE references removed — moved to M31 per OQ-1.1=B; measurement-entry references removed for QS_MANAGER — moved to M14 per OQ-1.2=C; COMPLIANCE_MANAGER row dropped from M04 since compliance lives in M09); rows added for PROCUREMENT_OFFICER (material receipts log), ANALYST (progress trend curves), READ_ONLY (status-badge card). QS_MANAGER primary becomes "Pending approvals queue" (M04's true QS-facing surface). NCR pipeline funnel confirmed as 8th instance of the §11 flagship pipeline pattern. Audit log: ROLE_DEFAULT_VIEW_CHANGED for all 7 M04 rows. No other sections changed. Catalogue + composition rules + design tokens unchanged. Reference Standards bumped to X8 v0.5 (with M04 ENUMs). |
| **v0.4** | **2026-05-04** | **M06 lock cascade (Round 27). NO new chart types — M06 wireframes consume only existing v0.3 catalogue entries. Two minor refinements: (a) §13.3.6 row expanded from 5 roles to 8 roles (added QS_MANAGER, EXTERNAL_AUDITOR, READ_ONLY) for parity with M06 Spec Block 5 + Wireframes role-switcher; (b) §9.5.1 Capital Funnel annotated as the **1st named flagship instance** of the §11 Pipeline Funnel pattern (formal-naming reconciliation per Round 26 cascade detection — chronologically the M04 NCR Funnel was the 8th implementation, but Capital Funnel is the formally-designated flagship per M06 Brief §7 + Wireframes line 12). Audit log: ROLE_DEFAULT_VIEW_CHANGED for 3 added M06 rows. No other sections changed. Catalogue + composition rules + design tokens unchanged. Reference Standards bumped to X8 v0.6 (with M06 ENUMs).** |

---

## TABLE OF CONTENTS

```
§1   Purpose
§2   Naming + Vocabulary
§3   Decision-First Principle (FOUNDATIONAL)
§4   Chart Type Catalogue (16 Types)
§5   Design Tokens
§6   Role-Tiered Field Display Inheritance
§7   Composition Rules (Combined vs Separate vs Composed)
§8   Module-by-Module Chart Matrix
§9   Pipeline Funnel — Deep Component Specification
§10  Performance Budgets
§11  Accessibility (WCAG AA)
§12  Mobile / PF01 Adaptation
§13  Role-Based Default Views
§14  Component Library Contracts
§15  Library Version Pins
§16  Anti-Patterns (Forbidden)
§17  Extension Protocol
§18  Enforcement
```

---

# §1 — PURPOSE

X9 specifies **how data is rendered as visual artefacts in EPCC**, mirroring how X8 specifies how data is named.

## 1.1 What X9 Covers

- Chart library choices (locked tech stack)
- 16 blessed chart types with use-case justification
- Design tokens (colours, typography, spacing) — single source of truth
- Component contracts (chart anatomy, props interface)
- Role-tiered chart behaviour (inherits M34 + M02 permission models)
- Composition rules (when to combine series; when to separate; when to compose)
- Module-by-module chart matrix (which charts each module uses)
- Role-based default views (what each role sees first per module)
- Performance budgets (latency targets per chart type)
- Accessibility (WCAG AA compliance)
- Mobile responsiveness (PF01 contract)

## 1.2 What X9 Does NOT Cover

- Module-specific business rules (those stay in M-module specs)
- Backend chart data API design (charts are client-rendered; API delivers JSON)
- BI tool integration (Tableau, Power BI etc. are out of v1.0 scope)
- Real-time WebSocket subscriptions (deferred to Phase 2)
- Custom dashboard builders (deferred — Level 1 role defaults only in v1.0)

---

# §2 — NAMING + VOCABULARY

## 2.1 Chart Component Naming

```
Convention:   PascalCase prefixed with "EPCC"
Examples:     <EPCCChart />
              <EPCCPipelineFunnel />
              <EPCCKPITile />
              <EPCCGantt />
```

## 2.2 Chart Type Identifier (for cross-references)

```
Convention:   snake_case
Examples:     line_multi_series
              pipeline_funnel
              gantt_with_overlay
              capital_funnel
              heatmap_5x5
```

## 2.3 Chart Pattern Naming

```
"Pattern"   = abstract (e.g., Pipeline Funnel)
"Type"      = specific implementation (e.g., Capital Funnel = M06's Pipeline Funnel)
"Component" = React export (e.g., <EPCCPipelineFunnel>)
```

---

# §3 — DECISION-FIRST PRINCIPLE (FOUNDATIONAL)

## 3.0 The Rule (LOCKED)

> **Every chart in EPCC must answer ONE specific decision in ONE sentence. Charts that cannot pass this test are CUT.**

## 3.1 The Test

Before any chart is added to a module wireframe, the spec author must complete this template:

```
Chart name:    ____________________
Decision it answers:  Does ____ user need to ____?
User role:     ____________________
Cadence:       ____________________
```

If the decision sentence cannot be written without ambiguity → CUT the chart.

## 3.2 Examples Passing the Test

| Chart | Decision Sentence |
|---|---|
| Capital Funnel | Does the FINANCE_LEAD have headroom to commit more capital this period? |
| EVM 3-Line | Is the project earning value as planned? |
| Risk Heatmap 5×5 | Which risks need the PMO_DIRECTOR's attention first? |
| Master Gantt | Is the project on schedule against baseline? |
| Permit Calendar | Which permits will expire in the next 90 days? |

## 3.3 Examples Failing the Test (CUT)

| Cut Chart | Why |
|---|---|
| "Project overview chart" | Decision unclear; user vague |
| "Activity dashboard" | Multiple decisions; needs decomposition |
| "Trend visualisation" | What trend; for whom; for what action? |

## 3.4 Cut Decoration

Charts that are decorative (look impressive, answer no decision) consume:
- Build effort (engineering)
- Maintenance effort (each module spec change)
- User cognitive load (every chart competes for attention)
- Performance budget (each chart loads data + renders)

**Decorative charts are negative-value features.** X9 forbids them.

---

# §4 — CHART TYPE CATALOGUE (16 Types)

## 4.1 Tier 1 — Universal (Use Liberally)

### 4.1.1 Line (Multi-Series)

```
Library:        Recharts <LineChart>
Use cases:      EVM 3-line (PV/EV/AC), CPI/SPI trend, S-curves, time-series KPIs,
                trend metrics, predictive forecasts
Decision pattern:  "Is X tracking against Y over time?"
Series limit:   Max 4 series before degraded readability
Y-axis rule:    All series must share same unit (or use a single ratio scale)
Library notes:  Use <CartesianGrid>, <XAxis>, <YAxis>, <Tooltip>, <Legend>
```

**Examples:**
- M07 EVM 3-line: PV (amber), EV (cyan), AC (red)
- M03 S-curve: Planned (amber), Actual (cyan)
- M07 CPI/SPI Trend: CPI (cyan), SPI (purple), reference at 1.0

---

### 4.1.2 Bar (Horizontal, Sortable)

```
Library:        Recharts <BarChart layout="vertical">
Use cases:      Variance ranking, top-N analysis, package comparison, vendor
                outstanding, owner workload
Decision pattern:  "Which X has the highest Y?"
Sort default:   Magnitude DESC (worst-first or best-first by context)
Categories:     Up to 20 visible; pagination beyond
Library notes:  Horizontal layout for readability with long category labels
```

**Examples:**
- M03 Variance Bar: WBS × days late
- M06 Vendor Outstanding: Vendor × ₹ outstanding
- M08 Gate Duration: Gate × avg days

---

### 4.1.3 Stacked Bar (Time)

```
Library:        Recharts <BarChart> + <Bar stackId="a">
Use cases:      Cashflow time-series (Budgeted/Committed/Accrued/Paid), RAG
                distribution over time, VO cumulative by category, gate
                pass-rates
Decision pattern:  "How has X composition changed over time?"
Stack count:    Max 5 stacks per bar
Time axis:      Always X; quantities Y
```

**Examples:**
- M06 Cashflow Time-Series: month × {Budgeted, Committed, Accrued, Paid}
- M01 RAG Distribution Trend: month × {Green, Amber, Red} project counts
- M05 VO Cumulative: month × cumulative ₹ by cause category

---

### 4.1.4 Pipeline Funnel ⭐ (FLAGSHIP PATTERN)

```
Library:        Custom React (X9 ships <EPCCPipelineFunnel>)
Use cases:      State-pipeline tracking ANYWHERE in EPCC (8+ modules)
Decision pattern:  "Where does our [items] flow get stuck and how much
                    headroom remains at each state?"
Layer count:    Exactly 4 nested layers (industry-standard)
Critical rule:  Each inner layer MUST be a SUBSET of its outer layer
                (e.g., Committed ≤ Budgeted; Accrued ≤ Committed; Paid ≤ Accrued)
Visual:         Nested horizontal bars; outer layer = container outline;
                inner layers = filled bars; gap = headroom (hatched)
```

**Specific implementations (deep spec in §9):**
- M06 Capital Funnel: Budgeted → Committed → Accrued → Paid
- M04 NCR Funnel: Open → In_Review → Approved → Closed
- M05 Risk Funnel: Identified → Assessed → Mitigated → Closed
- M05 VO Funnel: Submitted → Reviewed → Approved → Materialised
- M09 Compliance Funnel: Required → Applied → Issued → Active
- M11 Action Funnel: Open → In Review → Resolved → Closed
- M15 Defect Funnel: Reported → Assessed → Fixed → Verified
- HDI Import Funnel: Submitted → Validated → Confirmed → Locked

---

### 4.1.5 Heatmap

```
Library:        Custom Tailwind grid + d3-scale-chromatic
Use cases:      Risk matrix (5×5 Impact × Likelihood), project × KPI status,
                NCR concentration (WBS × severity), compliance status, calendar
                density
Decision pattern:  "Where are the hotspots in this 2D space?"
Cell sizes:     Min 32×32 px desktop; min 24×24 px mobile
Cell colour:    Severity-coded (#10b981 → #f59e0b → #ef4444 gradient)
                OR count-density (cyan low → cyan high)
Hover:          Reveals exact cell value + drill-down option
```

**Examples:**
- M05 Risk Heatmap 5×5: Impact × Likelihood
- M01 Portfolio Heatmap: Project × KPI (CPI, SPI, Margin, Risks, Compliance)
- M04 NCR Concentration: WBS × Severity

---

### 4.1.6 Gantt Chart

```
Library:        frappe-gantt (locked v0.7.x)
Use cases:      Master schedule, procurement schedule, look-ahead view, permit timeline
Decision pattern:  "Is X happening on time relative to its plan?"
Layers:         Up to 6 layers per row (baseline, actual, critical path indicator,
                milestones, today line, float — see Master Gantt anatomy in §7.5)
Mobile:         Limit to 4-week look-ahead by default; full Gantt = "View on desktop"
Performance:    < 500 rows acceptable; virtual scrolling beyond
```

**Examples:**
- M03 Master Gantt: WBS rows × time, with baseline + actual + critical path
- M03 Procurement Gantt: Items × order/delivery time
- M03 Look-ahead: Filtered to 4-week window
- M09 Permit Gantt: Permits × required-by/received timeline

---

### 4.1.7 Donut

```
Library:        Recharts <PieChart innerRadius={60} outerRadius={90}>
Use cases:      Concentration analysis, BAC by package, payment aging
Decision pattern:  "What's the distribution of X across categories?"
Slice limit:    Max 6 slices (rule from Round 13 brief OQ-2.6)
Beyond limit:   Group smallest into "Other" slice
Forbidden:      Pie charts (≥6 slices), 3D donuts
```

**Examples:**
- M01 BAC by Sector
- M02 BAC by Package Type
- M06 Payment Aging (0-30, 31-60, 61-90, 90+ days)
- M15 Defects by Discipline

---

### 4.1.8 KPI Tile

```
Library:        Custom React (X9 ships <EPCCKPITile>)
Use cases:      All dashboard surfaces (M01, M07, M10, all module headers)
Decision pattern:  "What's the current state of metric X?"
Anatomy:        Large numeric value (JetBrains Mono 28px) +
                Compact label (Inter 11px UPPERCASE) +
                Optional trend indicator (delta vs previous period) +
                Optional severity colour
Min size:       120×80 px desktop; 100×70 px mobile
```

**Examples:**
- "12 Active Projects"
- "₹847 Cr Total BAC"
- "CPI 0.94" with amber severity
- "3 Pending Decisions" with trend ↑

---

### 4.1.9 Card Grid (with Severity)

```
Library:        Custom React + Tailwind grid
Use cases:      Project cards (M01, M10), action cards (M11), risk cards (M05)
Decision pattern:  "Which entities need my attention, ordered by severity?"
Sort default:   Severity DESC; secondary by user-relevant field
Severity bar:   3-4px left border (#ef4444 / #f59e0b / #10b981 / #6b7280)
Hover:          Subtle elevation; cyan border highlight
```

**Examples:**
- M01 Project Card Grid: severity-ordered project cards
- M11 Action Card: SLA-breach-ordered action cards
- M05 Risk Card: priority-ordered risk cards

---

### 4.1.10 Timeline (Events on Axis)

```
Library:        Custom React (X9 ships <EPCCTimeline>)
Use cases:      Milestones, gate passages, key project events
Decision pattern:  "When did/will X events happen?"
Markers:        Diamond / Circle / Square (per event type)
Status colour:  Per X8 RAGStatus
Today line:     Always present (#ef4444 vertical line)
```

**Examples:**
- M03 Milestone Timeline: project milestones with status
- M08 Stage Gate Timeline: SG-0 to SG-11 with passage status
- M07 Audit-Event Timeline (when needed)

---

### 4.1.11 Calendar

```
Library:        Custom React grid (12-month visible by default)
Use cases:      Permit expiries, warranty expiries, monsoon overlays, HSE
                incident heatmap
Decision pattern:  "What time-bound events are coming up?"
Cell:           Day-cell with markers for events
Layouts:        Month grid OR linear strip (12 months)
```

**Examples:**
- M09 Permit Calendar: next 90 days × permit expiry
- M15 Warranty Calendar: 12 months × warranty expiry
- M03 Monsoon Overlay: project timeline × monsoon windows
- M04 HSE Calendar Heatmap: days × incident count

---

### 4.1.12 Sparkline

```
Library:        Recharts (small mode) OR pure SVG
Use cases:      Inline mini-trends in tables; project list reporting health
Decision pattern:  "Is this row's metric trending up/down at a glance?"
Width:          80-160 px
Height:         24-40 px
No axes:        Pure trend shape only
```

**Examples:**
- M01 Project list: reporting cadence sparkline per project
- M10 Portfolio rows: CPI sparkline per project
- M07 Package list: SPI sparkline

---

## 4.2 Tier 2 — Specialised (Use When Justified)

### 4.2.1 Network / DAG Graph

```
Library:        react-flow (locked v12.x)
Use cases:      Critical path graph, project dependencies, interface diagrams
Decision pattern:  "What is the topology of relationships and where are the bottlenecks?"
Node count:     Up to 100 desktop; 50 mobile
Layout:         Auto-layout via Dagre algorithm
Drill-down:     Click node → entity detail
```

**Examples:**
- M03 Critical Path DAG
- M10 Cross-Project Dependency Network
- M28 Interface Management Diagram

---

### 4.2.2 Histogram

```
Library:        Recharts <BarChart> with bucketed data
Use cases:      Float distribution, Monte Carlo P50/P80, productivity distribution
Decision pattern:  "What's the distribution of X values?"
Buckets:        Auto-calculated; min 5, max 30
Markers:        Vertical lines for P50/P80/Mean as needed
```

**Examples:**
- M03 Float Histogram: WBS count × float-day buckets
- M05 Monte Carlo Histogram: EAC distribution with P50/P80 markers
- M04 Productivity Distribution

---

### 4.2.3 Scatter Plot

```
Library:        Recharts <ScatterChart>
Use cases:      Package quadrant analysis (CPI × SPI sized by BAC)
Decision pattern:  "How are entities distributed across two metrics?"
Quadrant labels: Visible (e.g., "Healthy" top-right, "Critical" bottom-left)
Bubble size:    Optional third dimension (proportional to scalar metric)
```

**Examples:**
- M07 Package Scatter: package CPI × SPI, sized by BAC
- M10 Project Scatter: schedule variance × cost variance

---

### 4.2.4 Forecast Cone

```
Library:        Recharts <Line> + <Area>
Use cases:      EAC range forecasting (P50/P80 confidence band)
Decision pattern:  "What's the forecasted range with uncertainty?"
Layers:         Historical line + forecast median line + P10-P90 band
                + P25-P75 band (darker)
```

**Examples:**
- M07 EAC Forecast Cone

---

## 4.3 Library Selection Rationale

| Library | Locked | Bundle | Reason |
|---|---|---|---|
| **Recharts** | v3.x | ~120 KB gzipped | Declarative React, light, Tailwind-friendly, supports 80% of chart types |
| **frappe-gantt** | v0.7.x | ~50 KB | MIT, Gantt-specific, Recharts can't do this |
| **react-flow** | v12.x | ~100 KB (lazy-loaded) | Industry-standard for node-edge UIs |
| **d3-scale-chromatic** | v3.x | ~10 KB | For heatmap colour scales (avoid full d3) |

**Rejected libraries:**
- D3 directly (too low-level)
- Chart.js (canvas-based, harder to style)
- Highcharts / amCharts (commercial complications)
- Plotly (heavy bundle ~3MB)

---

# §5 — DESIGN TOKENS

## 5.1 Colour Palette (CSS Custom Properties)

```css
:root {
  /* Page surfaces */
  --bg-page:        #0a0a0a;
  --bg-surface-1:   #141414;  /* chart card */
  --bg-surface-2:   #1c1c1c;  /* chart inner */
  --bg-surface-3:   #232323;  /* hover, active row */

  /* Borders */
  --border-subtle:    #262626;
  --border-emphasis:  #2a2a2a;
  --border-active:    #22d3ee;

  /* Text */
  --text-primary:   #e5e5e5;
  --text-dim:       #9ca3af;
  --text-mute:      #6b7280;
  --text-inverse:   #0a0a0a;  /* on cyan/emerald backgrounds */

  /* Data — semantic palette */
  --data-primary:   #22d3ee;  /* cyan: actuals, primary line, active state */
  --data-positive:  #10b981;  /* emerald: Green RAG, EV, on-track, terminal-safe */
  --data-warning:   #f59e0b;  /* amber: Amber RAG, baseline, warning, pending action */
  --data-negative:  #ef4444;  /* red: Red RAG, breach, AC over, critical path */
  --data-special:   #a855f7;  /* purple: predictive, scenario, audit */
  --data-info:      #3b82f6;  /* blue: informational, neutral */
  --data-mute:      #6b7280;  /* gray: historical, archived, container outline */

  /* Severity bar colours (for severity-* row borders) */
  --severity-critical: #ef4444;
  --severity-warning:  #f59e0b;
  --severity-info:     #3b82f6;
  --severity-success:  #10b981;
}
```

## 5.2 Colour Semantics — Locked Mappings

| Colour | Reserved For | Forbidden For |
|---|---|---|
| Cyan (#22d3ee) | Primary actuals, current state | Pleasant decoration; warning |
| Emerald (#10b981) | Positive outcomes, Green RAG, on-track | Anything ambiguous |
| Amber (#f59e0b) | Warning, baseline, planned-but-not-done | Active states |
| Red (#ef4444) | Negative, breach, critical path, error | Decoration |
| Purple (#a855f7) | Predictive forecasts, scenarios, audit context | Primary data |
| Blue (#3b82f6) | Informational only | Operational data |
| Gray (#6b7280) | Historical, archived, container/container | Active series |

**Rule:** Anyone proposing a chart that uses semantic colours for non-semantic purposes (e.g., red for "highlighted item" instead of "negative state") must update X9 first.

## 5.3 Typography

```
Font — UI labels:        'Inter', system-ui, sans-serif
Font — numerics:         'JetBrains Mono', monospace
Font — chart titles:     Inter 600, 14px, letter-spacing 0.02em
Font — chart axis:       JetBrains Mono 400, 11px
Font — chart legend:     Inter 500, 12px
Font — chart tooltip:    Inter 400 / JetBrains Mono 500 (mixed)
Font — KPI value:        JetBrains Mono 700, 28px
Font — KPI label:        Inter 600, 11px UPPERCASE, letter-spacing 0.08em
Font — data values:      JetBrains Mono 500, 13px
```

## 5.4 Spacing Scale (4px Base Grid)

```
Base unit:               4px
Chart padding:           16px (compact) / 24px (standard) / 32px (large)
Chart card border:       1px solid var(--border-subtle)
Chart card radius:       4px
KPI card padding:        16px
KPI grid gap:            12px
Section spacing:         16-24px between charts
Chart-to-chart gap:      16px (in dashboards)
```

## 5.5 Animation

```
Transitions:             150-200ms ease-out (chart enter)
Hover response:          50ms (instant feel)
Tooltip fade:            100ms
Reduced motion:          ALL transitions disabled if user prefers-reduced-motion
Loading shimmer:         1.5s linear infinite (skeleton states)
Chart redraw on data update:  NO animation (would distract from change-detection)
```

## 5.6 Iconography

Use **Lucide React** (already in stack). Standard sizes 16px / 20px / 24px.

## 5.7 Locale Defaults (per OQ-2 lock)

```
Locale:                  en-IN
Number formatting:       Indian comma grouping (1,00,00,000)
Currency display:        ₹ Cr / ₹ L for ≥ ₹1L; ₹ for < ₹1L
Date format (axis):      DD MMM YYYY (e.g., "23 Apr 2026")
Date format (compact):   DD MMM (e.g., "23 Apr")
Time format:             24-hour HH:mm (e.g., "14:30")
```

---

# §6 — ROLE-TIERED FIELD DISPLAY INHERITANCE

## 6.1 The Inheritance Contract

Charts inherit field-level permission rules from M02 (BR-02-008) and entity scope rules from M34. **Charts are visual API responses, not hardcoded SVG.**

## 6.2 Rate Display Inheritance (M02 BR-02-008)

Per OQ-1.5 from Round 13 — **API serialiser pre-applies the spike formula. Chart components are dumb renderers.**

| Role | Y-axis Rate Display | Tooltip Behaviour |
|---|---|---|
| SYSTEM_ADMIN, PMO_DIRECTOR, FINANCE_LEAD, EXTERNAL_AUDITOR | Actual values | Actual + audit log entry |
| PORTFOLIO_MANAGER, PROJECT_DIRECTOR, PROCUREMENT_OFFICER, COMPLIANCE_MANAGER | Loaded (× 1.15) | Loaded values |
| PLANNING_ENGINEER, QS_MANAGER | Indexed (× 1.08) | Indexed values |
| SITE_MANAGER, READ_ONLY | `[RESTRICTED]` axis labels | "Restricted" tooltip |

## 6.3 Implementation

```
Backend:
  - JWT + role in auth context
  - Serialiser at API layer applies spike formula
  - Response contains pre-spiked values
  - Chart component receives sanitised values

Frontend:
  - Chart component is dumb renderer
  - Receives `rateMode` prop from auth context (for axis-label rendering)
  - NEVER applies spike formula client-side
  - NEVER stores actual rate in client memory
```

## 6.4 Defence-in-Depth Principle

Spike formula is applied at the API serialiser layer, NOT at the database query layer. Even a SQL injection that returned BOQ rows would still pass through the serialiser before client.

**Privileged access logged:** When SYSTEM_ADMIN, PMO_DIRECTOR, FINANCE_LEAD, or EXTERNAL_AUDITOR views actual rates in charts, audit log entry `RATE_ACCESSED_PRIVILEGED` is created (X8 §4.12).

## 6.5 Project Scope Filtering

PROJECT_DIRECTOR sees own projects' data; PMO_DIRECTOR sees all. Enforced at API layer; chart components receive scoped data.

## 6.6 Sensitive Data Visibility

Some charts may surface sensitive data (specific risks, party names). X9 default: respect entity-level permissions. Per-chart overrides in module specs.

---

# §7 — COMPOSITION RULES

## 7.0 Three Patterns Locked

```
Pattern 1: SINGLE-SERIES CHART      → one chart, one data type
Pattern 2: COMBINED CHART           → multi-series, shared axes
Pattern 3: COMPOSED VIEW            → multiple charts in one screen
```

## 7.1 When to COMBINE Series in One Chart

ALL of the following must be true:

| Criterion | Required |
|---|---|
| Series share the same X-axis (time, category) | ✅ Required |
| Series share the same Y-axis (or compatible scales) | ✅ Required |
| Comparison is the PRIMARY insight | ✅ Required |
| ≤ 4 series total (cognitive limit) | ✅ Required |
| Series are conceptually related (planned vs actual; baseline vs current) | ✅ Required |

**Examples that pass:**
- Gantt: baseline + actual + forecast (same time axis, same WBS rows)
- EVM 3-line: PV + EV + AC (same time axis, same currency)
- S-curve: planned + actual (same time, same cumulative %)
- Resource histogram: stacked types per period (same time axis)

## 7.2 When to SEPARATE into Multiple Charts

ANY of the following triggers separation:

| Criterion | Triggers Separation |
|---|---|
| Different units on Y-axis (₹ and %) | ✅ Separate |
| Different time scales | ✅ Separate |
| Comparison is secondary, not primary | ✅ Separate |
| Combined would exceed 4 series | ✅ Separate |
| Series are conceptually unrelated | ✅ Separate |

**Examples that fail combining:**
- Schedule progress (%) + cashflow (₹) — different units → separate
- Gantt + S-curve — different chart types → separate, side-by-side OK
- Risk heatmap + cost breakdown — unrelated concepts → separate

## 7.3 When to COMPOSE into a Dashboard View

ALL of the following must be true:

| Criterion | Required |
|---|---|
| User needs holistic perspective in single view | ✅ Required |
| Each chart has clear, distinct purpose | ✅ Required |
| Drill-down available between charts | ✅ Required |
| Total cognitive load is sustainable (≤ 8 elements) | ✅ Required |

**Examples:**
- M10 Command Dashboard: KPI tiles + project cards + heatmap
- M07 EVM Dashboard: 3-line + CPI/SPI trend + EAC cone
- M03 Schedule Workspace: Gantt + variance bar + milestone timeline

## 7.4 Anti-Patterns (FORBIDDEN by §16)

| ❌ Anti-Pattern | Why Forbidden |
|---|---|
| Dual-axis chart with different scales (e.g., ₹ left, % right) | Cognitive load; users misread; statistically deceptive |
| > 4 series on one chart | Visual noise; nothing readable |
| Pie chart with > 6 slices | Use Donut variant only |
| Mixing chart types in one canvas (line + bar + pie inside one space) | Confusion; pick the right type |
| Stacking unrelated series | Different concepts mixed |
| 3D charts of any kind | Visual deception |
| Animated rotating charts | Distracting; performance cost |
| Word clouds | Not analytically useful |

These don't just look ugly — they actively mislead users making capital decisions.

## 7.5 Per-Chart-Type Composition Specifications

### 7.5.1 Master Gantt — 6 Layered Elements (M03)

```
For each WBS row (single chart space, multi-layer):
  Layer 1 (background):   Subtle grid, time axis
  Layer 2 (baseline):     Amber bars (40% opacity, behind)
  Layer 3 (actual):       Cyan bars (full opacity, foreground)
  Layer 4 (critical):     Red highlight on critical-path rows
  Layer 5 (milestones):   Diamond markers on dates
  Layer 6 (today):        Vertical red line at report_date
```

All 6 layers share the time axis AND the WBS row axis. They are coordinated, not just stacked.

### 7.5.2 EVM 3-Line (M07)

```
Single chart space, 3 series:
  PV  → amber line (planned, baseline)
  EV  → cyan line (earned)
  AC  → red line (actual cost)
  Reference at variance points; variance band shaded
```

### 7.5.3 Capital Funnel (M06) — Pipeline Funnel Pattern

See §9 for deep specification. 4-layer nested bars with headroom visualisation.

### 7.5.4 Cashflow Time-Series (M06)

```
Stacked bar over time:
  X-axis: months
  Y-axis: ₹ (single scale)
  Stacks per bar (bottom-to-top):
    Paid     → emerald
    Accrued  → cyan
    Committed → amber
    Budgeted → gray (outline)
```

### 7.5.5 S-curve Combined (M03, M04)

```
Single chart space, 2 series:
  Planned (cumulative %)  → amber line
  Actual (cumulative %)   → cyan line
  Variance area between curves: shaded amber/red
  Y-axis: 0-100%
  X-axis: time (project months)
```

---

# §8 — MODULE-BY-MODULE CHART MATRIX

This is the canonical reference for every chart-bearing module. Module specs reference this section by module ID.

## 8.1 M01 — Project Registry

| Chart | Type | Pattern | Decision Answered |
|---|---|---|---|
| Portfolio Heatmap | heatmap | Heatmap | Which projects need attention right now? |
| Portfolio RAG Trend | stacked_bar_time | Stacked Bar (time) | Is the portfolio drifting toward risk? |
| BAC Concentration | donut | Donut | Where is capital concentrated? |
| Reporting Health | sparkline | Sparkline (in table) | Which projects are stale on reporting? |
| Exception Trend | bar_simple | Bar | How are exclusivity exceptions trending? |

## 8.2 M02 — Structure & WBS

| Chart | Type | Pattern | Decision Answered |
|---|---|---|---|
| WBS Tree | custom_tree | Custom (already shipped) | Is my WBS structurally complete? |
| BAC by Package | donut | Donut | Where is BAC concentrated by package? |
| BAC Drift | line_with_events | Line | How has BAC drifted over time? |

## 8.3 M03 — Planning & Milestones (Chart-heavy)

| Chart | Type | Pattern | Decision Answered |
|---|---|---|---|
| Master Gantt with Baseline + Critical Path | gantt_with_overlay | Gantt | Is the project on schedule? |
| Variance Bar | bar_horizontal | Bar (horizontal) | What's the variance to baseline by WBS? |
| Look-ahead Gantt | gantt_filtered | Gantt | What needs to happen in next 4 weeks? |
| Critical Path DAG | network_dag | Network/DAG | Are critical path activities healthy? |
| Milestone Timeline | timeline | Timeline | Are milestones being hit? |
| Schedule S-curve | line_multi_series | Line | Is planned vs actual progress tracking? |
| Resource Histogram | bar_stacked_time | Stacked Bar | Are resources over/under-loaded? |
| Procurement Gantt | gantt | Gantt | Are long-lead-time items ordered in time? |
| Float Histogram | histogram | Histogram | Float distribution — close to critical? |

## 8.4 M04 — Execution Capture

| Chart | Type | Pattern | Decision Answered |
|---|---|---|---|
| Progress S-curve | line_multi_series | Line (reuse M03) | Is progress matching plan? |
| NCR Heatmap | heatmap | Heatmap | Where are NCRs concentrated? |
| NCR Pipeline Funnel | pipeline_funnel | Pipeline Funnel | Are NCRs being closed? |
| Productivity Trend | line_simple | Line | Is the team improving? |
| HSE Calendar Heatmap | calendar_heatmap | Calendar | HSE incident patterns? |

## 8.5 M05 — Risk & Change

| Chart | Type | Pattern | Decision Answered |
|---|---|---|---|
| Risk Heatmap 5×5 | heatmap_5x5 | Heatmap | Which risks need attention? |
| Risk Score Trend | line_simple | Line | Is risk exposure trending up or down? |
| Risk Pipeline Funnel | pipeline_funnel | Pipeline Funnel | Are risks being mitigated? |
| EAC Monte Carlo Histogram | histogram_with_markers | Histogram | What is project EAC range? |
| VO Pipeline Funnel | pipeline_funnel | Pipeline Funnel | VO pipeline status? |
| VO Cumulative Stacked Bar | stacked_bar_time | Stacked Bar | VO impact on BAC over time? |

## 8.6 M06 — Financial Control

| Chart | Type | Pattern | Decision Answered |
|---|---|---|---|
| **Capital Funnel** ⭐ | pipeline_funnel | Pipeline Funnel (FLAGSHIP) | Where is capital RIGHT NOW in the funnel? |
| Cashflow Time-Series | stacked_bar_time | Stacked Bar | How has cashflow evolved over time? |
| Payment Aging Donut | donut | Donut | Are payments on schedule? |
| Outstanding Vendor Bar | bar_horizontal | Bar | What's outstanding to subcontractors? |
| Margin by Package | bar_with_target | Bar | Is gross margin healthy by package? |
| Variance Bar | bar_horizontal | Bar (reuse M03) | Where is variance from budget? |

## 8.7 M07 — EVM Engine (Chart-rich)

| Chart | Type | Pattern | Decision Answered |
|---|---|---|---|
| **EVM 3-Line** ⭐ | line_multi_series | Line (CANONICAL) | Is the project earning value as planned? |
| CPI/SPI Trend | line_dual_with_reference | Line | CPI/SPI trend — accelerating or decelerating? |
| EAC Forecast Cone | forecast_cone | Forecast Cone | What is forecasted EAC? |
| Package Scatter | scatter | Scatter | Per-package CPI/SPI matrix? |
| TCPI Bar with Zones | bar_with_zones | Bar | TCPI feasibility — can we recover? |

## 8.8 M08 — Gate Control

| Chart | Type | Pattern | Decision Answered |
|---|---|---|---|
| Stage Gate Timeline | timeline | Timeline | Where is the project in gates? |
| Gate Duration Bar | bar_horizontal | Bar | How long does each gate take? |
| Gate Pass-Rate Stack | stacked_bar | Stacked Bar | Are gates passing on first try? |
| Gate Heatmap | heatmap | Heatmap | Gate health across portfolio? |

## 8.9 M09 — Compliance Tracker

| Chart | Type | Pattern | Decision Answered |
|---|---|---|---|
| Permit Gantt | gantt | Gantt | Are regulatory clearances on track? |
| Compliance Heatmap | heatmap | Heatmap | Compliance status across categories? |
| Permit Calendar | calendar | Calendar | What permits coming up for renewal? |
| Compliance Pipeline Funnel | pipeline_funnel | Pipeline Funnel | Pipeline of compliance items? |

## 8.10 M10 — EPCC Command (Dashboard)

| Chart | Type | Pattern | Decision Answered |
|---|---|---|---|
| KPI Tile Grid | kpi_tiles | KPI Tile | Portfolio health at a glance? |
| Project Card Grid | card_grid | Card Grid | Which projects need triage? |
| Portfolio Distribution | bar_with_quartile_markers | Bar (replaces box plot) | CPI/SPI distribution? |
| Dependency Network | network_dag | Network | Cross-project dependencies? |

## 8.11 M11 — Action Register

| Chart | Type | Pattern | Decision Answered |
|---|---|---|---|
| Action Aging Heatmap | heatmap | Heatmap | What's pending and breaching SLA? |
| Action Pipeline Funnel | pipeline_funnel | Pipeline Funnel | Decision queue throughput? |
| SLA Breach Trend | line_simple | Line | SLA breach trend? |
| Owner Workload Bar | bar_with_overlay | Bar | Action ownership distribution? |

## 8.12 M15 — Handover & DLP

| Chart | Type | Pattern | Decision Answered |
|---|---|---|---|
| Defect Burn-down Line | line_simple | Line | Defect closure timeline? |
| Defect Donut | donut | Donut | Defects by category? |
| Defect Aging Heatmap | heatmap | Heatmap | Defect aging? |
| Warranty Calendar | calendar | Calendar | Warranty expiry calendar? |

## 8.13 Other Modules (Light Chart Use)

| Module | Charts |
|---|---|
| M12 Document Control | DocumentType distribution donut |
| M13 Correspondence | RFI cycle time bar |
| M14 QS Measurement | Measurement vs BOQ progress bar |
| M16-M19 Strategic | KPI tiles + portfolio views (similar to M10) |
| M22-M26 | Compliance/Performance heatmaps + donuts |
| M27 Design Control | Pipeline funnel (Design status pipeline) |
| M28 Interface Mgmt | Network DAG (Interface diagram) |
| M29 Tendering | Bid comparison bar + evaluation matrix heatmap |
| M30 Vendor PQ | Vendor scorecard bar (NOT radar — forbidden) |
| M33 Audit | Audit findings severity heatmap |
| HDI | Pipeline funnel (Import status) |
| PF01-PF06 | Inherits from primary modules; mobile-adapted |

---

# §9 — PIPELINE FUNNEL — DEEP COMPONENT SPECIFICATION

This is the FLAGSHIP pattern — used in 8+ modules. Worth a dedicated specification.

## 9.1 Pattern Definition

A **Pipeline Funnel** visualises a state-pipeline where each state is a SUBSET of the previous. Inner bars are nested within outer bars; visible "headroom" gaps represent capacity remaining at each state.

## 9.2 Core Anatomy

```
LAYER 1 (Container):    Outermost — represents total capacity
                        Outline only (gray border, transparent fill)
                        Example: Budgeted, Required, Identified

LAYER 2:                Filled — first transition state
                        Example: Committed, Applied, Assessed

LAYER 3:                Filled — second transition state
                        Example: Accrued, Issued, Mitigated

LAYER 4:                Filled — terminal state
                        Example: Paid, Active, Closed

GAP (between layers):   Hatched/diagonal pattern
                        Represents headroom at each state
                        Click reveals: "₹X.XX available at this state"
```

## 9.3 Component Contract

```typescript
interface PipelineFunnelData {
  layers: PipelineFunnelLayer[];      // Exactly 4 layers
  reportDate: ISO8601;
  containerLabel: string;              // e.g., "Budgeted"
  thresholds?: PipelineFunnelThresholds;
}

interface PipelineFunnelLayer {
  label: string;                       // e.g., "Committed"
  value: number;                       // Absolute value
  percentOfContainer: number;          // 0.0 to 1.0
  count?: number;                      // Optional item count
  metadata?: Record<string, any>;      // Module-specific extras
}

interface PipelineFunnelThresholds {
  amberAtPercent: number;              // e.g., 0.95 — show amber dot
  redAtPercent: number;                // e.g., 1.00 — show red dot
}

interface EPCCPipelineFunnelProps {
  title: string;
  subtitle?: string;
  data: PipelineFunnelData;
  rateMode?: RateMode;                 // From auth context
  sourceModule: string;
  height?: number;                     // Default 320
  variant?: 'horizontal' | 'vertical'; // Default horizontal; mobile = vertical
  onLayerClick?: (layer: PipelineFunnelLayer) => void;
  onActionExport?: () => void;
}
```

## 9.4 Visual Specifications

### 9.4.1 Layout

```
Horizontal layout (desktop):

  Container Label    ┃░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░┃   100.0%
                     ↓ headroom annotation
  Layer 2 Label   ⚠  ┃░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██████████┃    XX.X%
                     ↓ headroom annotation
  Layer 3 Label      ┃░░░░░░░░░░░░░░░░░░░░░░██████████████████┃    XX.X%
                     ↓ headroom annotation
  Layer 4 Label      ┃░░░░░░░░░░░░██████████████████████████████┃   XX.X%
```

### 9.4.2 Colours

```
Container (Layer 1):   Outline #6b7280 (gray); transparent fill
Layer 2:               Amber (#f59e0b) for "pending action" semantic
Layer 3:               Cyan (#22d3ee) for "active state" semantic
Layer 4:               Emerald (#10b981) for "terminal-safe" semantic
Headroom (gap):        Diagonal stripes #2a2a2a on transparent
```

### 9.4.3 Annotations

Between each pair of layers, render a delta annotation:

```
↓ Δ ₹5.40 Cr available headroom (committable capacity)
↓ Δ ₹14.85 Cr in pipeline (work to deliver)
↓ Δ ₹13.85 Cr payable backlog
```

The label text comes from the module spec (each instance customises).

### 9.4.4 Threshold Indicators

```
At amberAtPercent (default 0.95):
  ⚠ Amber dot next to layer label
  Tooltip: "Near capacity — review before committing more"

At redAtPercent (default 1.00):
  🔴 Red dot next to layer label
  Tooltip: "AT CAPACITY — no more headroom"

Above redAtPercent (over-spent):
  Layer extends past container with red striped overlay
  Header banner: "OVER-COMMITTED by ₹X.XX (X.X%)"
```

### 9.4.5 Hover Behaviour

```
Hover on Layer 2 ("Committed"):
  ┌───────────────────────────────────────┐
  │ COMMITTED                             │
  │                                       │
  │ Amount:           ₹63.00 Cr           │
  │ % of Budget:      92.1%               │
  │ Available to commit: ₹5.40 Cr (7.9%)  │
  │                                       │
  │ Source: M06 CommitmentLedger          │
  │ As-of: 2026-04-23                     │
  │ Click to drill into commitment list   │
  └───────────────────────────────────────┘
```

## 9.5 Module-Specific Implementations

### 9.5.1 M06 Capital Funnel ⭐ — **1st named flagship instance** (annotated v0.4)

> **Formal-naming reconciliation (v0.4):** Capital Funnel is the FIRST formally-named instance of the §11 Pipeline Funnel pattern. Chronologically, the M04 NCR Funnel was the 8th implementation built into wireframes, but Capital Funnel is designated the FLAGSHIP per M06 Brief §7 + Wireframes line 12. Future modules referencing the pattern should cite "Pipeline Funnel (M06 Capital Funnel = flagship instance)".

```yaml
module: M06
container_label: Budgeted
layers:
  - { label: Committed, color: amber, semantic: "pledged_via_contracts" }
  - { label: Accrued, color: cyan, semantic: "work_delivered_accepted" }
  - { label: Paid, color: emerald, semantic: "cash_disbursed" }
delta_annotations:
  - "Δ Committable headroom"
  - "Δ Work pipeline (committed - accrued)"
  - "Δ Payable backlog (accrued - paid)"
thresholds:
  - committed_amber_at: 0.95
  - committed_red_at: 1.00
```

### 9.5.2 M04 NCR Funnel

```yaml
module: M04
container_label: Open NCRs
layers:
  - { label: In_Review, color: amber }
  - { label: Approved, color: cyan }
  - { label: Closed, color: emerald }
```

### 9.5.3 M05 Risk Funnel

```yaml
module: M05
container_label: Identified
layers:
  - { label: Assessed, color: amber }
  - { label: Mitigated, color: cyan }
  - { label: Closed, color: emerald }
```

### 9.5.4 M05 VO Funnel

```yaml
module: M05
container_label: Submitted
layers:
  - { label: Reviewed, color: amber }
  - { label: Approved, color: cyan }
  - { label: Materialised, color: emerald }
```

### 9.5.5 M09 Compliance Funnel

```yaml
module: M09
container_label: Required
layers:
  - { label: Applied, color: amber }
  - { label: Issued, color: cyan }
  - { label: Active, color: emerald }
```

### 9.5.6 M11 Action Funnel

```yaml
module: M11
container_label: Open
layers:
  - { label: In_Review, color: amber }
  - { label: Resolved, color: cyan }
  - { label: Closed, color: emerald }
```

### 9.5.7 M15 Defect Funnel

```yaml
module: M15
container_label: Reported
layers:
  - { label: Assessed, color: amber }
  - { label: Fixed, color: cyan }
  - { label: Verified, color: emerald }
```

### 9.5.8 HDI Import Funnel

```yaml
module: HDI
container_label: Submitted
layers:
  - { label: Validated, color: amber }
  - { label: Confirmed, color: cyan }
  - { label: Locked, color: emerald }
```

## 9.6 Composition Rules (Pipeline Funnel)

| Rule | Detail |
|---|---|
| Layer count | Exactly 4 layers (industry-tested) |
| Subset rule | Each inner layer MUST be ≤ outer layer |
| Layer relationships | Each layer represents a clear state transition |
| Anti-pattern | Never nest unrelated quantities (only state-pipeline data) |
| Anti-pattern | Never add 5+ layers (cognitive overload) |
| Time dimension | NOT a Pipeline Funnel concern — pair with separate time-series |

---

# §10 — PERFORMANCE BUDGETS

| Operation | Target | Notes |
|---|---|---|
| Initial chart render (1000 data points) | < 400 ms | Recharts handles natively |
| Interaction response (hover/click) | < 50 ms | "Instant" feel |
| Drill-down navigation | < 200 ms | URL change + new chart load |
| Real-time chart update | < 100 ms | Avoid re-render of entire canvas |
| Large dataset (10000 points line) | Switch to canvas-based renderer or aggregate | Recharts SVG slows ≥ 5000 points |
| Mobile chart rendering (PF01) | < 600 ms (3G) | Smaller dataset; simpler interactions |
| Bundle size impact (X9 components) | < 150 KB gzipped (Recharts + react-flow + frappe-gantt + X9 wrappers) | Lazy-load Gantt + network on first use |
| Pipeline Funnel render (4 layers) | < 100 ms | Lightweight component |
| Heatmap render (50×20 cells) | < 250 ms | Custom Tailwind grid is fast |
| Master Gantt (200 rows, 6 layers) | < 500 ms | frappe-gantt handles natively |
| Network/DAG (50 nodes) | < 400 ms | react-flow handles natively |

---

# §11 — ACCESSIBILITY (WCAG AA)

| Requirement | Implementation |
|---|---|
| Colour contrast | All chart colours pass 3:1 against backgrounds |
| Colour-blind safe | ALWAYS dual-encode (colour + shape/icon/label per OQ-1.6) |
| Alternative palette | Opt-in colour-blind variant via M34 user setting (Phase 1 ships standard; alt palette in Phase 1.5) |
| Keyboard navigation | All interactive charts support arrow + Enter |
| Screen reader | Charts have `aria-label` describing data; tabular fallback via "View as table" toggle |
| Reduced motion | Disable transitions when `prefers-reduced-motion` |
| Focus indicators | Visible focus ring on data points and controls |
| Text alternatives | Critical charts have prose summary in surrounding text |
| Tabular fallback | Every chart MUST offer "View as table" per OQ-1.10 |

---

# §12 — MOBILE / PF01 ADAPTATION

| Strategy | Detail |
|---|---|
| Layout | Charts stack vertically; full-width on mobile |
| Interactions | Touch-first; tap = hover; long-press = context menu |
| Density | Reduce data points or aggregate at smaller breakpoints |
| Gantt | Limit to 4-week look-ahead by default; full Gantt = "View on desktop" |
| Network | Limit to 50 nodes; show "View on desktop" for larger |
| Heatmap | Auto-rotate to portrait grid; smaller cells |
| KPI tiles | 2-column on mobile; 4-6 column on desktop |
| Pipeline Funnel | Vertical layout (already supports) |
| Hide non-essential | Subtitle, source attribution can collapse |

---

# §13 — ROLE-BASED DEFAULT VIEWS (LOCKED)

## 13.0 Architectural Rule (LOCKED)

> **Each module surfaces a role-specific default view on entry. Defaults are system-wide, not tenant-overridable in v1.0. User personalisation deferred to Phase 2.**

## 13.1 Implementation Contract

```
1. User authenticates → JWT contains role
2. User navigates to Module M-X
3. Frontend reads X9.role_default_views[M-X][role]
4. Renders primary view + secondary widgets per spec
5. User can navigate to other views via tabs (no role lock; just default lock)
```

## 13.2 No Tenant Override Rule

Tenant-level customisation is FORBIDDEN in v1.0. Reasons:
- Consistency across tenants enables training, support, documentation
- Tenant-level customisation = configuration drift over time
- Phase 2 can add overrides if real demand emerges

## 13.3 Default Views Per Module

### 13.3.1 M01 — Project Registry

| Role | Primary View | Secondary Widgets | Hidden |
|---|---|---|---|
| PMO_DIRECTOR | Portfolio Heatmap | Reporting health sparklines, BAC concentration donut, exception count | — |
| PORTFOLIO_MANAGER | Portfolio Heatmap (own portfolio filter) | RAG distribution trend, BAC by program | — |
| PROJECT_DIRECTOR | Single project card (own) full detail | Recent decisions, recent gates | Cross-project views |
| FINANCE_LEAD | BAC concentration donut + project list (financial fields) | Contract value totals | — |
| PLANNING_ENGINEER | Project list with schedule fields | Reporting health | Financials |
| QS_MANAGER | Project list with measurement context | — | Financials |
| PROCUREMENT_OFFICER | Project list with contract refs | — | Financials beyond contract value |
| SITE_MANAGER | Own project card only, minimal detail | — | Financials, cross-project |
| COMPLIANCE_MANAGER | Project list with sector fields | Exception count | Financials |
| READ_ONLY | Project list (scoped) | — | Most widgets |
| EXTERNAL_AUDITOR | Forensic detail view (own scope) | Audit log access | Operational dashboards |

### 13.3.2 M02 — Structure & WBS

| Role | Primary View | Secondary Widgets | Hidden |
|---|---|---|---|
| PMO_DIRECTOR | BAC Integrity Dashboard | Package list with BAC values, BAC drift line | — |
| PROJECT_DIRECTOR | WBS Tree builder (own project) | Package summary, BOQ progress | — |
| PLANNING_ENGINEER | WBS Tree | BOQ count per WBS, depth distribution | Rates |
| QS_MANAGER | BOQ editor (current package) | Package list, BOQ progress | — |
| FINANCE_LEAD | BAC by package donut + BOQ list (actual rates) | BAC totals | — |
| PROCUREMENT_OFFICER | Package list + BOQ list | — | Actual rates (Loaded only) |
| SITE_MANAGER | WBS tree (read-only) + BOQ list | Package summary | Rates redacted |
| READ_ONLY | WBS tree (read-only) | — | Most |
| EXTERNAL_AUDITOR | BAC ledger (forensic view) | Audit log | — |

### 13.3.3 M03 — Planning & Milestones

| Role | Primary View | Secondary Widgets | Hidden |
|---|---|---|---|
| PMO_DIRECTOR | Master Gantt with baseline + critical path | Milestone timeline, S-curve variance, RAG status | — |
| PORTFOLIO_MANAGER | Schedule variance summary (multi-project) | Cross-project critical path comparison | Single-project detail |
| **PROJECT_DIRECTOR** | Master Gantt (own) + variance bar | Look-ahead Gantt, milestone timeline, **PV S-curve (cost overlay)** ⭐ v0.2 | — |
| **PLANNING_ENGINEER** | WBS Gantt builder + float histogram | Critical path DAG, baseline lock state, **PV roll-up shape (no values)** ⭐ v0.2 | Financials (₹ values still hidden per M02 BR-02-008) |
| **SITE_MANAGER** | **4-week Look-ahead Gantt** | Today's milestones, resource roster | Master Gantt, financials, baseline detail |
| QS_MANAGER | Master Gantt (read) + procurement schedule | BOQ progress | — |
| FINANCE_LEAD | PV S-curve + procurement Gantt | Financial milestones, schedule variance ₹ impact | — |
| PROCUREMENT_OFFICER | Procurement Gantt | Long-lead-time alerts, vendor schedule | Master Gantt detail |
| COMPLIANCE_MANAGER | Permit Gantt + milestone timeline | Compliance events on schedule | — |
| READ_ONLY | Master Gantt (read-only) | — | Most |

**v0.2 changes (per M03 OQ-1.11=B):**
- **PROJECT_DIRECTOR** gains PV S-curve as secondary — Project Director balances schedule + cost; PV S-curve surfaces cost trajectory
- **PLANNING_ENGINEER** gains PV roll-up shape (curve only, no ₹ values) — provides feedback loop on Loading Profile choices

**Important:** PLANNING_ENGINEER's PV view shows shape only — actual ₹ values remain hidden per M02 BR-02-008 spike formula (Indexed tier). The aggregate curve shape is permitted; the underlying values are not.

### 13.3.4 M04 — Execution Capture (rewritten v0.3 per M04 Brief OQ-1.8 + Spec Block 5)

| Role | Primary View | Secondary Widgets | Hidden |
|---|---|---|---|
| **SITE_MANAGER** | **Today's progress entries** (data-entry surface — declared & in-Draft list with quick-Submit) | 4-week look-ahead Gantt with site-relevant WBS slice (link → M03) | Strategic financials; ContractorPerformanceScore |
| PROJECT_DIRECTOR | Project progress dashboard — **% complete heatmap by WBS** (with status badges) | NCR pipeline funnel (X9 §11 flagship — **8th instance**) | — |
| **QS_MANAGER** ⭐ v0.3 | **Pending approvals queue** — Submitted ProgressEntries awaiting QS review, sortable by entry_value_inr | Measurement variance — declared vs approved % delta per period | — |
| PMO_DIRECTOR | NCR pipeline funnel (X9 §11 flagship — **8th instance**) | Material receipts vs procurement schedule variance (link → M03) | — |
| PROCUREMENT_OFFICER | Material receipts log + receipt-vs-PO variance | Long-lead item tracking (link → M03 ProcurementScheduleItem) | — |
| ANALYST | Progress trend curves (S-curve actual vs planned by package) | NCR rate trend | — |
| READ_ONLY | Project progress card (status badges only; no approval actions) | — | All approval actions, all photo evidence |

**Scope-decomposition cleanup (v0.3):**
- HSE references removed → moved to **M31 HSESafetyManagement** (per M04 Brief OQ-1.1=B)
- "Measurement entry" for QS_MANAGER removed → moved to **M14 QSMeasurementBook** (per OQ-1.2=C — M04 owns WBS-grain progress only; M14 owns BOQ-line measurement)
- COMPLIANCE_MANAGER row dropped — compliance lives in **M09 ComplianceTracker**, not M04
- Rows added: PROCUREMENT_OFFICER (material receipts focus), ANALYST (trend curves), READ_ONLY (status-badge card per F-031 redaction principle)

**v0.3 changes (per M04 Brief OQ-1.8):**
- Audit log: `ROLE_DEFAULT_VIEW_CHANGED` for all 7 M04 rows
- NCR pipeline funnel confirmed as **8th instance** of §11 flagship pipeline pattern (full list: M06 Capital Funnel, M04 NCR, M05 Risk, M05 VO, M09 Compliance, M11 Action, M15 Defect, HDI Import — order updated)

### 13.3.5 M05 — Risk & Change

| Role | Primary View | Secondary Widgets | Hidden |
|---|---|---|---|
| PMO_DIRECTOR | Risk Heatmap + Risk Score Trend | VO pipeline funnel, EAC histogram | — |
| PROJECT_DIRECTOR | Risk Heatmap (own project) | VO list, recent VO impact | — |
| FINANCE_LEAD | Cumulative VO Bar + EAC histogram | VO list with cost impact | — |
| QS_MANAGER | VO list + materialisation queue | Open VOs needing BOQ updates | — |
| COMPLIANCE_MANAGER | Regulatory risks heatmap (filtered) | Compliance-related VOs | Financial-only risks |

### 13.3.6 M06 — Financial Control (rewritten v0.4 per M06 Spec Block 5 + Wireframes role-switcher — 8 roles)

| Role | Primary View | Secondary Widgets | Hidden |
|---|---|---|---|
| FINANCE_LEAD | **Capital Funnel** ⭐ (1st named flagship — see §9.5.1) | Cashflow time-series, payment aging, vendor outstanding | — |
| PMO_DIRECTOR | Capital Funnel (read primary) | Margin by package, variance bar, BAC integrity warnings | — |
| PROJECT_DIRECTOR | Capital Funnel (own project) | Recent payments, RA bills due, retention status | Cross-project |
| PROCUREMENT_OFFICER | Vendor outstanding bar + PO status | Procurement spend trend, GRN match status | Internal margins, EVM detail |
| QS_MANAGER | RA Bill approvals queue | Bill-line-by-line variance vs BOQ, invoice-match queue | Cross-project totals, internal margins |
| SITE_MANAGER | Capital Funnel (% only, no ₹) | Local PO/GRN status (own site) | All ₹ values |
| EXTERNAL_AUDITOR | Tabular immutable ledger view (CostLedgerEntry append-only) | Audit-event timeline, retention release log | Live in-flight states (Match_Pending, Draft, Submitted) |
| READ_ONLY | Capital Funnel summary card (% + RAG) | — | All ₹ values, all detail tables |

### 13.3.7 M07 — EVM Engine

| Role | Primary View | Secondary Widgets | Hidden |
|---|---|---|---|
| PMO_DIRECTOR | EVM 3-Line + CPI/SPI trend | EAC forecast cone, predictive alerts, package scatter | — |
| PROJECT_DIRECTOR | EVM 3-Line (own project) + CPI/SPI trend | Package scatter | — |
| FINANCE_LEAD | EVM 3-Line + EAC forecast cone | TCPI bar with thresholds | — |
| PORTFOLIO_MANAGER | Multi-project EVM comparison | CPI distribution box | Single-project |

### 13.3.8 M08 — Gate Control

| Role | Primary View | Secondary Widgets | Hidden |
|---|---|---|---|
| PMO_DIRECTOR | Stage Gate Heatmap (cross-project) | Gate duration bar, gate pass-rate stack | — |
| PROJECT_DIRECTOR | Stage Gate Timeline (own project) | Upcoming gate criteria | — |

### 13.3.9 M09 — Compliance Tracker

| Role | Primary View | Secondary Widgets | Hidden |
|---|---|---|---|
| COMPLIANCE_MANAGER | Permit Gantt + Permit Calendar (next 90d) | Compliance heatmap, pipeline funnel | — |
| PMO_DIRECTOR | Compliance Heatmap (cross-project) | Permit calendar | — |
| PROJECT_DIRECTOR | Permit Gantt (own project) | Compliance status checklist | — |

### 13.3.10 M10 — EPCC Command

| Role | Primary View | Secondary Widgets | Hidden |
|---|---|---|---|
| PMO_DIRECTOR | KPI Tile Grid + Project Card Grid | Decision queue, exception view | — |
| PORTFOLIO_MANAGER | Portfolio dashboard (own portfolio) | Cross-project distribution | — |

### 13.3.11 M11 — Action Register

| Role | Primary View | Secondary Widgets | Hidden |
|---|---|---|---|
| PMO_DIRECTOR | Action Aging Heatmap + SLA breach trend | Owner workload bar, pipeline funnel | — |
| All other roles | My pending actions list (own only, sorted by SLA) | Recent decisions | Cross-user views |

### 13.3.12 M15 — Handover & DLP

| Role | Primary View | Secondary Widgets | Hidden |
|---|---|---|---|
| PROJECT_DIRECTOR | Defect Burn-down Line + open defects list | Defect aging heatmap, warranty calendar | — |
| FACILITIES (future role) | Warranty Calendar | Defect trend | — |

## 13.4 Site Manager Subtraction Principle

Notice consistent Site Manager treatment across modules:
- Action-oriented views (today's work, this week's incidents, 4-week look-ahead)
- Redacted financials (no rates, no costs)
- Own-package scope (not portfolio-wide)
- Forms for capture (NCR entry, progress entry)

**Intentional design:** Site Manager's job is execution; surfacing strategic dashboards distracts. Clarity through subtraction.

## 13.5 Read-Only and External Auditor Treatment

- READ_ONLY: structure visible, insight hidden (legal/audit context)
- EXTERNAL_AUDITOR: forensic trail (audit logs, ledgers), not operational dashboards

## 13.6 Default View Spec Format (Module Spec Reference)

When a module spec (e.g., M03 Spec) is written, Block 5 (Filters & Views) references X9 §13:

```
M03 Block 5 — Filters and Views
─────────────────────────────────
5a. Default Role-Based Views: see X9 §13.3.3 M03 — Planning & Milestones
5b. View Components: as listed below (each with full spec)
```

Module specs do NOT redefine role defaults. They reference X9 by section.

---

# §14 — COMPONENT LIBRARY CONTRACTS

## 14.1 Shared Components (X9 ships)

Implemented when first module needs them (Round 17 M03 wireframes onward):

```typescript
<EPCCChart />              // Standard chart wrapper with title, subtitle, actions
<EPCCKPITile />             // KPI tile with value, label, optional trend
<EPCCLineChart />           // Recharts wrapper with EPCC defaults
<EPCCBarChart />            // Recharts wrapper with EPCC defaults
<EPCCHorizontalBar />       // Recharts horizontal layout wrapper
<EPCCStackedBar />          // Recharts stacked variant
<EPCCDonut />               // Recharts donut wrapper
<EPCCPipelineFunnel />      // Custom — flagship pattern
<EPCCHeatmap />             // Custom Tailwind grid
<EPCCTimeline />            // Custom timeline component
<EPCCCalendar />            // Custom calendar grid
<EPCCSparkline />           // Recharts small mode
<EPCCNetwork />             // react-flow wrapper
<EPCCGantt />               // frappe-gantt wrapper
<EPCCCardGrid />            // Custom severity-bordered card grid
<EPCCEmptyState />          // "No data" state
<EPCCLoadingState />        // Skeleton with shimmer
<EPCCErrorState />          // "Failed to load" with retry
<EPCCChartTooltip />        // Standard tooltip
<EPCCChartLegend />         // Standard legend
<EPCCDrillDownButton />     // Drill-down entry point
```

## 14.2 Standard Props (Every Chart Component)

```typescript
interface EPCCBaseChartProps {
  title: string;
  subtitle?: string;
  data: ChartData;
  loading?: boolean;
  error?: string;
  emptyMessage?: string;
  rateMode?: RateMode;
  sourceModule: string;
  lastUpdated?: ISO8601;
  onActionExport?: () => void;
  onActionDrillDown?: (entity: string) => void;
  height?: number;
  className?: string;
}
```

## 14.3 Standard Chart Anatomy

Every chart MUST have:

```
┌─────────────────────────────────────────────────┐
│ TITLE                          [actions: ⋯ ↓]   │
│ Subtitle (text-dim)                              │
│                                                  │
│   ┌──────────────────────────────────────────┐  │
│   │           CHART CANVAS                     │  │
│   └──────────────────────────────────────────┘  │
│                                                  │
│  ● Legend item 1   ● Legend item 2              │
│                                                  │
│  Source: [module] · Last updated: [timestamp]   │
└─────────────────────────────────────────────────┘
```

---

# §15 — LIBRARY VERSION PINS

| Library | Pinned Version | Bundle | License | Purpose |
|---|---|---|---|---|
| Recharts | 3.x (latest stable) | ~120 KB gzipped | MIT | Primary chart library |
| frappe-gantt | 0.7.x | ~50 KB | MIT | Gantt charts |
| react-flow | 12.x | ~100 KB (lazy) | MIT | Network/DAG charts |
| d3-scale-chromatic | 3.x | ~10 KB | BSD-3 | Heatmap colour scales |
| Lucide React | latest stable | ~30 KB | ISC | Icons |
| Tailwind CSS | 3.x | runtime via CDN | MIT | Styling |
| Inter font | latest | via Google Fonts | OFL | UI font |
| JetBrains Mono | latest | via Google Fonts | OFL | Numeric font |

**Lock policy:** Major version bumps require X9 version bump + audit. Minor/patch updates via standard package manager.

---

# §16 — ANTI-PATTERNS (FORBIDDEN)

| ❌ Forbidden | Why |
|---|---|
| 3D charts (any) | Visual deception; no analytical value |
| Radar / spider charts | Misleading for >5 axes |
| Dual-axis with different scales (₹ left, % right) | Cognitive load; statistically deceptive |
| Gauge / speedometer | Wastes space; KPI tile better |
| Pie with >6 slices | Donut variant only, max 6 |
| Animated rotating charts | Distracting; performance cost |
| Word clouds | Not analytically useful |
| Mixing chart types in one canvas (line + bar + pie) | Confusion |
| Stacking unrelated series | Different concepts mixed |
| > 4 series on one chart | Visual noise |
| Charts that answer no specific decision | Decoration; cut |
| Tenant-level role-default override (v1.0) | Configuration drift |
| Personal dashboard builder (v1.0) | Phase 2 |
| Real-time WebSocket subscriptions (v1.0) | Phase 2 |

---

# §17 — EXTENSION PROTOCOL

When a module spec needs a chart pattern X9 doesn't cover:

```
1. Test against §3 Decision-First Principle — does it answer one specific decision?
2. If yes, propose addition to X9 catalogue (§4)
3. Submit to X9 owner (PMO_DIRECTOR)
4. If accepted, X9 version bump (e.g., v0.1 → v0.2)
5. Update §4 catalogue + §8 module matrix + §13 role defaults
6. Re-issue X9 spec with change log entry
```

When a module spec needs a role-default change:

```
1. Update X9 §13.3.X table only
2. Minor X9 version bump (v0.1 → v0.1.1)
3. Audit log entry: ROLE_DEFAULT_VIEW_CHANGED
```

When extending chart catalogue:

```
1. Verify decision-first principle
2. Confirm not forbidden in §16
3. Confirm library license compatibility
4. Confirm bundle size acceptable
5. Document component contract
6. Update relevant module specs with chart reference
```

---

# §18 — ENFORCEMENT

## 18.1 Pre-Commit Checks

```
[ ] Every chart in module wireframes references X9 §4 catalogue type
[ ] Every chart has decision-first sentence per §3.1 template
[ ] No forbidden anti-patterns (§16)
[ ] Colour usage respects §5.2 semantic mapping
[ ] Role-default views match §13.3 table for that module
[ ] Performance budget confirmed (§10)
[ ] Accessibility tested (§11)
[ ] Mobile adaptation confirmed (§12)
```

## 18.2 Code Review Checks

```
[ ] Chart components use X9 shared library (§14.1)
[ ] Standard props interface respected (§14.2)
[ ] Standard anatomy rendered (§14.3)
[ ] Field-level rate display via API serialiser, not client-side (§6.3)
[ ] Library versions match pin (§15)
```

## 18.3 X9 Owner

PMO_DIRECTOR maintains X9 spec. Updates require:
- Justification per decision-first principle
- Audit log entry per change
- Version bump per change
- Notify affected modules

---

## APPENDIX A — Chart Type Decision Tree

```
What decision does this chart answer?
│
├─ "How has X changed over time?"
│   └─ Use Line (multi-series) — §4.1.1
│
├─ "Which X has the highest Y?"
│   └─ Use Horizontal Bar — §4.1.2
│
├─ "How has composition changed over time?"
│   └─ Use Stacked Bar (time) — §4.1.3
│
├─ "Where does state pipeline get stuck?"
│   └─ Use Pipeline Funnel — §4.1.4 + §9 ⭐
│
├─ "Where are hotspots in 2D space?"
│   └─ Use Heatmap — §4.1.5
│
├─ "Is X happening on time?"
│   └─ Use Gantt — §4.1.6
│
├─ "What's the distribution across categories?"
│   └─ Use Donut (≤6 slices) — §4.1.7
│
├─ "What's the current value of metric?"
│   └─ Use KPI Tile — §4.1.8
│
├─ "Which entities need attention?"
│   └─ Use Card Grid — §4.1.9
│
├─ "When did/will events happen?"
│   └─ Use Timeline — §4.1.10
│
├─ "What time-bound events coming up?"
│   └─ Use Calendar — §4.1.11
│
├─ "Trend at a glance in a row?"
│   └─ Use Sparkline — §4.1.12
│
├─ "What's the topology of relationships?"
│   └─ Use Network/DAG — §4.2.1
│
├─ "What's the distribution of values?"
│   └─ Use Histogram — §4.2.2
│
├─ "How are entities distributed across two metrics?"
│   └─ Use Scatter Plot — §4.2.3
│
└─ "What's the forecasted range with uncertainty?"
    └─ Use Forecast Cone — §4.2.4
```

---

## APPENDIX B — Living Document Notice

X9 is a LIVING document. Future bumps:

| Version | Trigger |
|---|---|
| v0.2 | First module wireframe locks (M03 Round 17) |
| v0.3 | Add new chart pattern from real module need |
| v0.5 | Phase 2 features added (personalisation, WebSocket) |
| v1.0 | All Phase 1 modules locked |

---

*v0.2 — X9 Visualisation Standards Spec locked. 18 sections. 16 chart types. Pipeline Funnel flagship pattern. Role-based default views per module updated for M03 (PROJECT_DIRECTOR + PV S-curve, PLANNING_ENGINEER + PV roll-up shape). Decision-first principle foundational. Awaiting first use in Round 17 M03 Wireframes.*
