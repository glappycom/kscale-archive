# Default-branch snapshots

These trees are the files from each repository's default branch at capture time, with no git history, so they can be read on GitHub. They are not the archival copy. History and Git LFS objects live under `history/`.

A `*.OVERSIZED.txt` note means a file was larger than GitHub's 100 MB limit and was left out of the snapshot. A `*.OMITTED.txt` note means a file was left out on purpose (a private key that had been committed upstream).

Where a project tracked Git LFS, the snapshot's attribute file is named `.gitattributes.upstream` instead of `.gitattributes`. The patterns are unchanged. Renaming the file keeps GitHub from trying to upload those paths through Git LFS again (the bytes are already in the tree, or the pointer text is already the file, and the LFS objects that could be fetched are under `history/`).
