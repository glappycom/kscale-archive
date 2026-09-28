# Restoring a repository from this archive

This archive keeps upstream history as [git bundles](https://git-scm.com/docs/git-bundle). A bundle is a single file (sometimes split into 90 MB parts so GitHub will accept the push) that contains commits, branches, and tags. Git LFS blobs are stored beside the bundle as a tar archive, because a git bundle only contains the pointer files.

Capture metadata for every repository is `history/<org>/<repo>/META.json`.

## 1. Put the bundle back together

If `META.json` lists `repo.bundle` or `delta.bundle`, that file is already whole.

If it lists `repo.bundle.part-001`, `repo.bundle.part-002`, and so on:

```bash
cd history/<org>/<repo>
cat repo.bundle.part-* > repo.bundle
sha256sum repo.bundle   # compare with bundle_sha256 in META.json
```

Do the same for `lfs-objects.tar.part-*` when those files exist. Check `lfs_archive_sha256`.

## 2. Full bundles (`history_method` = `git-bundle-all-refs`)

These bundles stand alone. They contain every branch and tag that was on the upstream repository at capture time.

```bash
git clone repo.bundle restored
cd restored
git branch -a
git tag
```

`git clone` of a bundle checks out the bundle's HEAD. The other branches are in `refs/heads` inside the bundle; list them with `git bundle list-heads repo.bundle` and check out any you need:

```bash
git clone repo.bundle restored
cd restored
git bundle list-heads ../repo.bundle
git checkout <branch>
```

## 3. Delta bundles (`history_method` = `delta-bundle-of-diverging-refs`)

Used for large forks of projects that still live somewhere else. The bundle contains the commits that are **not** reachable from `delta_prerequisite_sha` in `META.json`. You need that commit first.

When `delta_prerequisite_repo` is another K-Scale or Zeroth repository, restore that repository's full bundle from this archive. Otherwise clone the upstream named in `META.json` (it was public on the capture date):

```bash
git clone https://github.com/<delta_prerequisite_repo>.git restored
cd restored
git fetch origin <delta_prerequisite_sha>
git checkout <delta_prerequisite_sha>
git pull /path/to/delta.bundle
```

`git bundle verify delta.bundle` from inside `restored` should report that the bundle is okay once the prerequisite commit is present.

## 4. History that lives in a parent bundle

`history_method` = `contained-in-archived-parent` means every branch and tag commit of the fork already exists in the parent repository's full bundle (`parent` in `META.json`). Restore the parent, then:

```bash
git checkout <default_branch_sha from META.json>
```

## 5. Forks with no unique commits

`history_method` = `upstream-pointer-no-unique-commits` means the fork did not contain any commit that was missing from its parent, and that parent is **not** in this archive (it is a third-party project that was still public). `META.json` records the parent and the commit SHA:

```bash
git clone https://github.com/<parent>.git restored
cd restored
git checkout <default_branch_sha>
```

## 6. Git LFS

When `lfs_status` is `yes` and `lfs_files` is set, the blobs are in `lfs-objects.tar` next to the bundle. Pointers inside the git history are unchanged.

```bash
cd restored
git lfs install
mkdir -p .git/lfs
tar -C .git/lfs -xf /path/to/lfs-objects.tar
git lfs checkout
```

The tar contains an `objects/` directory, which is what Git LFS expects at `.git/lfs/objects`.

If `lfs_status` is `yes` but there is no tar, the objects were archived with the parent named in the notes (identical fork). Use that parent's `lfs-objects.tar`.

`lfs_status` = `n.a.` means the repository did not use Git LFS.

`lfs_status` = `no` means pointer files may be in the bundle, and the blobs were not downloaded. The notes say why (almost always a third-party fork whose objects are large and still hosted upstream).

## 7. Snapshots on `main`

`snapshot/<org>/<repo>/` is the default-branch tree only, with no git history, so it can be read on GitHub. It is not a substitute for the bundle. Where a snapshot note says LFS pointers were left in place, run the LFS steps above on a restored clone instead of using those pointer files.

A file named `*.OVERSIZED.txt` means the original file was over GitHub's 100 MB limit and was left out of the snapshot. It is still inside the bundle or the LFS archive.

## 8. Submodules

Some repositories (notably `kscalelabs/kbot`) reference other K-Scale repositories as git submodules. Those URLs are preserved as they were. The submodule repositories are archived here under their own `history/` directories. After restoring the parent and the submodule repo, point the submodule at your local clone, or replace the `git@github.com:` URL with the upstream HTTPS URL while those remotes still exist.

## 9. Empty repositories

`history_method` = `empty-repository` means the upstream had no commits to bundle.
