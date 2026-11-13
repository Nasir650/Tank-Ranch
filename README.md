# Tank & Trench — Static Site Generator (Astro + Cloudflare Pages)

## Postcard results and QR destinations

The supplied `Tank & Trench - Results Pages.zip` is the source for the 3,590
postcard results. Keep it at the repository root when deploying this batch.
`npm run build` runs Astro and then uses Python 3 (available as `python`) to
add the personalized pages and legacy code links to `dist`.

- New QR destinations use `/check/<company-name>/`. Companies whose names
  produce the same slug get their card code appended. Existing `/r/<code>/`
  links and the postcard-code lookup on `/check/` continue to work.
- Export the QR mapping after the build with
  `python scripts/build-postcard-results.py postcard-qr-links.csv`.
  Join the export to the mailing list by `card_code`. In Thanks.io, map
  `custom1` to the full URL and set the message template's QR destination to
  `~CUSTOM1~`. Preview individual recipients before sending. The export's
  `proof_complete` column marks whether the page has a date, a screenshot,
  and three company-specific fixes. The supplied archive has transcripts but
  no screenshot files, check dates, or company-specific fixes.
- To add missing evidence to an existing postcard, add a CSV row keyed by
  `card_code` and fill `date_checked`, `screenshot`, and `fix_1` through
  `fix_3`. Put the screenshot in `public/checks/`. A row for an existing
  archive page can leave `slug` blank. The original prompt and transcripts
  stay paired. Run a fresh check if the prompt itself needs to change.
- For standalone CSV-driven checks, use `slug` and `Card line` for the URL
  and trade. The question and proof fields should come from the same check.
  The fictional rows in `postcards-sample.csv` illustrate the format.
- Call and text links use `617-579-8197` from `src/data/contact.json`.

Official agency website and automated postcard check page generator for **Tank & Trench** (`tankandtrench.com`), built with **Astro**.

Category: **AI Search for Septic & Excavation**  
Measurement: **Inbound phone calls and form submissions**

---

## 🚀 Key Features

1. **Pure Static Architecture**:
   - Zero WordPress bloat or database overhead.
   - Instant edge delivery on Cloudflare Pages.
   - 100% component-driven templates (`BaseLayout.astro`, `Header.astro`, `Footer.astro`, `MobileStickyBar.astro`).

2. **Automated Postcard Page Generation at Scale (`/check/[slug]/`)**:
   - Driven directly by CSV: [`src/data/postcards.csv`](src/data/postcards.csv).
   - Generates 2,000+ individual company check pages in seconds at build time (`dist/check/<company-slug>/index.html`).
   - Version A vs. Version B dynamic copy:
     - **Version A** (`company_named == 'no'`): *"[Company] wasn't in the answer. That's not about your work. It's about what the AI can find about you."*
     - **Version B** (`company_named == 'yes'`): *"[Company] was in the answer. Here's how to stay there as competitors catch on."*
   - Proof box with prompt question, screenshot, and AI-named competitors.
   - 3 actionable fixes per company.
   - Form for 5-minute video audit and click-to-text Joe.
   - Strict `noindex, nofollow, noarchive` on all postcard pages.

3. **Forms & Lead Handling**:
   - Pre-configured for Formspree (or any form backend service).
   - Smooth asynchronous submission with instant inline confirmation.

4. **CallRail Dynamic Number Insertion (DNI)**:
   - Ready for CallRail phone swapping script integration in `BaseLayout.astro`.
   - Postcard tracking number: `617-579-8197`.

---

## 🛠️ CSV Workflow (Google Sheets &rarr; Site Generation)

1. Manage your outreach list in Google Sheets (reference: [Tank & Trench Postcards Sheet](https://docs.google.com/spreadsheets/d/1Pl9pxFX5b_FevgofP7GHwzYFH34KyvnkWULRBVJFISk/edit?usp=sharing)).
2. Download or export as CSV.
3. Replace [`src/data/postcards.csv`](src/data/postcards.csv).
4. Run `npm run build` (or push to your Git repo). Cloudflare Pages will automatically rebuild and deploy all pages.

### CSV Columns Supported:
| Column | Description |
|---|---|
| `slug` | URL slug (e.g. `pine-ridge-septic` &rarr; `/check/pine-ridge-septic/`) |
| `company` | Business name (e.g. `Pine Ridge Septic`) |
| `owner_first_name` | Recipient first name (e.g. `Dale`) |
| `city` | Target town/city (e.g. `Sanford`) |
| `state` | State code (e.g. `NC`) |
| `zip` | Postal code |
| `question_asked` | AI prompt query (e.g. `Who's the best septic company in Sanford NC?`) |
| `ai_assistant` | AI platform (e.g. `ChatGPT`) |
| `date_checked` | Verification date (e.g. `2026-11-20`) |
| `ai_named` | Competitors or companies returned in the answer |
| `company_named` | `yes` or `no` (switches between Version A and Version B) |
| `screenshot` | Filename in `public/checks/` |
| `Card line` | Trade wording for the page heading, such as `excavation and site work` |
| `card_code` | Printed postcard code to attach evidence to an existing archive result |
| `fix_1`, `fix_2`, `fix_3` | Three prioritized reasons from research |
| `wave` | Campaign wave tracking ID |

---

## 🌐 Cloudflare Pages Deployment Settings

- **Framework preset**: `Astro`
- **Build command**: `npm run build`
- **Build output directory**: `dist`
- **Build dependencies**: Node 20+ and Python 3

---

## 💻 Local Development

```bash
# Install dependencies
npm install

# Run dev server (http://localhost:4321)
npm run dev

# Build static output to dist/
npm run build

# Preview the full build, including postcard pages
npm run preview
```
