# How to put this on your GitHub profile

You can delete this file once everything is working.

## 1. Create the special profile repository
1. Go to https://github.com/new
2. **Repository name:** `supulsavinda`. It must match your username exactly. GitHub will show a message about a "special" repository.
3. Set it to **Public**. Don't tick "Add a README" (you already have one).
4. Click **Create repository**.

## 2. Upload the files
1. Unzip `supulsavinda.zip` on your laptop.
2. On the new repo's page, click **uploading an existing file**.
3. Open the unzipped `supulsavinda` folder, select **everything inside it** (`.github`, `assets`, `README.md`, `.gitignore`), and drag it all onto the upload page.
   - `.github` and `.gitignore` start with a dot, so they may be hidden. On Windows, in File Explorer go to **View → Show → Hidden items**.
4. Click **Commit changes**.

## 3. Turn on the live stats and the snake
1. In the repo, open the **Actions** tab. If GitHub asks, click to enable workflows.
2. Click **Generate profile assets** in the left list, then **Run workflow → Run workflow**.
3. Wait about a minute until it shows a green tick.

After that, open https://github.com/supulsavinda. Your profile is live. The stats, streak and snake update by themselves every hour.

> If the run fails with a "permission" error: go to **Settings → Actions → General → Workflow permissions**, choose **Read and write permissions**, save, and run it again.

## Changing things later
Every change follows the same pattern: edit a file, then run a script that redraws the pictures (the stats update on their own).

| What | Where |
|---|---|
| Name, tagline, typing line, About, toolbox, footer | `.github/scripts/draw_assets.py`, the CONTENT block at the top |
| Languages and level bars | `.github/scripts/stat_cards.py`, `KNOWN_LANGUAGES` |
| Colour (amber-yellow `ACCENT`) | `.github/scripts/theme.py` |
| Links | `README.md` |

After editing `draw_assets.py`, run this on your laptop from the repo folder:

```
python .github/scripts/draw_assets.py
```

Then upload the new files in `assets/` again. To check how it looks before uploading, run `python .github/scripts/preview.py` and open `preview/index.html` in your browser.

### Adding projects
1. In `draw_assets.py`, add entries to `PROJECTS`. There's an example in the comments just above it.
2. Re-run `draw_assets.py`.
3. In `README.md`, uncomment the Projects block, then put in the image file names and repo links.
