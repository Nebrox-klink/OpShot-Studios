# D.B. COOPER: pre-production v001

**Status:** script draft for review. Nothing has been generated: no images, voice or video. Waiting for producer feedback.
**Channel:** Spectare Animations · **Language:** English · **Audience:** adults, general audience · **Target length:** about 10 minutes (the NOKAS film held viewers for 4:45 on average at 9:54).

---

## 0. What carries over from THE NOKAS ROBBERY

| Lesson from the last film | How it is built into this one |
|---|---|
| "The pauses are very long" | Scene tails about 1.5 s; pauses inside sentences capped at 0.8 s (`timing.py` tight profile from day one). Long silences only at three designed beats: the cold open, 8:13 pm and the last line. |
| "The voice is flat and monotone" | Narration is written for performance: short sentences, performance tags ([tense], [softly], [beat]) and varied sentence length. The voice is cast with a 3-voice pilot of the cold open **before** the full voice is recorded (see §2.6). |
| Same painterly look | Same gouache style prompt and reference method as NOKAS (§2.2), with a new period colour palette: 1971 Kodachrome warmth against rain-night indigo. |
| Viewers didn't click (3.8% CTR) | The title and thumbnail hooks are chosen now, from facts in the script (§5), not after release. Hook first, name second. |
| Shorts get distribution | Four Shorts moments are marked in the script (◆). Their key shots are composed so they also crop to 9:16. |
| Facts | Every narrated fact goes into a source ledger before the voice is recorded. Uncertain items are flagged ⚠ in §4. No superlatives that aren't sourced. |
| Real people | No likeness of real people. Cooper's face is never shown, and the FBI sketch is not copied. The crew, the agent and the boy are seen from behind, in silhouette or at a distance. Nobody's inner thoughts are invented: the narration says only what they did or later said. |
| Generation hard limits | No lip sync (all dialogue is voice-over on shots without visible mouths). No precise hand work in motion (hands are stills only). No crowds in motion. No text, logos or airline livery in images; titles are added in the edit. |
| Don't glorify | Cooper is a mystery, not a hero. The film ends by asking why we made a hero of him, and gives the last word to the people on the plane. |

---

## 1. Logline and emotional core

**Logline:** The day before Thanksgiving 1971, a polite man in a dark suit hijacks a short flight to Seattle, trades the passengers for $200,000 and four parachutes, and steps out of the back of the plane into a freezing night. Then he vanishes so completely that America turns him into a legend.

**Emotional core:** *The legend and the people left behind.* The world remembers a clever thief who beat the system. This film sits in the seat next to him instead, with Tina Mucklow, 22, who spent hours beside a man with a bomb. It asks why the story we chose to love leaves her out.

---

## 2. Character sheet and visual style guide

### 2.1 Characters

All designs are stylised, not likenesses. Faces of real people are never shown clearly.

| Character | Role | Design (fixed for every shot) | Palette | Rules |
|---|---|---|---|---|
| **"Dan Cooper"** | The hijacker. Unknown identity. | Man in his mid-40s, about 180 cm, slim. Dark suit, white shirt, narrow black clip-on tie with a mother-of-pearl tie clip, dark raincoat, black attaché case, brown paper bag. Short dark hair. Dark wraparound sunglasses later in the flight. Cigarette smoke as his "signature". | Charcoal, white, black; a warm cigarette-ember accent. | **Never a clear face.** Shown from behind, in shadow, as a reflection in a dark window, or as sunglasses and smoke. Not based on the FBI composite sketch. |
| **Tina Mucklow** | Flight attendant, 22. Our eyes on the plane. | Generic 1971 airline uniform (no real airline's design or insignia): fitted jacket, short skirt, scarf, small cap; dark hair pinned up. | Muted teal and cream, which read as warm against Cooper's charcoal. | Seen from behind, over her shoulder, or as a small figure in a wide shot. No inner thoughts beyond what she told the FBI. |
| **Florence Schaffner** | Flight attendant, 23. Receives the note. | Same uniform as Tina; lighter hair, worn shorter. | Same. | Same rules. Appears in scenes 4–6 only. |
| **Captain William Scott** and crew | The cockpit. | Pilots' shirts and caps; seen from behind against the instrument panel. | Cockpit green-grey; red warning light. | Backs of heads only. |
| **Ralph Himmelsbach** | FBI agent, Portland; also a pilot. The pursuer. | Man in his 40s, 1970s suit and trench coat, short hair. Seen in silhouette at a small plane's window, or on a forest road. | Grey-brown, wet green. | No face. |
| **The boy** (Brian Ingram, 8, in 1980) | Finds the money. | A small boy in a red winter jacket, seen from behind on a river beach. | Red against pale winter sand. | No face; never named on screen unless the family's public statements support it. |
| **The plane** | A character in its own right. | Boeing 727-100 with a rear airstair under the tail. Livery: **plain, generic**, with no logo or lettering. | Silver and white; the open rear stairs as a dark mouth. | The aft stairs must match the real 727 design. |

### 2.2 Style (the same look as NOKAS)

The prompt prefix stays the same, so the series has one look:

> *Painterly 2D gouache illustration for a serious animated documentary, graphic-novel lighting, visible brush strokes, muted palette, atmospheric haze, cinematic composition, not photorealistic; match the style of any reference images. No text, letters, numbers, signs or logos. No blood.*

Additions for this film: *1971 United States, period-accurate clothing, cars, airport and aircraft interiors; Boeing 727-100 with rear airstair; generic aircraft livery without logos.*

The method is the same as before: first approve 4–6 style references (the airport, the cabin, the 727 at night, the forest, the river beach), then use them as `image_references` for every shot.

### 2.3 Colour script (the palette follows the story)

| Act | Scenes | Palette | Feeling |
|---|---|---|---|
| Cold open | 1 | Rain-night indigo, black, a single red cockpit light | Dread |
| I: Portland, the flight | 3–6 | 1971 Kodachrome: amber, mustard, olive, warm cabin cream; grey rain outside | Ordinary, almost cosy, which makes the threat feel worse |
| II: Circling, Seattle | 7–11 | Dusk magenta into blue; then sodium-orange airfield floodlights in the rain | Waiting, pressure |
| III: The jump | 12–15 | Deep indigo and black; red warning light; a cold white crack of light at the open stairs | Point of no return |
| IV: The search | 16–19 | Daylight forest: wet green-grey, fog | Emptiness |
| V: The river, the legend | 20–22 | Pale winter gold on sand; faded newsprint sepia for the legend montage (no readable text) | Mystery, irony |
| Ending | 23 | Back to the cabin: one warm amber reading light in the dark | Reflection |

**Creative freedom:** Act V may break palette (sepia folk-art posters, festival lights at the town party) as a deliberate tonal shift. The Shorts can lean harder into the indigo and red.

### 2.4 Camera language
- **Establishing:** wide painterly plates with slow parallax (Portland airport in rain, the 727 on a dark apron, the forest canopy from above).
- **Tension:** slow push-ins on objects instead of faces: the folded note, the briefcase latch, the red light, the stair handle.
- **Emotion:** close-ups of hands and objects (stills only), backs of heads, the empty seat.
- **Signature shot:** the open rear stairs seen from inside the cabin, rain streaming past. It is used three times: the cold open, 8:13 pm and the final image.

### 2.5 Sound palette
- **Ambience:** 727 engine drone (three rear engines), cabin ventilation hiss, seatbelt chime, intercom crackle, rain on aluminium, forest rain, river water.
- **Music:** a sparse 1970s-tinged motif (electric piano, muted strings, low synth pulse). It thins out as tension rises and **cuts to silence at 8:13 pm**.
- **Silence beats (the only long pauses):** after the cold open's last line, at the jump, and before the last line.

### 2.6 Narrator voiceover (fix for "flat and monotone")
- **Casting brief:** a deep, warm, serious voice, 45–60. A storyteller by a fire, not a newsreader. A slight American warmth suits the story.
- **Process:**
  1. Generate the cold open (scene 1, about 35 s) with **3 candidate voices** on `eleven_v4`, using performance tags and a lower stability setting. About 1,000–1,300 credits.
  2. The producer picks one.
  3. Record the full film. About 7,000 characters, roughly the same credits.
- **Delivery rules in the script:** short sentences in tense passages; [beat] or [pause] before reveals; [softly] in the emotional scenes; no long lists.
- **Dialogue lines** (Cooper's three short lines) use a separate, quiet, flat voice through an intercom-style filter. They are never played over a visible mouth.

---

## 3. The script

Durations are approximate (narration at about 145 words per minute plus breathing room). **Total ≈ 9:45 before credits** (1,215 narration words; tight timing). ◆ = a Shorts moment.

---

### Scene 1 · Cold open: 8:13 pm · 0:00–0:35 ◆
**VISUAL:** Black. A red light blinks on a dark instrument panel, seen past a pilot's shoulder. Cut to the empty rear cabin: dim, rows of empty seats, cigarette smoke still in the air. Slow push-in down the aisle toward the open rear stairs: a dark rectangle with rain streaming past, cold white light. Exterior: a 727 seen from far below, a silver shape in rain and cloud over black forest.
**NARRATION:**
[low, close] Eight-thirteen in the evening. About ten thousand feet above the forests of southwest Washington.
[pause] In the cockpit, the crew feel it. A small jolt. The tail lifts, just slightly.
[beat] Then nothing.
Behind a closed door, at the back of the plane, the stairs are open to the rain and the dark. And the man who opened them… [pause] is gone.
[softly] No one saw him jump. No one has seen him since.
**SOUND:** Engine drone, wind roar from the open stairs, rain. A soft thump in the airframe, then the music drops out. 2 s of near-silence after the last line.

### Scene 2 · Title · 0:35–0:41
**VISUAL:** Rain on a dark cabin window. The title fades up (added in the edit): **D.B. COOPER**.
**SOUND:** One low electric-piano chord.

### Scene 3 · Portland, the day before Thanksgiving · 0:41–1:08
**VISUAL:** Wide establishing shot: Portland airport, 1971, grey afternoon, rain. Period cars, travellers with suitcases. Interior: the ticket counter from behind the man in the dark raincoat. Cash on the counter (still).
**NARRATION:**
[warm, unhurried] Portland, Oregon. The afternoon before Thanksgiving, nineteen seventy-one. Rain on the windows. People heading home for the holiday.
At the Northwest Orient counter, a man in a dark suit buys a one-way ticket to Seattle. A thirty-minute flight. He pays cash.
He gives his name as Dan Cooper.
[beat] Remember that name. Because the world is about to get it wrong.
**SOUND:** Terminal murmur, rain on glass, a distant boarding announcement (no words).

### Scene 4 · The man near the back · 1:08–1:34
**VISUAL:** Warm cream-and-mustard 727 cabin. Cooper seated near the back, seen from behind and the side: raincoat, black tie, briefcase on his lap. Cigarette smoke curls in a beam of window light. A glass of bourbon and soda on the tray (still).
**NARRATION:**
He takes a seat near the back. Mid-forties, people will say. Calm. White shirt. A thin black tie.
A briefcase on his lap.
He orders a bourbon and soda, and lights a cigarette.
[pause] In nineteen seventy-one you could smoke on a plane. You could also carry a briefcase on board, and nobody would ask what was inside.
**SOUND:** Engines spooling, the seatbelt chime, a lighter's click.

### Scene 5 · The note · 1:34–2:01 ◆
**VISUAL:** The 727 pushes back in rain. Florence Schaffner in the rear jump seat, from behind. A folded note held out to her (still, hands). She slips it into her pocket. Push-in on the pocket. Cooper leans slightly toward her: a silhouette against the window.
**NARRATION:**
Ten to three. The plane pulls away from the gate.
Florence Schaffner is twenty-three. A flight attendant, sitting in the jump seat at the back. The man hands her a folded note.
She slips it into her pocket, unread. Men did that. Phone numbers, mostly.
[pause] He leans toward her.
**DIALOGUE:** COOPER (V.O., quiet, flat): "Miss, you'd better look at that note. I have a bomb."
**SOUND:** Engine rising. The music stops dead before his line. Silence under the dialogue.

### Scene 6 · The briefcase · 2:01–2:23
**VISUAL:** Schaffner now seated beside him (seen from behind, two heads in a row). The briefcase lid opens a few centimetres (still): red cylinders, coloured wires, a battery, all in shadow. Push-in. Cut to her pen on a small notepad (still, no readable writing).
**NARRATION:**
[tense] She sits down beside him. He opens the briefcase. Just a crack.
Red cylinders. Wires. A battery.
[pause] Then he tells her what he wants. Calmly. Precisely.
Two hundred thousand dollars in cash. Four parachutes. And a fuel truck, waiting in Seattle.
She writes it all down.
**SOUND:** Low synth pulse begins. The latch click is exaggerated.

### Scene 7 · The cockpit · 2:23–2:46
**VISUAL:** The long aisle seen from the back: Schaffner walking forward, passengers reading newspapers (still figures, no readable text). Cockpit: Captain Scott and crew from behind, radio headset, rain on the windscreen.
**NARRATION:**
Florence walks the length of the plane to the cockpit. Captain William Scott radios the ground.
[pause] Behind them, three dozen passengers read their newspapers and watch the rain. The captain tells them there's a small mechanical problem. They'll circle for a while.
[beat] Not one of them knows about the briefcase.
**SOUND:** Radio crackle with indistinct voices, cabin chime.

### Scene 8 · The seat beside him · 2:46–3:19
**VISUAL:** Tina Mucklow sits down beside Cooper: two figures from behind. He puts on dark sunglasses: seen as a reflection in the black window. Through the window: Puget Sound in rain-light, wooded islands far below.
**NARRATION:**
Another flight attendant takes Florence's place. Tina Mucklow. Twenty-two.
For the next few hours, she will be the one sitting beside him.
[pause] Later she'll tell the FBI he was calm. Polite. Not nervous at all.
He puts on dark glasses. He looks out of the window and seems to recognise the ground below. He mentions Tacoma. He knows where the air force base is.
[softly] A man who seems to know exactly where he is.
**SOUND:** Engine drone, muted. The motif returns, very quietly.

### Scene 9 · The money · 3:19–3:52
**VISUAL:** Seattle, ground, late afternoon: a bank vault interior with stacks of banknotes on a table (no readable print). An agent at a microfilm camera, seen from behind, with a flash of light. Parachute packs on a hangar bench.
**NARRATION:**
On the ground, everything moves fast. The airline's president agrees to pay.
The FBI gathers ten thousand twenty-dollar bills. And before they hand them over, agents photograph every single one.
[beat] Every serial number. On film.
[pause] The parachutes come from a skydiving school near Seattle. And the agents notice something about the order. Four parachutes. Not one.
[tense] Four means he might take someone with him. So nobody dares give him a faulty one.
**SOUND:** Camera shutters, a bank's hush, the low pulse.

### Scene 10 · Circling · 3:52–4:12
**VISUAL:** Exterior: the 727 small against a vast dusk sky over Puget Sound, magenta into blue. City lights coming on below. Interior: the warm reading light over two figures, Tina and Cooper, from behind.
**NARRATION:**
For two hours, Flight 305 circles over Puget Sound.
Below, the lights of Seattle come on. Up here, it's strangely quiet.
[softly] A man with a bomb. A young woman beside him. And three dozen people who think they'll be a little late for dinner.
**SOUND:** Engines, a soft chime, the motif on electric piano.

### Scene 11 · Seattle, 5:39 pm · 4:12–4:43
**VISUAL:** The 727 rolls to a remote, floodlit corner of the airfield in heavy rain. Sodium-orange light, long shadows. A figure at the foot of the stairs hands up a heavy canvas bag (wide shot, no faces). Then parachute packs. Passengers file off into the rain (a small, static group seen from a distance).
**NARRATION:**
Five thirty-nine. The plane lands in Seattle, and rolls to a dark corner of the airfield. Away from the terminal.
Tina goes to the door. A man from the airline hands up a cloth bag. Twenty-one pounds of cash. Then the parachutes.
[pause] Only then does he let the passengers go. They step out into the rain, still not sure what just happened.
Florence goes with them.
[beat] Tina stays.
**SOUND:** Rain hammering the fuselage, a fuel truck idling, footsteps on metal stairs.

### Scene 12 · The flight plan · 4:43–5:14
**VISUAL:** Cockpit from behind: the crew turning to listen to the intercom. Inserted diagram-style painting: the 727 in profile, gear down, flaps lowered, rear stairs hanging open beneath the tail (no labels). Map lines are added in the edit if needed.
**NARRATION:**
Now he tells the crew exactly how to fly.
To Mexico City. Low. Below ten thousand feet. Landing gear down. Flaps lowered. As slow as the plane can fly without falling out of the sky.
And once they're airborne… the rear stairs open.
[pause] A seven-twenty-seven can't get to Mexico like that. They agree on a fuel stop in Reno.
[beat] He doesn't argue. Maybe he never planned to get that far.
**SOUND:** Intercom crackle, the pulse rising.

### Scene 13 · The last look · 5:14–5:38 ◆
**VISUAL:** Takeoff at night in rain (exterior, wide). Interior: Tina walks toward the cockpit, seen from behind; she turns her head slightly back (no face). Her point of view: at the far end of the dim cabin, Cooper standing in the aisle in silhouette, tying the bag around his waist (a still, with smoke drifting). The cockpit door closes on it.
**NARRATION:**
Seven-forty. Flight 305 takes off again, into the rain and the dark.
A few minutes later, he tells Tina to go up to the cockpit. And stay there.
[pause] She looks back, once. He's standing in the aisle, tying something around his waist.
[softly] She is the last person known to see him.
**SOUND:** Takeoff roar, then the muffled thunk of the cockpit door. Music thins.

### Scene 14 · The red light · 5:38–5:55
**VISUAL:** Close on the instrument panel: a red warning light blinks (no readable labels). The crew from behind. An intercom handset (still).
**NARRATION:**
Eight o'clock. A red light on the panel. The rear stairs are open.
[pause] Over the intercom, the crew ask if there's anything he needs.
One word comes back.
**DIALOGUE:** COOPER (V.O., through intercom crackle, wind behind it): "No!"
**SOUND:** Wind roar under the intercom. Then only engines.

### Scene 15 · 8:13 pm · 5:55–6:20 ◆
**VISUAL:** Repeat of the cold-open shot down the aisle to the open stairs, now held longer. Exterior: the 727 passes over the black forest in rain, moving away from camera. Nothing falls (no figure is shown jumping).
**NARRATION:**
[very quiet] Eight-thirteen.
The jolt. The tail lifts. [pause] And the plane flies on. A little lighter.
[long pause]
For two more hours they fly toward Reno, too afraid to open the door. Not knowing if he's still back there. Sitting in the dark. With the bomb.
**SOUND:** The thump. **3 s of total silence** (designed beat). Then engine drone fades back in.

### Scene 16 · Reno · 6:20–6:37
**VISUAL:** Reno airport at night, floodlights, police cars (1971 models, no markings readable) around the plane. A figure climbs the rear stairs with a flashlight. Inside: the empty seat. On it, a black clip-on tie with a mother-of-pearl clip (still). Two parachutes on the floor, one cut open.
**NARRATION:**
Ten-fifteen. Reno. Police surround the plane. Someone climbs the rear stairs, into the cabin.
[pause] Empty.
He took the money. He took the briefcase.
He left behind two parachutes, a few cigarette ends… and a black clip-on tie.
**SOUND:** Car radios, a flashlight click, rain dripping in the open cabin.

### Scene 17 · The wrong name · 6:37–7:03
**VISUAL:** A 1971 newsroom at night: typewriters, smoke, a teletype (no readable text). A newspaper press rolling (blurred, no headlines).
**NARRATION:**
That night, police question a man in Portland whose name really is D.B. Cooper. He has nothing to do with it, and he's cleared quickly.
But a reporter hears that name. And it gets into the news.
[beat] The hijacker who called himself Dan becomes "D.B." Cooper. A name that never belonged to him. And it sticks.
**SOUND:** Typewriters, teletype chatter, the press thumping.

### Scene 18 · The search · 7:03–7:28
**VISUAL:** A small plane low over endless wet forest; inside, a silhouette at the window (Himmelsbach). Spring 1972: lines of soldiers seen from far above in fog (a static wide shot, no crowd motion). Mud, a creek, nothing.
**NARRATION:**
Ralph Himmelsbach is an FBI agent in Portland, and a pilot. He flies low over the woods for days, looking for a parachute caught in the trees.
In the spring, hundreds of soldiers search on foot. Rain. Mud. Endless forest.
[pause] They find nothing. Not a shoe. Not a strap. Not a scrap of nylon.
**SOUND:** Small-plane engine, rain on leaves, a creek.

### Scene 19 · The legend · 7:28–8:07
**VISUAL:** A tonal break: a sepia montage in folk-poster style, with silhouettes of a man with a parachute, a smalltown tavern with warm windows and string lights, festival bunting (no readable text). Then back to grey: a 727 tail with the "Cooper vane" (a small metal flap by the stairs), a technical still.
**NARRATION:**
And then something strange happens. People start rooting for him.
There are songs. T-shirts. A small town throws a party in his name.
To many, he's the man who beat the system, and nobody got hurt.
[pause] Himmelsbach saw it differently. He called Cooper a rotten, sleazy crook. A man who carried a bomb onto a plane full of people.
[beat] Others try to copy him. So Boeing adds a small metal flap that keeps the rear stairs shut in flight. Pilots call it the Cooper vane.
**SOUND:** A jaunty period tune, distant and tinny, as if from a jukebox. It cuts abruptly to cold wind on "Himmelsbach saw it differently".

### Scene 20 · The river · 8:07–8:36 ◆
**VISUAL:** February 1980. A pale sandy beach on the Columbia River, grey water, winter light. A small boy in a red jacket kneels in the sand, from behind (still for the hands and the find). Rotten bundles of banknotes, held by old rubber bands, half-buried (no readable print).
**NARRATION:**
February, nineteen eighty. Eight years later.
On a sandy bank of the Columbia River, an eight-year-old boy is helping his family clear a spot for a campfire.
[pause] In the sand, he finds money. Bundles of old twenty-dollar bills, rotting, still held by rubber bands.
Five thousand eight hundred dollars.
[beat] The serial numbers match the ones the FBI photographed. Eight years before.
**SOUND:** River water, wind, a child's distant voice (no words), the motif returning.

### Scene 21 · More questions · 8:36–8:57
**VISUAL:** The river from above, winding through forest toward the hills of the likely drop zone. The current over sand. A drifting mist.
**NARRATION:**
It should have solved the case. Instead it made it stranger.
How did the money get here? Did the river carry it? Did someone bury it?
Did he make it… [pause] or did he never make it at all?
The rest of the money has never been found.
**SOUND:** Water, low strings.

### Scene 22 · Closed · 8:57–9:10
**VISUAL:** An archive room: filing boxes stacked high, a lamp switching off (no readable labels).
**NARRATION:**
In twenty sixteen, after forty-five years and hundreds of suspects, the FBI stopped actively investigating.
It remains the only unsolved hijacking of an American passenger plane.
**SOUND:** A lamp click. Silence.

### Scene 23 · The seat beside him · 9:10–9:45
**VISUAL:** Back in the 1971 cabin at night, empty, one warm reading light over two empty seats side by side. Slow push-in. Final image: the open rear stairs, rain, darkness. Fade to black.
**NARRATION:**
[softly] Tina Mucklow spent more time with him than anyone. She gave her statements. And for most of her life, she chose not to talk about it.
[pause] We remember the money. The parachute. The name that wasn't his.
We tend to forget the people who were on that plane.
[long pause] For fifty years, people have asked where Dan Cooper landed.
[beat] Maybe the better question is why we wanted him to.
**SOUND:** Engine drone, very faint; the motif's last chord; **2 s of silence** before the last line; rain into black.

### Credits · 9:45–10:15
Text cards (added in the edit): sources, "Dramatised reconstruction; scenes and dialogue are recreated", the AI disclosure and music credits.

> **Runtime:** about 9:45 plus 30 s of credits, estimated from 1,215 narration words at the NOKAS v005 pace (about 2.45 words per second plus the designed pauses). That is close to the 10-minute target. If the chosen voice reads slower, the first cuts are scene 22 and the second half of scene 19.

---

## 4. Dramatised versus documented

**Documented** (widely reported, from the FBI case and contemporary accounts; to be sourced in the ledger):
- 24 November 1971, the day before Thanksgiving. Northwest Orient Flight 305, Portland to Seattle, a Boeing 727. One-way ticket bought in cash under the name "Dan Cooper".
- His appearance: a dark suit, white shirt, black clip-on tie, raincoat, briefcase. Bourbon and soda; he smoked.
- The note handed to Florence Schaffner, who pocketed it unread. The line "Miss, you'd better look at that note. I have a bomb."
- The briefcase with red cylinders, wires and a battery.
- His demands: $200,000, four parachutes, a fuel truck in Seattle.
- The passengers were told of a mechanical problem, and the plane circled about two hours.
- Tina Mucklow sat with him. She described him as calm and polite. He appeared to recognise Tacoma and McChord Air Force Base from the air.
- 10,000 twenty-dollar bills, with the serial numbers photographed on microfilm. Parachutes from a local skydiving school. About 21 lb of cash.
- Landed in Seattle at 5:39 pm; the passengers and two flight attendants were released.
- His flight instructions: Mexico City, low and slow, gear down, flaps, the rear stairs. A fuel stop in Reno agreed.
- Took off about 7:40 pm. Mucklow was sent to the cockpit, saw him tying something around his waist, and was the last to see him.
- About 8:00 pm the aft-stair warning light. The intercom answer: "No!"
- About 8:13 pm the tail pitched up.
- Landed in Reno about 10:15 pm; the cabin was empty. Left behind: the tie and clip, two parachutes, cigarette butts.
- A Portland man named D.B. Cooper was questioned and cleared; the press used "D.B.".
- The Himmelsbach search; the soldiers' search in spring 1972.
- The folk hero, the songs and the annual party in Ariel, Washington.
- Copycat hijackings, and the "Cooper vane" on the 727.
- February 1980: Brian Ingram, 8, found $5,800 at Tena Bar on the Columbia River; the serial numbers matched.
- 2016: the FBI ended its active investigation. The only unsolved US commercial air piracy case.

**Dramatised** (atmosphere and staging, not new facts):
- Rain at the Portland airport and the terminal atmosphere. The lighter click, the light beams, the smoke "signature".
- The exact staging of the note and the briefcase moments (who sat where, camera angles).
- "Men did that. Phone numbers, mostly": the narrator's interpretation of why she pocketed it.
- The cabin's quiet during the circling; "late for dinner".
- Tina "looking back once": she did see him in the aisle, but the turn of her head is staged.
- The newsroom scene and the reporter (it compresses how the name spread).
- The sepia legend montage.
- The final reflections (scene 23): an editorial voice, clearly the narrator's, not attributed to anyone.
- No dialogue has been invented. Cooper's two spoken lines are reported quotes, with the wording to be checked against the sources.

**⚠ To verify in the ledger before the voice is recorded:**
1. Florence Schaffner's age (23) and Tina Mucklow's age (22).
2. The exact wording of "Miss, you'd better look at that note. I have a bomb."
3. Whether he put on sunglasses during the flight (widely reported) and his remarks about Tacoma and McChord.
4. That the plane left the gate at about 2:50 pm, and the landing times (5:39 pm and about 10:15 pm).
5. That Himmelsbach personally flew search flights.
6. That the intercom reply was "No!" and the time it was given.
7. Whether "three dozen passengers" (36) excludes Cooper.
8. Whether the boy is described as "helping clear a spot for a campfire" in the family's own accounts.
9. "Only unsolved hijacking" (use the FBI's exact phrasing: "the only unsolved air piracy in American aviation history").
10. Whether "eight years later" is correct for February 1980, counted from November 1971 (8 years 3 months). The script uses "eight years later".

**Rights and dignity:**
- Mucklow, Schaffner and Ingram are living private individuals, so no likeness and no invented feelings. Consider a courtesy check, the same as for the Klungland family.
- No real airline logo or livery in the images; the airline is named only in the narration.
- The FBI composite sketch is not reproduced.

---

## 5. Packaging, planned before production

- **Title directions (hook first):**
  - *He Asked for Four Parachutes. Then He Vanished.*
  - *The Man Who Stepped Off a Plane and Disappeared*
  - *His Name Wasn't D.B. Cooper*
- **Thumbnail directions:**
  - the open rear stairs, with rain and darkness: "8:13 PM";
  - a silhouette with a parachute bag against the indigo sky: "NEVER FOUND";
  - the river-sand money: "$5,800. THE REST? GONE."
- **Shorts (◆):**
  - the cold open (scene 1);
  - "Miss, you'd better look at that note" (scene 5);
  - "the last person to see him" (scene 13 into 15);
  - the boy on the river (scene 20).

---

## 6. Next steps (after the producer approves the script)
1. The source ledger, checking every narrated fact, with §4 ⚠ resolved.
2. The voice pilot: the cold open in 3 voices (needs approval; spends ElevenLabs credits).
3. Style references (4–6 images; needs approval; Higgsfield credits).
4. Shot list and shot stills, then motion, then the animatic. Same pipeline as NOKAS.
