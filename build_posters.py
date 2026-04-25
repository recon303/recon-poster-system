#!/usr/bin/env python3
"""
RECON Poster System — Build Script
Generates 14 standalone poster HTML files from the system config.

Usage:
    python3 build_posters.py

Outputs all HTML files into the posters/ subfolder.
Run generate_images.py first to populate assets/ with hero images.
"""

from pathlib import Path
import json

ROOT = Path(__file__).parent

PILLARS = {
    "activate": {"hex": "#2DE3C8", "label": "ACTIVATE", "ink": "#0A1F1B", "protocol": "ACTIVATE / CIRCULATE"},
    "renew":    {"hex": "#3FA9F5", "label": "RENEW",    "ink": "#051522", "protocol": "RECON RENEW PROTOCOL"},
    "restore":  {"hex": "#E85D3A", "label": "RESTORE",  "ink": "#1F0A06", "protocol": "RESTORE RED LIGHT"},
}

POSTERS = [
    dict(id="vol04-output",      pillar="renew",    heroImg="hero-kettlebell.jpg",        topLine1="OWN",   topLine2="THE", closer="OUTPUT",  giantLetter="O", letterSize="90cqw",  letterTransform="translate(-2%, 12%)", heroObjectPosition="42% 28%", heroFilter="grayscale(0.4) contrast(1.22) brightness(0.72) saturate(0.5) hue-rotate(-6deg)",   subjectFilter="grayscale(1) contrast(1.7) brightness(0.95) saturate(0)",  edition="VOL.04", year="2026", sessionCode="RNW–08", fileCode="FILE 008/2026", locations="DENVER, CO",  bodyCopy="Output is earned. The body is the vehicle. Service it like one. Sixty minutes. Three modalities. Zero guesswork."),
    dict(id="vol05-break",       pillar="activate", heroImg="hero-sprinter.jpg",          topLine1="BREAK", topLine2="THE", closer="LINE",    giantLetter="L", letterSize="100cqw", letterTransform="translate(2%, 16%)",  heroObjectPosition="55% 35%", heroFilter="grayscale(0.65) contrast(1.32) brightness(0.62) saturate(0.35) hue-rotate(-10deg)", subjectFilter="grayscale(1) contrast(1.85) brightness(0.95) saturate(0)", edition="VOL.05", year="2026", sessionCode="ACT–12", fileCode="FILE 009/2026", locations="DENVER, CO",  bodyCopy="First step decides the race. Activate the circulation. Prime the system. Then go."),
    dict(id="vol06-view",        pillar="renew",    heroImg="hero-mtb.jpg",               topLine1="EARN",  topLine2="THE", closer="VIEW",    giantLetter="V", letterSize="108cqw", letterTransform="translate(0%, 14%)",  heroObjectPosition="52% 38%", heroFilter="grayscale(0.7) contrast(1.3) brightness(0.78) saturate(0.4) hue-rotate(-8deg)",   subjectFilter="grayscale(1) contrast(1.9) brightness(0.95) saturate(0)",  edition="VOL.06", year="2026", sessionCode="RNW–14", fileCode="FILE 010/2026", locations="BACKCOUNTRY", bodyCopy="The summit is the receipt. Climb hard. Recover harder. The mountain remembers what you spent to be there."),
    dict(id="vol07-burn",        pillar="restore",  heroImg="hero-sprinter-stadium.jpg",  topLine1="BURN",  topLine2="THE", closer="LANE",    giantLetter="L", letterSize="100cqw", letterTransform="translate(0%, 14%)",  heroObjectPosition="50% 38%", heroFilter="contrast(1.28) brightness(0.7) saturate(1.6) hue-rotate(-150deg)",                   subjectFilter="grayscale(1) contrast(1.85) brightness(1) saturate(0)",    edition="VOL.07", year="2026", sessionCode="RST–03", fileCode="FILE 011/2026", locations="TRACK / EMPTY HOUSE", bodyCopy="No crowd. No excuses. Just the lane and the clock. Ignite the system. Empty the tank. Then do it again."),
    dict(id="vol08-form",        pillar="activate", heroImg="hero-vol08-form.jpg",        topLine1="HOLD",  topLine2="THE", closer="FORM",    giantLetter="F", letterSize="95cqw",  letterTransform="translate(-4%, 10%)", heroObjectPosition="42% 22%", heroFilter="grayscale(0.5) contrast(1.3) brightness(0.65) saturate(0.45) hue-rotate(160deg)",  subjectFilter="grayscale(1) contrast(1.8) brightness(0.95) saturate(0)",  edition="VOL.08", year="2026", sessionCode="ACT–09", fileCode="FILE 012/2026", locations="DENVER, CO",  bodyCopy="Technique is the rep that compounds. Break form and you're moving iron. Build the pattern. The weight follows."),
    dict(id="vol09-edge",        pillar="restore",  heroImg="hero-vol09-edge.jpg",        topLine1="FIND",  topLine2="THE", closer="EDGE",    giantLetter="E", letterSize="100cqw", letterTransform="translate(-1%, 12%)", heroObjectPosition="55% 32%", heroFilter="grayscale(0.55) contrast(1.35) brightness(0.68) saturate(0.6) hue-rotate(10deg)",   subjectFilter="grayscale(1) contrast(1.9) brightness(0.95) saturate(0)",  edition="VOL.09", year="2026", sessionCode="RST–07", fileCode="FILE 013/2026", locations="BACKCOUNTRY", bodyCopy="The trail beyond the trail. Go until the map runs out. That's where the real work starts."),
    dict(id="vol10-base",        pillar="activate", heroImg="hero-vol10-base.jpg",        topLine1="BUILD", topLine2="THE", closer="BASE",    giantLetter="B", letterSize="98cqw",  letterTransform="translate(-2%, 14%)", heroObjectPosition="50% 40%", heroFilter="grayscale(0.6) contrast(1.28) brightness(0.64) saturate(0.4) hue-rotate(-16deg)",  subjectFilter="grayscale(1) contrast(1.85) brightness(0.95) saturate(0)", edition="VOL.10", year="2026", sessionCode="ACT–15", fileCode="FILE 014/2026", locations="DENVER, CO",  bodyCopy="Speed is a symptom. Base fitness is the condition. Build the bottom and everything else rises from there."),
    dict(id="vol11-pace",        pillar="renew",    heroImg="hero-vol11-pace.jpg",        topLine1="PUSH",  topLine2="THE", closer="PACE",    giantLetter="P", letterSize="96cqw",  letterTransform="translate(0%, 14%)",  heroObjectPosition="55% 35%", heroFilter="grayscale(0.55) contrast(1.32) brightness(0.66) saturate(0.38) hue-rotate(-4deg)", subjectFilter="grayscale(1) contrast(1.85) brightness(0.95) saturate(0)", edition="VOL.11", year="2026", sessionCode="RNW–11", fileCode="FILE 015/2026", locations="DENVER, CO",  bodyCopy="The splits don't lie. Neither does the body. Set the pace. Hold it. Then push it one second further."),
    dict(id="vol12-drop",        pillar="activate", heroImg="hero-vol12-drop.jpg",        topLine1="TRUST", topLine2="THE", closer="DROP",    giantLetter="D", letterSize="104cqw", letterTransform="translate(1%, 11%)",  heroObjectPosition="50% 42%", heroFilter="grayscale(0.6) contrast(1.3) brightness(0.7) saturate(0.5) hue-rotate(175deg)",   subjectFilter="grayscale(1) contrast(1.9) brightness(0.95) saturate(0)",  edition="VOL.12", year="2026", sessionCode="ACT–18", fileCode="FILE 016/2026", locations="BACKCOUNTRY", bodyCopy="You don't descend a mountain. You commit to it. Trust your inputs. The trail rewards conviction."),
    dict(id="vol13-reps",        pillar="restore",  heroImg="hero-vol13-reps.jpg",        topLine1="FORGE", topLine2="THE", closer="REPS",    giantLetter="R", letterSize="92cqw",  letterTransform="translate(-3%, 13%)", heroObjectPosition="42% 30%", heroFilter="grayscale(0.45) contrast(1.32) brightness(0.66) saturate(0.7) hue-rotate(-140deg)", subjectFilter="grayscale(1) contrast(1.8) brightness(0.95) saturate(0)",  edition="VOL.13", year="2026", sessionCode="RST–11", fileCode="FILE 017/2026", locations="DENVER, CO",  bodyCopy="One rep earns the next. Consistency is the only strategy that has never failed. Forge it rep by rep."),
    dict(id="vol14-moment",      pillar="renew",    heroImg="hero-vol14-moment.jpg",      topLine1="CLAIM", topLine2="THE", closer="MOMENT",  giantLetter="M", letterSize="80cqw",  letterTransform="translate(0%, 16%)",  heroObjectPosition="50% 38%", heroFilter="grayscale(0.5) contrast(1.25) brightness(0.72) saturate(0.42) hue-rotate(-2deg)", subjectFilter="grayscale(1) contrast(1.85) brightness(0.95) saturate(0)", edition="VOL.14", year="2026", sessionCode="RNW–17", fileCode="FILE 018/2026", locations="DENVER, CO",  bodyCopy="The race doesn't wait. Neither does the window. When the body says go — go. Every second is a decision."),
    dict(id="vol15-grade",       pillar="renew",    heroImg="hero-vol15-grade.jpg",       topLine1="RISE",  topLine2="THE", closer="GRADE",   giantLetter="G", letterSize="92cqw",  letterTransform="translate(-2%, 13%)", heroObjectPosition="54% 36%", heroFilter="grayscale(0.65) contrast(1.28) brightness(0.74) saturate(0.38) hue-rotate(-10deg)", subjectFilter="grayscale(1) contrast(1.9) brightness(0.95) saturate(0)",  edition="VOL.15", year="2026", sessionCode="RNW–20", fileCode="FILE 019/2026", locations="BACKCOUNTRY", bodyCopy="The grade is honest. It doesn't care about excuses. Elevation is earned one meter at a time. Rise to it."),
    dict(id="vol16-tempo",       pillar="restore",  heroImg="hero-vol16-tempo.jpg",       topLine1="KEEP",  topLine2="THE", closer="TEMPO",   giantLetter="T", letterSize="88cqw",  letterTransform="translate(0%, 15%)",  heroObjectPosition="55% 37%", heroFilter="contrast(1.32) brightness(0.68) saturate(1.5) hue-rotate(-145deg)",                   subjectFilter="grayscale(1) contrast(1.85) brightness(1) saturate(0)",    edition="VOL.16", year="2026", sessionCode="RST–14", fileCode="FILE 020/2026", locations="DENVER, CO",  bodyCopy="Rhythm is durability. Find the frequency your body can sustain. Then hold it longer than you thought you could."),
    dict(id="vol17-system",      pillar="activate", heroImg="hero-vol17-system.jpg",      topLine1="WORK",  topLine2="THE", closer="SYSTEM",  giantLetter="S", letterSize="85cqw",  letterTransform="translate(-2%, 14%)", heroObjectPosition="42% 25%", heroFilter="grayscale(0.5) contrast(1.28) brightness(0.68) saturate(0.55) hue-rotate(155deg)", subjectFilter="grayscale(1) contrast(1.8) brightness(0.95) saturate(0)",  edition="VOL.17", year="2026", sessionCode="ACT–22", fileCode="FILE 021/2026", locations="DENVER, CO",  bodyCopy="Recovery is training. Sleep is training. Nutrition is training. The body is always listening. Give it something worth hearing."),
]

POSTER_CSS = """
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap');
@font-face { font-family:'Rajdhani'; src:url('../fonts/Rajdhani-Bold.ttf') format('truetype'); font-weight:700; }
@font-face { font-family:'Montserrat'; src:url('../fonts/Montserrat-VariableFont_wght.ttf') format('truetype-variations'); font-weight:100 900; }

*, *::before, *::after { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: #080A0C; display: flex; align-items: center; justify-content: center; min-height: 100vh; }

.poster-wrap { width: min(720px, 100vw); aspect-ratio: 720/1000; position: relative; }

.poster {
  position: relative; width: 100%; height: 100%;
  background: #080A0C; overflow: hidden;
  isolation: isolate; container-type: inline-size;
}
.hero { position: absolute; inset: 0; z-index: 1; }
.hero-img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.hero-vignette {
  position: absolute; inset: 0; pointer-events: none;
  background:
    radial-gradient(ellipse 90% 80% at 50% 45%, transparent 30%, rgba(8,10,12,0.55) 75%, rgba(8,10,12,0.92) 100%),
    linear-gradient(180deg, rgba(8,10,12,0.45) 0%, transparent 25%, transparent 70%, rgba(8,10,12,0.85) 100%);
}
.hero-grain {
  position: absolute; inset: 0; pointer-events: none; opacity: 0.04; mix-blend-mode: overlay;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.6 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");
}
.giant-letter-wrap { position: absolute; inset: 0; z-index: 2; pointer-events: none; display: flex; align-items: center; justify-content: center; }
.giant-letter { font-family: 'Rajdhani', sans-serif; font-weight: 700; line-height: 0.78; color: var(--accent); letter-spacing: -0.04em; }
.hero-masked { position: absolute; inset: 0; z-index: 3; pointer-events: none; mix-blend-mode: lighten; }
.corner { position: absolute; z-index: 5; color: var(--accent); }
.tl { top: 32px; left: 32px; }
.tr { top: 32px; right: 32px; }
.bl { bottom: 142px; left: 32px; max-width: 44%; }
.br { bottom: 230px; right: 32px; text-align: right; }
.tl-logo { width: 156px; }
.tl-logo img { width: 100%; height: auto; display: block; }
.meta-row { display: flex; flex-direction: column; align-items: flex-end; gap: 3px; }
.mono { font-family: 'JetBrains Mono', monospace; font-size: 12px; font-weight: 700; letter-spacing: 0.08em; color: var(--accent); text-transform: uppercase; text-shadow: 0 1px 6px rgba(8,10,12,0.85); }
.headline-top { position: absolute; z-index: 5; top: 64px; right: 32px; font-family: 'Rajdhani', sans-serif; font-weight: 700; font-size: clamp(58px, 10.5cqw, 104px); line-height: 0.88; letter-spacing: 0.005em; text-transform: uppercase; color: var(--accent); text-align: right; text-shadow: 0 2px 14px rgba(8,10,12,0.7); }
.headline-top > div + div { margin-top: -0.04em; }
.hairline { position: absolute; left: 32px; right: 32px; bottom: 112px; height: 1px; background: var(--accent); opacity: 0.6; z-index: 5; }
.body { font-family: 'Montserrat', sans-serif; font-size: 13px; font-weight: 700; line-height: 1.5; color: var(--accent); margin: 0 0 16px 0; max-width: 30ch; text-wrap: pretty; letter-spacing: 0.005em; text-shadow: 0 1px 8px rgba(8,10,12,0.9); }
.footer-eyebrow { display: flex; align-items: center; gap: 8px; font-family: 'Rajdhani', sans-serif; font-weight: 700; font-size: 11.5px; letter-spacing: 0.22em; text-transform: uppercase; color: var(--accent); text-shadow: 0 1px 8px rgba(8,10,12,0.9); }
.footer-eyebrow .dot { width: 5px; height: 5px; background: var(--accent); display: inline-block; }
.locations { font-family: 'Rajdhani', sans-serif; font-weight: 700; font-size: 16px; letter-spacing: 0.15em; text-transform: uppercase; color: var(--accent); line-height: 1.35; margin-bottom: 10px; text-shadow: 0 1px 8px rgba(8,10,12,0.9); }
.closer { position: absolute; z-index: 5; bottom: 38px; right: 32px; font-family: 'Rajdhani', sans-serif; font-weight: 700; font-size: clamp(72px, 13cqw, 132px); line-height: 0.85; letter-spacing: 0.005em; text-transform: uppercase; color: var(--accent); text-shadow: 0 2px 18px rgba(8,10,12,0.7); }
.closer .period { display: inline-block; margin-left: 0.02em; }
.instrument { position: absolute; z-index: 5; left: 32px; bottom: 38px; display: flex; gap: 10px; align-items: center; font-family: 'JetBrains Mono', monospace; font-size: 11px; font-weight: 700; letter-spacing: 0.12em; color: var(--accent); text-shadow: 0 1px 8px rgba(8,10,12,0.9); }
"""

JSX_TEMPLATE = """
const PILLARS = {{
  activate: {{ hex: "#2DE3C8", protocol: "ACTIVATE / CIRCULATE" }},
  renew:    {{ hex: "#3FA9F5", protocol: "RECON RENEW PROTOCOL" }},
  restore:  {{ hex: "#E85D3A", protocol: "RESTORE RED LIGHT" }},
}};

const CONFIG = {config_json};

function Poster() {{
  const pillar = PILLARS[CONFIG.pillar] || PILLARS.renew;
  const ACCENT = pillar.hex;

  return (
    <div className="poster-wrap">
      <div className="poster" style={{{{ "--accent": ACCENT }}}}>
        <div className="hero">
          <img src={{"assets/" + CONFIG.heroImg}} alt="" className="hero-img"
            style={{{{ filter: CONFIG.heroFilter, objectPosition: CONFIG.heroObjectPosition }}}} />
          <div className="hero-vignette" />
          <div className="hero-grain" />
        </div>

        <div className="giant-letter-wrap" style={{{{ opacity: 1 }}}}>
          <span className="giant-letter"
            style={{{{ fontSize: CONFIG.letterSize, transform: CONFIG.letterTransform }}}}>
            {{CONFIG.giantLetter}}
          </span>
        </div>

        <div className="hero-masked" aria-hidden="true">
          <img src={{"assets/" + CONFIG.heroImg}} alt="" className="hero-img"
            style={{{{ filter: CONFIG.subjectFilter, objectPosition: CONFIG.heroObjectPosition }}}} />
        </div>

        <div className="corner tl">
          <div className="tl-logo"><img src="assets/recon-vertical-whiteblue.png" alt="RECON" /></div>
        </div>

        <div className="corner tr">
          <div className="meta-row">
            <span className="mono" style={{{{ fontWeight:"900" }}}}>{{CONFIG.edition}}</span>
            <span className="mono">{{CONFIG.year}}</span>
          </div>
        </div>

        <div className="headline-top">
          <div>{{CONFIG.topLine1}}</div>
          <div>{{CONFIG.topLine2}}</div>
        </div>

        <div className="hairline" />

        <div className="corner bl">
          <p className="body">{{CONFIG.bodyCopy}}</p>
          <div className="footer-eyebrow">
            <span className="dot" />
            <span>{{pillar.protocol}}</span>
          </div>
        </div>

        <div className="corner br">
          <div className="locations">
            {{CONFIG.locations.split("/").map((loc, i) => <div key={{i}}>{{loc.trim()}}</div>)}}
          </div>
        </div>

        <div className="closer">{{CONFIG.closer}}<span className="period">.</span></div>

        <div className="instrument">
          <span className="mono">SESSION {{CONFIG.sessionCode}}</span>
          <span className="mono">·</span>
          <span className="mono">{{CONFIG.fileCode}}</span>
        </div>
      </div>
    </div>
  );
}}

ReactDOM.createRoot(document.getElementById("root")).render(<Poster />);
"""

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>RECON · {title}</title>
  <style>{css}</style>
</head>
<body>
  <div id="root"></div>
  <script src="https://unpkg.com/react@18.3.1/umd/react.production.min.js" crossorigin></script>
  <script src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.production.min.js" crossorigin></script>
  <script src="https://unpkg.com/@babel/standalone@7.29.0/babel.min.js" crossorigin></script>
  <script type="text/babel">
{jsx}
  </script>
</body>
</html>
"""


def build_poster_html(poster: dict) -> str:
    pillar_info = PILLARS[poster["pillar"]]
    config_fields = {
        "pillar":             poster["pillar"],
        "heroImg":            poster["heroImg"],
        "heroFilter":         poster["heroFilter"],
        "subjectFilter":      poster["subjectFilter"],
        "heroObjectPosition": poster["heroObjectPosition"],
        "giantLetter":        poster["giantLetter"],
        "letterSize":         poster["letterSize"],
        "letterTransform":    poster["letterTransform"],
        "topLine1":           poster["topLine1"],
        "topLine2":           poster["topLine2"],
        "closer":             poster["closer"],
        "edition":            poster["edition"],
        "year":               poster["year"],
        "sessionCode":        poster["sessionCode"],
        "fileCode":           poster["fileCode"],
        "locations":          poster["locations"],
        "bodyCopy":           poster["bodyCopy"],
    }
    config_json = json.dumps(config_fields, indent=4)
    jsx = JSX_TEMPLATE.format(config_json=config_json)
    title = f"{poster['topLine1']} THE {poster['closer']}. — {poster['edition']}"
    return HTML_TEMPLATE.format(title=title, css=POSTER_CSS, jsx=jsx)


def main():
    out_dir = ROOT / "posters"
    out_dir.mkdir(exist_ok=True)

    for poster in POSTERS:
        html = build_poster_html(poster)
        out_path = out_dir / f"{poster['id']}.html"
        out_path.write_text(html, encoding="utf-8")
        print(f"  Built → posters/{poster['id']}.html")

    print(f"\nDone — {len(POSTERS)} posters in posters/")


if __name__ == "__main__":
    main()
