"""D.B. Cooper shot list v001: the single source for the shot list table and the Higgsfield still requests.

Usage: python3 -I make_shot_list.py   (run inside this folder)
Writes shot_list_v001.md, requests_round1.json and requests_round2.json (batches of at most 8 for generate_image_batch).

Columns: id (scene*100+n), scene, seconds on screen, refs, round, source, prompt.
  source: NEW = generate a still; REUSE:<ref> = use an approved style reference as the shot (no cost);
          CARD = text card or graphic made in the edit (no cost).
  round 1 = scenes 1-14 (hijacking, case board, clues); round 2 = scenes 15-23 (suspects, endings), when credits allow.
Motion is decided after the stills are approved (12.5 credits per clip). Default treatment is a slow push or pan in the edit.
"""
import json

STYLE = ("Painterly 2D gouache illustration for a serious animated documentary, graphic-novel lighting, visible brush "
         "strokes, muted palette, atmospheric haze, cinematic composition, not photorealistic; match the style of the "
         "reference images. United States, 1971 unless stated, period-accurate. No text, letters, numbers, signs, logos "
         "or airline livery anywhere. No blood. SHOT: ")
NOFACE = " Only the back of the head visible, no face, no profile, no ear."
R = {"BG1": "826a7f5f-2146-4512-a039-46fd29d84570", "BG2": "28037ef8-ea01-4930-9c66-6c5e03dadf75",
     "BG3": "a54e85da-f465-46eb-b7aa-2330992beb60", "BG4": "9de80d91-7999-4146-be0c-6d5052d9cfbf",
     "BG5": "a214d6dd-f881-4628-919a-206cefa1e4a0", "BG6": "7dae2e1d-e6bb-45e3-a9bb-8dc698d991a9",
     "CH1": "d0aaa0df-f31a-4943-85da-2cd62c9916ed", "CH2": "e6286f34-9eaa-45aa-a156-f532957fd62a"}

S = [
 # --- 1 Cold open (0:00-0:38) ---
 (101, 1, 5, "BG2", 1, "NEW", "Extreme close-up of a dark 1971 cockpit instrument panel at night, one small red warning light glowing, round analogue gauges, seen past the shoulder of a pilot in shadow." + NOFACE + " Palette: black, deep green-grey, one red accent."),
 (102, 1, 9, "BG2", 1, "NEW", "The empty rear of the 1971 Boeing 727 cabin at night, dim, cigarette smoke hanging in the air, looking down the aisle toward the open rear stair door at the very back: a dark rectangle with rain streaming past and cold white light. No people. Palette: indigo, dim amber, cold white."),
 (103, 1, 8, "BG3", 1, "REUSE:BG3", "727 at night, stairs down (style reference BG3)."),
 (104, 1, 10, "BG4", 1, "REUSE:BG4", "Forest from above at night (style reference BG4); slow push in the edit."),
 # --- 2 Title (0:38-0:44) ---
 (201, 2, 6, "BG2", 1, "NEW", "Close-up of a small round-cornered airplane window at night, rain streaking across the dark glass, faint distant lights below blurred. Empty, moody. Lots of dark negative space for a title. Palette: indigo, black, silver raindrops."),
 # --- 3 Portland (0:44-1:07) ---
 (301, 3, 8, "BG1", 1, "REUSE:BG1", "Portland airport in the rain (BG1, clean version)."),
 (302, 3, 8, "BG1 CH1", 1, "NEW", "Inside a 1971 airport terminal: an airline ticket counter with warm amber light, a slim man in a dark raincoat and dark suit standing at the counter seen from behind, a black attaché case at his feet; an airline agent behind the counter is a blurred background figure. Rain on the big windows." + NOFACE),
 (303, 3, 7, "BG1", 1, "NEW", "Close-up still life on a 1971 airline counter: a few folded US banknotes and a paper ticket envelope (completely blank, no printing), warm amber light, a man's dark coat sleeve at the edge of frame. No readable text."),
 # --- 4 The note (1:07-1:29) ---
 (401, 4, 7, "BG2 CH1", 1, "NEW", "The 1971 727 cabin in warm Kodachrome light: the man in the dark suit seated in an aisle seat near the back, seen from behind and above, cigarette smoke curling up in a beam of window light, a glass of bourbon and soda on the tray table." + NOFACE),
 (402, 4, 7, "BG2 CH2", 1, "NEW", "A flight attendant in a teal 1971 uniform seated on a fold-down jump seat at the back of the cabin, seen from behind; a folded white note being handed toward her from the side (simple shapes, no visible writing)." + NOFACE),
 (403, 4, 8, "BG2 CH1", 1, "NEW", "Dark silhouette of the man in the suit leaning slightly toward the aisle, seen from behind against a bright rainy airplane window, smoke drifting. Tense." + NOFACE + " Palette: dark charcoal against cool window light."),
 # --- 5 The demands (1:29-1:54) ---
 (501, 5, 7, "BG2", 1, "NEW", "Close-up of a black attaché case on a man's lap in an airplane seat, the lid open just a few centimetres: inside in deep shadow, red cylinders, coloured wires and a battery. Tense, low light. No hands in motion, no text."),
 (502, 5, 7, "BG3", 1, "NEW", "A small silver Boeing 727 trijet circling at dusk high above Puget Sound, wooded islands and calm water far below, a magenta-to-blue sky, the city lights just coming on in the distance. Generic unmarked livery. Peaceful, vast."),
 (503, 5, 11, "BG6", 1, "NEW", "A 1971 bank back office: stacks of twenty-dollar bills bundled on a table (no readable print), an FBI agent in a 1970s suit seen from behind photographing them with a bulky microfilm camera on a stand, a bright flash of light." + NOFACE),
 # --- 6 The exchange (1:54-2:26) ---
 (601, 6, 10, "BG3", 1, "NEW", "A remote corner of a rainy airfield at night lit by sodium-orange floodlights: the Boeing 727 parked with its front stairs down, a small dark figure at the foot of the stairs handing up a heavy canvas bag, wet tarmac reflecting orange light, a fuel truck in the distance. Wide shot, figures tiny, no faces."),
 (602, 6, 8, "BG3", 1, "NEW", "Passengers in 1970s coats walking away from the parked 727 across a wet floodlit airfield in heavy rain, seen from behind at a distance, a small static group. Sodium-orange light."),
 (603, 6, 7, "BG2", 1, "NEW", "A 1971 airliner cockpit at night seen from behind the pilots: two pilots in caps and white shirts, one turning his head slightly toward the intercom handset, rain on the windscreen, instrument glow." + NOFACE),
 (604, 6, 7, "BG3", 1, "NEW", "A clean side-profile painting of a Boeing 727 trijet in flight against a plain dusk sky, landing gear down, flaps lowered, and the rear ventral airstair under the tail hanging open. Technical, calm, like an illustrated diagram but painterly, no labels."),
 # --- 7 The jump (2:26-3:01) ---
 (701, 7, 6, "BG3", 1, "NEW", "The Boeing 727 taking off from a wet runway at night into rain, runway lights streaking, seen from the side at a distance. Generic livery."),
 (702, 7, 8, "BG2 CH1", 1, "NEW", "Point of view down a dim airplane aisle at night: at the far end, the silhouette of a man in a dark suit standing in the aisle, tying a cloth bag around his waist with a cord, cigarette smoke drifting, a single reading light. Seen from far away, a dark silhouette only, no face."),
 (703, 7, 6, "BG2", 1, "NEW", "Close-up of a closed cockpit door from the cabin side at night, dim light, an old metal handle, ominous quiet. No people."),
 (704, 7, 7, "BG2", 1, "REUSE:102", "The open rear stairs (shot 102, held longer); the 8:13 beat."),
 (705, 7, 8, "BG6", 1, "NEW", "The interior of an empty 1971 airliner cabin lit by harsh flashlight beams at night, as police look inside: an empty seat with a black clip-on tie left on it, two parachute packs on the floor, cigarette butts in an armrest ashtray. No people visible, just the light beams."),
 # --- 8 The case board (3:01-3:20) ---
 (801, 8, 10, "BG6", 1, "REUSE:BG6", "Case board master (BG6); slow lateral track in the edit."),
 (802, 8, 9, "BG6", 1, "NEW", "Close-up of part of the 1970s case board: pinned small paintings of an airplane, a black tie and a forest, connected with red string, warm lamp light, shallow focus. No writing anywhere."),
 # --- 9 Clue 1: the name (3:20-4:08) ---
 (901, 9, 10, "BG6", 1, "NEW", "A busy 1971 newspaper newsroom at night: rows of typewriters, cigarette smoke, desk lamps, a teletype machine, reporters as dark seated silhouettes seen from behind, papers everywhere (no readable text)." + NOFACE),
 (902, 9, 8, "BG6", 1, "NEW", "A printing press rolling newspapers at night, a blur of paper and ink, motion streaks, no readable headlines or letters."),
 (903, 9, 14, "", 1, "NEW", "A bold, flat, mid-century European adventure-comic style painting (original design, not copying any real comic): a heroic jet test pilot in a 1950s flight suit and helmet, seen from behind, parachuting from a sleek silver jet against a bright blue sky with stylised clouds. Golden and blue palette, clean confident line art. No speech bubbles, no text, no logos."),
 (904, 9, 10, "BG6", 1, "NEW", "A 1950s-60s French-language comic book lying closed on a dim desk under a lamp, its cover a painted jet aircraft in the sky, the title area left completely blank, no letters at all. Gold accent light."),
 # --- 10 Clue 2: what he knew (4:08-4:57) ---
 (1001, 10, 10, "BG3", 1, "NEW", "A painterly cut-away side view of a Boeing 727 at night with the rear ventral airstair lowered beneath the tail, the open stairway glowing faintly, wind lines streaming past. Technical but atmospheric, no labels."),
 (1002, 10, 12, "BG3", 1, "NEW", "The view out of an airplane window at dusk in 1971: far below, the city of Tacoma and a military air base with long runways beside the water, lights coming on. Seen through the round-cornered window frame."),
 (1003, 10, 13, "BG3", 1, "NEW", "A 1960s cargo plane flying low over green jungle hills in Southeast Asia, a supply pallet with a parachute dropping from the rear, misty green palette. Faded like an old memory, softer and greener than the rest of the film. No markings."),
 (1004, 10, 14, "BG6", 1, "NEW", "On the case board, a red string connecting a pinned painting of a parachute to a pinned painting of a military airplane, under warm lamp light. No writing."),
 # --- 11 Clue 3: the night (4:57-5:32) ---
 (1101, 11, 9, "BG4", 1, "NEW", "Pure storm: a dark night sky over black forest, rain lashing diagonally, wind, clouds racing, no lights below, no aircraft, no people. Indigo and black."),
 (1102, 11, 7, "BG4 CH1", 1, "NEW", "Abstract close-up in a freezing night wind: the cuff of a dark business suit sleeve and a brown leather loafer silhouetted against rain and dark sky, motion streaks, no face, no person fully visible."),
 (1103, 11, 9, "BG6", 1, "NEW", "A small 1970s single-engine light aircraft flying low over endless wet evergreen forest by day in grey mist, a pilot's silhouette at the window seen from behind." + NOFACE),
 (1104, 11, 10, "BG4", 1, "NEW", "A long line of soldiers in 1970s olive rain ponchos searching a wet forest floor in fog, seen from far above, tiny figures standing still in a static line among the trees. Grey-green, misty."),
 # --- 12 Clue 4: the money (5:32-6:02) ---
 (1201, 12, 10, "BG6", 1, "NEW", "A 1970s bank teller's counter: a teller seen from behind holding a twenty-dollar bill up to the light, a long printed list on the counter (illegible abstract marks only), cool blue accent light." + NOFACE),
 (1202, 12, 10, "BG6", 1, "NEW", "A quiet 1970s American street at dusk with shop windows, a bank, a diner and a racetrack sign shape (signs blank, no letters), muted blue tones, nobody spending anything. Lonely."),
 (1203, 12, 10, "BG6", 1, "NEW", "Close-up of the case board: a pinned long strip of paper covered in abstract dotted marks (no numbers or letters), with a blue pin, warm lamp light."),
 # --- 13 Clue 5: the river (6:02-6:54) ---
 (1301, 13, 8, "BG5", 1, "REUSE:BG5", "Columbia River sandbar (BG5)."),
 (1302, 13, 10, "BG5", 1, "NEW", "The same winter sandbar on the Columbia River: a small boy in a red winter jacket seen from behind, kneeling in the pale sand near a ring of campfire stones, grey water beyond." + NOFACE),
 (1303, 13, 10, "BG5", 1, "NEW", "Close-up on wet pale sand: half-buried rotting bundles of old twenty-dollar bills, held together by perished rubber bands, faded and torn, no readable print. Winter light, muted green and gold."),
 (1304, 13, 12, "BG5", 1, "NEW", "A painterly cross-section of river sand showing distinct coloured layers like a geology diagram, a small bundle of banknotes lying above one grey clay layer. Educational, clean, no labels or text."),
 (1305, 13, 12, "", 1, "NEW", "A circular microscope view: tiny translucent glass-like diatoms (microscopic algae) in many geometric shapes, glowing pale green and gold against dark, scientific and beautiful. No text, no scale bar."),
 # --- 14 Clue 6: the tie (6:54-7:28) ---
 (1401, 14, 9, "BG6", 1, "NEW", "A black clip-on tie with a small mother-of-pearl tie clip inside a clear plastic evidence bag lying on a desk under a lamp, cold white accent light. The bag tag is blank."),
 (1402, 14, 9, "", 1, "NEW", "An electron-microscope style view of dark woven fabric fibres with tiny glittering metallic particles caught between the threads, silver and pale gold sparkles on black. Scientific, no text, no scale bar."),
 (1403, 14, 16, "BG6", 1, "NEW", "A 1960s aerospace factory floor: a large silver aircraft fuselage section on stands, engineers in white shirts and narrow ties seen from behind as small static silhouettes, high windows with light beams, no logos or text." + NOFACE),
 # --- 15 The suspects (7:28-7:43) ---
 (1501, 15, 15, "BG6", 2, "NEW", "The case board under the lamp: five cut-out black paper silhouettes of men pinned in a row, each a different simple outline, red strings from each to small pinned paintings. No faces, no writing."),
 # --- 16 McCoy (7:43-8:12) ---
 (1601, 16, 12, "BG6", 2, "NEW", "A single cut-out paper silhouette of a young man, steel-blue accent colour, pinned on cork under a lamp. No face details, no writing."),
 (1602, 16, 17, "BG3", 2, "NEW", "A Boeing 727 at dawn flying over a vast Utah desert with red-brown mesas, the rear airstair under the tail lowered, a pale gold-blue sky. Generic livery."),
 # --- 17 Christiansen (8:12-8:40) ---
 (1701, 17, 12, "BG6", 2, "NEW", "A single cut-out paper silhouette of a slight man, airline-red accent colour, pinned on cork under a lamp. No face details, no writing."),
 (1702, 17, 16, "BG1", 2, "NEW", "A small 1970s suburban house in the rain in Washington state, a wet lawn, warm light in one window, an unmarked airline uniform jacket hanging on a hook seen through the porch door. No people, no text."),
 # --- 18 Weber (8:40-8:58) ---
 (1801, 18, 8, "BG6", 2, "NEW", "A single cut-out paper silhouette of an older man, pale hospital-green accent, pinned on cork under a lamp. No face details, no writing."),
 (1802, 18, 10, "", 2, "NEW", "A dark quiet bedroom at night, a single bedside lamp glowing, an empty bed with rumpled sheets, a glass of water. No people. Soft pale green and amber."),
 # --- 19 Rackstraw (8:58-9:21) ---
 (1901, 19, 10, "BG6", 2, "NEW", "A single cut-out paper silhouette of a young man in a military cap, olive-drab accent, pinned on cork under a lamp. No face details, no writing."),
 (1902, 19, 13, "BG3", 2, "NEW", "A 1960s military helicopter flying over misty green jungle hills, seen from a distance, faded and soft like an old memory. No markings."),
 # --- 20 The one who never existed (9:21-9:42) ---
 (2001, 20, 21, "BG6", 2, "NEW", "On the cork board under the lamp: an empty dotted outline of a man's silhouette drawn on paper with nothing inside it, red strings hanging slack from it to the other pinned items. Eerie. No writing."),
 # --- 21 Three endings (9:42-10:21) ---
 (2101, 21, 13, "BG4", 2, "NEW", "Dense evergreen forest canopy from above in cold blue rain-light, a torn pale parachute canopy caught high in one tall tree far away, no person visible."),
 (2102, 21, 13, "BG4 CH1", 2, "NEW", "A muddy forest dirt road at first light in fog, golden dawn; far away a man in a dark raincoat walking away from the camera, small, seen from behind." + NOFACE),
 (2103, 21, 13, "BG5", 2, "NEW", "The Columbia River under a grey sky, a small dark bundle drifting in the current near a sandbar, muddy green water, bare trees. No people."),
 # --- 22 Closed (10:21-10:41) ---
 (2201, 22, 10, "BG6", 2, "NEW", "A 1970s FBI archive room: tall metal shelves stacked with cardboard evidence boxes (blank labels), a single desk lamp, dust in the light. No people."),
 (2202, 22, 10, "BG6", 2, "NEW", "The case board in the dark office after the lamp is switched off: only a faint streetlight through venetian blinds catching the red strings. Dark, quiet."),
 # --- 23 The last question (10:41-11:02) ---
 (2301, 23, 8, "BG2", 2, "REUSE:102", "Signature shot again: the open rear stairs in the rain (102), slow push to black."),
 (2302, 23, 13, "BG2", 2, "NEW", "The empty 1971 airplane cabin at night: two empty seats side by side under one warm reading light, rain on the dark window, a thin wisp of smoke. No people. Quiet, final."),
]


def main():
    rows, reqs = [], {1: [], 2: []}
    for i, sc, sec, refs, rnd, src, text in S:
        rows.append(f"| {i} | {sc} | {sec} | {refs or '–'} | {rnd} | {src} | {text.replace('|', '/')} |")
        if src == "NEW":
            p = {"model": "nano_banana_2_1", "resolution": "2k", "aspect_ratio": "16:9", "prompt": STYLE + text}
            if refs:
                p["medias"] = [{"value": R[r], "role": "image_references"} for r in refs.split()]
            reqs[rnd].append({"index": i, "params": p})
    for rnd, rq in reqs.items():
        json.dump([rq[k:k + 8] for k in range(0, len(rq), 8)], open(f"requests_round{rnd}.json", "w"), indent=1)
    secs = {}
    for _, sc, sec, *_ in S:
        secs[sc] = secs.get(sc, 0) + sec
    new = {r: len(v) for r, v in reqs.items()}
    head = ["# D.B. Cooper: shot list v001", "",
            "Generated by `make_shot_list.py` (edit the script, not this file). Script: `01_SCRIPT/DB_COOPER_preproduction_v003.md`.", "",
            f"- **Shots:** {len(S)} in total, **{len(S) - sum(new.values())} reused or free**.",
            f"- **New stills:** **{new[1]}** in round 1 and **{new[2]}** in round 2, at 2 credits each: {2 * new[1]} and {2 * new[2]} credits, plus redos.",
            f"- **Screen time covered:** {sum(secs.values())} s ({sum(secs.values()) // 60}:{sum(secs.values()) % 60:02d}). Cards, the title and the credits are added in the edit.",
            "- **Rules in every prompt:**",
            "  - no text or logos;",
            "  - real people only from behind (\"only the back of the head, no face, no profile, no ear\");",
            "  - hands appear in stills only;",
            "  - no crowds in motion;",
            "  - suspects appear only as paper silhouettes.",
            "- **Motion:** chosen after the stills are approved (Seedance 2.0, 12.5 credits per clip). The default treatment is a slow push or pan in the edit.", "",
            "| ID | Scene | Sec | Refs | Round | Source | Description / prompt |", "|---|---|---|---|---|---|---|"]
    open("shot_list_v001.md", "w").write("\n".join(head + rows) + "\n")
    print(len(S), "shots;", new, "new stills; seconds", sum(secs.values()))
    for sc in sorted(secs):
        print(sc, secs[sc], end="; ")


if __name__ == "__main__":
    main()
