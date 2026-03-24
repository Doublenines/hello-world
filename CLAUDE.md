# Claude Code — Project Guidelines

## Annotation Policy

After every file edit, apply the annotation format defined in `.claude/commands/annotate.md`:

- Add or update the **changelog block** at the top of each modified file (or at the top of the modified `<style>`/`<script>` block for inline code)
- Add an **inline section note** immediately above each changed code region

Do this as part of completing the edit — not as a separate follow-up step.
Use `/annotate` or `/annotate {filename}` to apply notes retroactively if this was missed.
