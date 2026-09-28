# klog-sync

Syncing daemon responsible for transferring data from data sources (cameras,
robot) to klog-server for postprocessing.

## Installation & Usage
- Make sure you have `rsync` installed (it should yell at you on install if you
  don't)
- `pip install -e klog-sync`
- Set up config in `~/.config/klog-sync.yaml`, using parameters shown in example
  config in `klog-sync/`
  - You can set up a max size for the log directory and a minimum remaining disk
    space. After every sync `klog-sync` will check if these limits are exceeded
    and delete sucessfully synced runs, starting with the oldest, until the
    limits are no longer exceeded
- You should now be able to run `klog-sync` to run the syncing daemon in the
  foreground.
- Run `klog-sync install` to install the systemd service file, and you'll have
  access to all the systemd bindings documented in the top-level readme.

### Notes & Gotchas
- Directory size & remaining disk space rules are enforced **after** each run
  ends, so during a run you can still exceed these limits. Because of this you
  should leave some headroom on these limits to avoid running out of space.

- This expects to sync to an rsync "module", not just a target directory the way
  you normally would use rsync on the command-line. So the server you choose to
  sync to needs to have an rsync daemon running and configured for this (see
  klog-server for example config and details)

- if for any reason `klog-sync` can't enforce your size limits, it'll exit.
  Ideally it would do something better like prevent you from trying to collect
  more data, but since it's running as a separate daemon from the data collector
  this isn't easy. Basically it really wants to get your attention if this
  happens, since it could result in a full disk which would lead to other
  unexpected behavior--so hopefully you'll notice that all your syncing just
  stops. This should definitely be done better

## The weeds
- klog-sync makes sure that while a deployment is running (and its data source is
collecting), it isn't syncing. One could reasonably disagree about whether this
is necessary, but the idea is to avoid as much overhead as possible during
deployments (especially on the robot).

- To that end, it subscribes to `logging/run/start` and `logging/run/stop` but
  does the opposite of what the data sources do--it pauses syncing when it
  recieves a `start` message and resumes syncing when it recieves a `stop`

- While we could technically just sync the entire log directory and let rsync
  handle it, I chose to have klog-sync keep its own per-run sync queue so the
  server can have more visibility (and potentially control in the future). To
  accomplish this, on startup it scans the log directory and checks each run
  directory for a `.sync_status` file whose structure is:

  ```
  {
    "status": "completed|not_synced",
    "last_attempt": <TIMESTAMP>
  }
  ```

  - based on this scan it builds its initial queue of to-be-synced directories
  - when a directory is finished syncing it adds this file to mark the directory
    as synced

- whenever it recieves a stop command, the run that ended is added to the sync
  queue

- Whenever a deployment isn't running, `SyncManager`'s `sync_loop` will be
  running, constantly looping through the sync queue and syncing the runs in it
  one directory at a time

- It doesn't sync a directory unless no file inside it has been modified in the
  last 10 seconds -- this is to give whatever data source is running alongside
  klog-sync some time to do whatever it needs to to get files ready to sync.

- Reasoning for rsync options documented in comments
