# K-Scale archive

Unofficial preservation mirror of the public code, documentation, and robot designs published by **K-Scale Labs** and **Zeroth Robotics**.

K-Scale Labs shut down in November 2025. `kscale.dev` and `docs.kscale.dev` no longer resolve. This repository was assembled on **28 September 2026** from the public GitHub organizations `kscalelabs` (133 repositories) and `zeroth-robotics` (12 repositories), plus [`Justin-Riekehof/zeroth-01-build`](https://github.com/Justin-Riekehof/zeroth-01-build), and from Wayback Machine captures of the websites.

The mirror exists so the work stays readable and restorable if those GitHub organizations disappear. It is not a product of K-Scale Labs, Zeroth Robotics, or Glappy Inc. **This archive does not claim ownership of the upstream work.** Copyright stays with the authors named in each repository. License files are unchanged; read [LICENSES.md](LICENSES.md) before you reuse anything.

## What is in this repository

| Path | What it is |
| --- | --- |
| `snapshot/` | Default-branch files for the core repositories and the smaller original repositories, with no git history, so they can be browsed on GitHub. |
| `history/` | Git bundles (full history, or a delta of the commits a fork added) and Git LFS object archives. See [RESTORE.md](RESTORE.md). |
| `docs-site/` | Wayback Machine copies of `docs.kscale.dev`, `kscale.dev`, and the other hostnames listed in the snapshot CSV. |
| `guides/` | The 62-page Zeroth-01 assembly guide (`zeroth-assembly-guide.docx` and a PDF export of the same Google Doc). |
| `meta/` | The inventory used to drive the capture, the Wayback URL list, and a per-repository status table. |
| [SOURCES.md](SOURCES.md) | Upstream URL, default-branch commit, and capture time for all 146 repositories. |
| [LICENSES.md](LICENSES.md) | What each repository's license files actually say. |
| [RESTORE.md](RESTORE.md) | How to turn a bundle (and its LFS archive) back into a normal git clone. |

## Capture summary

Re-checked against the GitHub API on 28 September 2026: **146 public repositories**, the same set as `meta/REPO-INVENTORY.csv`. Nothing had been added or removed.

| | Count |
| --- | ---: |
| Repositories | 146 |
| History preserved (`yes`) | 127 |
| History partial | 19 |
| History missing | 0 |
| Git LFS objects stored (`yes`) | 11 |
| Git LFS not stored (`no`) | 4 |
| Git LFS not used (`n.a.`) | 131 |
| Browsable snapshot on this branch | 102 |
| Bundle bytes | 3.68 GB |
| LFS archive bytes | 1.19 GB |

`meta/PRESERVATION-STATUS.csv` is the row-by-row table (history, LFS, snapshot, commit SHA, license files).

### How history is stored

GitHub rejects files over 100 MB and rejects a single push over 2 GB. A normal git repository also should not grow without limit. Full history is therefore stored as **git bundles**, split into 90 MB parts when a bundle is larger than that. Cloning this archive does not by itself give you 146 separate checkouts; [RESTORE.md](RESTORE.md) shows how to rebuild each one.

- **Full bundle** (`git-bundle-all-refs`, 120 repositories). Every branch and tag. This includes every K-Scale-owned repository that had commits, including the large ones (`zeroth-robotics/zeroth-frontend`, `kscalelabs/sysid`, `kscalelabs/sim`, `kscalelabs/ksim-kbot`, and the rest).
- **Contained in a parent we also archived** (3). `kscalelabs/zeroth-bot`, `kscalelabs/kbot-unit-tests`, and `kscalelabs/zbot-joystick` add no commits of their own. Their history is the parent bundle plus the recorded tip SHA.
- **Empty** (2). `kscalelabs/kos-rpi-firmware` and `kscalelabs/webrtc-with-auth` had no commits.
- **Delta bundle** (9). Large forks that do contain K-Scale commits. The bundle is only the commits that are not in the upstream base, so it can be applied on top of that upstream (or, when the parent is `kscalelabs` / `zeroth-robotics`, on top of the parent bundle in this archive).
- **Upstream pointer** (12). Forks of third-party projects whose default branch and tags contained no commit that was missing from the parent. The parent URL and the exact commit SHA are in `META.json`. Those parents were still public on the capture date: `google-deepmind/mujoco_menagerie`, `buildroot/buildroot`, `hshi74/toddlerbot`, `hatomist/tonic-milkv`, `vrtnis/robot-web-viewer`, `nfreq/ktune`, `Toni-SM/skrl`, `NVlabs/HOVER`, `Rhoban/bam`, `superna9999/meta-meson`, `google-deepmind/mujoco_playground`, `leggedrobotics/rsl_rl`.

GitHub release assets were not used. The token available to this mirror can push git data; publishing multi-gigabyte history as bundle parts inside the repository does not depend on the Releases API.

### Git LFS

`git lfs fetch --all` was run for K-Scale-owned LFS repositories, and for third-party forks whose pointer metadata was under about 250 MB.

Stored: `kscale-assets` (STL/OBJ meshes), `kinfer-sim`, `kinfer-kbot`, `kos-sim`, `kbot-inference`, `klab`, `zbot-unit-tests`, plus fork LFS that was still on the server for `loco-mujoco`, `IsaacLab`, and `humanoid-gym` (that last one declares LFS patterns but references no objects). `kbot-unit-tests` is the same commits as `zbot-unit-tests`, so its objects are the `zbot-unit-tests` archive.

Not stored:

- `kscalelabs/kteleop` — 870 LFS pointers (about 3.5 GB), all HTTP 404 from GitHub LFS. The paths are LeRobot test fixtures. The same object IDs also 404 on `huggingface/lerobot` and `kscalelabs/lerobot`. Pointers are in the bundle.
- `kscalelabs/ksim-gym-zbot` — 1 of 2 objects stored; the other 404s. Marked `no` because the set is incomplete. The object that still exists is in `history/kscalelabs/ksim-gym-zbot/`.
- `kscalelabs/lerobot` — third-party fork, about 3.4 GB of LFS pointers. Blobs were not downloaded. Upstream is `huggingface/lerobot`.
- `kscalelabs/HOVER` — identical to `NVlabs/HOVER`, no unique commits. LFS blobs were not copied.

### Snapshots

Browsing copies (no history) are under `snapshot/` for the requested core set — `kbot`, `docs`, `zeroth-robotics/zeroth-bot`, `ksim`, `ksim-gym`, `kbot-models`, `kos`, `firmware`, `zeroth-robotics/hardware`, `onshape`, `kteleop`, `Justin-Riekehof/zeroth-01-build` — and for other non-fork repositories whose git size was at most about 30 MB. Larger originals are in `history/` only, so this repository stays within what GitHub will accept.

`kscalelabs/kbot` records submodules pointing at `kos-kbot`, `ksim-kbot`, and `kbot-inference`. Those repositories are archived separately. Submodule contents are not copied into the `kbot` tree.

### Documentation site

`docs-site/` is the Wayback capture listed in `meta/KSCALE-DEV-WAYBACK-SNAPSHOTS.csv` (205 URLs), fetched with `id_` raw URLs on 28 September 2026.

| | Count |
| --- | ---: |
| URLs attempted | 205 |
| Saved | 200 |
| Failed | 5 |
| `docs.kscale.dev` saved | 148 / 148 |
| `kscale.dev` saved | 23 / 23 |
| Pages with article text converted to Markdown | 96 |
| ReadMe.io JavaScript shells (HTML saved, article body was not in the capture) | 55 |

Failures: `api.kscale.dev/`, `notion.kscale.dev/`, and `media.kscale.dev/` (empty body) were Wayback misses; `blog.kscale.dev/_/graphql` and one Medium post URL returned HTTP 403. `docs-site/manifest.csv` has the row for every URL. Images that could be fetched (136 files) are under `docs-site/_assets/`.

A third-party `secretKey` embedded in some ReadMe page shells was removed before publication. Nothing else in those pages was edited.

### Assembly guide

`guides/zeroth-assembly-guide.docx` is the supplied 62-page Zeroth-01 assembly guide (Google Doc `1d3hXxOXammY6yR6EJ_lT8lXaUeGtjSJwcDIc-OJ2SfY`). `guides/zeroth-assembly-guide.pdf` is a PDF export of that same document, downloaded on the capture date.

## License conflict, reported not resolved

`kscalelabs/kbot`'s README, and the K-Bot pages in `kscalelabs/docs`, say hardware is CERN-OHL-S and software is GPL v3, and they point at `LICENSE-HW` and `LICENSE`. `LICENSE-HW` is CERN-OHL-S. `LICENSE` is the MIT License, not GPL v3. Both files are preserved as published. Per-repository file contents are in [LICENSES.md](LICENSES.md).

## Credits

K-Scale Labs and Zeroth Robotics, and the contributors named in each upstream repository, wrote this work. The Zeroth-01 build log is from [Justin Riekehof](https://github.com/Justin-Riekehof/zeroth-01-build)'s public repository. Wayback Machine captures are from the Internet Archive.
