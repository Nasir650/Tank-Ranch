# Tank & Trench — Static Site Generator (Astro + Cloudflare Pages)

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
   - Form for 5-minute video audit + click-to-text Joe button (`sms:15085550198?...`).
   - Strict `noindex, nofollow, noarchive` on all postcard pages.

3. **Forms & Lead Handling**:
   - Pre-configured for Formspree (or any form backend service).
   - Smooth asynchronous submission with instant inline confirmation.

4. **CallRail Dynamic Number Insertion (DNI)**:
   - Ready for CallRail phone swapping script integration in `BaseLayout.astro`.
   - General phone: `(508) 555-0198`.

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
| `screenshot` | Filename in `public/checks/` (with automatic fallback visual) |
| `fix_1`, `fix_2`, `fix_3` | Three prioritized reasons from research |
| `wave` | Campaign wave tracking ID |

---

## 🌐 Cloudflare Pages Deployment Settings

- **Framework preset**: `Astro`
- **Build command**: `npm run build`
- **Build output directory**: `dist`
- **Environment variables**: Node 18+ or 20+

---

## 💻 Local Development

```bash
# Install dependencies
npm install

# Run dev server (http://localhost:4321)
npm run dev

# Build static output to dist/
npm run build

# Preview build locally
npm run preview
```
