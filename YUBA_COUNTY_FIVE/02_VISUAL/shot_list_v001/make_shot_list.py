"""Yuba County Five shot list v001: the single source for the shot table and the Higgsfield still requests.

Usage: python3 -I make_shot_list.py   (run inside this folder)
Writes shot_list_v001.md and requests_batchNN.json (8 per batch, the Higgsfield concurrency limit).

Columns: id (scene*100+n), scene, cuts (how many cuts the still gives: wide / medium / close), ref, motion, big, prompt.
  ref:    style reference (Higgsfield job id key, see R)
  motion: KU = Kling clip made by the producer on their own Kling plan (hero shots)
          KH = Kling 3.0 std through Higgsfield (7.5 credits / 5 s, silent)
          L  = local motion (09_DELIVERABLES/tools/motion_fx.py + edit graphics), free
          G  = graphic made in the edit (map, cards, counters), free
  big:    the ONE big, clearly visible thing that moves or changes (retention rule 11)
  prompt: NEW still prompt, or REUSE:<still> for an existing image.
"""
import json

STYLE = ("Painterly 2D gouache illustration for a serious animated documentary, graphic-novel lighting, visible brush "
         "strokes, muted palette, atmospheric haze, cinematic composition, not photorealistic; match the style of the "
         "reference images. Northern California, 1978, period-accurate cars and clothing. No text, letters, numbers, "
         "signs, logos or licence plates anywhere. No blood, no bodies. SHOT: ")
NOFACE = " People only from behind or as distant silhouettes: no faces, no profiles."
CAR = " The car is a 1969 Mercury Montego two-door coupe, turquoise body with a white roof, exactly as in the reference."
R = {"ST1": "d323f4d5-8d3e-4dca-8275-58e3a5a64ef2", "ST2": "8ed86d86-0edf-40ab-a92a-de0ee888d7b8",
     "ST3": "75238cbc-f868-4654-8b16-1b93298774e0", "ST4": "e3bacc27-c47c-4020-a182-325802df8cc8",
     "ST5": "5c848c77-806d-4a84-bf11-a91238d5cc2b", "BG4": "9de80d91-7999-4146-be0c-6d5052d9cfbf"}

S = [
 # S01 cold open: the car (24 s)
 (101, 1, 2, "ST1", "KH", "a gust drives a wall of snow across the car", "REUSE:ST1"),
 (102, 1, 2, "ST1", "L", "snow slides off the front fender in a clump", "Low close angle on the front wheel and fender of the car half sunk in a shallow snowdrift at night, snow piled on the fender, moonlit blue light, falling snow." + CAR),
 (103, 1, 2, "ST1", "KH", "the dashboard lights flare on as the engine catches", "Inside the empty car at night seen from the back seat: dark dashboard, empty front bench seat, snow covering the windshield, faint blue moonlight through the glass. No people." + CAR),
 (104, 1, 2, "ST1", "KH", "exhaust bursts from the tailpipe and the tail lights glow red", "Close on the rear bumper and tailpipe of the car on a snowy road at night, tail lights dark, snow falling, cold blue light." + CAR),
 (105, 1, 2, "BG4", "L", "clouds rush past as the camera flies over the peaks", "Wide aerial view at night over dark snow-covered Sierra Nevada mountains and pine forests, one thin winding road climbing into the peaks, moonlight, drifting clouds below the camera."),
 # S02 title (6 s)
 (201, 2, 1, "ST3", "L", "the desk lamp clicks on and lights the board", "REUSE:ST3"),
 # S03 the five (33.5 s)
 (301, 3, 3, "ST1", "L", "a 1970s station wagon drives through frame", "A small Sacramento Valley town main street at dusk in 1978: low brick shops with blank awnings, a few parked period cars, warm shop windows, palm and valley oak trees, orange sky. Two distant pedestrians seen from behind." + NOFACE),
 (302, 3, 2, "ST4", "L", "the bedside lamp clicks on", "REUSE:ST4"),
 (303, 3, 2, "ST4", "KH", "the ball rolls slowly across the floor", "An empty high school gym at night in 1978, polished wooden floor, a single basketball resting at the free-throw line, high windows, warm pools of light, bleachers empty."),
 (304, 3, 2, "ST4", "L", "the front door light snaps on, flooding the porch", "Five green sports bags lined up by the front door of a modest 1970s family house at night, a porch light outside the frosted door glass, warm hallway, wood panelling. No people."),
 (305, 3, 2, "ST4", "KH", "a basketball drops through the net and the net swishes", "Close low angle on a basketball hoop and white net in an empty gym, a basketball in the air just above the rim, warm light, dust in the beams."),
 # S04 the night in Chico (27.5 s)
 (401, 4, 3, "ST1", "KU", "the car drives away down the road, tail lights shrinking", "Night, a straight two-lane valley road between orchards, the car seen from behind driving away, red tail lights, headlight glow ahead, stars, distant farmhouse lights." + CAR),
 (402, 4, 2, "ST4", "L", "camera flashes pop across the bleachers", "A packed college basketball arena in 1978 painted loose and warm: players as dark silhouettes mid-game under bright lights, the crowd a soft impressionistic blur of colour with no individual faces, a ball in the air."),
 (403, 4, 2, "ST1", "L", "the shop lights switch off one bank at a time", "A small downtown grocery store at night in 1978 with big lit windows and a blank sign board, the car parked at the kerb in front, wet street reflecting the light." + CAR),
 (404, 4, 2, "ST4", "L", "the fluorescent light above the counter flickers off", "Close on a grocery checkout counter at night: cartons of milk, soda bottles and bags of snacks with blank labels, an old mechanical cash register, fluorescent light. No people, no hands."),
 (405, 4, 1, "ST4", "L", "the clock's minute hand jumps to ten", "A plain round wall clock with no numbers on a store wall, the hands just before ten o'clock, warm light, simple composition with empty wall around it."),
 # S05 case board (10.7 s)
 (501, 5, 2, "ST3", "G", "red pins drop onto the map and the string snaps tight", "REUSE:ST3"),
 (502, 5, 1, "ST4", "L", "the receiver rattles on its hook as the phone rings", "A 1970s rotary telephone on a kitchen wall at night, receiver on the hook, a dim kitchen with a window, warm lamp light. No people."),
 # S06 clue 1: the wrong road (28.7 s)
 (601, 6, 3, "ST3", "G", "the route draws itself south, then bends north-east into the mountains", "Top-down hand-painted topographic map of a flat green farming valley on the left and forested snowy mountains on the right, a river, roads as thin lines, aged paper, no labels or text at all."),
 (602, 6, 2, "BG4", "L", "the camera rushes up the winding road", "A narrow winding mountain road climbing through tall pines into snow, overcast grey daylight, snow banks growing deeper up the road."),
 (603, 6, 2, "ST1", "KH", "the ranger walks up to the car", "Daylight, overcast: a forest ranger in a green 1970s uniform and hat seen from behind, standing on a snowy forest road a few metres from the parked car." + CAR + NOFACE),
 (604, 6, 1, "ST3", "L", "a flyer slides onto the corkboard", "A corkboard in a 1970s ranger station with a single paper flyer pinned in the centre: five blank grey rectangles where photos would be and blank lines, no writing at all, a desk lamp glow."),
 (605, 6, 1, "BG4", "L", "two skiers glide across the frame", "Two cross-country skiers seen from behind in the distance on a snowy forest road, sunny winter day, pines heavy with snow." + NOFACE),
 # S07 clue 2: the car (32.8 s)
 (701, 7, 2, "ST1", "L", "snow squall sweeps across", "REUSE:ST1"),
 (702, 7, 2, "ST1", "KH", "snow sprays up from the spinning rear tyre", "Close on the rear tyre of the car spun into a shallow snowdrift, ruts and churned snow around it, daylight, grey sky." + CAR),
 (703, 7, 2, "ST1", "KH", "the gauge needle swings up to a quarter as the dash lights come on", "Close on the car's 1969 dashboard: a round fuel gauge with the needle at empty (no numbers or letters), the ignition with no key and two loose wires hanging below, cold daylight."),
 (704, 7, 2, "ST1", "L", "the camera slides along the clean underside", "View from under the car: a clean undamaged undercarriage and low-hanging muffler above a rough rutted snowy dirt road, light from the sides."),
 (705, 7, 3, "ST1", "L", "red circles snap onto each object", "The car's front bench seat seen from above: a neatly folded road map, two blank game programmes, sweet wrappers and empty milk cartons, daylight through the window. No text on anything."),
 (706, 7, 1, "ST1", "KH", "the driver's door swings open", "Two sheriff's deputies in 1970s uniforms seen from behind standing at the closed driver's door of the car on the snowy road, daylight." + CAR + NOFACE),
 # S08 the storm (9.5 s)
 (801, 8, 2, "BG4", "KH", "the snowcat's headlights fade into the white", "A whiteout snowstorm on a mountain road, a tracked 1970s snowcat with two headlights barely visible through the driving snow, wind streaks."),
 # S09 clue 3: the voices (53.8 s)
 (901, 9, 2, "ST1", "L", "the stuck car's headlights switch on", "Dusk on the snowy mountain road: a dark 1970s sedan stuck in snow, a man in a parka seen from behind standing beside it with a shovel planted upright in the snow, pines, last blue light." + NOFACE),
 (902, 9, 2, "ST1", "KH", "frost creeps across the windscreen", "Inside a 1970s sedan at night seen from the passenger side: a man lying across the front seat seen only as a dark coat and the back of his shoulder, dashboard glowing green, engine running, fogged windows." + NOFACE),
 (903, 9, 3, "ST1", "KH", "two headlights snap on in the darkness behind, then go out", "Through a fogged rear car window at night: the dark snowy road behind, black pines, total darkness except two headlights of another car shining from behind."),
 (904, 9, 2, "ST1", "KU", "the figures shift in the glare", "In the blinding glare of a car's headlights on a snowy road at night, a small group of dark human silhouettes stands beside the car, one figure appearing to hold a bundle in its arms. Silhouettes only, no faces, shapes blurred by glare."),
 (905, 9, 2, "BG4", "KU", "flashlight beams sweep through the trees and go out", "A dark pine forest at night beside a snowy road, three small flashlight beams among the trees, cold blue, misty."),
 (906, 9, 2, "BG4", "KH", "the man walks away down the road", "Grey dawn on a snowy mountain road, a single man in a parka seen from far behind walking downhill alone, pines, mist." + NOFACE),
 (907, 9, 2, "ST1", "L", "the camera pushes past the empty car", "Grey dawn: the car empty and dusted with fresh snow on the mountain road, a line of footprints passing beside it, mist in the pines." + CAR),
 (908, 9, 1, "BG4", "KH", "the lodge door opens and warm light spills out", "A rustic 1970s mountain lodge at dawn in snow, smoke rising from the chimney, one warm lit window, a wooden porch."),
 # S10 the weeks after (13.5 s)
 (1001, 10, 2, "ST3", "G", "flyers slide onto the board one by one", "REUSE:ST3"),
 (1002, 10, 1, "ST1", "KH", "a red pickup truck pulls away from the store", "A tiny 1970s mountain-town general store with a wooden porch and a blank sign, a red pickup truck parked in front, pines, slush on the ground."),
 (1003, 10, 1, "BG4", "L", "a heavy branch dumps its load of snow", "Heavy snow falling on dense pines, branches bowed under thick snow, soft grey light, quiet."),
 # S11 clue 4: the trailer (41.3 s)
 (1101, 11, 2, "ST2", "KU", "three motorcyclists ride up the gravel road", "Late spring in the mountains: three motorcyclists seen from behind riding up a gravel forest road, snow patches in the shade, sunlight through pines." + NOFACE),
 (1102, 11, 2, "ST2", "L", "the camera rushes toward the trailer", "REUSE:ST2"),
 (1103, 11, 2, "ST2", "KH", "a torn curtain blows out through the broken window", "Close on the broken window of an old 1970s camper trailer, jagged glass, a faded curtain inside, spring light, pine needles."),
 (1104, 11, 2, "ST2", "L", "a shaft of light swings across the room as the door opens", "Inside a dim old camper trailer seen from the doorway: a narrow bed at the far end under a pile of white sheets (only the sheets, nothing visible under them), a small table, dust in the air. Calm and respectful."),
 (1105, 11, 2, "ST2", "L", "the clearing changes from deep winter to spring", "The same forest clearing in deep winter: the old camper trailer and shed buried in snow up to the windows, pines heavy with snow, grey sky."),
 # S12 clue 5: what was never used (34.9 s)
 (1201, 12, 2, "ST2", "KH", "a draught swirls cold ash in the fireplace", "A small cold iron fireplace inside the trailer, a box of matches and a stack of paperback books beside it with blank covers, grey light."),
 (1202, 12, 2, "ST2", "L", "the heavy coats sway on their hooks", "Heavy green-and-brown forestry coats and boots hanging on hooks inside the trailer, dim light from a window."),
 (1203, 12, 2, "ST2", "KH", "an empty ration can topples and rolls", "Inside a wooden storage shed: a pile of opened empty olive-drab army ration cans on the floor, light through gaps in the planks, no labels or text."),
 (1204, 12, 2, "ST2", "L", "a red ring snaps around the closed locker", "Inside the same shed: a tall closed metal locker, untouched, dust on top, stacked boxes, light through the plank gaps."),
 (1205, 12, 1, "ST2", "L", "frost spreads over the closed valve", "A propane tank in a second small shed with its valve closed, cold blue light, frost on the metal, cobwebs."),
 (1206, 12, 1, "ST2", "L", "a snow squall blows past the dark trailer", "Night in deep winter: the camper trailer in the snowy clearing, all windows completely dark, no smoke, falling snow, cold blue."),
 # S13 clue 6: the shoes (48 s)
 (1301, 13, 2, "ST2", "L", "a red ring snaps around the shoes", "A pair of worn white tennis shoes alone on the plank floor of the trailer, pale light from the doorway."),
 (1302, 13, 2, "ST2", "L", "footprints appear one by one, leading away", "A single line of footprints in melting snow leading from the trailer's doorstep into the pine forest, grey dawn light."),
 (1303, 13, 2, "BG4", "KH", "the red marker flags flutter in the wind", "A spring roadside in the mountains with snowmelt, small red survey marker flags on wires stuck in the ground along the road, pines, overcast. No people, no bodies."),
 (1304, 13, 2, "ST3", "G", "pins drop on the map with distance counters", "REUSE:601"),
 (1305, 13, 1, "BG4", "L", "a gust shakes the manzanita bush", "A lone manzanita bush with red branches on a rocky mountain hillside, spring light, wide and quiet."),
 (1306, 13, 2, "BG4", "KH", "the search party walks up the forest road", "A search party of four men in 1970s outdoor clothes seen from behind walking up a muddy forest road in spring." + NOFACE),
 (1307, 13, 1, "BG4", "L", "fog rolls in and swallows the path", "An empty forest path at dusk disappearing into dense pines, fog gathering, nobody there."),
 # S13b clue 7: what the bodies showed (47.4 s)
 (1351, 14, 2, "ST2", "L", "a torch beam sweeps across the bed", "REUSE:1104"),
 (1352, 14, 3, "ST2", "L", "red circles snap onto each object", "Close on a small table in the trailer: a leather wallet, a plain ring, a thin gold chain necklace, a gold wristwatch with its glass crystal missing, and a half-melted candle stub. Soft grey window light."),
 (1353, 14, 2, "ST3", "G", "a checklist types itself line by line", "REUSE:ST3"),
 (1354, 14, 1, "ST2", "KH", "the second hand twitches, then stops", "Extreme close-up of a gold wristwatch face with no crystal and no numbers, simple hands, dust on the dial."),
 (1355, 14, 1, "ST2", "L", "a red ring around the empty floor", "The bare plank floor beside the trailer bed, no shoes there, a shaft of pale light."),
 # S14 bizarre as hell (8.3 s)
 (1401, 15, 2, "ST3", "G", "the red string snaps between car, trailer and road", "REUSE:ST3"),
 # S15 theory A: lost (39.9 s)
 (1501, 16, 2, "ST1", "KU", "the car's headlights swing onto the mountain road", "Night at a fork in the road at the foot of the mountains: one road leads flat into the valley, the other climbs into dark forest; the car turning onto the mountain road, headlight beams sweeping the trees, a blank road sign." + CAR),
 (1502, 16, 2, "BG4", "KH", "the snowcat crawls up the road leaving tracks", "Daylight: a 1970s orange tracked snowcat driving up a snowy forest road, leaving two wide tracks in the snow between high drifts."),
 (1503, 16, 2, "BG4", "L", "the camera pushes along the tracks", "Night: two wide snowcat tracks running up a snowy road between drifts taller than a person, moonlight, black pines."),
 (1504, 16, 3, "ST5", "KU", "the five walk away up the snow tunnel", "REUSE:ST5"),
 (1505, 16, 2, "ST5", "KH", "the five trudge forward through deep snow", "Five young men in light 1970s jackets seen from far behind trudging in a line through knee-deep snow on a moonlit snowfield, black pines, breath haze." + NOFACE),
 (1506, 16, 1, "ST2", "L", "a red ring snaps around the padlock", "Close on the trailer's door at night with a padlock on the latch, snow on the step, cold blue."),
 # S16 theory B (25.5 s)
 (1601, 17, 2, "ST1", "L", "the lights in the glare go dark", "REUSE:904"),
 (1602, 17, 2, "BG4", "L", "the distant lodge lights flicker", "Night on a high snowy road looking down the valley: far below, the tiny warm lights of a lodge; on the road above, five small dark figures seen from behind walking the other way, uphill." + NOFACE),
 (1603, 17, 2, "ST2", "L", "a question card slams in", "REUSE:1352"),
 # S17 theory C: Gary (17.5 s)
 (1701, 18, 2, "ST2", "L", "fluorescent lights flicker on down the corridor", "A long empty 1970s hospital corridor, pale green walls, linoleum floor, doors along the side, cold light. No people."),
 (1702, 18, 2, "BG4", "L", "the fog parts and reveals the deep forest", "A misty pine forest at grey dawn, deep and endless, a faint path."),
 # S18 the last question (19.5 s)
 (1801, 19, 2, "ST4", "KH", "the ball rolls off the court into shadow", "An empty outdoor basketball court at dusk beside a small-town school, a single ball resting under the hoop, orange sky."),
 (1802, 19, 2, "ST1", "KH", "the car's headlights flick on, then off", "Dusk: the car alone on the snowy mountain road seen from behind, the same framing as the opening, purple-blue sky, falling snow." + CAR),
 (1803, 19, 1, "ST3", "L", "the lamp clicks off", "REUSE:ST3"),
]

new = [s for s in S if not s[6].startswith("REUSE:")]
reqs = [dict(index=s[0], params=dict(model="nano_banana_2_1", resolution="2k", aspect_ratio="16:9",
             prompt=STYLE + s[6], medias=[dict(value=R[s[3]], role="image_references")])) for s in new]
for b in range(0, len(reqs), 8):
    json.dump(dict(requests=reqs[b:b + 8]), open(f"requests_batch{b // 8 + 1:02d}.json", "w"), indent=1)
cnt = {}
for s in S: cnt[s[4]] = cnt.get(s[4], 0) + 1
with open("shot_list_v001.md", "w") as f:
    f.write("# Yuba County Five: shot list v001\n\nGenerated by `make_shot_list.py` from script v002 and narration v001. "
            f"{len(S)} stills ({len(new)} new, {len(S) - len(new)} reused) → about {sum(s[2] for s in S)} cuts.\n"
            f"Motion: {cnt}. KU = producer's Kling plan, KH = Higgsfield Kling 3.0 std, L = local, G = edit graphic.\n\n"
            "| ID | Scene | Cuts | Motion | Big moving thing | Still |\n|---|---|---|---|---|---|\n")
    for s in S:
        f.write(f"| {s[0]} | {s[1]} | {s[2]} | {s[4]} | {s[5]} | {s[6][:110].replace('|', '/')} |\n")
print(len(S), "stills,", len(new), "new,", sum(s[2] for s in S), "cuts", cnt)
