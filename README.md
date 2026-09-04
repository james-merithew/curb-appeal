# EntryMap

Point a phone at a storefront and know in 15 seconds if someone in a wheelchair
can actually get in. This repo starts as the **vision-accuracy eval harness** —
the day-1 test of the riskiest assumption: can a vision model reliably assess
ADA features from a real photo?

## Eval harness quick start

1. **Drop photos** into `photos/`, one folder per door:

   ```
   photos/
     door-01/
       IMG_0001.HEIC      (any name; HEIC, JPG, PNG all fine)
       IMG_0002.HEIC
     door-02/
       ...
   ```

   The folder name is the door ID. Device (iPhone 16 Pro vs iPhone 16) is read
   automatically from EXIF — no need to encode it in filenames.

2. **Set the API key** — create a file named `.env` in the repo root:

   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```

   (Get one at console.anthropic.com → API keys. `.env` is gitignored.)

3. **Install** (once):

   ```
   python -m venv .venv
   .venv\Scripts\pip install -r eval\requirements.txt
   ```

4. **Run the eval**:

   ```
   .venv\Scripts\python eval\run_eval.py
   ```

   Writes `eval\out\results.csv` + `results.json`. Roughly $0.01–0.05 per photo.

5. **Fill in ground truth** — the run also writes `eval\out\ground_truth.csv`
   with one row per door × criterion. Fill the `truth` column from what you
   know about the actual doors (vocabulary: `present`, `absent`; for
   `door_width_adequate` use `appears_wide` / `appears_narrow`). Leave a cell
   blank to skip that criterion for that door.

6. **Build the report**:

   ```
   .venv\Scripts\python eval\report.py
   ```

   Writes `eval\out\report.md`: per-criterion accuracy, cross-view consistency
   per door, iPhone 16 Pro vs iPhone 16 delta, and latency vs the 15s budget.

## Flags

- `--model claude-opus-5` (default) — also try `claude-sonnet-5`,
  `claude-haiku-4-5` to map the accuracy/latency/cost tradeoff.
- `--limit N` — only process the first N images (cheap smoke test).

## What this test decides

- **Accuracy per criterion** — which of the 8 checks the model can actually be
  trusted with from imagery.
- **Cross-view consistency** — does the verdict flip between the 5–6 views of
  the same door? (Decides whether live video capture is viable or whether we
  keyframe + majority-vote.)
- **Device delta** — iPhone 16 Pro vs iPhone 16 (expected: negligible).
- **Latency** — p95 vs the 15-second demo budget, per model.
