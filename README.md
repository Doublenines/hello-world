# Double Nines — Hello World

Minimalist marketing site for [Double Nines](https://doublenines.co), a digital product design and build studio.

## Pages

### `index.html` — Landing page
The main entry point. Features the animated gradient blob background, live clock, and a compact hero with a CTA that links to the services page.

### `services.html` — Services page
Accessible from the "Our services" CTA on the landing page. Lists what Double Nines offers across six categories:
- Strategy & Research
- Product Design
- Software Development
- eCommerce
- DevOps & QA
- Brand & Visual Design

Same design language as the landing page — Helvetica, #111 on white, blob animation (at reduced opacity to let content breathe), live clock in the header.

## Design notes

- No frameworks or build tools — plain HTML/CSS/JS
- Self-contained single files (styles and scripts inline)
- Responsive down to mobile via CSS grid breakpoints
- Blob animation uses `conic-gradient` + `filter: blur` with four keyframe animations (`morph`, `spin`, `pulse`, `drift`) running at different durations and phases for organic movement
