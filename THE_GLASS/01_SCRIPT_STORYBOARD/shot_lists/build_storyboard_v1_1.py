"""Build THE_GLASS storyboard v1.1 from the read-only v1.0 original.

Applies the v004 script corrections (February 2004 attempt, Malaga internet-cafe
arrest), fixes the SH-060 column misalignment, adds source-class columns and a
CHANGE LOG sheet, translates the whole workbook from Norwegian to English
(translation_no_en.json), and exports shot_tracker.csv.

Run:  python3 build_storyboard_v1_1.py   (from any directory)
"""
import copy
import csv
import json
import pathlib
import re

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "01_SCRIPT_STORYBOARD/originals/THE_GLASS_102_shot_storyboard_v1.0.xlsx"
DST = ROOT / "01_SCRIPT_STORYBOARD/revised/THE_GLASS_102_shot_storyboard_v1.1.xlsx"
TRACKER = ROOT / "00_PROJECT_MANAGEMENT/shot_tracker.csv"

# Column letters in SHOTBOARD
C = dict(id="A", start="B", end="C", sec="D", type="E", section="F", vo="G", visual="H",
         camera="I", layers="J", anim="K", trans="L", sound="M", fact="N", note="O",
         assets="P", prio="Q", status="R", words="S")

SEC_3D1 = "3D 1 · Through the Glass"
SEC_03A = "03a · The First Time"
SEC_03B = "03b · Back to the Drawing Board"

# ---------------------------------------------------------------- shot edits
EDITS = {
    "SH-006": dict(visual="Splittet glasspeil med fire korte refleksjoner: maskert figur, slegge, politimann, kafévindu i Málaga.",
                   layers="L01 shard-masker; L02 figur; L03 slegge; L04 offisersilhuett; L05 Málaga-kafé"),
    "SH-028": dict(section=SEC_03A),
    "SH-029": dict(section=SEC_03A, vo="The fifth of April was not the first time they came for NOKAS.",
                   visual="Kalenderkort FEB 2004 skyves inn; stempel «AVBLÅST» lander.",
                   anim="Kortet skyves inn; stempel slår ned med liten rist",
                   fact="Dokumentert: februar-forsøket ble avblåst (S04, S05). Toska nektet i retten for at det var et forsøk (S04).",
                   note="Ikke vis metode for februar-forsøket; kun dato + avblåst."),
    "SH-030": dict(section=SEC_03A, vo="Two months earlier, Toska was already inside the courtyard.",
                   visual="Pennen river papiret; riften blir glassprekk som sprenges mot kamera.",
                   fact="Dokumentert: Toska lå i bakgården i februar 2004 (S04, S05)."),
    "SH-031": dict(section=SEC_3D1, vo="— (ingen VO)",
                   visual="Mørk vintermorgen. Rim på steinene i NOKAS-bakgården. Ett opplyst vindu; under det en enslig figur sammenkrøpet mot muren.",
                   camera="Kran fra takhøyde til lav kamerahøyde bak figuren; 24→35 mm",
                   layers="M01 bakgård; M02 ramme+rute (opplyst); M03b Toska-silhuett (huket); M04b vegglampe; FX01 rim/pustdamp",
                   anim="Kamera ned ~4 m i kontinuerlig bue; figuren nesten ubevegelig (pust)",
                   trans="SIGNATUR INN 1: 2D-shards flyr ut over første 3D-frame",
                   sound="Vind, fjern by, summende lampe. Ingen musikk.",
                   fact="Rekonstruert fra kilder (S04, S05); lys, vær og staging dramatisert",
                   note="PROTOTYPE v001 bygget i Blender: 05_BLENDER/scripts/build_SH031_courtyard.py",
                   assets="M01,M02,M03b,M04b,FX01"),
    "SH-032": dict(section=SEC_3D1, vo="— (ingen VO)",
                   visual="Gjennom tykt laminert glass, uskarpt: ansatte triller pengetraller bort og ut av bildet.",
                   camera="OTS 50 mm, fokus på glassflaten og refleksene",
                   layers="M02 glass; M06 tellerom (uskarpt); M20 pengetraller; M21 ansattsilhuetter",
                   anim="Silhuetter beveger seg bak glasset; kamera nesten stille",
                   trans="Matchcut fra gård til over-skulder", sound="Dempede trallehjul bak glass",
                   fact="Rekonstruert fra kilder (så penger flyttes fra kjelleren, S05); staging dramatisert",
                   note="Ansatte skal være anonyme og uskarpe.", assets="M02,M06,M20,M21"),
    "SH-033": dict(section=SEC_3D1, vo="Through the glass, he watched the money being moved away.",
                   visual="Pusten hans dugger glasset; hånden lukkes langsomt.",
                   camera="ECU 85 mm på kondens på glass", layers="M02 glass; FX01 pustdamp; M03b hånd",
                   anim="Dugg vokser/fader med pust; hånd lukkes", trans="L-kutt", sound="Pust, vind",
                   fact="Dramatisert detalj (dugg) over dokumentert hendelse (S04, S05)",
                   note="Ingen våpen i bildet.", assets="M02,M03b,FX01"),
    "SH-034": dict(section=SEC_3D1, vo="He called it off.",
                   visual="Han senker hodet og trekker seg inn i mørket. Kamera blir; dugg falmer fra glasset.",
                   camera="Statisk; langsom push 50→85 mm", layers="M01 bakgård; M02 glass; FX01 dugg",
                   anim="Push til falmende dugg fyller bildet",
                   trans="SIGNATUR UT 1: dugg → viskelærsmuss over FEB 2004 i notatbok",
                   sound="Én lav cellotone → blyant/viskelær",
                   fact="Dokumentert utfall: avblåst (S04, S05); bevegelse dramatisert",
                   note="Siste frame eksporteres som stillbilde til 2D-match.", assets="M01,M02,FX01"),
    "SH-035": dict(section=SEC_03B, vo="He had lain in that courtyard, freezing, for nothing.",
                   visual="Viskelærsmuss over FEB 2004; tom bakgårdsskisse i notatboka.",
                   anim="Smuss morph fra 3D-dugg; kort hold", trans="SIGNATUR UT 1 fullføres",
                   sound="Cello → viskelær", fact="Dokumentert (lå og frøs i bakgården, S04)"),
    "SH-036": dict(section=SEC_03B, vo="In court, Toska would later insist it was never an attempt. Only a plan.",
                   visual="Kort rettssalskisse; sitatkort «never an attempt».", camera="Grafisk insert",
                   layers="L01 rettssalskisse; L02 sitatkort", anim="Sitatkort fader inn",
                   trans="Grafisk swipe fra bok", sound="Romtone rettssal",
                   fact="Dokumentert (Toskas forklaring i retten, S04)",
                   note="Parafrasert. Original: «Det er aldri gjort et forsøk på et ran på Nokas.»", assets="A26,A10"),
    "SH-037": dict(section=SEC_03B),
    "SH-038": dict(section=SEC_03B, vo="And he made one assumption that would cost them dearly: that the window was ordinary glass.",
                   visual="Notatbok: ved «VINDU» skrives «vanlig glass?»; ordet glir inn i en glassrefleks.",
                   camera="Top-down, push", layers="L01 notatbok; L02 håndskrift; L03 glassrefleks",
                   anim="Håndskrift animeres; refleks glir over", trans="Refleks-wipe",
                   sound="Blyant; lav glasstone",
                   fact="Dokumentert (Toska trodde vinduet var vanlig glass, S04)",
                   note="Denne linjen planter vendepunktet i 3D 2.", assets="A15,A01"),
    "SH-039": dict(section=SEC_03B, fact="Dokumentert (prøvekjørte fluktruta senvinter 2004, S03)"),
    "SH-040": dict(section=SEC_03B, fact="Dokumentert retning (S03); detaljert rute ikke vist"),
    "SH-041": dict(section=SEC_03B, visual="Gateruten fader ut. Notatboksiden blas til APRIL."),
    "SH-049": dict(vo="It was not ordinary glass.",
                   fact="Dokumentert (sikkerhetsglass; Toska trodde vanlig glass, S04)",
                   note="Første 3D-frame må være samme vinkel som siste 2D-frame. Ingen «third time»-påstand."),
    "SH-052": dict(vo="One hundred and thirteen shots. And finally… the glass gives."),
    "SH-060": dict(sound="Pianosustain; dempet brannlyd",
                   fact="Forenkling korrigert: ikke alle tjenestepersoner var innesperret",
                   note="Visualet korrigerer overforenklingen i kapittel 4.", assets="A02,A03,A22", prio="P1"),
    "SH-082": dict(vo="A new life on the Costa del Sol. But he kept using the same email address. The investigators traced it.",
                   visual="Kart over Costa del Sol; ett e-postikon pulserer gjentatte ganger fra samme punkt i Málaga.",
                   layers="L01 kart Costa del Sol; L02 e-postikon; L03 etterforskningstavle",
                   anim="E-postikon pulserer 3 ganger fra samme punkt; linje til Toska-kort",
                   fact="Dokumentert (samme e-postadresse og kafé flere ganger; elektronisk sporing, S06)",
                   note="Ikke vis faktisk e-postadresse eller meldingsinnhold."),
    "SH-083": dict(vo="— (ingen VO)",
                   visual="4A: Málaga 2005, vanlig bygate nær jernbanestasjonen; periodebiler; liten internettkafé med generisk skilt.",
                   camera="Langsom dolly mot inngangen; 35 mm",
                   layers="M12 Málaga-gate; M13 kafé-fasade (generisk); M14 byprops/periodebiler",
                   anim="Dolly frem ~4 m; fotgjengere i bakgrunn",
                   trans="SIGNATUR INN 4: glare på foto → 3D dagslys",
                   sound="Fjern trafikk, fotgjengere, vanlig gatelyd",
                   fact="Rekonstruert fra kilder (Chicoti, litt over 100 m fra jernbanestasjonen, S06, S08); fasade generisk",
                   note="Ikke kopier ekte fasade uten pålitelig referanse.", assets="M12,M13,M14"),
    "SH-084": dict(visual="4B: Enkel internettkafé fra tidlig 2000-tall: beige PC-tårn, CRT-skjermer. Mann sett bakfra/delvis silhuett ved PC. Datografikk 5 APRIL 2005 komponert inn.",
                   camera="Låst OTS 50 mm; skjermen viser uleselig nyhetsside",
                   layers="M13 kafé-interiør; M19 CRT/PC-arbeidsplass; M03b Toska-silhuett; G04 datografikk",
                   anim="Liten skjermflimmer; tastetrykk", trans="Cut fra gate til interiør",
                   sound="Tastetrykk, vifter; klokketikk returnerer",
                   fact="Rekonstruert fra kilder (pågrepet ved datamaskin etter ca. 10 min, S07); skjerminnhold generisk",
                   note="Dato i 2D-kompositt. 5. april (S06, S10) vs 6. april (S11): avklar før låsing.",
                   assets="M13,M19,M03b,G04"),
    "SH-085": dict(vo="— (ingen VO)",
                   visual="4C: Døren åpnes; en håndfull sivilkledde politifolk kommer inn. Han snur seg og blir sittende.",
                   camera="Rack focus fra skjerm til inngang; rolig, aldri kaotisk håndholdt",
                   layers="M13 kafé; M16 sivilkledde politifigurer (3–4); M03b Toska-silhuett",
                   anim="Politifigurer går rolig inn; han snur hodet; ingen motstand",
                   trans="Motion cut", sound="Skritt, lave spanske stemmer; kafélyd faller",
                   fact="Rekonstruert fra kilder (håndfull politimenn; overga seg umiddelbart uten motstand, S07)",
                   note="Ingen jakt, ingen kamp. Ikke vis håndjern-detaljer som dokumentert.",
                   assets="M13,M16,M03b"),
    "SH-086": dict(visual="4D: Skjermen går i svart. I det mørke glasset ses refleksen av ham og politifolkene et øyeblikk – glassmotivet.",
                   camera="Låst ECU 70 mm på mørk skjerm", layers="M19 CRT-skjerm; FX03 refleks",
                   anim="Skjerm slukner; refleks fader inn/ut",
                   trans="SIGNATUR UT 4: skjermrefleks → 2D identifikasjonskort",
                   sound="Ambiens faller bort; én kontrollert THUNK; stillhet",
                   fact="Symbolsk overgang over dokumentert pågripelse (S07)",
                   note="Refleksen er motivet; ingen ansiktsdetaljer.", assets="M19,FX03"),
    "SH-087": dict(vo="Spanish police arrested David Toska in an internet café in Málaga.",
                   visual="Skjermrefleks blir stilisert identifikasjonskort: DAVID TOSKA — ARRESTED — MÁLAGA — 5 APRIL 2005.",
                   fact="Dokumentert (internettkafé Chicoti, S06, S07, S10)"),
    "SH-088": dict(fact="Dato omstridt: 5. april (S06, S10: «ett år og sju timer») vs 6. april (S11)"),
    "SH-099": dict(vo="First, they watched through the glass. Then they broke it.",
                   visual="Rute i total; refleksflash av 3D 1 (dugg) og 3D 2 (brudd).",
                   layers="L01 vindu; L02 refleks 3D 1; L03 refleks 3D 2",
                   fact="Dokumentert (februar avblåst S04/S05; april brutt S01)",
                   note="Erstatter «held them back twice» som ikke er støttet av kildene."),
}

# ------------------------------------------------- source class per shot
DOC, REC, DRA, UNV = ("DOCUMENTED", "RECONSTRUCTED FROM EVIDENCE",
                      "DRAMATISED / ILLUSTRATIVE", "UNVERIFIED — REQUIRES REVIEW")
CLASS = {}
def cls(ids, k, src):
    for i in ids:
        CLASS[f"SH-{i:03d}"] = (k, src)
cls([2, 3, 46, 47], REC, "S01")
cls([4, 13], REC, "S15,S01")
cls([5, 50, 51, 52], REC, "S01,S15 (113: secondary sources only – confirm against ruling)")
cls([9, 14, 17, 42, 43, 57, 73, 75, 76, 100], UNV, "—")
cls([11, 12], DOC, "S02")
cls([18, 81], DOC, "S13")
cls([25], DOC, "S14,S01")
cls([26], DOC, "S03,S14")
cls([27, 93, 94, 95], DOC, "S12")
cls([29, 30, 35, 36, 38, 49], DOC, "S04,S05")
cls([31, 32, 33, 34], REC, "S04,S05")
cls([39, 40], DOC, "S03")
cls([45, 48, 61, 62, 68, 69, 89, 90, 91, 92], DOC, "S01")
cls([53, 55], REC, "S01")
cls([56, 96, 97, 101], DOC, "S02,S17 (time-sensitive)")
cls([63, 64, 65, 66, 67], DRA, "S01 (vehicle/outcome only)")
cls([72], DOC, "S03")
cls([78, 79], UNV, "S16 (theory – labelled UNPROVEN)")
cls([82], DOC, "S06")
cls([83, 84, 85, 86], REC, "S06,S07,S08,S10")
cls([87], DOC, "S06,S07,S10")
cls([88], UNV, "S10,S11 (5 vs 6 April)")
cls([99], DOC, "S04,S05,S01")


def words(vo):
    if not vo or vo.startswith("—"):
        return 0
    return len(re.findall(r"[A-Za-zÀ-ÿ0-9'’-]+", vo))


def main():
    wb = openpyxl.load_workbook(SRC)
    ws = wb["SHOTBOARD"]
    rows = {ws[f"A{r}"].value: r for r in range(5, ws.max_row + 1) if ws[f"A{r}"].value}
    assert len(rows) == 102, len(rows)

    changed = []
    for sid, ed in EDITS.items():
        r = rows[sid]
        for k, v in ed.items():
            cell = ws[f"{C[k]}{r}"]
            if cell.value != v:
                changed.append((sid, k, cell.value, v))
                cell.value = v
        ws[f"S{r}"].value = words(ws[f"G{r}"].value)

    # new columns V (KILDEKLASSE), W (KILDE-ID), X (FILSTI)
    hdr = ws["U4"]
    for col, title, width in (("V", "SOURCE CLASS", 26), ("W", "SOURCE ID (source_log.csv)", 26), ("X", "FILE PATH / OUTPUT", 40)):
        c = ws[f"{col}4"]
        c.value = title
        c.font = copy.copy(hdr.font); c.fill = copy.copy(hdr.fill)
        c.alignment = copy.copy(hdr.alignment); c.border = copy.copy(hdr.border)
        ws.column_dimensions[col].width = width
    fills = {DOC: "FFDDEFD8", REC: "FFE3ECF7", DRA: "FFF1ECE2", UNV: "FFF9DCD6"}
    for sid, r in rows.items():
        k, src = CLASS.get(sid, (DRA, "—"))
        for col, val in (("V", k), ("W", src)):
            c = ws[f"{col}{r}"]
            c.value = val
            ref = ws[f"U{r}"]
            c.font = copy.copy(ref.font); c.border = copy.copy(ref.border)
            c.alignment = Alignment(wrap_text=True, vertical="top")
        ws[f"V{r}"].fill = PatternFill("solid", fgColor=fills[k])
        ws[f"X{r}"].alignment = Alignment(wrap_text=True, vertical="top")
    ws[f"X{rows['SH-028']}"].value = "04_2D_ANIMATION/previews/SH-028-030_notebook_prototype_v001.mp4"
    ws[f"X{rows['SH-029']}"].value = ws[f"X{rows['SH-028']}"].value
    ws[f"X{rows['SH-030']}"].value = ws[f"X{rows['SH-028']}"].value
    ws[f"X{rows['SH-031']}"].value = "05_BLENDER/sequences/SH-031_courtyard_v001.blend; 05_BLENDER/renders/SH-031_preview_v001.mp4"
    for sid in ("SH-028", "SH-029", "SH-030", "SH-031"):
        ws[f"R{rows[sid]}"].value = "Prototype v001"
    ws["A2"].value = ("102 shots • 00:00:00–00:13:00 • v1.1 (17 Nov 2026): February attempt and Málaga arrest "
                      "corrected after source search • columns V–X added")
    ws["A3"].value = ("SOURCE CLASS (col. V) is an editorial assessment based on searches on 17 Nov 2026 – see "
                      "00_PROJECT_MANAGEMENT/source_log.csv. FACT STATUS (col. N) describes the production image.")
    if ws.auto_filter.ref:
        ws.auto_filter.ref = re.sub(r"[A-Z]+(\d+)$", r"X\1", ws.auto_filter.ref)

    # ---------------- 3D DETALJER: sync from SHOTBOARD
    d3 = wb["3D DETALJER"]
    ai = {
        "SH-031": ("TEST AI: frost, tekstur, lys – aldri figurens posisjon", "Ingen våpen, ingen ekstra figurer; ruten skal være hel"),
        "SH-032": ("BLENDER MASTER: uskarphet bak glass styres i Blender", "Ansatte må forbli anonyme/uskarpe"),
        "SH-033": ("BLENDER MASTER + 2D dugg-overlay", "Dugg må ikke se ut som sprekk"),
        "SH-034": ("BLENDER MASTER", "Siste frame = 2D-match til notatbok"),
        "SH-083": ("TEST AI: periodedetaljer 2005 – aldri skilt/tekst", "Ingen flatskjermer, smarttelefoner eller moderne biler"),
        "SH-084": ("BLENDER MASTER + dato i 2D-kompositt", "Ingen lesbar faktisk nyhetstekst; ingen AI-tekst"),
        "SH-085": ("IKKE AI SOM STANDARD: rolig, dokumentert blocking", "Ingen jakt, kamp eller våpen trukket"),
        "SH-086": ("BLENDER MASTER", "Refleks må ikke gi gjenkjennelige ansikter"),
    }
    for r in range(5, d3.max_row + 1):
        sid = d3[f"A{r}"].value
        if sid in ai:
            sr = rows[sid]
            d3[f"E{r}"].value = ws[f"F{sr}"].value
            for dc, sc in zip("FGHIJKL", "GHIJKLM"):
                d3[f"{dc}{r}"].value = ws[f"{sc}{sr}"].value
            d3[f"M{r}"].value, d3[f"N{r}"].value = ai[sid]
        if sid == "SH-031":
            d3[f"P{r}"].value = "Prototype v001 (Blender, EEVEE)"
    d3["A1"].value = "3D DETALJER  •  4 SEKVENSER / 15 SHOTS / 120 SEK  •  v1.1"

    # ---------------- TID OG VO: rename + recompute word counts
    tv = wb["TID OG VO"]
    sec_words = {}
    for sid, r in rows.items():
        sec_words[ws[f"F{r}"].value] = sec_words.get(ws[f"F{r}"].value, 0) + (ws[f"S{r}"].value or 0)
    for r in range(5, 23):
        name = tv[f"A{r}"].value
        if name == "03a · Strike One, Strike Two":
            tv[f"A{r}"].value = name = SEC_03A
        if name == "3D 1 · The Window Wins":
            tv[f"A{r}"].value = name = SEC_3D1
        if name == "03b · Back to Drawing Board":
            tv[f"A{r}"].value = name = SEC_03B
        if name in sec_words:
            tv[f"G{r}"].value = sec_words[name]
            if not str(tv[f"H{r}"].value).startswith("="):
                tv[f"H{r}"].value = round(sec_words[name] * 60 / tv[f"E{r}"].value) if tv[f"E{r}"].value else 0

    # ---------------- OVERGANGER
    ov = wb["OVERGANGER"]
    upd = {
        "INN 1": ["SH-030 → SH-031", "Papirrift → glasssprekk → 2D-shards flyr ut over første 3D-frame",
                  "Første Blender-frame holdes under shards i 12 frames", "Papirriving → lav glasstone",
                  "Bygget i prototype v001", "Stilisert illustrativ overgang", "Prototype v001"],
        "UT 1": ["SH-034 → SH-035", "Falmende pustdugg på glass → viskelærsmuss over FEB 2004",
                 "Dugg-flekken i samme pikselkoordinat før/etter", "Cello → viskelær",
                 "Render alpha-pass av dugg", "Dugg er dramatisert detalj", "Ikke startet"],
        "INN 4": ["SH-082 → SH-083", "Glare på fotografi → middelhavsdagslys i bygate",
                  "Dagslysets retning lik i begge bilder", "Gatelyd + tikkelyd",
                  "Bruk Blender-still som kontrollbilde", "Kafé/bygate generisk, ikke ekte fasade", "Ikke startet"],
        "UT 4": ["SH-086 → SH-087", "Refleks i mørk CRT-skjerm → 2D identifikasjonskort",
                 "Match skjermrefleks og kortramme", "Kontrollert THUNK (samme som åpning)",
                 "Ikke falskt politifoto", "Kortet er tydelig illustrert", "Ikke startet"],
    }
    for r in range(5, ov.max_row + 1):
        k = ov[f"A{r}"].value
        if k in upd:
            for col, v in zip("BCDEFGH", upd[k]):
                ov[f"{col}{r}"].value = v

    # ---------------- ASSETS
    asr = wb["ASSETS"]
    arow = {asr[f"A{r}"].value: r for r in range(5, asr.max_row + 1) if asr[f"A{r}"].value}
    def aset(aid, **kw):
        r = arow[aid]
        for col, v in kw.items():
            asr[f"{col}{r}"].value = v
    aset("A18", C="Málaga gate / kafé (2D)", F="Bygate, kafévindu, dagslys", G="Generisk fasade – ikke kopi av ekte kafé")
    aset("M01", I="Prototype v001")
    aset("M02", I="Prototype v001 (intakt tilstand)", E="3D 1 (intakt, opplyst) og 3D 2")
    aset("M03", E="3D 2/3", F="Maskerte silhuetter (3D 2) og fjern silhuett (3D 3)")
    aset("M04", E="3D 2 (slegge)")
    aset("M12", G="Generisk bygate nær jernbanestasjonen (S08) – ikke eksakt sted")
    aset("M13", C="Internettkafé – fasade + interiør", F="Generisk skilt, beige PC-tårn, CRT, pulter",
         G="Chicoti (S06/S07) – generisk rekonstruksjon, ikke kopi", H="P1")
    aset("M14", C="Byprops / periodebiler 2005", F="Gatelys, skilt, 2–3 periodebiler")
    aset("M15", C="(UTGÅR) Kalender – erstattet av G04 datografikk", I="Utgår")
    aset("M16", F="3–4 sivilkledde politifigurer, rolig inngang", G="Ingen dokumentert koreografi utover «håndfull» og «uten motstand» (S07)")
    aset("M17", C="(UTGÅR) Generisk bil m vindu – strandscene fjernet", I="Utgår")
    aset("M18", C="(UTGÅR) Kaffekopp – oppdiktet motiv fjernet", I="Utgår")
    aset("FX01", C="Rim / pustdamp / vinterlys", D="Shader + 2D-overlay", F="Rim på bakken, pustdugg på glass, kald lampe",
         G="Dramatisert atmosfære", I="Prototype v001 (rim)")
    template = asr[f"A{asr.max_row}"].row
    new = [
        ("M03b", "3D", "Toska-silhuett (huket / sittende)", "Low-poly figur", "3D 1 og 3D 4",
         "Hette/lue, mørk jakke, ingen ansiktstrekk", "Ingen gjenkjennelig likhet", "P1", "Prototype v001 (huket)", ""),
        ("M04b", "3D", "Vegglampe bakgård", "Prop + punktlys", "3D 1", "Enkel armatur, kaldt lys", "Dramatisert", "P2", "Prototype v001", ""),
        ("M19", "3D", "CRT-skjerm / PC-arbeidsplass 2005", "Low-poly props", "3D 4",
         "Beige tårn, CRT, tastatur, mus, pult", "Periodekorrekt 2005; ingen lesbar tekst", "P1", "Ikke startet", ""),
        ("M20", "3D", "Pengetraller bak glass", "Low-poly props", "3D 1",
         "2 traller med poser, sett uskarpt", "Generisk – ikke NOKAS-spesifikk", "P2", "Ikke startet", ""),
        ("M21", "3D", "Anonyme ansattsilhuetter", "Simple rigs", "3D 1/2",
         "2–3 figurer, bare silhuett bak glass", "Ingen identifiserbare ansatte", "P2", "Ikke startet", ""),
        ("G04", "2D", "Datografikk 5 APRIL 2005", "Motion graphics", "3D 4 / 07b",
         "Samme typografi som kalendermotiv A17", "Dato omstridt (S10/S11) – avklar", "P1", "Ikke startet", ""),
    ]
    for rowvals in new:
        r = asr.max_row + 1
        for col, v in zip("ABCDEFGHIJ", rowvals):
            c = asr[f"{col}{r}"]
            c.value = v
            ref = asr[f"{col}{template}"]
            c.font = copy.copy(ref.font); c.fill = copy.copy(ref.fill)
            c.border = copy.copy(ref.border); c.alignment = copy.copy(ref.alignment)

    # ---------------- FAKTA OG RISIKO
    fr = wb["FAKTA OG RISIKO"]
    fr["A2"].value = ("v1.1: Påstander kontrollert mot søkeresultater 17.11.2026 (fulltekst ikke lest – se "
                      "source_log.csv). Primærkilder (dom, rettsreferat) gjenstår.")
    frow = {fr[f"A{r}"].value: r for r in range(5, fr.max_row + 1) if fr[f"A{r}"].value}
    def fset(fid, **kw):
        for col, v in kw.items():
            fr[f"{col}{frow[fid]}"].value = v
    fset("F01", C="Februar-forsøket / «vindu holdt to ganger»",
         E="Kildene (S04, S05) sier februar ble AVBLÅST fordi pengene ble flyttet – glasset stoppet dem ikke. «Tredje forsøk» (S04) er omstridt; Toska nektet i retten.",
         F="RETTET i manus v004: 3D 1 skrevet om; epilog-linje endret.", G="KORRIGERT v004 – bekreft mot dom")
    fset("F02", C="3D 1 vintermorgen / rim / dugg", E="Lys, vær, traller og dugg er dramatisert over dokumentert hendelse.",
         G="DRAMATISERT – merket")
    fset("F05", E="Strandpromenade og kaffekopp var oppdiktet. Kilder: internettkafé Chicoti, ca. 100 m fra jernbanestasjonen, ca. 10 min ved PC, håndfull politi, ingen motstand (S06–S10).",
         F="RETTET i manus v004: 3D 4 bygget om rundt kafeen.", G="KORRIGERT v004")
    tmpl = fr.max_row
    for vals in (
        ("F13", "HØY", "Pågripelsesdato 5. vs 6. april 2005", "Ch7, 3D 4, 07b",
         "Aftenbladet/Nettavisen: 5. april («ett år og sju timer»); Dagbladet/Aftenposten: 6. april.",
         "Avklar mot primærkilde før dato låses i grafikk.", "ÅPEN"),
        ("F14", "MIDDELS", "Toska trodde vinduet var vanlig glass", "Ch3, Ch4",
         "Kun én kilde (S04, Klikk) i søket.", "Bekreft i rettsreferat/bok før publisering.", "ÅPEN"),
        ("F15", "LAV", "Danny Bungard pågrepet samtidig", "3D 4",
         "S06 sier Toska ble pågrepet sammen med Bungard; ikke vist i scenen.",
         "Bevisst utelatt; vurder om en ekstra figur bør vises.", "BEVISST UTELATT"),
        ("F16", "MIDDELS", "113 skudd", "Cold open, 3D 2, epilog",
         "Tallet funnet i sekundærkilder (Wikipedia-utdrag, VoiceMap).", "Bekreft i dom.", "ÅPEN"),
    ):
        r = fr.max_row + 1
        for col, v in zip("ABCDEFG", vals):
            c = fr[f"{col}{r}"]; c.value = v
            ref = fr[f"{col}{tmpl}"]
            c.font = copy.copy(ref.font); c.border = copy.copy(ref.border); c.alignment = copy.copy(ref.alignment)

    # ---------------- START HER
    sh = wb["START HER"]
    sh["A3"].value = "KOMPLETT PRODUKSJONS-STORYBOARD • versjon 1.1 • 17.11.2026 • basert på manus v004"

    # ---------------- ENDRINGSLOGG
    log = wb.create_sheet("ENDRINGSLOGG", 1)
    log["A1"].value = "ENDRINGSLOGG v1.0 → v1.1"; log["A1"].font = Font(bold=True, size=14)
    log.append([])
    log.append(["Shot", "Felt", "Før", "Etter"])
    for c in log[3]:
        c.font = Font(bold=True)
    for sid, k, before, after in changed:
        log.append([sid, k, before, after])
    for col, w in zip("ABCD", (10, 12, 70, 70)):
        log.column_dimensions[col].width = w
    for row in log.iter_rows(min_row=4):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")

    # ---------------- ENGLISH PASS: translate every remaining Norwegian string (translation_no_en.json)
    tr = json.load(open(pathlib.Path(__file__).with_name("translation_no_en.json"), encoding="utf-8"))
    formula_tr = (("SVÆRT STRAMT", "VERY TIGHT"), ("STRAMT", "TIGHT"), ("INGEN VO", "NO VO"))
    n_tr = 0
    for sheet in wb.worksheets:
        for row in sheet.iter_rows():
            for c in row:
                v = c.value
                if isinstance(v, str):
                    if v.startswith("="):
                        for a, b in formula_tr:
                            v = v.replace(f'"{a}"', f'"{b}"')
                        c.value = v
                    elif v in tr:
                        c.value = tr[v]
                        n_tr += 1
    renames = {"START HER": "START HERE", "ENDRINGSLOGG": "CHANGE LOG", "3D DETALJER": "3D DETAILS",
               "TID OG VO": "TIMING & VO", "OVERGANGER": "TRANSITIONS", "FAKTA OG RISIKO": "FACTS & RISKS",
               "PRODUKSJONSSYSTEM": "PRODUCTION SYSTEM"}
    for old, new in renames.items():
        if old in wb.sheetnames:
            wb[old].title = new
    print(f"english pass: {n_tr} cells translated")

    DST.parent.mkdir(parents=True, exist_ok=True)
    wb.save(DST)

    # ---------------- shot_tracker.csv
    fields = ["shot_id", "chapter", "start", "end", "duration_s", "type", "vo_exact", "vo_words", "vo_wpm",
              "camera", "assets", "transition", "priority", "source_class", "source_ids", "production_status",
              "render_stage", "file_paths", "depends_on"]
    deps = {"SH-031": "SH-030 (INN 1 match)", "SH-035": "SH-034 (UT 1 match)", "SH-050": "SH-031 (M01/M02 sett), SH-049",
            "SH-053": "SH-052", "SH-064": "SH-063", "SH-068": "SH-067", "SH-083": "SH-082", "SH-087": "SH-086"}
    TRACKER.parent.mkdir(parents=True, exist_ok=True)
    with open(TRACKER, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(fields)
        for sid, r in sorted(rows.items()):
            v = lambda col: ws[f"{col}{r}"].value
            dur = v("D") or 0
            wpm = round((v("S") or 0) * 60 / dur) if dur else 0
            stage = "prototype_v001" if sid in ("SH-028", "SH-029", "SH-030", "SH-031") else "storyboard"
            w.writerow([sid, v("F"), v("B"), v("C"), dur, v("E"), v("G"), v("S"), wpm, v("I"), v("P"), v("L"),
                        v("Q"), v("V"), v("W"), v("R"), stage, v("X") or "", deps.get(sid, "")])
    print(f"saved {DST.name}; {len(changed)} field changes; tracker rows {len(rows)}")


if __name__ == "__main__":
    main()
