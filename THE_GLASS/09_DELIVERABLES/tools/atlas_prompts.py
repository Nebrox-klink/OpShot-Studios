"""Build per-scene ElevenLabs (eleven_v4) prompts from a script .md.

Pauses: *(beat)* -> [pause], *(hold)* -> [long pause], *(white ...)* -> split into a new chunk (silence added in the edit).
Pronunciations: IPA between slashes, as eleven_v4 expects (producer-confirmed: Kloongland, Shooman).
Usage: python atlas_prompts.py SCRIPT.md OUT.json
"""
import json, re, sys
IPA = [("Arne Sigve Klungland", "/ˈɑːrnə ˈsɪɡvə ˈkluːŋlænd/"), ("Klungland", "/ˈkluːŋlænd/"),
       ("Kjell Alrich Schumann", "/ʃɛl ˈɑːlrɪk ˈʃuːmən/"), ("Schumann", "/ˈʃuːmən/"), ("Håland", "/ˈhɔːlɑːn/"),
       ("Sørmarka", "/ˈsɜːrmɑːrkə/"), ("Nedre Dalgate", "/ˈneːdrə ˈdɑːlɡɑːtə/"), ("NOKAS", "/ˈnuːkɑːs/"),
       ("Stavanger", "/stɑːˈvɑːŋər/"), ("Sandnes", "/ˈsɑːnnəs/")]
SOFT = {9: "One of the men", 17: None, 19: None, 22: "In Stavanger, the news", 24: None}  # where [softly] starts
scene_re = re.compile(r"^#### Scene (\d+) · (.+?) \(")
chunks, cur = [], None
for line in open(sys.argv[1], encoding="utf-8"):
    if m := scene_re.match(line):
        cur = {"scene": int(m.group(1)), "title": m.group(2), "parts": [[]]}
        chunks.append(cur)
    elif cur and line.startswith("> "):
        b = line[2:].strip()
        if b.startswith("*("):
            if "white" in b:
                cur["parts"].append([])
            else:
                cur["parts"][-1].append("[long pause]" if "hold" in b else "[pause]")
        else:
            cur["parts"][-1].append(re.sub(r"\s*`[^`]*`", "", b).strip())
out = []
for c in chunks:
    for i, p in enumerate(c["parts"]):
        text = " ".join(p)
        n = c["scene"]
        if n in SOFT:
            key = SOFT[n]
            text = text.replace(key, "[softly] " + key, 1) if key else "[softly] " + text
        for a, b in IPA:
            text = text.replace(a, b)
        out.append({"id": f"S{n:02d}" + (chr(97 + i) if len(c["parts"]) > 1 else ""), "title": c["title"], "text": text})
json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for o in out:
    print(o["id"], len(o["text"]), o["text"])
print("TOTAL", sum(len(o["text"]) for o in out), "chunks", len(out))
