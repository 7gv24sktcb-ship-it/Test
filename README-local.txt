TDK RELEASE BENCH
=================

An intake bench for TDK Electronics product press releases. Drop in the
datasheet and the product marketing form, and it assembles one briefing
packet you paste into Claude to write the release, plus a document scaffold
with every fixed block already in place.


HOW TO OPEN IT
--------------

Simplest: double-click index.html. It opens in your default browser and
works straight away.

If you would rather serve it (so the browser remembers your drafts between
visits, and so it behaves exactly as it would on an intranet), open a
terminal in this folder and run one of:

    python -m http.server 8000
    npx http-server -p 8000

Then open http://localhost:8000 in your browser.

To put it on a shared machine or an internal web server, copy index.html
wherever that server serves files from. It is a single self-contained file
with no dependencies, no build step, and no configuration.


WHAT IT NEEDS
-------------

A current browser: Chrome, Edge, Firefox or Safari. Nothing else. No
internet connection, no install, no account, no API key. The fonts and the
PDF engine are built into the file.


HOW IT WORKS
------------

1. DATASHEET — drop a PDF, Word (.docx), TXT or MD file. The text is
   extracted in your browser. Datasheet tables come through as tab-separated
   rows.

2. PRODUCT MARKETING FORM — same again. This is what decides positioning:
   target markets, USP, customer value. A form laid out as a Word table
   keeps its label-and-value structure.

   Both panels open for review. Read the extracted text before you hand it
   off: PDF extraction flattens page layout, and a misread figure in a press
   release is a real liability. Edit anything wrong right there.

3. RELEASE SETTINGS — the things no document carries: release date, the
   product category slug for the download URL, the length and list
   convention, whether to include a specs table, whether the brand list
   includes EPCOS, and any approved quote.

Then take the Briefing packet tab, Copy or Download it, and paste it into
Claude. The bench does not write the release itself.


THE THREE OUTPUT TABS
---------------------

BRIEFING PACKET   Everything the drafting step needs in one block:
                  structure, voice, hard rules, your settings, the fixed
                  blocks, and both source documents.

DOCUMENT SCAFFOLD The release with every fixed part already filled in —
                  dateline, About TDK Corporation, download links, media
                  contacts — and placeholders where the prose goes.

PRE-FLIGHT        What to check before the draft leaves your desk.


BEFORE ANYTHING GOES OUT
------------------------

The boilerplate and the media contacts in this file are the June 2026
versions. Sales and headcount figures, contact names, locations and phone
numbers all drift between releases. Verify them against the most recent
approved release every time.

The dated download URL is assigned by the web team on publication; the
scaffold leaves a marked placeholder for it.


PRIVACY
-------

Nothing leaves your machine. The documents you drop are read in the browser
and never uploaded. Your settings and extracted text are kept in that
browser's local storage so the page survives a reload, and nowhere else.
Use the Clear button on a slot to drop a document again.


BUILT FROM
----------

index.html is generated from bench.template.html by build.py, which inlines
pdfjs-dist 4.10.38 (Apache-2.0) and the web fonts. To change the app, edit
the template and run:

    python3 build.py --target local
