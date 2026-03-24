# Annotate

Leave thorough, structured notes in every file you modify. This skill defines the exact
format for file changelog blocks and inline section notes across HTML, CSS, and JS.

## When to Apply

Apply this format whenever you:
- Modify, add, or remove any HTML element, CSS rule, or JS statement
- Finish a task and are about to report completion
- Are invoked with `/annotate` to retroactively document prior changes

You do **not** need to be explicitly called with `/annotate` — treat annotation as part of
completing any edit. However, `/annotate` alone will retroactively annotate recently
changed files, and `/annotate {filename}` will annotate a specific file.

---

## Format: File Changelog Block

Every file you touch must have a changelog block. Entries are **append-only** — never
modify or delete existing entries. When adding a new entry, insert it above the `╚╝`
footer row using a `╠═╣` divider.

### HTML files
Place immediately after `<!DOCTYPE html>`, before `<html>`:

```html
<!--
╔══════════════════════════════════════════════════════════════╗
║  FILE  {filename}                                            ║
║  CHANGELOG                                                   ║
╠══════════════════════════════════════════════════════════════╣
║  {YYYY-MM-DD}  Claude  {Summary of change, ≤ 50 chars}      ║
║                  ↳ {Why: requirement, decision, or reason}   ║
╚══════════════════════════════════════════════════════════════╝
-->
```

Multiple entries use stacked `╠═╣` dividers (newest entry on top):

```html
<!--
╔══════════════════════════════════════════════════════════════╗
║  FILE  index.html                                            ║
║  CHANGELOG                                                   ║
╠══════════════════════════════════════════════════════════════╣
║  2026-03-24  Claude  Added contact CTA to hero section       ║
║                ↳ Increase lead-gen touchpoints on landing    ║
╠══════════════════════════════════════════════════════════════╣
║  2026-03-20  Claude  Reduced blob opacity on mobile          ║
║                ↳ Content legibility at narrow viewport       ║
╚══════════════════════════════════════════════════════════════╝
-->
```

### Inline `<style>` blocks
Place at the top of the `<style>` tag, before any CSS rules:

```css
/*
 * ╔══════════════════════════════════════════════════════════╗
 * ║  BLOCK  <style> in {filename}                            ║
 * ║  CHANGELOG                                               ║
 * ╠══════════════════════════════════════════════════════════╣
 * ║  {YYYY-MM-DD}  Claude  {Summary}                         ║
 * ║                  ↳ {Reason}                              ║
 * ╚══════════════════════════════════════════════════════════╝
 */
```

### Inline `<script>` blocks
Place at the top of the `<script>` tag, before any JS statements:

```js
/*
 * ╔══════════════════════════════════════════════════════════╗
 * ║  BLOCK  <script> in {filename}                           ║
 * ║  CHANGELOG                                               ║
 * ╠══════════════════════════════════════════════════════════╣
 * ║  {YYYY-MM-DD}  Claude  {Summary}                         ║
 * ║                  ↳ {Reason}                              ║
 * ╚══════════════════════════════════════════════════════════╝
 */
```

### Standalone `.css` or `.js` files
Place at the very top of the file:

```css
/*
 * ╔══════════════════════════════════════════════════════════╗
 * ║  FILE  {filename}                                        ║
 * ║  CHANGELOG                                               ║
 * ╠══════════════════════════════════════════════════════════╣
 * ║  {YYYY-MM-DD}  Claude  {Summary}                         ║
 * ║                  ↳ {Reason}                              ║
 * ╚══════════════════════════════════════════════════════════╝
 */
```

---

## Format: Inline Section Notes

Place an inline section note immediately **above** the changed code region. These notes
are permanent — do not remove them unless the associated code is deleted.

Use the lighter `──` rule style (not the `╔╗` box — that's changelog-only).

### HTML
```html
<!-- ── CHANGE · {section label} ──────────────────────────────
     {What changed and why. Be specific enough that a developer
     reading cold understands the intent and the decision made.}
     ──────────────────────────────────────────────────────── -->
```

### CSS
```css
/* ── CHANGE · {section label} ──────────────────────────────
   {What changed and why.}
   ──────────────────────────────────────────────────────── */
```

### JS
```js
// ── CHANGE · {section label} ─────────────────────────────────
// {What changed and why. Use multiple // lines for longer notes.}
// ─────────────────────────────────────────────────────────────
```

**Section label** should match the nearest meaningful identifier: a CSS class name
(`.blob`), an HTML role/description (`hero CTA`), or a JS function name (`tick()`).

---

## Rules

1. **Date** — always use today's real date in `YYYY-MM-DD`. Never use placeholders.
2. **Summary length** — keep changelog summary lines ≤ 55 characters so they fit the box.
3. **↳ reason is mandatory** — never leave just the summary line. Always explain the why.
4. **Changelog is append-only** — never edit or remove existing entries.
5. **Inline notes are permanent** — remove only if the associated code is deleted.
6. **Box width** — 64 characters total (including outer `║`). Pad shorter lines with spaces.
7. **No nested boxes** — inline section notes always use `──` rule style, never `╔╗`.
8. **One block per scope** — one changelog block per file (HTML) or per `<style>`/`<script>`
   block. Do not create multiple changelog blocks in the same file or block.

---

## Examples

### HTML inline note
```html
<!-- ── CHANGE · hero CTA ─────────────────────────────────────
     Added secondary "Contact us" anchor alongside "Our services".
     Positioned as a row below the primary button to preserve
     visual hierarchy while increasing lead-gen touchpoints.
     ──────────────────────────────────────────────────────── -->
<div class="hero-ctas">
  <a href="services.html">Our services</a>
  <a href="mailto:hi@doublenines.co">Contact us</a>
</div>
```

### CSS inline note
```css
/* ── CHANGE · .blob ─────────────────────────────────────────
   Reduced opacity from 0.9 to 0.6 on narrow viewports.
   Content legibility was poor on mobile when blob was opaque.
   ──────────────────────────────────────────────────────── */
@media (max-width: 600px) {
  .blob { opacity: 0.6; }
}
```

### JS inline note
```js
// ── CHANGE · tick() ──────────────────────────────────────────
// Extracted interval init to module scope. Previously it was
// inside tick(), causing duplicate intervals when CTA was clicked.
// ─────────────────────────────────────────────────────────────
function tick() {
  // ...
}
```
