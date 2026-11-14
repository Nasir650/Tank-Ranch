# Tank & Trench project handoff

Updated November 13, 2026. Open this file first when resuming work in a new chat.

## Project and current state

- Local folder: `D:\POSTS\TANK AND TRENCH`
- Repository: [Nasir650/Tank-Ranch](https://github.com/Nasir650/Tank-Ranch), branch `main`
- Last known pushed commit: [702af56](https://github.com/Nasir650/Tank-Ranch/commit/702af56). It contains the postcard generator, results archive, QR export, tracking number, and site updates.
- The user confirmed the postcard pages are working on the Cloudflare Workers preview. Production routing on `tankandtrench.com` still needs verification.
- The About page contact layout fix is a local edit in `src/pages/about.astro`. Astro built successfully and the layout passed checks at 320, 375, 430, 768, 1024, and 1440 px. Check Git status before committing or deploying it.

## Client goal

Each mailed postcard should open the recipient company's own `/check/<company>/` page. The page should help the recipient quickly see what ChatGPT said and reply to Joe. Keep the personalized page focused on the result and the reply options. The general `/check/` page serves people requesting a check or looking up a printed postcard code.

On phones, show **Text Joe** near the top with **617-579-8197** and offer a short **Get my 5-minute video** form. The proof should show the original question, check date, real screenshot, who ChatGPT named, and three researched fixes for the recipient. The result headline differs depending on whether ChatGPT named the company.

The main site now addresses septic and excavation contractors, including those serving builders. Pricing is $750/mo for Pro and $1,250/mo for Territory. Territory is one company per county per side, Tank or Trench.

## Client review links

Send the personalized examples first and the fallback last. Ask the client to try them on a phone.

| Page | Preview |
| --- | --- |
| Anderson Pumping Service, named in 3 of 3 answers | [Open Anderson](https://tank-ranch-website.nasirkhnbaloch.workers.dev/check/anderson-pumping-service/) |
| RooterPLUS!, did not appear | [Open RooterPLUS!](https://tank-ranch-website.nasirkhnbaloch.workers.dev/check/rooterplus/) |
| General check form and printed code lookup | [Open fallback](https://tank-ranch-website.nasirkhnbaloch.workers.dev/check/) |
| Original RooterPLUS! QR destination | [Open legacy redirect](https://tank-ranch-website.nasirkhnbaloch.workers.dev/r/GA127-xd6t/) |

On the fallback page, open **Have a postcard code?** and enter `GA127-XD6T` to reach RooterPLUS!. The personalized layouts and client-side lookup and video form were checked locally. The form test used simulated responses.

## Build and data

Run `npm run build` with Node and Python 3 available. Astro builds the main site, then `scripts/build-postcard-results.py` adds 3,590 personalized pages and their legacy redirects to `dist/` using `Tank & Trench - Results Pages.zip`. See `README.md` for setup and evidence fields.

`postcard-qr-links.csv` contains the mailing destinations in `custom1`. Match rows to recipients by `card_code` and set the Thanks.io QR destination to `~CUSTOM1~`. The CSV currently uses `tankandtrench.com`. The Workers links above are for review.

## Before mailing

- [ ] Obtain the actual check dates, screenshots, and three researched fixes for the companies in the mailing batch. The archive supplies the prompts and transcripts. All 3,590 rows currently have `proof_complete=no`. Add evidence keyed by `card_code` in `src/data/postcards.csv`, place screenshots in `public/checks/`, and rebuild and re-export.
- [ ] Verify a personalized page and its legacy redirect on the production domain. Scan a Thanks.io test postcard on a phone to check that its QR opens the right company. Check the under-two-second load target on mobile.
- [ ] Test a real SMS to 617-579-8197 and a real video request. Confirm Joe receives both.
- [ ] Verify the Engage screenshot and the calls and form-fills breakdown behind the homepage's 40+ engagements figure if the client supplies the evidence.

To resume, ask: “Read PROJECT-HANDOFF.md, check Git status, and pick up from the remaining items.”
