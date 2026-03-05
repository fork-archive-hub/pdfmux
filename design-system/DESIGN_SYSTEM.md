# pdfmux Design System

> Canonical source of truth for all visual, typographic, and interaction rules.
> Every rule in this document is machine-enforceable. If it's not lintable, it's not contractual.

---

## Color Tokens

All colors are defined as CSS custom properties in `:root`. **Never use raw hex, rgb, or hsl values outside `:root`.**

### Core Palette (Light — default)

| Token | Value | Usage |
|-------|-------|-------|
| `--bg` | `#ffffff` | Page background |
| `--fg` | `#1a1a1a` | Primary text |
| `--dim` | `#6b6b6b` | Secondary text, descriptions |
| `--muted` | `#999999` | Tertiary text, hints, placeholders |
| `--accent` | `#4f46e5` | Primary brand (indigo). Links, buttons, highlights. |
| `--accent-light` | `#eef2ff` | Accent tint for backgrounds |
| `--code-bg` | `#fafafa` | Code block backgrounds |
| `--border` | `#e5e5e5` | Borders, dividers |

### Core Palette (Dark — `[data-theme="dark"]`)

| Token | Value | Usage |
|-------|-------|-------|
| `--bg` | `#0f0f0f` | Page background |
| `--fg` | `#e5e5e5` | Primary text |
| `--dim` | `#a0a0a0` | Secondary text |
| `--muted` | `#666666` | Tertiary text |
| `--accent` | `#818cf8` | Lighter indigo for dark backgrounds |
| `--accent-light` | `#1e1b4b` | Accent tint for dark backgrounds |
| `--code-bg` | `#1a1a1a` | Code block backgrounds |
| `--border` | `#2a2a2a` | Borders, dividers |

### Semantic Colors

| Token | Light Value | Dark Value | Usage |
|-------|------------|------------|-------|
| `--green` | `#059669` | `#4ade80` | Success, "good" states, free tags |
| `--green-light` | `#ecfdf5` | `#052e16` | Green tint backgrounds |
| `--blue` | `#2563eb` | `#60a5fa` | Info, function names in code |
| `--blue-light` | `#eff6ff` | `#172554` | Blue tint backgrounds |
| `--orange` | `#d97706` | `#fbbf24` | Warnings, "fix" states, API tags |
| `--orange-light` | `#fffbeb` | `#451a03` | Orange tint backgrounds |
| `--purple` | `#7c3aed` | `#a78bfa` | Keywords in code |
| `--purple-light` | `#f5f3ff` | `#2e1065` | Purple tint backgrounds |
| `--rose` | `#e11d48` | `#fb7185` | Errors, destructive actions |
| `--rose-light` | `#fff1f2` | `#4c0519` | Rose tint backgrounds |

### Shadows

| Token | Light Value | Dark Value |
|-------|------------|------------|
| `--shadow-sm` | `0 1px 2px rgba(0,0,0,0.05)` | `0 1px 2px rgba(0,0,0,0.3)` |
| `--shadow-md` | `0 4px 6px rgba(0,0,0,0.07)` | `0 4px 6px rgba(0,0,0,0.4)` |
| `--shadow-lg` | `0 10px 15px rgba(0,0,0,0.1)` | `0 10px 15px rgba(0,0,0,0.5)` |

### Color Rules

1. **All color references in CSS must use `var(--token-name)`**. Never write `color: #4f46e5` — write `color: var(--accent)`.
2. **`:root` and `[data-theme="dark"]` are the only places raw hex values appear.** Any hex/rgb/hsl outside these is a violation.
3. **Each semantic color has a light tint variant.** Use the `-light` variant for backgrounds, use the base for text/borders.
4. **Accent hover state is `#4338ca` (light) / `#6366f1` (dark).** Defined on `.btn-primary:hover`.
5. **Dark mode is activated by `[data-theme="dark"]` on `<html>`.** Also respect `prefers-color-scheme: dark` as default when no preference is saved.

---

## Typography

### Font Stacks

| Token | Value | Usage |
|-------|-------|-------|
| `--font` | `-apple-system, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif` | All UI text |
| `--mono` | `'SF Mono', 'Fira Code', 'JetBrains Mono', 'Cascadia Code', Menlo, monospace` | Code blocks, inline code |

### Type Scale

| Element | Size | Weight | Letter-spacing | Line-height |
|---------|------|--------|---------------|-------------|
| Body | `16px` | 400 | normal | `1.7` |
| Hero h1 | `44px` (mobile: `32px`) | 600 | `-1.2px` | `1.2` |
| Hero subtitle | `18px` | 400 | normal | `1.6` |
| Section overline | `11px` | 500 | `1px` | normal |
| Section h2 | `20px` | 600 | `-0.3px` | `1.3` |
| Sub-heading h3 | `18px` | 500 | normal | `1.4` |
| Feature title | `14px` | 600 | normal | normal |
| Feature desc | `14px` | 400 | normal | `1.5` |
| Code blocks | `13px` | 400 | normal | `1.8` |
| Code header | `12px` | 400 | normal | normal |
| Nav links | `14px` | 400 | normal | normal |
| Logo | `17px` | 700 | `-0.3px` | normal |
| Footer | `13px` | 400 | normal | normal |
| Tags | `11px` | 500 | normal | normal |
| Table header | `12px` | 500 | `0.5px` | normal |
| Table body | `14px` | 400 | normal | normal |
| Social proof | `14px` | 500 | normal | normal |

### Typography Rules

1. **Section headings (h2) use `var(--fg)` color** with a small accent overline label above.
2. **Section overlines are `var(--accent)`, 11px, uppercase**, placed above h2 via `data-label` attribute.
3. **Never set `font-family` inline.** Always use `var(--font)` or `var(--mono)`.
4. **No font sizes outside the type scale above.** If you need a new size, add it to this table first.

---

## Spacing

### Layout Constants

| Property | Value | Usage |
|----------|-------|-------|
| Max width | `720px` | Container, nav, footer |
| Container padding | `0 28px 80px` (mobile: `0 20px 60px`) | Horizontal page margins |
| Nav padding | `24px 28px` (mobile: `20px 20px`) | Top bar |
| Section margin-bottom | `56px` | Between major sections |
| Hero padding | `56px 0 48px` | Above/below hero |

### Component Spacing

| Token / Pattern | Value | Usage |
|----------------|-------|-------|
| Small gap | `6px` | Button icon gap, overline margin-bottom |
| Medium gap | `12px` | Grid gap, hero p margin |
| Large gap | `16px` | Nav link gap, h2 margin-bottom, CTA gap, feature grid gap |
| XL gap | `20px` | Footer link gap, card padding |
| XXL gap | `24px` | Card padding, nav padding, code block padding |
| Section gap | `56px` | Between sections |

### Border Radius

| Size | Value | Usage |
|------|-------|-------|
| Small | `4px` | Tags (`.tag-free`, `.tag-api`) |
| Default | `8px` | Buttons |
| Large | `10px` | Cards, code blocks, install box |

### Spacing Rules

1. **Spacing values must come from the scale above.** No arbitrary pixel values.
2. **Max-width is always `720px`** for the main content track.
3. **Border-radius is always `4px`, `8px`, or `10px`.** No other values.

---

## Components

### Buttons

| Variant | Background | Text | Border | Padding | Radius |
|---------|-----------|------|--------|---------|--------|
| Primary | `var(--accent)` | `#fff` | none | `10px 22px` | `8px` |
| Secondary | transparent | `var(--dim)` | `1px solid var(--border)` | `10px 20px` | `8px` |

- Primary hover: `background: #4338ca` (light) / `#6366f1` (dark)
- Secondary hover: `border-color: var(--accent); color: var(--accent)`
- All buttons use `font-size: 14px; font-weight: 500`
- Buttons use `display: inline-flex; align-items: center; gap: 6px`

### Cards (`.feature`)

- Border: `1px solid var(--border)`
- Radius: `10px`
- Padding: `20px`
- Hover: `border-color: var(--dim); transform: translateY(-1px)`
- Each card has a unique background tint from the semantic color palette

### Code Blocks

Wrapped in `.code-block` container:

```html
<div class="code-block">
  <div class="code-header">
    <span class="code-lang">python</span>
    <button class="code-copy">copy</button>
  </div>
  <pre>...</pre>
</div>
```

- Background: `var(--code-bg)`
- Border: `1px solid var(--border)`
- Radius: `10px`
- Header: `padding: 10px 24px`, `border-bottom: 1px solid var(--border)`
- Code area: `padding: 20px 24px`
- Font: `var(--mono)` at `13px`, line-height `1.8`
- Copy button: `font-size: 12px`, `color: var(--muted)`, hover `var(--fg)`
- Language label: `font-size: 12px`, `color: var(--muted)`
- Syntax classes: `.c` (comments, muted), `.k` (keywords, purple), `.f` (functions, blue), `.s` (strings, green), `.o` (operators, orange)

### Install Box

- Same as code block styling but with `cursor: pointer`
- Hover: accent border + `box-shadow: 0 0 0 3px var(--accent-light)`
- Contains `<code>` + copy hint

### Tags

| Variant | Background | Text Color |
|---------|-----------|-----------|
| `.tag-free` | `var(--tag-free-bg)` | `var(--green)` |
| `.tag-api` | `var(--tag-api-bg)` | `var(--orange)` |

### Pipeline Block

- Left border: `3px solid var(--accent)`
- Background: `linear-gradient(135deg, var(--accent-light) 0%, var(--bg) 60%)`
- Step labels: `font-weight: 600`
- `.good` spans: `var(--green)`
- `.fix` spans: `var(--orange)`

### Social Proof Bar

- `display: flex`, `gap: 24px`, centered
- `font-size: 14px`, `font-weight: 500`, `color: var(--dim)`
- Separator: `·` between items or thin border
- Placed immediately after install box

---

## Icons

- **Feature icons must be inline SVG**, not emoji. Emoji renders differently across OS.
- Size: `24×24` viewBox, `stroke-based`, using `currentColor` or `var(--dim)`
- Stroke width: `1.5px`
- No filled icons unless specifically needed.

---

## Interactions

### Transitions

All interactive elements use `transition: <property> 0.15s`. Properties:

- `color` — links, text hover states
- `background` — buttons
- `border-color` — cards, inputs
- `box-shadow` — install box focus ring
- `transform` — card hover lift

**Rule**: `0.15s` is the only transition duration. No other values.

### Focus States (Accessibility)

```css
a:focus-visible,
button:focus-visible,
.install-box:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
```

- Use `:focus-visible` (not `:focus`) — visible only on keyboard navigation.
- **Every element with a `:hover` state MUST also have a `:focus-visible` state.**
- Minimum contrast ratios: 4.5:1 for body text, 3:1 for large text (WCAG AA).

---

## Dark Mode

- Activated by `data-theme="dark"` on `<html>` element.
- Default: respect `prefers-color-scheme: dark` media query.
- User toggle: saves to `localStorage('theme')`.
- Toggle priority: `localStorage` > `prefers-color-scheme` > light default.
- Toggle UI: sun/moon SVG icon in nav bar.

---

## Responsive Breakpoint

Single breakpoint at `max-width: 560px`.

Changes at mobile:
- Hero h1: `44px` → `32px`
- Features grid: `1fr 1fr` → `1fr`
- Hero CTAs: row → column
- Footer: row → column with `16px` gap
- Container padding: `28px` → `20px`
- Nav padding: `24px 28px` → `20px 20px`

**Rule**: only one breakpoint. If you need another, add it to this document first.

---

## Content Hierarchy

Sections appear in this order on the page:

```
1. Nav
2. Hero (title, subtitle, CTAs)
3. Install box
4. Social proof bar
5. How it works (the differentiator)
6. Python API
7. CLI
8. Features grid
9. Extractors table
10. MCP server
11. Optional extras
12. Footer
```

**Rule**: "How it works" must appear before code examples. It explains WHY before showing HOW.

---

## Anti-patterns (Never Do This)

1. **Raw hex colors** — `color: #4f46e5` → `color: var(--accent)`
2. **Inline font-family** — `font-family: Arial` → `font-family: var(--font)`
3. **Arbitrary spacing** — `margin: 37px` → use a value from the spacing scale
4. **Arbitrary radius** — `border-radius: 6px` → use `4px`, `8px`, or `10px`
5. **Non-0.15s transitions** — `transition: all 0.3s` → `transition: color 0.15s`
6. **`!important`** — never. If specificity is wrong, fix the selector.
7. **External stylesheets** — the site is a single self-contained HTML file. No external CSS.
8. **External JS libraries** — no jQuery, no frameworks. Vanilla JS only.
9. **Width > 720px** — content must not exceed the max-width track.
10. **Emoji icons in feature cards** — use inline SVG with `currentColor`.
11. **`:hover` without `:focus-visible`** — every hover needs a keyboard equivalent.

---

## Machine Enforcement

The following commands enforce these rules automatically:

| Command | What It Checks |
|---------|---------------|
| `python3 design-system/lint.py site/` | All design system rules on HTML/CSS files |

### Pre-commit

Design system lint runs on every commit via `.git/hooks/pre-commit`. Staged HTML/CSS files in `site/` are checked automatically.

### CI

GitHub Actions runs `python3 design-system/lint.py site/` on every PR that touches `site/**`. Failures block merge.

### Enforcement Layers

```
Layer 1: This document (DESIGN_SYSTEM.md)     — canonical rules
Layer 2: design-system/SKILL.md               — agent routing
Layer 3: design-system/lint.py                 — local lint
Layer 4: .git/hooks/pre-commit                 — staged-file check
Layer 5: .github/workflows/design-system.yml   — CI gate
```
