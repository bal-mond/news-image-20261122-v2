#!/usr/bin/env python3
"""Sum up 22 November 2026's world news in one image.

Renders a 1024x1024 newspaper front page (32 dated stories, 7 regions)
with Pillow only. No network, no randomness, no timestamps: the same
input always produces the same bytes. Writes to $MAKEFUN_OUTPUT_DIR
(default /output), or ./out when that is not writable.
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (22, 21, 19)
RED = (178, 32, 44)
NAVY = (26, 43, 74)
GREY = (90, 86, 78)
RULE = (180, 172, 156)
HERO_BG = (255, 255, 255)
TICKER_BG = (26, 43, 74)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def wrap(draw, text, fnt, max_w, max_lines):
    """Greedy word wrap, capped at max_lines; last line gets an ellipsis."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
        if len(lines) == max_lines:
            break
    if len(lines) < max_lines and cur:
        lines.append(cur)
    elif len(lines) == max_lines and cur and lines[-1] != cur:
        # text overflowed: ellipsize the final line
        last = lines[-1]
        while last and draw.textlength(last + "…", font=fnt) > max_w:
            last = last.rsplit(" ", 1)[0] if " " in last else last[:-1]
        lines[-1] = last + "…"
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


# (kicker, headline, body, source) — every story happened or was first
# reported on Sunday 22 November 2026.
HERO = [
    ("CLIMATE  •  ANTALYA", "COP31 COLLAPSES — NO DEAL",
     "UN climate talks end with no deal as the EU rejects a text that never "
     "mentions fossil fuels.",
     "Reuters / AP / AFP"),
    ("WAR  •  GULF", "IRAN STRIKES US BASES IN BAHRAIN",
     "Missiles and drones hit US bases; Bahrain says a civilian site was "
     "hit and two people hurt.",
     "Reuters / AFP / Al Jazeera"),
    ("MEXICO  •  SINALOA", "MEXICO CAPTURES 'EL CHAPO ISIDRO'",
     "Special forces seize cartel boss Fausto Isidro Meza Flores; 11 are "
     "killed in the raid.",
     "AP / Al Jazeera"),
]

COLUMNS = [
    ("WAR & DIPLOMACY", [
        ("UKRAINE", "Russian drone hits flats in Dymer",
         "2 killed, 11 missing — incl. two children — as a drone strikes a "
         "five-storey block north of Kyiv.", "Al Jazeera / AP"),
        ("UKRAINE", "Missile hits Kryvyi Rih",
         "A 7-year-old boy and a 20-year-old woman are killed and 60 wounded "
         "in Zelenskyy's hometown.", "AP / CNN"),
        ("LIBYA", "Russian corvette 'destroyed' at Benghazi",
         "Suspected Ukrainian sea drones hit the Merkury at its naval base; "
         "10 hurt, the ship later capsizes.", "AP / Reuters / BBC Verify"),
        ("WEST BANK", "Settlers torch 12 Palestinian vehicles",
         "Arson and racist graffiti hit four villages near Ramallah "
         "overnight.", "Reuters / AP"),
        ("SUDAN", "Drone strikes hit Khartoum",
         "A UN facility is damaged while staff are inside; at least 3 are "
         "killed in a house in Omdurman.", "Reuters / AP"),
        ("DENMARK", "Copenhagen expels Russian defence attache",
         "Russia is accused of plotting to kill a Ukrainian rapper at a "
         "concert; Moscow denies it.", "Al Jazeera / Reuters"),
        ("USA–CANADA", "Pentagon curbs US–Canada defence ties",
         "Defence Secretary Hegseth imposes new restrictions in a "
         "classified memo, the Post reports.", "Washington Post"),
        ("USA–ISRAEL", "US, Israel plan for escalation on Iran",
         "The allies agree joint plans for a possible escalation as the "
         "tanker war spreads.", "Reuters"),
        ("SOUTH KOREA", "Education minister quits over AI exam row",
         "The minister resigns after last-minute rule changes to stop "
         "AI-assisted cheating.", "BBC / Reuters"),
        ("UN", "China renews push to sanction BLA",
         "Beijing presses the Security Council to sanction the Baloch "
         "Liberation Army's Majeed Brigade.", "Reuters"),
    ]),
    ("AMERICAS & MARKETS", [
        ("USA", "Democrats' biggest House win since 1992",
         "At least 258 of 435 seats after a North Carolina win; the Senate "
         "is projected 56–44 Democrat.", "AP"),
        ("USA", "Trump orders contractors to clear Congress",
         "An executive order tells federal contractors to consult the White "
         "House before answering Congress.", "AP / Reuters"),
        ("USA", "Trump backs a 10% credit-card cap",
         "The president says he will work with Democrats to cap rates; "
         "lenders warn of tighter credit.", "AP"),
        ("USA", "FBI probes hack of its crime database",
         "An apparent intrusion into the National Crime Information Center; "
         "the extent is unclear.", "AP"),
        ("USA", "ICE detains father and daughter in Seattle",
         "The pair are held on a jet bridge while boarding a flight to a "
         "family baptism.", "AP"),
        ("USA", "Bessent warns Fed not to overtighten",
         "The Treasury chief, on CBS Sunday, cites hawkish governors and "
         "tight financial conditions.", "Reuters / CBS"),
        ("MARKETS", "Wall Street's worst week since Covid",
         "The S&P 500 falls 3.7% on Friday to 6,910 as doubts grow over "
         "AI spending.", "Reuters"),
        ("MARKETS", "Asian shares fall after the US rout",
         "Markets slide across the region as the S&P 500 drops into a "
         "correction.", "AP"),
        ("TECH", "Anthropic's record IPO lifts nonprofits",
         "The biggest IPO ever raises hopes of a charitable windfall for "
         "nonprofits preparing to scale.", "AP"),
        ("TECH", "US probes Nvidia chip-export links",
         "The intelligence chief confirms a probe of Alice Huang and "
         "Singapore firm Megaspeed.", "ABC / Reuters"),
    ]),
    ("SCIENCE, SPORT & CULTURE", [
        ("SPACE", "BepiColombo reaches orbit around Mercury",
         "After an eight-year trip, only the second mission ever to orbit "
         "Mercury; a thruster glitch is reported.", "ESA / Reuters"),
        ("PAKISTAN", "Lahore again the world's most polluted city",
         "AQI hits 538 on Sunday morning; eight Punjab cities are among "
         "Pakistan's ten worst.", "Dawn / IQAir"),
        ("JAPAN", "Shuri Castle's main hall restored",
         "Okinawa celebrates the rebuild, seven years after fire destroyed "
         "the castle in 2019.", "AP / Reuters"),
        ("INDONESIA", "Candy factory fire: 3 dead, 36 missing",
         "Rescuers recover 24 body bags from the Cikande blaze on Sunday; "
         "dozens are still missing.", "AP / Reuters"),
        ("NIGERIA", "Boat accident death toll rises to 24",
         "At least 24 die when a crowded boat carrying passengers "
         "capsizes.", "Reuters"),
        ("BASEBALL", "Skubal signs record $450m Mets deal",
         "Nine years for the top free-agent pitcher, days before a possible "
         "lockout.", "AP"),
        ("CULTURE", "Miley Cyrus marries Maxx Morando",
         "An intimate Palm Springs wedding on Sunday for the singer and the "
         "rock drummer.", "AP"),
        ("NFL  •  WEEK 11", "Sunday scores: Cowboys 51, Titans 30",
         "Chiefs 34–7 Cardinals; Giants edge Jaguars 23–18; Jets beat "
         "Chargers 27–24.", "AP / ESPN"),
        ("OBITUARY", "Tom Jackson, Broncos star, dies at 75",
         "The former linebacker and 'Sunday NFL Countdown' analyst is "
         "remembered.", "AP"),
    ]),
]

TICKER = ("COP31: NO DEAL  •  IRAN STRIKES US BASES  •  MEXICO NABS EL CHAPO "
          "ISIDRO  •  S&P 500 −3.7%  •  SKUBAL $450M TO METS  •  LAHORE AQI 538")


def draw_masthead(d):
    d.rectangle([0, 0, W, 4], fill=RED)
    d.text((24, 16), "THE WORLD IN ONE DAY", font=font(SERIF_B, 46), fill=INK)
    d.text((24, 70), "SUNDAY  •  22 NOVEMBER 2026",
           font=font(SANS_B, 17), fill=RED)
    d.text((24, 70), "", font=font(SANS_B, 17), fill=INK)
    right = "32 STORIES  •  WORLDWIDE  •  ONE DAY"
    d.text((W - 24 - d.textlength(right, font=font(SANS_B, 15)),
            72), right, font=font(SANS_B, 15), fill=GREY)
    d.line([24, 98, W - 24, 98], fill=RULE, width=2)


def draw_hero(d):
    y0, y1 = 108, 250
    xs = [24, 352, 680]
    wbox = 320
    for i, (kick, head, body, src) in enumerate(HERO):
        x = xs[i]
        d.rectangle([x, y0, x + wbox, y1], outline=RULE, width=1, fill=HERO_BG)
        d.rectangle([x, y0, x + wbox, y0 + 4], fill=RED)
        d.text((x + 12, y0 + 12), f"{i + 1}.  {kick}",
               font=font(SANS_B, 11), fill=RED)
        lines = wrap(d, head, font(SERIF_B, 19), wbox - 24, 2)
        yy = draw_lines(d, x + 12, y0 + 34, lines, font(SERIF_B, 19), INK, 23)
        blines = wrap(d, body, font(SANS, 12), wbox - 24, 2)
        yy = draw_lines(d, x + 12, yy + 4, blines, font(SANS, 12), INK, 15)
        d.text((x + 12, y1 - 18), src, font=font(SANS, 9), fill=GREY)


def draw_columns(d, body_size=10):
    """Draw the three story columns. Returns True if everything fits."""
    y_top, y_bot = 262, 940
    xs = [24, 352, 680]
    wcol = 320
    head_f = font(SANS_B, 12)
    body_f = font(SANS, body_size)
    kick_f = font(SANS_B, 9)
    for ci, (title, stories) in enumerate(COLUMNS):
        x = xs[ci]
        d.rectangle([x, y_top, x + wcol, y_top + 24], fill=NAVY)
        d.text((x + 10, y_top + 5), title, font=font(SANS_B, 12), fill=(255, 255, 255))
        d.text((x + wcol - 10 - d.textlength(str(len(stories)), font=font(SANS_B, 12)),
                y_top + 5), str(len(stories)), font=font(SANS_B, 12), fill=(255, 255, 255))
        y = y_top + 31
        for kick, head, body, src in stories:
            d.text((x, y), f"{kick}  —  {src}", font=kick_f, fill=RED)
            y += 12
            hl = wrap(d, head, head_f, wcol, 2)
            y = draw_lines(d, x, y, hl, head_f, INK, 15)
            bl = wrap(d, body, body_f, wcol, 2)
            y = draw_lines(d, x, y + 1, bl, body_f, (60, 58, 52),
                           body_size + 3)
            y += 5
            d.line([x, y, x + wcol, y], fill=RULE, width=1)
            y += 5
            if y > y_bot:
                return False
    return True


def draw_footer(d):
    d.rectangle([0, 944, W, 984], fill=TICKER_BG)
    d.text((24, 954), "TICKER  •  " + TICKER, font=font(SANS_B, 10),
           fill=(255, 255, 255))
    d.text((24, 994), "All events of Sunday 22 November 2026. Sources: Reuters  •  AP  •  "
           "AFP  •  Al Jazeera  •  BBC  •  ESA  •  Dawn  •  CBS  •  Washington Post",
           font=font(SANS, 10), fill=GREY)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_hero(d)
    # Shrink body text until the columns fit (legibility guard).
    for size in (10, 9, 8):
        trial = Image.new("RGB", (W, H), PAPER)
        td = ImageDraw.Draw(trial)
        draw_masthead(td)
        draw_hero(td)
        if draw_columns(td, size):
            img, d = trial, td
            break
    else:
        raise RuntimeError("columns do not fit even at smallest body size")
    draw_footer(d)
    return img


def verify_output(path):
    """Re-open the written file and enforce the competition gate.

    Exits non-zero (with the reason on stderr) when the file is missing,
    too large, the wrong size, or not a loadable PNG.
    """
    import hashlib
    if not os.path.isfile(path):
        print(f"ERROR: output missing: {path}", file=sys.stderr)
        sys.exit(1)
    size = os.path.getsize(path)
    if size > 1048576:
        print(f"ERROR: output {size} bytes exceeds 1 MiB", file=sys.stderr)
        sys.exit(1)
    try:
        with Image.open(path) as im:
            im.verify()
        with Image.open(path) as im:
            im.load()
            if im.size != (W, H) or im.format != "PNG":
                print(f"ERROR: bad image {im.size} {im.format}",
                      file=sys.stderr)
                sys.exit(1)
    except SystemExit:
        raise
    except Exception as exc:
        print(f"ERROR: output failed to verify: {exc}", file=sys.stderr)
        sys.exit(1)
    digest = hashlib.sha256(open(path, "rb").read()).hexdigest()
    print(f"verified {path}: {size} bytes, {W}x{H} PNG, sha256={digest}")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        os.makedirs(out_dir, exist_ok=True)
        probe = os.path.join(out_dir, ".write-test")
        with open(probe, "w") as fh:
            fh.write("ok")
        os.remove(probe)
    except Exception:
        out_dir = "out"
        os.makedirs(out_dir, exist_ok=True)
    img = render()
    path = os.path.join(out_dir, "entry.png")
    img.save(path, format="PNG", optimize=True)
    print("wrote", path, img.size)
    verify_output(path)


if __name__ == "__main__":
    main()
