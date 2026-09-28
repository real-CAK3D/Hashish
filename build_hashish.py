#!/usr/bin/env python3
"""HASHISH — the Garden's glossy monthly (a clean parody of the old men's glossies): a centerfold glamour shot of one of the
Garden's machines, an agent interview, features, "Hash Tags" gadgets and the Strain of the Month. Disco Stu edits it.

Usage: build_hashish.py [drafts/<YYYY-MM>.json]   (draws the cover + centerfold photos once, then prints the issue and home page)
"""
import base64, datetime as dt, importlib.util, io, json, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")
sys.path.insert(0, ROOT)
import pubkit as pk   # noqa: E402
import flipbook as fb   # noqa: E402
from pubkit import e   # noqa: E402

fb.CSS_FILE = "hashish.css"
REPO = "https://github.com/real-CAK3D/Hashish"


def draw(name, prompt, size="1024x1536"):
    out = os.path.join(SITE, "img", name)
    if os.path.exists(out):
        return True
    os.makedirs(os.path.dirname(out), exist_ok=True)
    sys.path.insert(0, os.path.join(pk.HERMES, "hermes-agent"))
    spec = importlib.util.spec_from_file_location("cx", os.path.join(pk.HERMES, "hermes-agent", "plugins", "image_gen", "openai-codex", "__init__.py"))
    cx = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cx)
    token = cx._read_codex_access_token()
    try:
        b64 = cx._collect_image_b64(token, prompt=prompt + " Tasteful, family-friendly product photography: no people, no nudity, no real brands or logos.",
                                    size=size, quality="medium") if token else None
    except Exception:
        b64 = None
    if not b64:
        return False
    from PIL import Image
    im = Image.open(io.BytesIO(base64.b64decode(b64))).convert("RGB")
    im.thumbnail((1200, 1800))
    im.save(out, "JPEG", quality=86, optimize=True, progressive=True)
    return True


def render(ed):
    m = ed["month"]
    d = dt.date.fromisoformat(m + "-01")
    no = (d.year - 2026) * 12 + d.month - 8
    pin = ed.get("pinup") or {}
    cover_ok = draw("cover-%s.jpg" % m, "A glossy 1970s men's-lifestyle magazine cover photograph, dramatic warm studio lighting, rich red velvet and gold tones: "
                    "%s posed like a cover star on a velvet chaise, soft focus glow, bokeh lights. Leave the top quarter clear for the magazine title." % (pin.get("look") or "a small single-board computer"))
    fold_ok = draw("centerfold-%s.jpg" % m, "A glamorous glossy magazine centerfold photograph of %s, lying on crushed red velvet with gold satin, dramatic rim lighting, "
                   "shallow depth of field, a single rose nearby, warm vintage film grain, shot like a luxury product pin-up." % (pin.get("look") or "a small single-board computer"),
                   size="1536x1024")
    seal = '<a class="seal" href="/" aria-label="Back to The Corner Chronicle">%s</a>' % fb.SEAL
    cover = ('<div class="hs-cover">%s<div class="hs-logo">HASHISH</div><div class="hs-issue">%s · No. %d · THE GARDEN\'S GLOSSY</div>'
             '<div class="hs-lines"><span>CENTERFOLD: %s</span><span>%s</span><span>STRAIN OF THE MONTH: %s</span>%s</div>'
             '<div class="hs-corner">ONE PINCH<br><b>THE MACHINE ISSUE</b></div></div>'
             % (('<img src="../img/cover-%s.jpg" alt="">' % m) if cover_ok else "", e(d.strftime("%B %Y").upper()), no, e((pin.get("title") or "").upper()),
                e(((ed.get("interview") or {}).get("headline") or "").upper()), e(((ed.get("strain") or {}).get("name") or "").upper()),
                ('<span class="hs-plus">PLUS: %s</span>' % " · ".join(e(str(f.get("title") or "").upper()) for f in (ed.get("features") or [])[:2] if isinstance(f, dict))
                 if ed.get("features") else "")))
    pages = [fb.page("Hashish", cover, " hardcover hs-cov")]
    toc = [("Centerfold", pin.get("title")), ("The Interview", (ed.get("interview") or {}).get("headline")), ("Features", ", ".join(f.get("title", "") for f in ed.get("features") or [])),
           ("Hash Tags", "gadgets worth drooling over"), ("Strain of the Month", (ed.get("strain") or {}).get("name"))]
    pages.append(fb.page("Contents", '<div class="hs-toc"><h2>Inside</h2><p class="hs-edl">%s<span>— Disco Stu, Editor</span></p><ol>%s</ol></div>'
                         % (e(ed.get("editor_letter")), "".join('<li><a data-goto="%d"><b>%s</b> <span>%s</span></a></li>' % (i + 3, e(a), e(b)) for i, (a, b) in enumerate(toc) if b))))
    turn = "".join("<li>%s</li>" % e(x) for x in pin.get("turn_ons") or [])
    offs = "".join("<li>%s</li>" % e(x) for x in pin.get("turn_offs") or [])
    specs = "".join('<tr><th>%s</th><td>%s</td></tr>' % (e(k), e(v)) for k, v in (pin.get("vitals") or {}).items())
    pages.append(fb.page("Centerfold", ('<div class="hs-fold">%s<div class="hs-fold-card"><div class="hs-miss">%s</div><h2>%s</h2><table>%s</table>'
                                        '<div class="hs-2"><div><h4>Turn-ons</h4><ul>%s</ul></div><div><h4>Turn-offs</h4><ul>%s</ul></div></div><p class="hs-quote">“%s”</p></div></div>')
                         % (('<img class="hs-fold-img" src="../img/centerfold-%s.jpg" alt="Centerfold: %s">' % (m, e(pin.get("title")))) if fold_ok else "",
                            e(pin.get("miss") or "Miss %s" % d.strftime("%B")), e(pin.get("title")), specs, turn, offs, e(pin.get("quote"))), " hs-centerfold"))
    iv = ed.get("interview") or {}
    qa = "".join('<p class="hs-q">%s</p><p class="hs-a">%s</p>' % (e(x.get("q")), e(x.get("a"))) for x in iv.get("qa") or [])
    pages.append(fb.page("The Interview", '<div class="hs-iv"><div class="hs-kick">The Hashish Interview</div><h2>%s</h2><div class="byline">%s<span>%s, in conversation with Disco Stu</span></div>'
                         '<p class="hs-dek">%s</p><div class="hs-qa">%s</div></div>' % (e(iv.get("headline")), fb.mug(iv.get("agent")), e(iv.get("agent")), e(iv.get("intro")), qa)))
    feats = "".join('<article class="hs-feat"><h3>%s</h3>%s</article>' % (e(f.get("title")), fb.para(f.get("body"))) for f in ed.get("features") or [])
    pages.append(fb.page("Features", '<div class="hs-feats"><div class="hs-kick">Features</div>%s</div>' % (feats or "")))
    tags = "".join('<div class="hs-tag"><b>%s</b><span class="hs-price">%s</span><p>%s</p>%s</div>'
                   % (e(g.get("name")), e(g.get("price")), e(g.get("why")), ('<a href="%s" target="_blank" rel="noopener">Look ›</a>' % e(g["url"])) if str(g.get("url", "")).startswith("https://") else "")
                   for g in ed.get("hash_tags") or [])
    st = ed.get("strain") or {}
    pages.append(fb.page("Hash Tags & Strain of the Month", '<div class="hs-2c"><div><div class="hs-kick">#HashTags</div><h2 class="hs-h">Gadgets worth drooling over</h2>%s</div>'
                         '<div class="hs-strain"><div class="hs-kick">Strain of the Month</div><h2>%s</h2><p class="hs-lin">%s</p><p>%s</p><p class="small">A made-up strain, named for the Garden. Nobody\'s selling anything.</p></div></div>'
                         % (tags, e(st.get("name")), e(st.get("lineage")), e(st.get("notes")))))
    pages.append(fb.page("Back Page", ('<div class="gum"><span>HASHISH · THE GARDEN\'S GLOSSY</span></div><div class="pb-body">%s<h2 class="pb-title">HASHISH</h2>'
                                       '<p>Edited by Disco Stu. Every centerfold is one of the Garden\'s own machines.<br>Keep it classy, keep it clean.</p>%s'
                                       '<p class="pb-code">%s · No. %d</p><p><a href="../archive.html">Back issues ›</a></p></div>')
                         % (seal, fb.back_codes(REPO, "Hashish"), e(d.strftime("%B %Y")), no), " hardcover back"))
    return fb.book(pages, date=m + "-01", no=no, lists={}, paper="HASHISH", motto="The Garden's glossy", gum="HASHISH · THE GARDEN'S GLOSSY",
                   price="PRICE: ONE PINCH", delivered="EDITED BY DISCO STU", flap="Hashish · the Garden's glossy", body_class="pub-hs", est="THE GARDEN'S GLOSSY")


def build(path=None):
    pk.sync_portraits(SITE)
    if path:
        ed = json.load(open(path))
        os.makedirs(os.path.join(SITE, "issues"), exist_ok=True)
        open(os.path.join(SITE, "issues", ed["month"] + ".html"), "w").write(render(ed))
    eds = pk.issues(SITE, pattern=r"\d{4}-\d{2}")
    if eds:
        open(os.path.join(SITE, "index.html"), "w").write(open(os.path.join(SITE, "issues", eds[0] + ".html")).read().replace('href="../', 'href="').replace('src="../', 'src="'))
        ed = pk.load(os.path.join(ROOT, "drafts", eds[0] + ".json"))
        lines = ["Centerfold: %s" % ((ed.get("pinup") or {}).get("title") or ""), (ed.get("interview") or {}).get("headline") or "",
                 "Strain of the month: %s" % ((ed.get("strain") or {}).get("name") or "")]
        pk.latest(SITE, "Hashish", eds[0] + "-01", "Centerfold: %s" % ((ed.get("pinup") or {}).get("title") or ""), "issues/%s.html" % eds[0], [x + "-01" for x in eds[:10]],
                  lines=[x for x in lines if x.split(": ")[-1]], cover=("img/cover-%s.jpg" % eds[0]) if os.path.exists(os.path.join(SITE, "img", "cover-%s.jpg" % eds[0])) else "")
    else:   # before the first issue: a preview
        today = dt.date.today()
        nxt = today.replace(day=15) if today.day < 15 else (today.replace(day=1) + dt.timedelta(days=32)).replace(day=15)
        seal = '<a class="seal" href="/" aria-label="Back to The Corner Chronicle">%s</a>' % fb.SEAL
        pages = [fb.page("Hashish", '<div class="hs-cover"><div class="hs-logo">HASHISH</div><div class="hs-issue">THE GARDEN\'S GLOSSY · FIRST ISSUE %s</div>'
                         '<div class="hs-lines"><span>CENTERFOLD: ONE OF THE GARDEN\'S OWN MACHINES</span><span>THE HASHISH INTERVIEW</span><span>STRAIN OF THE MONTH</span></div></div>'
                         % e(nxt.strftime("%B %-d").upper()), " hardcover hs-cov"),
                 fb.page("Coming Soon", '<div class="hs-toc"><h2>Coming %s</h2><p class="hs-edl">Every month the Garden\'s classiest glossy puts one of its own machines on the centerfold, '
                         'sits an agent down for the Hashish Interview, and names a Strain of the Month.<span>— Disco Stu, Editor</span></p></div>' % e(nxt.strftime("%B %-d"))),
                 fb.page("Back Page", '<div class="gum"><span>HASHISH · THE GARDEN\'S GLOSSY</span></div><div class="pb-body">%s<h2 class="pb-title">HASHISH</h2>%s</div>'
                         % (seal, fb.back_codes(REPO, "Hashish")), " hardcover back")]
        html = fb.book(pages, date=nxt.isoformat(), no=1, lists={}, paper="HASHISH", motto="The Garden's glossy", gum="HASHISH · THE GARDEN'S GLOSSY", price="PRICE: ONE PINCH",
                       delivered="EDITED BY DISCO STU", flap="Hashish · the Garden's glossy", body_class="pub-hs", est="THE GARDEN'S GLOSSY")
        open(os.path.join(SITE, "index.html"), "w").write(html.replace('href="../', 'href="').replace('src="../', 'src="'))
        pk.latest(SITE, "Hashish", today.isoformat(), "First issue %s" % nxt.strftime("%B %-d"), "", [])
    pk.archive_page(SITE, os.path.join(ROOT, fb.CSS_FILE), "pub-hs", "Hashish", "every issue",
                    "".join('<li><a href="issues/%s.html">%s</a></li>' % (x, pk.nice(x + "-01", "%B %Y")) for x in eds), "💋")
    print("hashish built:", eds[:1])


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else None)
