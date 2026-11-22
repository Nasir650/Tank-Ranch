"""Install the supplied postcard results without replacing the public check form."""

import csv
import html
import json
import os
import re
import sys
from collections import Counter
from unicodedata import normalize
import zipfile
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "Tank & Trench - Results Pages.zip"
OUTPUT = ROOT / "dist"
CODE_PAGE = re.compile(r"r/([A-Z]{2}\d+-[a-z0-9]{4})/index\.html")
RESULT_LABEL = re.compile(r'<p class="label">(?:Who it recommended|Also on the list)</p>')
SITE = "https://tankandtrench.com"
CONTACT = json.loads((ROOT / "src/data/contact.json").read_text(encoding="utf-8"))
PHONE = html.escape(CONTACT["number"])
GA_ID = os.environ.get("PUBLIC_GA_MEASUREMENT_ID", "").strip()
CALLRAIL_ID = os.environ.get("PUBLIC_CALLRAIL_COMPANY_ID", "").strip()


def company_name(source):
    return html.unescape(re.search(r'<span class="co">(.*?)</span>', source)[1])


def company_slug(company):
    ascii_name = normalize("NFKD", company.lower()).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", ascii_name).strip("-")[:100].rstrip("-")


def evidence_panel(record):
    date = record.get("date_checked", "").strip()
    screenshot = record.get("screenshot", "").strip()
    if screenshot and not (Path(screenshot).name == screenshot and (OUTPUT / "checks" / screenshot).is_file()):
        raise ValueError(f"Screenshot for {record['card_code']} is missing from public/checks")

    evidence = f'<p class="small">Checked {html.escape(date)}</p>' if date else ""
    if screenshot:
        image = f"/checks/{quote(screenshot)}"
        evidence += (
            f'<figure class="result-screenshot"><a href="{image}">'
            f'<img src="{image}" alt="Screenshot of the ChatGPT answer"></a>'
            '<figcaption><a href="' + image + '">Open full screenshot</a></figcaption></figure>'
        )
    return evidence


def fixes_panel(record, no_website):
    fixes = [record.get(f"fix_{index}", "").strip() for index in range(1, 4)]
    if all(fixes):
        heading = "Three fixes for your company"
    elif any(fixes):
        heading = "What we’d fix first"
        fixes = [fix for fix in fixes if fix]
    else:
        heading = "What we’d fix first"
        if no_website:
            fixes = [
                "Build a custom WordPress website (service pages, town pages, and schema) in the first 30 days — included with both plans.",
                "Add structured schema and an llms.txt file so ChatGPT, Claude, and Google’s AI can verify your services and towns.",
                "Clean up your Google Business Profile categories, service areas, and local citations so AI answers match your company.",
            ]
        else:
            fixes = [
                "Add dedicated service and town pages answering the exact questions homeowners and builders ask in your county.",
                "Wire up structured schema markup and an llms.txt file so AI assistants can cite your company with confidence.",
                "Align your Google Business Profile, reviews, and local citations around your highest-value jobs.",
            ]
    items = "".join(f"<li>{html.escape(fix)}</li>" for fix in fixes)
    return f'<section class="card result-fixes"><h2>{heading}</h2><ol>{items}</ol></section>'


def head_tracking_snippets():
    snippets = []
    if GA_ID:
        safe_ga = html.escape(GA_ID, quote=True)
        snippets.append(
            f'<script async src="https://www.googletagmanager.com/gtag/js?id={safe_ga}"></script>'
            f'<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}'
            f'window.gtag=gtag;gtag("js",new Date());gtag("config","{safe_ga}");</script>'
        )
    if CALLRAIL_ID:
        safe_cr = html.escape(CALLRAIL_ID, quote=True)
        snippets.append(
            f'<script type="text/javascript" src="//cdn.callrail.com/companies/{safe_cr}/12/swap.js" async></script>'
        )
    return "".join(snippets)


def build_page(source, code, record):
    company = company_name(source)
    no_website = ("Without a website" in source) or ("A real website" in source)
    text_link = f"sms:{PHONE}?&amp;body={quote(f'Hi Joe, this is {company}. Ref {code.upper()}.')}"
    video_button = '<a class="btn" href="#video" data-track="video-scroll">Get my 5-minute video</a>'
    text_button = f'<a class="btn ghost" href="{text_link}" data-track="text">Text Joe</a>'
    call_button = f'<a class="btn ghost" href="tel:{PHONE}" data-track="call">Call Joe</a>'
    source = source.replace(
        '<p class="eyebrow">Your ChatGPT results</p>',
        '<p class="eyebrow">Did it say your name?</p>',
        1,
    )
    if "didn't come up in any" not in source.split("</h1>", 1)[0]:
        intro = "ChatGPT already named you. Here’s who else came up and what you can do to keep getting found."
    else:
        intro = "When your name is missing, that could mean work going down the road. Here’s who ChatGPT named."
    if no_website:
        intro += " No website yet? Both plans include a custom WordPress site (service pages, town pages, and schema) built in the first 30 days."

    source = re.sub(
        r'<p class="lede">.*?</p>',
        f'<p class="lede">{intro}</p><div class="btns result-top-actions">{video_button}{text_button}</div>',
        source,
        count=1,
    )
    source, labels_replaced = RESULT_LABEL.subn(
        lambda _: evidence_panel(record) + '<h2 class="label">Who ChatGPT named</h2>', source, count=1
    )
    if not labels_replaced:
        raise ValueError(f"Results heading missing for {code}")
    source = source.replace('<p class="label">The question we asked</p>', '<h2 class="label">The question we asked</h2>', 1)
    start = source.index('<section class="leads">')
    end = source.index('<h2 class="answers-h">', start)
    video = (
        '<section class="card result-video" id="video"><h2>Get my 5-minute video</h2>'
        '<p>Joe will walk through what came up and what to fix first.</p>'
        f'<form action="{html.escape(CONTACT["formEndpoint"], quote=True)}" method="post" data-video-request>'
        '<input type="hidden" name="_subject" value="Tank &amp; Trench: 5-Minute Video Request (Postcard)">'
        '<input type="hidden" name="source" value="postcard-video-request">'
        f'<input type="hidden" name="company" value="{html.escape(company, quote=True)}">'
        f'<input type="hidden" name="card_code" value="{code.upper()}">'
        '<label for="reply-phone">Your mobile number</label>'
        '<div class="result-video-row">'
        '<input type="tel" inputmode="tel" name="phone" id="reply-phone" autocomplete="tel" required>'
        '<button class="btn" type="submit" data-track="video">Get my 5-minute video</button>'
        '</div>'
        '<p class="sms-consent">By submitting, you agree to receive texts from Tank &amp; Trench about your results. Msg &amp; data rates may apply. Reply STOP to opt out. <a href="/privacy/">Privacy Policy</a> &middot; <a href="/terms/">Terms</a></p>'
        '</form></section>'
    )
    source = source[:start] + fixes_panel(record, no_website) + video + source[end:]
    source = source.replace('<details open>', '<details>', 1)
    extra_head = head_tracking_snippets()
    if extra_head:
        source = source.replace('</head>', extra_head + '</head>', 1)
    source = source.replace(
        '</main></body>',
        f'</main><div class="result-mobile-bar" aria-label="Mobile quick actions">{text_button}{call_button}</div>'
        '<script src="/contact-forms.js" defer></script></body>',
    )
    return source


def main():
    with (ROOT / "src/data/postcards.csv").open(encoding="utf-8-sig", newline="") as file:
        records = list(csv.DictReader(file))
    evidence = {row["card_code"].strip().upper(): row for row in records if row.get("card_code")}

    occupied = {row["slug"] for row in records if row.get("slug")}
    links = []
    with zipfile.ZipFile(ARCHIVE) as archive:
        for name in ("r/index.html", "r/assets/style.css", "r/assets/track.js"):
            archive.extract(name, OUTPUT)

        pages = [
            (match[1], archive.read(name).decode("utf-8"))
            for name in archive.namelist()
            if (match := CODE_PAGE.fullmatch(name))
        ]
        slug_counts = Counter(company_slug(company_name(source)) for _, source in pages)
        for code, source in pages:
            company = company_name(source)
            slug = company_slug(company)
            if not slug or slug_counts[slug] > 1 or slug in occupied:
                slug = f"{slug or 'company'}-{code.lower()}"
            if slug in occupied:
                raise ValueError(f"Duplicate postcard page slug: {slug}")
            occupied.add(slug)
            target = f"/check/{slug}/"
            page = build_page(source, code, evidence.get(code.upper(), {}))
            path = OUTPUT / "check" / slug / "index.html"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(page, encoding="utf-8")

            legacy = OUTPUT / "r" / code / "index.html"
            legacy.parent.mkdir(parents=True, exist_ok=True)
            legacy.write_text(
                '<!doctype html><html lang="en"><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width,initial-scale=1">'
                '<meta name="robots" content="noindex,nofollow,noarchive">'
                f'<meta http-equiv="refresh" content="0;url={target}">'
                f'<title>Your postcard results</title><a data-postcard-result href="{target}">Open your postcard results</a></html>',
                encoding="utf-8",
            )
            row = evidence.get(code.upper(), {})
            complete = all(row.get(field, "").strip() for field in ("date_checked", "screenshot", "fix_1", "fix_2", "fix_3"))
            links.append((code.upper(), company, f"{SITE}{target}", "yes" if complete else "no"))

    css = OUTPUT / "r/assets/style.css"
    base_css = css.read_text(encoding="utf-8")
    base_css = re.sub(r"^@import[^\n]+\n", "", base_css, count=1)
    css.write_text(base_css + (ROOT / "src/styles/postcard-results.css").read_text(encoding="utf-8"), encoding="utf-8")

    track_js = OUTPUT / "r/assets/track.js"
    track_js.write_text(
        "(function(){\n"
        "  var s=document.currentScript; var CODE=s&&s.getAttribute('data-code');\n"
        "  if(typeof window.gtag==='function'){window.gtag('event','results_page_view',{ref_code:CODE});}\n"
        "  document.addEventListener('click',function(e){\n"
        "    var a=e.target.closest&&e.target.closest('[data-track]'); if(!a) return;\n"
        "    if(typeof window.gtag==='function'){window.gtag('event','results_'+a.getAttribute('data-track'),{ref_code:CODE});}\n"
        "  });\n"
        "})();\n",
        encoding="utf-8",
    )

    if len(links) != len({link[0] for link in links}) or not links:
        raise ValueError("Postcard archive must contain a unique page for each card code")
    if len(sys.argv) == 2:
        with Path(sys.argv[1]).open("w", encoding="utf-8-sig", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(("card_code", "company", "custom1", "proof_complete"))
            writer.writerows(sorted(links))
    print(f"Built {len(links)} postcard results")


if __name__ == "__main__":
    main()
