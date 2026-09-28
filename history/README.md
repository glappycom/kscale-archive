# History bundles

Each directory is one upstream repository.

- `repo.bundle` or `repo.bundle.part-*` is a full git bundle of every branch and tag.
- `delta.bundle` or `delta.bundle.part-*` is only the commits that diverged from the upstream named in `META.json`.
- `lfs-objects.tar` or `lfs-objects.tar.part-*` is the Git LFS object store.
- `META.json` records the upstream commit, the method, checksums, and anything that could not be fetched.

See [RESTORE.md](../RESTORE.md) for the commands that turn these files back into a git repository.
