# AI style-pass prompts v001: PREPARED, NOT RUN

**Status: no generation has been run.** The spending limit is $0. These prompts and settings are ready for one free or low-cost test once you approve it. Before any upload, check the current pricing, the input limits and whether the chosen model really accepts a **video** reference. Not every Kling model does.

## Rules (from the brief and storyboard sheet "PRODUKSJONSSYSTEM")
- **The Blender render is the master.** AI may change surface, light and atmosphere. It must never change geometry, figure positions, the camera path, dates, numbers or text.
- AI is not allowed on: SH-051/052 (glass damage and counter), any shot in 🎬 3 (Klungland), any frame with dates or text, or 4C/4D in 🎬 4 (the arrest blocking).
- Reject the output if any of these appear: morphing architecture, extra figures, weapons that are not in the source, faces, modern objects in 2005 scenes, camera rotation that is not in the source, or text.

## Test 1 (candidate): SH-031 "Through the Glass", opening crane (7 s)

- **Input:** `05_BLENDER/renders/SH-031_preview_v001.mp4` (960×540 EEVEE blockout).
- **Tool, first choice:** Higgsfield. Use its video-to-video / motion-transfer mode with a style control, if the current plan allows video input. Use 5 s at the lowest resolution as a test.
- **Tool, alternative:** Kling, only with a model and mode that take a video reference. Check this in the UI first.

**Prompt:**
> Cinematic still-camera documentary reconstruction, pre-dawn winter, a narrow inner courtyard of a 1970s Norwegian commercial building, plastered walls in cold slate-blue, thin frost on old cobblestones, one warm amber-lit office window with thick laminated security glass, a single anonymous hooded figure crouched in silhouette against the wall below the window, cold wall lamp, light mist, muted desaturated palette, deep navy shadows, subtle film grain, grounded realistic lighting, restrained, no text

**Negative prompt / avoid:**
> faces, visible facial features, weapons, extra people, police, snow storm, rain, neon, modern LED signage, readable text, logos, camera shake, morphing walls, changing window shape, broken glass, cartoon, anime, oversaturated colours

- **Strength:** low to medium. Keep structure and motion as close to the source as the tool allows.
- **Accept only if:** the window size and position stay stable, the figure stays in the same place and the same pose, the camera path matches the source, and there is nothing period-inaccurate.
- **Log in `00_PROJECT_MANAGEMENT/cost_tracker.csv`:** model, prompt version, settings, cost, result and approval.

## Test 2 (later): 🎬 4A street establishing shot (SH-083), and only after the Blender blockout exists

> Málaga, Spain, spring 2005, an ordinary city street a short walk from the railway station, mid-rise residential and commercial buildings, small shopfronts, a modest internet café with a plain generic sign, early-2000s parked cars, bright Mediterranean daylight, warm sun, documentary realism, restrained camera, no readable text

Avoid: palm-lined seafront, beach, smartphones, flat-screen monitors, modern cars, readable signs, crowds running, police action.
