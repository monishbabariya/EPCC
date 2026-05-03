# X9 — Visualisation Standards
## Brief v0.1
**Status:** Draft — Pending Review
**Type:** Cross-Cutting LIVING Document (parallel to X8)
**Author:** PMO Director / System Architect
**Created:** 2026-05-03
**Last Audited:** v0.1 on 2026-05-03
**Reference Standards:** X8_GlossaryENUMs_v0_3.md, M34_SystemAdminRBAC_Spec_v1_0.md, M02_StructureWBS_Spec_v1_0.md
**Folder:** /10_CrossCutting/

> **Why X9 exists:** Without a system-wide visualisation specification, every module would invent its own chart approach. With ~12 of 23 modules needing charts (M03 Gantt, M04 progress curves, M05 risk heatmap, M06 cashflow waterfall, M07 EVM 3-line, M10 dashboards, M11 decision queue, M15 DLP timeline, etc.), divergence is inevitable. X9 locks the visual contract before the first chart-bearing module (M03) is wireframed.

---

## 1. PURPOSE

X9 specifies **how data is rendered as visual artefacts in EPCC**, in the same way X8 specifies how data is named.

X9 covers:
- **Chart library choices** (which JS libraries are blessed)
- **Chart type catalogue** (which types are blessed; which are forbidden)
- **Design tokens** (colours, typography, spacing — locked across all charts)
- **Component contracts** (chart anatomy: title, axes, legend, tooltip, interaction)
- **Role-tiered chart behaviour** (charts inherit M34 + M02 permission model)
- **Data loading patterns** (real-time vs snapshot vs computed)
- **Performance budgets** (latency targets per chart)
- **Accessibility** (WCAG AA compliance, keyboard navigation, screen readers)
- **Mobile responsiveness** (graceful degradation on PF01)

X9 does NOT cover:
- Module-specific business rules (those stay in M-module specs)
- Backend chart data API design (charts are client-rendered; API is JSON)
- BI tool integration (Tableau, Power BI etc. are out of v1.0 scope)

---

## 2. DECISION IT ENABLES

> When module M-X needs to render data as a chart, the developer reads X9 and finds: which chart type to use, which library, which design tokens, which interaction patterns, and which role-permission contract to implement. Zero invention required at module level.

---

## 3. SCOPE — WHAT X9 STANDARDISES

| Area | Locked Decision Examples |
|---|---|
| Chart library — primary | **Recharts** (declarative React, light bundle, integrates with Tailwind) |
| Chart library — Gantt | **frappe-gantt** or equivalent (Recharts can't do this well) |
| Chart library — network | **react-flow** (M03 critical path, M11 dependency graphs) |
| Chart library — geographic | Deferred — no v1.0 module needs maps |
| Chart type catalogue | ~10 blessed types; others require X9 version bump |
| Colour palette | 7-colour core + 4 semantic states (matches existing wireframes) |
| Typography | JetBrains Mono for numerics; Inter for labels |
| Spacing scale | 4px base grid (Tailwind default) |
| Animation | Subtle only; respect `prefers-reduced-motion` |
| Tooltip behaviour | Hover-to-show; click-to-pin; keyboard accessible |
| Empty-state pattern | Standard "No data" component (X9 ships) |
| Loading-state pattern | Skeleton with shimmer; standard component |
| Error-state pattern | Standard "Failed to load" with retry |
| Drill-down navigation | URL-driven, browser-back compatible |
| Export formats | PNG, CSV, shareable URL (PDF deferred) |
| Role-tiered rate display | Inherits M02 BR-02-008 — Loaded/Indexed/Flat_Redacted applies in chart Y-axes |
| Role-tiered scope | Inherits M34 permission model — charts only show data user can access |

---

## 4. CHART TYPE CATALOGUE (Phase 1)

Based on systematic survey of all 23 modules + 6 platform features:

### 4a. Blessed Chart Types

| # | Chart Type | Primary Modules | Blessed Library | Why |
|---|---|---|---|---|
| 1 | **Line chart** | M07 EVM 3-line (PV/EV/AC), M07 CPI/SPI trend, M03 PV S-curve, M04 progress S-curve, M11 SLA trend | Recharts | Declarative, performant, dark-mode native |
| 2 | **Bar chart (stacked)** | M06 cashflow Budgeted→Committed→Accrued→Paid, M05 risk distribution, M10 KPI breakdowns | Recharts | Same as line |
| 3 | **Bar chart (horizontal)** | M03 resource histogram, M07 EAC variance | Recharts | Better for many categories |
| 4 | **Waterfall** | M06 cashflow waterfall, M07 EAC variance breakdown | Recharts (composed bars) | Built from primitives |
| 5 | **Donut/Pie** | M01 RAG distribution, M02 BAC by package, M05 risk by category | Recharts | Use sparingly — only for ≤6 categories |
| 6 | **Heatmap** | M05 risk heatmap (impact × likelihood), M11 decision queue density | Custom Tailwind grid + d3-scale-chromatic | Lightweight; no full d3 |
| 7 | **Histogram** | M05 Monte Carlo P50/P80, M04 productivity distribution | Recharts | For quantitative risk |
| 8 | **Gantt chart** | M03 master Gantt, M03 procurement Gantt, M09 permit Gantt | **frappe-gantt** | Recharts can't do this; frappe-gantt is light + free |
| 9 | **Timeline / milestone** | M03 milestone timeline, M15 DLP defect timeline, M08 gate passage | Custom React (Tailwind + small SVG) | Simple enough not to warrant a library |
| 10 | **Network / DAG** | M03 critical path graph, M11 dependency map | **react-flow** | Industry-standard for node-edge UIs |
| 11 | **Tree** | M02 WBS roll-up tree (already implemented) | Custom React | Already in wireframes; X9 just blesses |
| 12 | **Calendar grid** | M15 DLP warranty expiry, M03 monsoon overlay | Custom React | Specific layout; small enough |
| 13 | **KPI tile** | All dashboard surfaces (M01, M10, M07, etc.) | Custom React | Already used; X9 specifies anatomy |
| 14 | **Sparkline** | Inline mini-trends in tables (M01 project cards, M10 portfolio rows) | Recharts (small mode) | Embedded in row context |

### 4b. Forbidden Chart Types

| ❌ Forbidden | Why |
|---|---|
| 3D charts | Visual deception; no analytical value |
| Radar / spider | Misleading for >5 axes; rarely interpreted correctly |
| Dual-axis with different scales | Cognitive load; users misread |
| Gauge / speedometer | Wastes space; KPI tile communicates better |
| Pie with >6 slices | Donut variant only, max 6 categories |
| Animated rotating charts | Distracting; performance cost |
| Word clouds | Not analytically useful |

### 4c. Library Decision Rationale

**Recharts is the primary choice because:**
- Declarative React (matches our stack)
- Built on D3 primitives but doesn't expose d3 complexity
- Bundle size ~120 KB gzipped (acceptable)
- TypeScript-first
- Active maintenance (v3.x line)
- Theme-able via standard React patterns
- Supported in our React artefact stack

**Alternatives rejected:**
- **D3 directly** — too low-level; every chart a custom build; high maintenance
- **Chart.js** — canvas-based; harder to style consistently with rest of UI; less React-native
- **Highcharts / amCharts** — commercial license complications
- **Plotly** — heavy bundle (~3 MB); overkill for our needs
- **Visx (Airbnb)** — closer to D3; steeper curve; better as fallback for esoteric charts later

**frappe-gantt for Gantt because:**
- Recharts has no Gantt component
- frappe-gantt is MIT-licensed, ~50 KB
- Built specifically for project schedules
- Drag-resize support out of the box
- Critical path overlay achievable

**react-flow for network/DAG because:**
- Industry-standard for node-edge UIs
- MIT-licensed
- Handles drag, zoom, pan natively
- TypeScript-first, declarative

---

## 5. DESIGN TOKENS (locked from current wireframe palette)

### 5a. Colours

```
Page backgrounds:
  --bg-page:        #0a0a0a   (canvas)
  --bg-surface-1:   #141414   (chart card)
  --bg-surface-2:   #1c1c1c   (chart inner)
  --bg-surface-3:   #232323   (hover, active row)

Borders:
  --border-subtle:  #262626
  --border-emphasis: #2a2a2a
  --border-active:  #22d3ee

Text:
  --text-primary:   #e5e5e5
  --text-dim:       #9ca3af
  --text-mute:      #6b7280
  --text-inverse:   #0a0a0a   (on cyan/emerald backgrounds)

Data — primary (cyan):       #22d3ee   — actuals, primary line
Data — emerald (positive):   #10b981   — Green RAG, EV, on-track
Data — amber (warning):      #f59e0b   — Amber RAG, baseline, warning
Data — red (negative):       #ef4444   — Red RAG, breach, AC over
Data — purple (special):     #a855f7   — predictive, scenario, audit
Data — blue (info):          #3b82f6   — informational, neutral
Data — mute (historical):    #6b7280   — historical, archived data

Severity bar colours (for severity-* row borders):
  Critical:  #ef4444
  Warning:   #f59e0b
  Info:      #3b82f6
  Success:   #10b981
```

### 5b. Typography

```
Font — UI labels:        'Inter', system-ui, sans-serif
Font — numerics:         'JetBrains Mono', monospace
Font — chart titles:     Inter 600, 14px, letter-spacing 0.02em
Font — chart axis:       JetBrains Mono 400, 11px
Font — chart legend:     Inter 500, 12px
Font — chart tooltip:    Inter 400 / JetBrains Mono 500 (mixed for value)
Font — KPI value:        JetBrains Mono 700, 28px
Font — KPI label:        Inter 600, 11px, UPPERCASE, letter-spacing 0.08em
```

### 5c. Spacing

```
Base grid:               4px
Chart padding:           16px (compact) / 24px (standard) / 32px (large)
Chart card border:       1px solid var(--border-subtle)
Chart card radius:       4px
KPI card padding:        16px
KPI grid gap:            12px
Section spacing:         16-24px between charts
```

### 5d. Animation

```
Transitions:             150-200ms ease-out (chart enter)
Hover response:          50ms (instant feel)
Tooltip fade:            100ms
Reduced motion:          Disable all transitions if user prefers-reduced-motion
Loading shimmer:         1.5s linear infinite (skeleton states)
Chart redraw:            No animation on data update (would distract from change-detection)
```

### 5e. Iconography

Use **Lucide React** (already in stack). Standard sizes 16px / 20px / 24px.

---

## 6. ROLE-TIERED CHART BEHAVIOUR

Charts are NOT neutral data renderers. They inherit two contracts from M34 + M02:

### 6a. Permission Inheritance

```
Chart visibility = MIN(user role's view permission for the underlying entity)

Example:
  M07 EVM 3-line chart (PV/EV/AC) for Project KDMC-001
  ├─ PV value visible if user can view M03 PVProfile for project
  ├─ EV value visible if user can view M04 ProgressEntry for project
  └─ AC value visible if user can view M06 CostLedgerEntry for project

If any underlying entity is not viewable → chart shows "Insufficient permissions"
```

### 6b. Rate Display Inheritance (per M02 BR-02-008)

Charts that display monetary values (BAC, AC, EV, cashflow, EAC) MUST apply spike formula based on viewer's role:

| Role | Y-axis rate display | Tooltip behaviour |
|---|---|---|
| SYSTEM_ADMIN, PMO_DIRECTOR, FINANCE_LEAD, EXTERNAL_AUDITOR | Actual values | Actual + audit log entry |
| PORTFOLIO_MANAGER, PROJECT_DIRECTOR, PROCUREMENT_OFFICER, COMPLIANCE_MANAGER | Loaded (× 1.15) | Loaded values |
| PLANNING_ENGINEER, QS_MANAGER | Indexed (× 1.08) | Indexed values |
| SITE_MANAGER, READ_ONLY | `[RESTRICTED]` axis labels | "Restricted" tooltip |

**Implementation:** Chart components receive `rateMode` prop from auth context; serialiser at API has already applied formula to data.

### 6c. Project Scope Filtering

PROJECT_DIRECTOR sees own projects' data; PMO_DIRECTOR sees all. This is enforced at API layer (already locked in M34 + M01); chart components receive scoped data and don't need their own filter.

### 6d. Sensitive Data Visibility

Some charts may surface sensitive data (e.g., specific risks, party names). X9 default: respect entity-level permissions. Per-chart overrides specified in module specs (e.g., M05 may say "Risk heatmap shows category only for non-PMO; PMO sees risk titles").

---

## 7. CHART ANATOMY (locked component contract)

Every chart component MUST have these elements:

```
┌─────────────────────────────────────────────────┐
│ TITLE (Inter 600 14px)        [actions: ⋯ ↓]    │
│ Subtitle (Inter 400 12px text-dim)              │
│                                                  │
│   ┌──────────────────────────────────────────┐  │
│   │                                            │  │
│   │           CHART CANVAS                     │  │
│   │                                            │  │
│   │   (Recharts / frappe-gantt / etc.)        │  │
│   │                                            │  │
│   └──────────────────────────────────────────┘  │
│                                                  │
│  ● Legend item 1   ● Legend item 2              │
│                                                  │
│  Source: M07 · Last updated: 2026-05-03 09:14   │
└─────────────────────────────────────────────────┘
```

### Required props (component contract)

```typescript
interface EPCCChartProps {
  title: string;
  subtitle?: string;
  data: ChartData;
  loading?: boolean;
  error?: string;
  emptyMessage?: string;          // Default "No data available"
  rateMode?: RateMode;             // Inherited from auth context
  sourceModule: string;            // e.g., "M07"
  lastUpdated?: ISO8601;
  onActionExport?: () => void;
  onActionDrillDown?: (entity: string) => void;
  height?: number;                 // Default 300
  className?: string;
}
```

### Standard child components (X9 ships)

- `<EmptyState />` — when data array is empty
- `<LoadingState />` — skeleton with shimmer
- `<ErrorState />` — failed to load with retry button
- `<ChartTooltip />` — standard tooltip layout
- `<ChartLegend />` — standard legend
- `<KPITile />` — already in wireframes; X9 ratifies
- `<DrillDownButton />` — entry point for navigation

---

## 8. DATA LOADING PATTERNS

Each chart declares ONE pattern in its module spec:

| Pattern | Use Case | Cache Strategy | Example |
|---|---|---|---|
| **Real-time** | Current state queries | No cache | Today's CPI, latest risk register |
| **Snapshot** | Period-anchored views | Cache per report_date | EVM 3-line on report_date X |
| **Computed** | Expensive aggregations | Redis cache, invalidate on dependency change | Portfolio rollup, sector breakdown |

Pattern choice drives backend API endpoint design — module specs reference X9 pattern by name.

---

## 9. INTERACTION MODEL (locked)

| Interaction | Behaviour |
|---|---|
| Hover on data point | Tooltip with full data per role permission |
| Click on data point | Drill-down to detail (URL-driven for browser-back) |
| Click on legend | Toggle series visibility |
| Drag axis | Pan (line/bar charts only) |
| Wheel | Zoom (Gantt, network, optional on line charts) |
| Right-click | Context menu (export, copy data, share URL) |
| Keyboard | Arrow keys navigate data points; Enter to drill; Escape to close tooltips |
| Touch | Tap = hover; pinch = zoom (where applicable) |

---

## 10. PERFORMANCE BUDGETS

| Operation | Target | Notes |
|---|---|---|
| Initial chart render (1000 data points) | < 400 ms | Recharts handles this natively |
| Interaction response (hover/click) | < 50 ms | "Instant" feel |
| Drill-down navigation | < 200 ms | URL change + new chart load |
| Real-time chart update | < 100 ms | Avoid re-render of entire canvas |
| Large dataset (10000 points line) | Switch to canvas-based renderer or aggregate | Recharts SVG slows ≥ 5000 points |
| Mobile chart rendering (PF01) | < 600 ms (3G) | Smaller dataset; simpler interactions |
| Bundle size impact (X9 components) | < 150 KB gzipped (Recharts + react-flow + frappe-gantt + X9 wrappers) | Lazy-load Gantt + network on first use |

---

## 11. ACCESSIBILITY (WCAG AA)

| Requirement | Implementation |
|---|---|
| Colour contrast | All chart colours pass 3:1 against backgrounds |
| Colour-blind safe | Don't rely on red-vs-green only; pair with shape or pattern |
| Keyboard navigation | All interactive charts support arrow + Enter |
| Screen reader | Charts have `aria-label` describing data; tabular fallback available via "View as table" toggle |
| Reduced motion | Disable transitions when `prefers-reduced-motion` |
| Focus indicators | Visible focus ring on data points and controls |
| Text alternatives | Critical charts have prose summary in surrounding text |

---

## 12. MOBILE RESPONSIVENESS (PF01 contract)

| Strategy | Detail |
|---|---|
| Layout | Charts stack vertically; full-width on mobile |
| Interactions | Touch-first; tap = hover; long-press = context menu |
| Density | Reduce data points or aggregate at smaller breakpoints |
| Gantt | Limit to 4-week look-ahead by default on mobile |
| Network | Limit to 50 nodes; show "View on desktop" for larger graphs |
| Heatmap | Auto-rotate to portrait grid; smaller cells |
| KPI tiles | 2-column on mobile; 4 or 6-column on desktop |
| Hide non-essential | Subtitle, source attribution can be collapsed |

---

## 13. M03 SPECIFIC PRE-COMMITMENTS (chart-by-chart)

Since M03 is the first chart-bearing module, X9 declares contracts in advance:

| M03 Chart | Type | Library | Pattern | Notes |
|---|---|---|---|---|
| Master Gantt with critical path | Gantt | frappe-gantt | Snapshot | Critical path highlighted in red; baseline overlay in amber |
| Baseline vs Actual S-curve | Line (2 series) | Recharts | Snapshot | Planned (cyan) + Actual (emerald); deviation area shaded |
| Milestone timeline | Timeline | Custom React | Real-time | Status colour-coded; delays in red |
| Resource histogram | Bar (stacked) | Recharts | Computed | Per period; resource type stack |
| PV S-curve | Line (cumulative) | Recharts | Snapshot | Role-tiered rate display |
| Procurement Gantt | Gantt | frappe-gantt | Real-time | Long-lead-time items red-tagged |
| Look-ahead view | Filtered Gantt | frappe-gantt | Real-time | 4-week default; configurable |
| Float distribution | Histogram | Recharts | Snapshot | Identifies near-critical activities |

---

## 14. CRITICAL OPEN QUESTIONS

### OQ-1 (Design — your decision required)

#### OQ-1.1 — Primary chart library: Recharts vs alternatives?

**Question:** Lock Recharts as the primary chart library?

**Options:**
- **A** Recharts (recommended) — declarative, React-native, ~120 KB
- **B** Chart.js — canvas-based, more performant for very large datasets
- **C** Both — Recharts default, Chart.js fallback for ≥5000 data points

**Recommendation:** **A** — single library reduces complexity. Switch to canvas only if specific module hits 10k+ points (very rare in EPCC).

---

#### OQ-1.2 — Gantt library: frappe-gantt vs alternatives?

**Question:** Lock frappe-gantt for Gantt charts?

**Options:**
- **A** frappe-gantt — MIT, ~50 KB, drag-resize, mature
- **B** dhtmlx-gantt — feature-rich but commercial license complications
- **C** Build custom Gantt in Recharts — more control, more work
- **D** react-gantt-task — React-native, smaller community

**Recommendation:** **A** — frappe-gantt is the cleanest fit. License-clean, lightweight, exactly the features needed.

---

#### OQ-1.3 — Network/DAG library: react-flow vs alternatives?

**Question:** Lock react-flow for critical path + dependency graphs?

**Options:**
- **A** react-flow — MIT, industry-standard, drag/zoom/pan native
- **B** Cytoscape.js — more analytical features but harder to style
- **C** D3 force layout — full control, heavy maintenance
- **D** Defer — declare network charts as v2 feature

**Recommendation:** **A** — react-flow ships with everything we need. Used by major SaaS products (Stripe, Vercel).

---

#### OQ-1.4 — Empty/Loading/Error states: X9 ships components or per-module?

**Question:** Should X9 ship reusable React components for empty, loading, error states?

**Options:**
- **A** X9 ships `<EmptyState />`, `<LoadingState />`, `<ErrorState />` as shared components
- **B** Each module implements its own
- **C** X9 specifies the design; modules implement consistently

**Recommendation:** **A** — concrete components prevent drift. Living spec.

---

#### OQ-1.5 — Rate display in charts: enforced by component or by API?

**Question:** Where is the role-tiered spike formula applied for chart Y-axis values?

**Options:**
- **A** API serialiser pre-applies (chart receives already-spiked values; consistent with M02 BR-02-008)
- **B** Chart component applies (more chart-specific control; data more flexible)
- **C** Hybrid — API for primary values; component for derived metrics

**Recommendation:** **A** — API serialiser. Defence-in-depth principle from M02 must extend to charts. Single source of truth for spike formula application.

---

#### OQ-1.6 — Colour-blind safe palette: dual-encode or alternative palette?

**Question:** Red/green is core to RAG status; ~5-8% of users have colour vision deficiency. Solution?

**Options:**
- **A** Dual-encode all RAG status (colour + icon/shape) — Green = ✓, Amber = !, Red = ✗
- **B** Use alternative palette (orange-red instead of red, blue-green instead of green) for RAG
- **C** User-configurable in M34 settings (default standard; opt-in colour-blind variant)

**Recommendation:** **A + C** — always dual-encode (universal best practice); offer alternative palette as opt-in.

---

#### OQ-1.7 — Export formats in v1.0?

**Question:** Which export formats does every chart support?

**Options:**
- **A** PNG + CSV + URL share (recommended)
- **B** PNG + PDF + CSV + URL share
- **C** Defer all exports to Phase 2

**Recommendation:** **A** — PNG (visual share), CSV (analysis), URL (collaboration). PDF is heavier, lower priority.

---

#### OQ-1.8 — Real-time updates: polling vs WebSocket?

**Question:** For real-time charts (today's cashflow, latest CPI), how do they update without manual refresh?

**Options:**
- **A** No real-time updates in v1.0 — manual refresh only
- **B** Polling every 30 seconds for "real-time" charts
- **C** WebSocket subscription (more architecture lift)

**Recommendation:** **A — no real-time in v1.0.** "Real-time" in EPCC means "current as-of report_date", not millisecond-fresh. Manual refresh + cache invalidation on report_date change is sufficient. WebSocket is Phase 2+ feature.

---

#### OQ-1.9 — Drill-down navigation: in-place vs new view?

**Question:** When user clicks a data point to drill down, does the chart morph or does the user navigate to a new page?

**Options:**
- **A** Always navigate to new view (URL-driven; browser-back compatible)
- **B** Drill in-place when same chart context (e.g., zoom into year)
- **C** Hybrid — in-place for zoom; navigation for entity drill

**Recommendation:** **C** — zoom = in-place; drilling to underlying entity = new page. Most intuitive.

---

#### OQ-1.10 — Tabular fallback per chart?

**Question:** Should every chart offer "View as table" for accessibility + analysis?

**Options:**
- **A** Yes for all charts (recommended)
- **B** Only for charts ≥ 20 data points
- **C** Defer to Phase 2

**Recommendation:** **A** — accessibility + power-user analysis. Cheap to implement (data is already there).

---

### OQ-2 (Pattern — defaults proposed, you accept/reject)

| # | Question | Default (proposed) |
|---|---|---|
| OQ-2.1 | Chart card padding | **24px (standard)** for most charts; 16px for inline sparklines |
| OQ-2.2 | Default chart height | **300px** (overrideable per module) |
| OQ-2.3 | Chart border | **1px solid #262626 + 4px border-radius** |
| OQ-2.4 | Chart background | **#141414** (matches surface-1) |
| OQ-2.5 | Tooltip behaviour on touch | **Tap = show; second tap = hide; tap outside = hide** |
| OQ-2.6 | Maximum legend items | **8** before "More" expansion |
| OQ-2.7 | Default chart locale | **`en-IN`** (Indian formatting: ₹, lakh/crore notation, DD-MM-YYYY) |
| OQ-2.8 | Currency display | **₹ Cr / ₹ L** for amounts ≥ ₹1L; **₹** for amounts < ₹1L |
| OQ-2.9 | Date format on charts | **DD MMM YYYY** for axes; **DD MMM** for tight axes |
| OQ-2.10 | Number formatting | **Indian comma grouping** (1,00,00,000) |
| OQ-2.11 | Empty-state illustration | **Subtle icon + helper text** (not whimsical illustration) |
| OQ-2.12 | Chart title casing | **Sentence case** (not Title Case) for clarity |

---

## 15. DELIVERABLES

This brief produces (Round 13). Locked items move to spec (Round 14):

| Round | Artefact | Description |
|---|---|---|
| 13 (this) | `X9_VisualisationStandards_Brief_v0_1.md` | This file. Surfaces decisions. |
| 14 | `X9_VisualisationStandards_Spec_v0_1.md` | Locks library choices, design tokens, component contracts. **Living document.** |
| (parallel) | Component library scaffold | `<EPCCChart />`, `<KPITile />`, `<EmptyState />`, `<LoadingState />`, `<ErrorState />`, `<ChartTooltip />`, `<ChartLegend />` — implemented when first module needs them (Round 17 M03 wireframes) |

---

## 16. RISKS / NOTES

| Risk | Mitigation |
|---|---|
| Recharts may not handle very large datasets (≥10K) | Document fallback: aggregate at backend, or switch to canvas-based renderer when needed |
| frappe-gantt is in maintenance mode (less active than dhtmlx) | Lock current version; revisit annually; alternative is to build custom in react-flow |
| react-flow has learning curve | Develop reusable components and patterns once, reuse across M03 critical path + M11 dependency map |
| Role-tiered chart Y-axis enforcement is novel | Reference architecture: API pre-applies formula; chart component is dumb renderer |
| Mobile (PF01) constraints not yet specified | Defer mobile-specific chart wireframes to PF01 Round; X9 establishes principles |
| Bundle weight may grow with Recharts + frappe-gantt + react-flow | Lazy-load Gantt + network on first use; primary bundle stays light |
| KDMC workbook charts not used as reference | **Confirmed by user — reference only, no parity required.** This actually strengthens X9. |

---

## 17. APPROVAL GATE

To proceed to Spec writing (Round 14), resolve:

```
OQ-1.1   Primary library:           A / B / C        (reco: A — Recharts)
OQ-1.2   Gantt library:             A / B / C / D    (reco: A — frappe-gantt)
OQ-1.3   Network library:           A / B / C / D    (reco: A — react-flow)
OQ-1.4   Empty/Loading/Error:       A / B / C        (reco: A — X9 ships components)
OQ-1.5   Rate display location:     A / B / C        (reco: A — API serialiser)
OQ-1.6   Colour-blind palette:      A / B / C        (reco: A+C — dual-encode + opt-in alt)
OQ-1.7   Export formats v1.0:       A / B / C        (reco: A — PNG + CSV + URL)
OQ-1.8   Real-time updates:         A / B / C        (reco: A — no real-time v1.0)
OQ-1.9   Drill-down nav:            A / B / C        (reco: C — hybrid)
OQ-1.10  Tabular fallback:          A / B / C        (reco: A — yes for all)

OQ-2 defaults: ACCEPT ALL / REJECT [list IDs] / MODIFY [specify]
```

---

## SHORTCUT REPLY

If you accept all my recommendations + OQ-2 defaults:

```
Use all your recommendations + ACCEPT OQ-2 defaults + GO Round 14
```

---

*v0.1 — Brief locked. Awaiting OQ resolutions to proceed to X9 Spec.*
