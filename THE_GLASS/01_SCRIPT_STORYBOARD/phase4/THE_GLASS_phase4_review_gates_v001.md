# THE GLASS: Phase 4 review gates (v001)

**Status:** for approval. It is the last gate before any image, voice or video generation. Nothing has been generated.
**Reviews:** `01_SCRIPT_STORYBOARD/revised/THE_GLASS_script_v007_phase3.md`, kept at full length (about 7,400 characters; the cut list was not applied).
**Not legal advice.** This is a production checklist. Items marked ⚖ should be confirmed by a Norwegian media lawyer before publication. Statutory details marked *(verify)* are from my knowledge, not from a source read in this project.

---

## 1 · Legal and ethics checklist

Status key: ✅ clear in v007 · ⚠ action needed · ⚖ lawyer or official check before publication.

### 1A · Facts and fairness (Vær Varsom-plakaten as our standard)

The Norwegian press code is binding only on members of the Norwegian Press Association, but it is the right standard for a documentary about real people. Section numbers are *(verify)* against the current text at presse.no, which this environment cannot reach.

| # | Check | Status | Notes |
|---|---|---|---|
| L1 | Every factual line traceable to a source | ✅ | All narration lines are tagged; 10 are `[FRAMING]`. The ledger holds the sources. |
| L2 | Medium-confidence facts | ⚠ | F20 ("fifteen seconds"), F60 (chess), F08 (15 March), F16 (silence). Confirm in *Dødsranet*, or soften to "reportedly". **Recommendation:** soften F20 in Scene 1 to "He had reportedly given it fifteen seconds" unless the book is checked. |
| L3 | Disputed facts presented as disputed | ✅ | F05 (why February was called off) is narrated as disputed. |
| L4 | Strong accusations: the accused's own position is included (4.14, simultaneous rebuttal) | ✅ | Schumann's "mistake" claim is given before the court's finding. The guard's "I thought it was a burglary" is given. |
| L5 | Court findings stated as findings, not as narrator verdicts | ✅ | "The court found it was an aimed shot." |
| L6 | Sentence figures | ✅ | Final Supreme Court sentence only: 18 years (F54). |
| L7 | Corrections process | ⚠ | Add a pinned comment or description line: "Spotted an error? Tell us," with a dated correction log in the repo. |

### 1B · Named and identifiable people

Identification in criminal matters is covered by section 4.7 *(verify)*.

| Person | Status | Named? | Assessment |
|---|---|---|---|
| David Toska | Convicted; released on parole 2018 | Yes | Name central to a widely documented case and used in all national media. Nothing about his present-day life. Shown only from behind or in shadow. ✅ |
| Kjell Alrich Schumann | Convicted; released 2019 | Yes | As above. His claim is quoted alongside the court finding. ✅ |
| William Ellingsen | Deceased, not convicted in this case | Yes | Named in NRK on record. Narrated as co-planner, which is documented (F06). ⚠ **Consider his family**: no images, no details of the shooting. v007 complies. |
| The 26-year-old guard | Convicted | **No** | Kept unnamed. ✅ |
| Erik Håland | Police officer | Yes | Quoted from his own on-record NRK interview. ✅ |
| Steffen Thesen | Police officer | Yes | Named in R01/R04, not interviewed by us. ⚠ **Recommendation:** drop his name in Scene 16 ("two officers, Erik Håland and his partner"). It costs nothing and avoids naming a private person needlessly. |
| Fred Sherling, the cyclist, the three women, NOKAS staff | Bystanders and staff | **No** | Kept unnamed and faceless. ✅ |
| Erling Havnå and other robbers | Convicted | **No** | "A man swings a sledgehammer." ✅ |
| Arne Sigve Klungland | Deceased victim | Yes | See section 2 and gate G-FAM. |
| Klungland's wife and children | Relatives | **No** | "A wife and two children": no names. ✅ |

### 1C · Images, likeness, AI

| # | Check | Status | Notes |
|---|---|---|---|
| L8 | **Klungland portrait** | ⚖⚠ | Under Norway's image-rights rule (åndsverkloven § 104 *(verify)*), the protection of a portrait of a person runs for the depicted person's life plus 15 years. He died in 2004, so it has likely expired. But **the reference photo itself is someone's copyrighted photograph.** Get a reference photo **from the family, with permission**, or from a rights holder under licence. Do not trace a press photo. |
| L9 | AI likeness of real people | ⚠ | Check the Higgsfield/model terms on depicting real, identifiable people before generating the portrait. Toska and Schumann are never shown as recognisable faces. |
| L10 | Illustrations looking like evidence | ✅/⚠ | Scene 20 shows a painted earplug and evidence marker in a stylised, painterly look. It must never look like a real police photograph. Keep it painterly and add no fake case numbers (v007 already has none). |
| L11 | AI disclosure | ⚠ | YouTube requires disclosure of realistic altered or synthetic content about real events or people. **Tick the disclosure box** and add an opening card: "A dramatised reconstruction. Illustrations are AI-assisted; the narration voice is synthetic. Quotes are from published interviews." |
| L12 | Real places | ✅ | Public exteriors only (cathedral square, police station, a generic courtyard). The NOKAS courtyard interior is a stylised interpretation; label it as such in the credits. |

### 1D · Quotes, sources, music

| # | Check | Status | Notes |
|---|---|---|---|
| L13 | Quotation right | ⚖ | Three short quotes (Schumann ×2, Håland), translated from NRK interviews. Short quotation "in accordance with good practice" is generally allowed (åndsverkloven § 29 *(verify)*). **Credit NRK on screen** when quoted, and in the description. |
| L14 | Source credits | ⚠ | End card or description: NRK (Nokas-ranet series, 2024), Stavanger Aftenblad, Aftenposten, *Dødsranet* (Aass & Widerøe) if used, Wikipedia, SNL. |
| L15 | Film *Nokas* (2010) and books | ✅ | Reference only. No footage, stills or text copied. |
| L16 | Music and sound effects | ⚠ | Not yet sourced. Use only owned, commissioned or properly licensed tracks; log every licence in `00_PROJECT_MANAGEMENT`. |
| L17 | Fonts and map data | ⚠ | Use licensed fonts. For maps use OpenStreetMap with attribution "© OpenStreetMap contributors" (ODbL). |

## 2 · Sensitivity pass: Arne Sigve Klungland (line by line)

Rule carried from the start: dignity, no gore, no invented words, seen only from outside.

| Scene | Line or image | Risk | Verdict |
|---|---|---|---|
| 9 | "One of the men who did read it was Arne Sigve Klungland." | None. Documented (F12). | ✅ Keep. |
| 9 | Portrait, warm, slow push-in | Likeness and consent (L8). An AI portrait may look "almost" right, which is worse than not at all. | ⚠ Keep **only** with a family-provided reference and their approval of the final image. **Fallback:** no face; his police cap on a desk, or the coastal road near Riska. |
| 9 | "Dog handler. Rescue leader. He trained police students." | None. | ✅ Keep. |
| 9 | "On church trips, he was the one who drove the pensioners' bus." | It sets up the bus at 08:17. If the audience notices the setup, the detail can feel engineered. | ⚠ Keep, but **no musical sting, no visual echo**: the Scene 9 vehicle is a small coach on a coastal road, and the Scene 17 vehicle is a city bus. **Test it in the screening (Q7).** Ask the family about it. |
| 11 | "It was Klungland who passed the warning on to the patrols." | It could imply he was responsible for any gaps in the warning. | ✅ It is the opposite (SEFO blamed the system, F11, which Scene 9 states before this). Keep the order: system failure first, his briefing second. |
| 17 | "In it, Arne Sigve Klungland, driving toward the shooting." | It could tip into hero framing, which the rules forbid us to invent. | ✅ This is factual movement, not a claim of heroism. No music under it. |
| 17 | "He tried to reverse. There was a bus behind him." | It could imply blame on the bus driver, a real and possibly identifiable person. | ⚠ Keep the bus fully anonymous: no route number and no visible driver in the image. Add nothing that suggests the bus did anything wrong. |
| 17 | White, 6 s silence, "Arne Sigve Klungland was killed there. He was fifty-three." | None. No wound, no body, no vehicle interior. | ✅ Keep. |
| 19 | Cathedral, about 600 officers, "a wife and two children" | None. | ✅ Keep. Optional family insert only with consent. |
| 22 | His memorial used as the setting of Toska's arrest | The memorial could become a device in the robber's story. | ✅ Mitigated: the scene's last line belongs to Stavanger ("the news went through the gathering like a murmur"). **Ask the family** whether they are comfortable with this pairing; it is the film's central irony. |
| 7 | "It would become a monument. Just not to William." | It could read as using his death as a punchline. | ⚠ **Test it (Q6).** Drop it if any screener reads it as glib, or if the family objects. |
| 24 | His portrait reflected in the intact glass | It could feel sentimental or ghostly. | ⚠ Test it (Q8). The fallback is the clean glass with no reflection. |

**Klungland, overall:** the script passes on facts and restraint. The two open risks are **consent** (portrait, bus, memorial pairing) and **craft** (whether the bus setup feels engineered). Both are resolved by gates G-FAM and G-SCREEN below.

### Other people needing care

- **The three women and the NOKAS staff:** unnamed, faceless, no panic. The last scene notes the late effects (F57) respectfully. ✅ Optional: notify Finansforbundet (the staff union) of the film before release, as a courtesy.
- **William Ellingsen's family:** he is named. There is no imagery of him and no detail of the shooting. ✅

## 3 · Family contact (gate G-FAM)

You approved contacting the family (D2). Drafts of the letter, in English and Norwegian, are in `THE_GLASS_klungland_family_letter_DRAFT_v001.md`. **You send it, not me**, and only after you've reviewed it. Questions for the family:

1. Do they consent to his name and life being told in the film?
2. Would they provide or approve a reference photo for a painted portrait, and approve the final image?
3. Are they comfortable with the bus detail, and with the arrest being shown during his memorial?
4. Do they want to see the script, or a cut, before publication?
5. Optional: may we include Kjetil's on-record account, or the family's choice to forgive? (Not in v007 unless they say yes.)

**If there is no answer within an agreed time, or they decline:**
- Use the no-portrait fallback.
- Keep only what is already widely published: name, rank, age, career, family size, funeral.
- Remove the bus detail from Scene 9 if they object to it.

## 4 · Cold test screening plan (gate G-SCREEN)

**What is screened:** an **audio-only animatic**. It contains:
- the full v007 narration, with a **free placeholder voice** (your own read-aloud, or a free offline text-to-speech tool, which needs your approval to install), not Atlas;
- basic sound (silence where scripted);
- black slates with the scene title and a one-line shot description.

**Cost: $0.** It tests the story, not the pictures.

**Who:** 3–5 people.
- At least 3 who **don't know the case**.
- Ideally 1 Norwegian who does, for accuracy and tone.
- No one who has seen the script.

**How:**
- Say only: "a 13-minute documentary, audio draft". Watch once, no pausing.
- You note the timestamp whenever someone's attention drifts (phone, fidgeting).
- Then ask the questions below in order, open questions first, without leading. Record answers with their consent.

| # | Question | What it tests | Pass |
|---|---|---|---|
| Q1 | In one sentence, what was it about? | The spine | ≥4/5 mention the cost or the victim, not just "a robbery" |
| Q2 | Who did you care about most? | The emotional core | ≥4/5 name Klungland, or the staff and the city |
| Q3 | Was there any moment you wanted the robbers to succeed? | Glorification (G1–G6) | **0/5**, or an explanation of which beat caused it |
| Q4 | Where were you confused? Any names, times or places? | Clarity | No beat confuses ≥2 people |
| Q5 | Where did you lose interest? | Pace (compare with your timestamp notes) | No stretch over 30 s loses ≥2 people |
| Q6 | How did the line "Just not to William" land? | Tone | Not described as glib or cruel by anyone |
| Q7 | Did anything feel too neat or set up? (Probe about the bus only if they raise it.) | The bus setup | ≤1/5 finds it manipulative |
| Q8 | What did the last line mean to you? | The ending | ≥3/5 connect it to Klungland or the people who paid |
| Q9 | What do you remember about the vault gate? | Did the surprise land? | ≥3/5 recall it unprompted |
| Q10 | Anything that felt disrespectful? | Sensitivity | 0 serious objections |

**After the screening:** I tabulate the answers into a short report, propose v008 edits for any failed test, and you approve the edits.

## 5 · Proposed v008 edits (not applied, for your approval)

1. Scene 1: "He had **reportedly** given it fifteen seconds." (L2)
2. Scene 16: drop the name "Steffen Thesen" and say "his partner". (1B)
3. Add the opening disclosure card. (L11)
4. Add NRK on-screen credits on the three quotes. (L13)
5. Plus whatever the screening and the family's answers require.

## 6 · Gates before anything is generated or published

| Gate | Unlocks | Status |
|---|---|---|
| G-SCRIPT: you approve v007 and the Phase 4 edits | Placeholder animatic (free) | **This document** |
| G-SCREEN: the screening passes, and v008 is approved | Atlas narration (about 7,400 ElevenLabs credits, **needs your explicit approval**) | Pending |
| G-FAM: family answer, or the fallback applied | Klungland portrait generation; any family material | Pending |
| G-STYLE: you approve character references and 4 master backgrounds | Shot stills (Higgsfield credits, **needs your explicit approval**) | Pending |
| G-LEGAL: lawyer review of L8, L13 and the final cut (recommended) | Publication (**needs your explicit approval**) | Pending |
