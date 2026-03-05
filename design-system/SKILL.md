# Design System Skill

> This file routes all design-related tasks to the canonical design system.
> Any agent editing files in `site/` MUST follow these instructions.

---

## When This Skill Activates

This skill applies when you are:
- Editing any file in `site/` (HTML, CSS, JS)
- Creating new UI components or pages
- Modifying colors, typography, spacing, or layout
- Adding new sections to the website
- Responding to design feedback or mockups

## Required Reading

Before making ANY visual change, read:

1. **`design-system/DESIGN_SYSTEM.md`** — the canonical source of truth
2. **`site/index.html`** — the current implementation (single-file site)

## Rules (Non-negotiable)

### Colors
- **NEVER** use raw hex, rgb, or hsl values outside `:root`
- **ALWAYS** reference CSS custom properties: `var(--accent)`, `var(--dim)`, etc.
- If you need a new color, add it to `:root` AND to `DESIGN_SYSTEM.md` first

### Typography
- **NEVER** set `font-family` directly — use `var(--font)` or `var(--mono)`
- **NEVER** invent new font sizes — use sizes from the type scale in `DESIGN_SYSTEM.md`
- Section headings (`h2`) are always `13px`, uppercase, `var(--accent)` color

### Spacing
- **NEVER** use arbitrary pixel values for margin/padding
- Use values from the spacing scale: `6px`, `12px`, `16px`, `20px`, `24px`, `56px`
- Border-radius is `4px`, `8px`, or `10px` — no other values
- Max content width is always `720px`

### Transitions
- All transitions use `0.15s` duration — no other values
- Specify individual properties, never `transition: all`

### Architecture
- The site is a single self-contained HTML file with embedded CSS and JS
- No external stylesheets, no external JS libraries, no frameworks
- No build step — the HTML file IS the site

### Component Patterns
- Buttons follow the Primary/Secondary pattern in `DESIGN_SYSTEM.md`
- Cards use `10px` radius, `20px` padding, `1px solid var(--border)`
- Code blocks use `var(--code-bg)` background, `var(--mono)` font, `10px` radius

## Workflow

1. Read `DESIGN_SYSTEM.md` for the rule that applies
2. Make your change using design tokens (CSS custom properties)
3. Run `python design-system/lint.py site/` to verify compliance
4. Fix any violations before committing
5. If you need a new token/pattern, update `DESIGN_SYSTEM.md` first, then implement

## What NOT To Do

- Do NOT add external CSS files or `<link>` tags
- Do NOT add `<script src="...">` for external JS
- Do NOT use `!important`
- Do NOT add new breakpoints without updating `DESIGN_SYSTEM.md`
- Do NOT use colors, sizes, or radii not documented in `DESIGN_SYSTEM.md`
- Do NOT skip running the lint after changes
