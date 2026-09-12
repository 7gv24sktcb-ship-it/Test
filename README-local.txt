TDK RELEASE BENCH
=================

An intake bench for TDK Electronics product press releases. Drop in the
datasheet and the product marketing form, and it produces the parts that
have to be written: the category eyebrow, the headline, the body text, and
the two bulleted lists. Boilerplate, media contacts, the dateline and the
download links are not written here - they belong to your release template.


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
install, no account. The fonts and the PDF engine are built into the file,
so reading documents and assembling the packet work with no internet
connection at all.

The one exception is step 4, drafting with Claude. That step is optional and
it does need internet and an API key. Everything else works offline.


HOW IT WORKS
------------

1. DATASHEET - drop a PDF, Word (.docx), TXT or MD file. The text is
   extracted in your browser. Datasheet tables come through as tab-separated
   rows.

2. PRODUCT MARKETING FORM - same again. This is what decides positioning:
   target markets, USP, customer value. A form laid out as a Word table
   keeps its label-and-value structure.

   Both panels open for review. Read the extracted text before you hand it
   off: PDF extraction flattens page layout, and a misread figure in a press
   release is a real liability. Edit anything wrong right there.

3. DRAFT SETTINGS - the product or series name and the category eyebrow, if
   you want to override what the documents say; the length and list
   convention; whether to include a specs table; and any notes for the
   drafting step, such as which spec to foreground.

4. DRAFT WITH CLAUDE (optional) - paste an Anthropic API key and press
   Generate. The page sends the briefing packet to the Claude API and streams
   the release text back into the Draft release tab.

   Without a key, the bench works exactly as before: Copy or Download the
   briefing packet and paste it into Claude yourself. Same packet, same
   rules, same result.


WHAT IT WRITES, AND WHAT IT DOES NOT
------------------------------------

WRITES      Category eyebrow. Headline. Two to four body paragraphs: the
            lede opening on "TDK Corporation (TSE:6762) ...", the technical
            paragraph, the mechanical and qualification paragraph, and a
            design-tool paragraph where the sources name one. Then "Main
            applications" and "Main features and benefits" as bullet lists,
            and a specs table if you asked for one.

DOES NOT    No dateline - the release date is not fixed at drafting time, so
            no date appears anywhere in the text. No "About TDK Corporation"
            paragraph, no media contacts, no download links. No quotes: TDK
            product releases never carry a spokesperson or customer
            statement, and the packet forbids inventing one or leaving a
            placeholder for one.

Those standing blocks go in when you paste the text into your release
template, where they can be checked against the latest approved release.


THE THREE OUTPUT TABS
---------------------

BRIEFING PACKET   Everything the drafting step needs in one block:
                  what to write, what not to write, length, voice, hard
                  rules, your settings, and both source documents.

DRAFT RELEASE     What Claude wrote, when you use step 4.

PRE-FLIGHT        What to check before the draft leaves your desk.


DRAFTING WITH CLAUDE
--------------------

GETTING A KEY   Claude Console -> Account settings -> API keys. The key
                belongs to your organization and is billed to it.

THE KEY         It is stored in this browser and sent to api.anthropic.com
                and nowhere else - not to any server of mine, not to TDK,
                not anywhere in between. By default it is kept only until
                you close the tab. Tick "Remember the key on this computer"
                and it is saved in the browser's local storage instead;
                leave that off on a shared machine.

MODEL AND COST  Claude Sonnet 5 by default, at $2 per million input tokens
                and $10 per million output tokens - a draft from a typical
                datasheet and marketing form runs about two cents. Claude
                Opus 5 stays in the dropdown for a release worth spending
                more on, at roughly 2.5 times that. The exact figure appears
                next to the button after each run.

WHAT IT SENDS   Exactly the briefing packet you can read in the first tab -
                both source documents, your settings, and the house rules -
                plus one added instruction: because the request is sent in
                one pass with nobody to answer a follow-up question, Claude
                is told to write the release on the best-supported reading
                and mark anything uncertain inline as [VERIFY: ...] rather
                than stopping to ask.

READ IT         The draft is a draft. Check every figure against the
                datasheet, resolve every [VERIFY: ...] mark, and work
                through the Pre-flight tab before it goes anywhere.


PRIVACY
-------

The documents you drop are read in the browser and never uploaded. Your
settings, extracted text and last draft are kept in that browser's local
storage so the page survives a reload, and nowhere else. Use the Clear
button on a slot to drop a document again.

The single exception is the optional Generate step: pressing that button
sends the briefing packet - which contains both source documents - to
api.anthropic.com. If the datasheet or the marketing form is confidential
and unreleased, that is a decision to make deliberately. Don't press
Generate if you would not paste the same documents into Claude by hand.


BUILT FROM
----------

index.html is generated from bench.template.html by build.py, which inlines
pdfjs-dist 4.10.38 (Apache-2.0) and the web fonts. To change the app, edit
the template and run:

    python3 build.py --target local
