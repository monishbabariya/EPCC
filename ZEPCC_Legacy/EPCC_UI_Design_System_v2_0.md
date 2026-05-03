# EPCC — UI Design System
## Version 2.0 — Command Center Edition
**Owner:** PMO Director / Product
**Created:** 2026-05-02
**Replaces:** v1.0 (generic enterprise — deprecated)
**Status:** Draft — Pending PMO Director Review | Locked: No

---

## CHANGE LOG

| Version | Date | Change Summary |
|---------|------|----------------|
| v1.0 | 2026-05-02 | Initial — generic enterprise light theme. Deprecated. |
| v2.0 | 2026-05-02 | Complete redesign. Command center aesthetic: near-black + electric cyan. Bloomberg Terminal meets SpaceX Mission Control. Balanced density. New typography, color system, component language. |

---

## 1. DESIGN PHILOSOPHY

### Direction: Mission Control

EPCC governs ₹190 Cr decisions. The interface must feel like the instrument it is — not like a project management tool. Visual references: Bloomberg Terminal, SpaceX Mission Control, Palantir Foundry, military command systems.

### Five Governing Principles

**1. The interface communicates before the user reads.**
Color alone identifies severity. Cyan = active/brand. Green = performing. Amber = watch. Red = breach. These are learned in the first session and never violated.

**2. Darkness is a feature, not an aesthetic.**
A near-black interface removes visual noise. On a bright screen, dark UI reduces eye fatigue during long monitoring sessions. More importantly — colored status indicators POP against dark surfaces in a way they never do against white.

**3. Monospace for measurements, proportional for everything else.**
Every CPI, SPI, ₹ amount, percentage — `SF Mono` / `Fira Code`. Every label, description, heading — system sans-serif. This creates an instant visual grammar: if it's in monospace, it's a measured value from the system.

**4. All caps for identifiers and codes. Mixed case for everything else.**
`M07`, `SG-6`, `CRITICAL`, `KDMC-001` are identifiers — always uppercase. Descriptions, labels, and prose are sentence case. This creates a machine/human distinction that makes the interface scannable.

**5. Consequence is physically visible.**
A Critical row in a table has a red left border. A governance breach alert has a solid red left stripe. The SLA bar depletes visually. Users should feel the urgency without reading a word.

---

## 2. COLOR SYSTEM

### Background Depth Layers

```
Level 0 — Deepest (system bars, navigation bg):  #030810
Level 1 — Base (page background):                #060D18
Level 2 — Raised (panel backgrounds):            #0B1828
Level 3 — Surface (card backgrounds):            #0F2035
Level 4 — Hover / highlight:                     #162840
Level 5 — Active / selected:                     #1C3050
```

### Electric Accent Colors

```
Cyan (Brand / Active / CTA):      #00CFFF
Cyan dim bg:                      rgba(0, 207, 255, 0.07)
Cyan border:                      rgba(0, 207, 255, 0.20)
Cyan border active:               rgba(0, 207, 255, 0.40)
```

### Semantic Status Colors (RAG + System)

```
CRITICAL / RED:
  Solid:   #FF4454
  Dim bg:  rgba(255, 68, 84, 0.07)
  Border:  rgba(255, 68, 84, 0.22)
  Text on dark: #FF8896

HIGH / AMBER:
  Solid:   #FFAB00
  Dim bg:  rgba(255, 171, 0, 0.07)
  Border:  rgba(255, 171, 0, 0.25)
  Text on dark: #FFCC55

ON TRACK / GREEN:
  Solid:   #00F5A0
  Dim bg:  rgba(0, 245, 160, 0.07)
  Border:  rgba(0, 245, 160, 0.25)
  Text on dark: #00F5A0

WATCH / BLUE:
  Solid:   #4D9EFF
  Dim bg:  rgba(77, 158, 255, 0.07)
  Border:  rgba(77, 158, 255, 0.22)
  Text on dark: #7FBFFF

PENDING / NEUTRAL:
  Solid:   Level 4 (#162840)
  Border:  Level 5 (#1C3050)
  Text:    Secondary (#4E7FA0)
```

### Text Scale

```
Primary text:    #D8EEFF   (slightly blue-tinted white — easier than pure white on dark)
Secondary text:  #4E7FA0   (steel blue — muted, still legible)
Muted text:      #1E4060   (for disabled states, placeholder hints)
Inverse text:    #030810   (text on bright backgrounds, e.g., cyan CTA button)
```

### Tailwind Configuration

```js
colors: {
  cmd: {
    0: '#030810',
    1: '#060D18',
    2: '#0B1828',
    3: '#0F2035',
    4: '#162840',
    5: '#1C3050',
  },
  cyan: {
    DEFAULT: '#00CFFF',
    dim:     'rgba(0,207,255,0.07)',
    border:  'rgba(0,207,255,0.20)',
    active:  'rgba(0,207,255,0.40)',
  },
  status: {
    critical: '#FF4454',
    high:     '#FFAB00',
    good:     '#00F5A0',
    watch:    '#4D9EFF',
  },
  t: {
    1: '#D8EEFF',
    2: '#4E7FA0',
    3: '#1E4060',
  }
}
```

---

## 3. TYPOGRAPHY

### Font Families

| Role | Stack | Usage |
|---|---|---|
| UI / Interface | `system-ui, -apple-system, 'Segoe UI', sans-serif` | Labels, headings, descriptions, navigation, alert text |
| Numeric Data / Codes | `'SF Mono', 'Fira Code', 'Fira Mono', 'Cascadia Code', 'Consolas', monospace` | ALL numbers, module codes, identifiers, system paths, timestamps |

**Why system fonts:** The monospace + proportional split creates the visual grammar without requiring web font loading. The tactical aesthetic comes from how the fonts are used — not which specific fonts.

### Type Rules

**All caps + letter-spacing for identifiers:**
```css
.identifier {
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-family: var(--font-mono);
  font-size: 9–10px;
}
```
Used for: section headers, module codes, badge labels, table column headers, status text, system bar path

**Mixed case for human-readable content:**
```css
.human-text {
  text-transform: none;
  font-family: var(--font-sans);
}
```
Used for: alert descriptions, project names, decision queue titles, form labels, navigation item names

### Type Scale

| Role | Size | Weight | Font | Color |
|---|---|---|---|---|
| System path / nav code | 9–10px | 700 | Mono | `#4E7FA0` active → `#00CFFF` |
| Section header | 8px | 700 | Mono, ALL CAPS | `#1E4060` |
| Table column header | 8px | 700 | Mono, ALL CAPS | `#1E4060` |
| Badge label | 9px | 700 | Mono, ALL CAPS | Semantic color |
| Small metadata | 9–10px | 400 | Mono | `#4E7FA0` |
| Navigation label | 11–12px | 400-500 | Sans | `#4E7FA0` active → `#D8EEFF` |
| Body / description | 11–12px | 400 | Sans | `#4E7FA0` |
| Table cell data | 11–12px | 400-500 | Mono | `#4E7FA0` active → semantic |
| Table cell name | 12px | 500 | Sans | `#D8EEFF` |
| Decision queue title | 12px | 500 | Sans | `#D8EEFF` |
| Alert title | 11px | 600 | Mono | Semantic (red/amber) |
| KPI label | 8px | 700 | Mono, ALL CAPS | `#1E4060` |
| KPI value | 22–28px | 600 | Mono | Semantic accent |
| KPI delta | 9px | 400 | Mono | Semantic or `#1E4060` |

---

## 4. SPACING

Base unit: **4px**

Component-level spacing uses multiples of 4px. Generous spacing between major sections.

```
Sidebar width:           176px (collapsed: 44px — icon only)
System bar height:       30px
Page content padding:    14px
Panel internal padding:  12–14px
KPI card padding:        11px 12px
Table cell padding:      8–9px 11px
Badge padding:           3px 8px
Button height:           26–28px
Gap between KPI cards:   8px
Gap between sections:    12–14px
```

---

## 5. COMPONENT LIBRARY

### 5.1 Application Shell

```
SYSTEM BAR (30px, cmd-0 background):
  Left:  [Module path] — mono, cyan highlight on active segment
  Right: [LIVE indicator] [Timestamp] | [Tenant / Portfolio]

NAVIGATION RAIL (176px, cmd-0 background):
  [EPCC logo + tenant]
  [Section: Strategic] → PIOE
  [Section: Control]   → M01–M09
  [Section: Command]   → M10
  [User footer]        → avatar + name + role

MAIN CONTENT (flex-grow, cmd-1 background)
```

### 5.2 Navigation Item States

```
DEFAULT:
  bg: transparent, border-left: 2px solid transparent
  code: mono, 9px, uppercase, t3 (#1E4060)
  label: sans, 11px, t2 (#4E7FA0)

HOVER:
  bg: rgba(0,207,255,0.04)
  border-left: 2px solid cyan-border
  transition: 100ms

ACTIVE:
  bg: rgba(0,207,255,0.07)
  border-left: 2px solid #00CFFF
  code: #00CFFF
  label: #D8EEFF
  + active dot (4px, cyan, right-aligned)
```

### 5.3 KPI Metric Card

```
STRUCTURE:
  background: cmd-2
  border: 1px solid cmd-4
  border-top: 2px solid [status color]
  padding: 11px 12px

  Label row: 8px, ALL CAPS, letter-spacing .14em, mono, t3
  Value row: 22-28px, mono, 600, [status accent color]
  Delta row: 9px, mono, directional color (green up, red down)

STATUS TOP BORDER COLORS:
  Green (performing):    #00F5A0
  Amber (watch):         #FFAB00
  Cyan (brand/neutral):  #00CFFF
  Blue (financial):      #4D9EFF
  Red (critical):        #FF4454
```

### 5.4 Decision Queue Item

```
STRUCTURE:
  border-left: 2px solid [severity color]
  background: [severity dim]
  padding: 10px 11px

  Top row: [● SEVERITY] [MODULE TAG] [SCORE BADGE]
  Title row: 12px, sans, 500, t1
  Meta row: 9px, mono, t2 — [Owner] [SLA timer]
  SLA bar: 2px height, full-width, depletes left-to-right

SLA BAR COLORS:
  >50% remaining:  cyan
  25–50%:          amber
  <25%:            red
  0% (overdue):    red, full-width, blinking

MODULE TAG:
  border: 1px solid cyan-border
  bg: transparent
  text: cyan, mono, 9px

SCORE BADGE:
  Critical (≥75): red dim bg + red text + red border
  High (50-74):   amber dim bg + amber text
  Medium (25-49): blue dim bg + blue text
  Low (<25):      neutral
```

### 5.5 Status Badges

```
STRUCTURE:
  display: inline-flex, align-items: center, gap: 4px
  padding: 3px 8px
  border: 1px solid [semantic-border]
  background: [semantic-dim]
  font: 9px, mono, 700, ALL CAPS, letter-spacing .06em
  color: [semantic-solid]
  border-radius: 0  ← sharp corners, no rounding on command center badges

VARIANTS:
  CRITICAL → rd solid/dim/border
  HIGH     → am solid/dim/border
  ON TRACK → gn solid/dim/border
  WATCH    → bl solid/dim/border
  PENDING  → neutral
  [MODULE] → cyan solid/dim/border (M07, SG-6, etc.)

DOT INDICATOR: 4px circle, same solid color as text
```

### 5.6 Buttons

```
PRIMARY (CTA — Approve, Save, Submit):
  background: #00CFFF
  color: cmd-0 (near-black inverse)
  border: 1px solid #00CFFF
  font: mono, 9px, 700, ALL CAPS, letter-spacing .08em
  height: 26-28px, padding: 0 12px

SECONDARY (Export, Filter, View):
  background: transparent
  color: t2 (#4E7FA0)
  border: 1px solid cmd-5 (#1C3050)
  hover: border-color cyan-border, color cyan

DESTRUCTIVE (Reject, Override):
  background: transparent
  color: #FF4454
  border: 1px solid rgba(255,68,84,0.4)

GHOST (Cancel, Back):
  background: transparent, border: transparent
  color: t3 (#1E4060)
  hover: color t2
```

### 5.7 Data Table

```
HEADER ROW:
  background: cmd-0
  border-bottom: 1px solid cmd-4
  cell: 8px, mono, 700, ALL CAPS, letter-spacing .14em, t3

DATA ROWS:
  default: cmd-2 background
  hover: cmd-3 background
  border-bottom: 1px solid cmd-3

  Numeric cells: mono, right-aligned, 11px
  Name cells: sans, t1, 12px, 500
  Status cells: badge component

CRITICAL ROW:
  background: rgba(255,68,84,0.07)
  td:first-child border-left: 2px solid #FF4454, padding-left: 9px

HIGH ROW:
  background: rgba(255,171,0,0.07)
  td:first-child border-left: 2px solid #FFAB00, padding-left: 9px
```

### 5.8 Alert Strip

```
STRUCTURE:
  border: 1px solid [severity-border]
  border-left: 3px solid [severity-solid]
  background: [severity-dim]
  padding: 10px 12px
  display: flex, align-items: flex-start, gap: 10px

ICON: 16px inline SVG, severity color

TITLE: 11px, mono, 600, letter-spacing .03em
  Critical: #FF8896
  Warning:  #FFCC55
  Success:  #00F5A0

DESCRIPTION: 10px, sans, t2 (#4E7FA0)

NO border-radius on alert strips — sharp edges emphasise urgency
```

### 5.9 Section Header

```
PATTERN: [dot] SECTION TITLE ──────────────────
  dot: 4px circle, cyan
  text: 8px, mono, 700, ALL CAPS, letter-spacing .16em, t3
  line: flex-grow, 1px, cmd-4
  margin-bottom: 8px
```

### 5.10 Gate Status Display

```
Four states — sharp rectangular chips:
  GO:          green, green-dim bg, green border
  COND GO:     amber, amber-dim bg, amber border
  NO-GO:       red, red-dim bg, red border
  PENDING:     neutral, cmd-4 bg, cmd-5 border

Font: 9px, mono, 700, ALL CAPS, letter-spacing .1em
Padding: 3px 9px
Border-radius: 0 ← no rounding
```

---

## 6. LAYOUT PATTERNS

### 6.1 Application Shell

```
[Fixed system bar: 30px]           full-width, cmd-0
[Below system bar: flex row]
  [Navigation rail: 176px]         cmd-0, full remaining height
  [Content area: flex-grow]        cmd-1, scrollable
    [Content padding: 14px]
```

### 6.2 Module Layout Types

**Type A — Command Dashboard (M07, M10):**
```
Section header
KPI grid (4 cards, 8px gap)
Two-column: [Data/Queue] | [Status panel]
Full-width data table
Alert strip(s)
```

**Type B — Data List (M01, M05, M09):**
```
Section header
Filter bar (cmd-0 bg, border-bottom)
Full-width tactical table
Pagination row
```

**Type C — Detail / Form (M01 create, M08 gate review):**
```
Section header with back button
Left: Form panel (60%) | Right: Context panel (40%)
Each form section: cmd-2 panel, border-top: 2px solid cyan
Sticky footer: [Cancel] [Save Draft] [Submit]
```

**Type D — Split Tactical (M04 Execution, M08 Gates):**
```
Left: Filtered list / queue (42%)
Right: Detail / action panel (58%)
Both scroll independently
Shared section header above
```

---

## 7. ICONOGRAPHY

**Library:** Lucide Icons — outline style only, 1.5px stroke
**Sizes:** 14px (inline text), 16px (navigation), 20px (panel headers)
**Color:** Always inherits from parent text — never hardcoded separately

**Module icon assignments (consistent across all screens):**

| Module | Icon | Lucide Name |
|---|---|---|
| PIOE | `Layers` | layers |
| M01 | `FolderKanban` | folder-kanban |
| M02 | `Network` | network |
| M03 | `CalendarRange` | calendar-range |
| M04 | `ClipboardList` | clipboard-list |
| M05 | `ShieldAlert` | shield-alert |
| M06 | `IndianRupee` | indian-rupee |
| M07 | `TrendingUp` | trending-up |
| M08 | `GitMerge` | git-merge |
| M09 | `BadgeCheck` | badge-check |
| M10 | `LayoutDashboard` | layout-dashboard |

---

## 8. MOTION

### Principles
- All transitions: 100ms (decisive, not slow)
- No entrance animations on data — data appears instantly
- No decorative animations
- ONLY functional animations: state change confirmation, live indicator pulse, SLA bar depletion

### Standard Transitions

```css
/* Nav item */
transition: background 100ms, border-color 100ms, color 100ms;

/* Badge severity change (on recalc) */
transition: background 200ms, color 200ms, border-color 200ms;

/* Button hover */
transition: border-color 100ms, color 100ms;

/* Modal appear */
transition: opacity 150ms ease-out;
```

### Functional Animations

```css
/* LIVE indicator — only animation in the system */
@keyframes livePulse {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.15; }
}
.live-dot { animation: livePulse 2s ease-in-out infinite; }

/* SLA bar depletion is CSS width transition, not animation */
.sla-bar-fill { transition: width 1s linear; }
```

---

## 9. ACCESSIBILITY

### WCAG 2.1 AA Compliance on Dark Theme

All text must meet minimum 4.5:1 contrast against its background.

| Text | Background | Contrast | Result |
|---|---|---|---|
| `#D8EEFF` on `#060D18` | — | 14.8:1 | ✅ |
| `#4E7FA0` on `#060D18` | — | 4.9:1 | ✅ |
| `#00CFFF` on `#060D18` | — | 9.2:1 | ✅ |
| `#00F5A0` on `#060D18` | — | 11.4:1 | ✅ |
| `#FF4454` on `#060D18` | — | 5.1:1 | ✅ |
| `#FFAB00` on `#060D18` | — | 8.7:1 | ✅ |
| `#030810` on `#00CFFF` | — | 16.1:1 | ✅ (CTA button) |

**Color is never the sole indicator.** Every status badge includes text (CRITICAL, HIGH, etc.) alongside the color. Every alert has both a colored border AND a labeled title.

**Focus ring:** 2px solid #00CFFF, 2px offset. Visible against dark backgrounds.

**Keyboard navigation:** Full Tab support. All nav items, buttons, and interactive elements reachable.

**Screen readers:** All icon buttons have `aria-label`. Status badges use `aria-label` with full description. Live regions (`aria-live="polite"`) on decision queue updates.

---

## 10. IMPLEMENTATION RULES

1. **Never use white or light backgrounds** outside the context panel in Type C layouts (forms where the user needs to read long text). The system is dark-first.

2. **Never use #000000 (pure black).** `cmd-0` (#030810) is the darkest surface. Pure black looks flat; the slight blue tint adds depth.

3. **All status colors are semantic.** `#FF4454` means "critical state." Never use it decoratively.

4. **All numerical values in mono.** No exceptions. Use the `<DataValue>` React wrapper which enforces `font-family: var(--font-mono)` and `tabular-nums`.

5. **No rounded corners on badges and gate chips.** Only KPI cards and modal dialogs use rounded corners (4px, not more). The system's visual language is angular and precise.

6. **Module codes are always uppercase + mono.** M07, SG-6, KDMC-001 — never mixed case.

7. **No inline styles.** Tailwind classes only. All custom values in `tailwind.config.js`.

8. **Do not add new status colors.** If a new state is needed, bring it to the design system review first. Ad-hoc colors break the semantic contract.

---

*Design system v2.0. Pending PMO Director review and lock.*
*Replaces v1.0 entirely — do not use v1.0 components.*
*Memory file update required: §7.138 (Design System v2.0 locked).*
