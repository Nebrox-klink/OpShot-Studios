import json
STYLE = ("Painterly 2D gouache illustration for a serious animated documentary, graphic-novel lighting, visible brush strokes, muted palette, atmospheric haze, cinematic composition, not photorealistic; match the style of any reference images. No text, letters, numbers, signs or logos. No blood. SHOT: ")
R = {"BG1": "51586c50-8a26-4f88-83bd-bac68e376044", "BG2": "24d23986-fca7-451a-b2bb-03f602511b57",
     "BG3": "d691a1fb-90d8-4292-8224-e33c22ceafbb", "BG4": "add729dd-cf38-4eec-8a6c-70c3174bec60",
     "TOS": "f90ae53d-c66f-4d10-bfc2-906fb4dfa3db", "ROB": "6a11be37-5311-4589-8fe4-7d9f606c57c0"}
S = [
 (101,"BG1","A paved enclosed inner courtyard on a grey early morning, wet flagstones; low in the pale far wall, a wide thick faintly green laminated window in a dark steel frame. Empty. Palette: grey-green glass, cold steel blue, one sodium-amber lamp."),
 (102,"BG1 ROB","The same courtyard. A faceless dark-clad figure in overalls and balaclava, seen from behind at a distance, frozen at the top of a sledgehammer swing in front of the wide green glass window. Dread, cold steel-blue light."),
 (103,"BG1","Extreme close-up of thick faintly green laminated security glass in a dark steel frame, cold morning light, a single small pale scuff mark on the surface. Quiet and abstract."),
 (104,"BG1 ROB","The same courtyard seen from behind a faceless dark-clad figure in overalls and balaclava raising a rifle toward the wide green window; near-black silhouette, rifle only partly visible, no heroic pose, cold grey light."),
 (201,"BG3","The cathedral square at dawn, wide view: old grey stone cathedral, wet cobbles, bare trees, a small pond. Calm. Palette: warm wood tones, North Sea teal, soft white sky."),
 (203,"BG1","A row of low basement windows glowing with cool fluorescent light at street level along a plain 1970s commercial building in a Norwegian city at dawn, wet pavement."),
 (301,"","A row of modest Norwegian terraced townhouses at winter dusk, patches of snow, bare trees, one window glowing warm. Palette: ink blue, chalk white."),
 (302,"TOS","Inside a small kitchen at night: a slim man in a dark zip jacket seen strictly from behind, seated at a table under a single lamp, studying a chessboard. His face is not visible. Palette: ink blue, charcoal, one ivory accent."),
 (401,"","Top-down view of a hand-drawn floor plan in plain pencil lines on paper lying on a wooden table: simple room outlines and a courtyard square, absolutely no writing or labels, warm lamp light."),
 (402,"","An empty dark security guard's uniform jacket hanging on the back of a chair in a dim room, no badges, no text."),
 (501,"BG1 BG2","Night. Looking through a low wide greenish window from a dark courtyard into a warm lit basement room: pallets stacked with grey sealed bundles and two soft distant silhouettes of staff. Deep night blue outside, warm light inside."),
 (502,"BG1","Close-up of greenish window glass at night with the faint ghostly reflection of a crouched dark silhouette lying over the warm lit room inside."),
 (601,"BG1 TOS","Night in the enclosed courtyard in February, frost on the flagstones, a slim man in a dark jacket lying low and crouched against the wall near the green window, seen from behind, face hidden. Deep night blue, frost white, breath vapour."),
 (701,"","An Oslo side street at night in winter, old apartment buildings, snow on the ground, one doorway with warm light behind a closed door. Empty street. Melancholy."),
 (702,"TOS","Inside a Norwegian church in winter with candles: a lone figure in a dark jacket standing at a lectern, seen from far behind, face not visible. Soft dim light."),
 (731,"","A long empty wooden table under one bare hanging bulb in a dark room, four empty wooden chairs around it. Seen from a slightly high angle."),
 (704,"","Close-up of a strip of white cloth tape lying on a dark wooden table, low light."),
 (801,"","A gravel footpath through Norwegian woods at dawn leading to a concrete pedestrian underpass, mist, bare birches. Cold."),
 (802,"","The open back of a dark van at night: old mattresses, bedding and towels stacked inside, lit by a single street lamp."),
 (803,"","A dark disused industrial building at night; on its wall a small red alarm light glowing, wet ground reflecting it."),
 (901,"","A plain 1970s Norwegian police station building seen from the street on a grey day, concrete facade, a driveway, no signs or text."),
 (902,"","A thick bound document lying on an office desk under a desk lamp, its pages blurred, no readable text, night."),
 (903,"","A white Norwegian police estate car of the early 2000s parked at night under a street lamp, no legible text or markings."),
 (905,"","A small white coach bus on a quiet coastal road by the sea in low spring sunlight, green fields, a small white church in the distance. Warm and peaceful."),
 (1001,"","A row of terraced townhouses in darkness at half past three in the morning, a van's headlights sweeping across the walls, sodium amber light."),
 (1002,"ROB","Pine woods at night, torch beams cutting through the trees, several faceless dark-clad figures in overalls and balaclavas seen from behind, standing still. No weapons visible."),
 (1003,"ROB","Close-up of a white cloth band taped around the dark sleeve of work overalls, torch light, night."),
 (1004,"","Close-up of a plain analog wristwatch with a blank dial and no numbers on a dark gloved wrist, cold light."),
 (1101,"","A police briefing room in early morning light: rows of uniformed officers seen from behind, seated, a figure at the front softly out of focus, no faces visible, nothing written on the walls."),
 (1201,"","High-angle grainy security-camera view of an empty city street at dawn, monochrome blue-green tint, no text or timecode."),
 (1202,"","A white truck with a covered flatbed in a driveway beside a plain building, thick grey smoke rising from the cab, no flames spreading. Fire orange glow against blue-grey."),
 (1301,"BG1 ROB","The enclosed courtyard seen from behind three faceless dark-clad silhouettes standing at the wide green window, cold grey light with faint orange flashes on the walls. No weapon pointed at the viewer."),
 (1302,"BG1","Extreme close-up of thick green laminated security glass covered in white star-shaped impact marks, cracked but not broken, cold light."),
 (1304,"BG1","A ragged dark hole where the wide green window used to be in the courtyard wall, fragments of laminated glass hanging from the frame, dust hanging in the light."),
 (1401,"BG2","A basement corridor under fluorescent light: two steel trolleys loaded with grey sealed plastic bags, open freight lift doors at the end. No people."),
 (1402,"BG2","Closed steel freight lift doors in a basement corridor under fluorescent light. No people."),
 (1404,"BG3","The cathedral square in morning light, a white police car turning in at the far edge, small in the frame, no text."),
 (1501,"BG2","The counting room in cold light: bundles of blue banknotes wrapped in clear plastic on a steel table, no readable print or faces on the notes."),
 (1502,"BG2","A heavy barred steel vault gate in a basement, a heavy steel battering ram lying on the floor in front of it, cold fluorescent light."),
 (1503,"","Close-up of a plain analog wristwatch with a blank dial and no numbers on a dark gloved wrist, harsh fluorescent light, blurred basement behind."),
 (1601,"BG3","The cathedral square, wide view on a weekday morning: a city bus crossing in the far background, a few small distant figures, one pushing a pram, no faces."),
 (1602,"BG3","A white police car seen from behind on a city square, two officer silhouettes crouched behind its open doors, tense morning light, no text."),
 (1603,"BG4 ROB","A city street corner in the morning; far away, a small dark faceless silhouette of a man holding a rifle, standing still. Cold, distant."),
 (1701,"BG4","A street with a plain modern hotel facade on a grey April morning; far down the street, a dark police van seen from behind. Almost fully desaturated, one muted warm tone."),
 (1702,"BG4","A city bus seen front-on from a low angle, stationary on a grey street, almost fully desaturated. No text, no route number."),
 (1704,"","A pale grey morning sky over wet rooftops of a Nordic city, quiet, almost white."),
 (1801,"BG3","The empty cathedral square after a shooting: tyre marks and a few spent cartridge cases on the wet cobbles, no people, no blood."),
 (1802,"","Woods seen from a distance with a single column of black smoke rising above the trees, grey sky."),
 (1803,"","A truck cab scorched but still standing beside a plain building, thin smoke rising, grey light."),
 (1804,"","A small flat with drawn curtains: three dark silhouettes seen from behind, lit only by the blue glow of a television, sports bags on the floor. No faces."),
 (1901,"BG3","A large medieval grey stone cathedral on a grey April day, its doors open with warm light inside, wet paving. Soft warm grey and candle gold."),
 (1902,"","A small helicopter flying low over wet rooftops of a Nordic city, grey sky."),
 (2001,"BG2","A small foam earplug lying on a grey linoleum floor beside a plain yellow evidence marker with no number, flat clinical light."),
 (2002,"BG2","Close-up of a barred steel vault gate, a simple steel handle visible on the inside of the bars, cold light."),
 (2101,"","A white Andalusian village on a hillside in hot afternoon sun and heat haze, bleached yellow light."),
 (2102,"","An internet cafe at night in 2004: a row of glowing CRT monitors on desks, empty chairs, screens blurred, office fluorescent green."),
 (2202,"","The front steps of a plain police station in the morning, many candles and flowers laid on the steps, no people. Soft warm grey and candle gold."),
 (2203,"TOS","A small internet cafe in southern Spain in 2005: the back of a slim man in a light shirt sitting at a CRT monitor with a blurred screen, face not visible, bright sunlight outside."),
 (2204,"","The doorway of a small cafe seen from inside, bright street light outside, two dark silhouettes entering, no faces."),
 (2301,"","A large plain hall set up as a courtroom: empty rows of chairs facing a long table, muted slate light, no flags, no text."),
 (2401,"BG1","Morning. The courtyard window, intact clear new glass in a dark steel frame, warm morning light, soft reflections on the glass. Quiet and muted."),
]
reqs = []
for idx, refs, text in S:
    p = {"model": "nano_banana_2_1", "resolution": "2k", "aspect_ratio": "16:9", "prompt": STYLE + text}
    if refs:
        p["medias"] = [{"value": R[r], "role": "image_references"} for r in refs.split()]
    reqs.append({"index": idx, "params": p})
json.dump(reqs, open("shot_requests_v001.json", "w"), indent=1)
print(len(reqs))
for i in range(0, len(reqs), 8):
    open(f"batch_{i//8+1}.json", "w").write(json.dumps(reqs[i:i+8]))
