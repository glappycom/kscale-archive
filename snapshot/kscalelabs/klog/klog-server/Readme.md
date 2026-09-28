# Klog-server

## Installation & Usage
- First off, for syncing to work you need an rsync daemon running & configured
  with a "module" for klog-sync to send data to. There's an example config
  (what's currently set up) in this directory, you just need to put it in
  /etc/rsyncd.conf so rsync uses it.
- Then install (`pip install -e klog-server`)
- Setup a yaml configuration file based on the example file here
- You should now have access to `klog-server` with all the systemd bindings
  documented in the top-level readme.

## State management logic (`state.py`)
This is where all the state tracking and management gets done.

### Notes on how state is stored
  - We keep a list known devices, each of which can be online or offline.
  - we keep a list of active runs, representing any runs which are in any state
    other than "done postprocessing." this includes runs which are currently
    collecting, waiting to sync, syncing, being postprocessed, or which failed
    in any of those steps 
    - Each run has its own list of devices, representing the devices which
      were registered and online when the run was started. These are the devices
      that will be waited on before sending all_ready, and the devices whose data
      will be expected to be synced before the run is declared done and removed
      from the queue
    - each run also has a `robot` property. this is meant so that we can
      ultimately be deploying multiple policies at once on different robots, all
      logging to the same server without issues
  - Take a look at the start of `state.py` where all the types are defined,
    should be pretty self-explanatory what the properties are.
    - The reason for each device having a collection state and a syncing state
      is because on the devices, these things are decoupled due to the 2
      different daemons. For example, cam-1 may finish collecting for run
      abc123 and then sync abc123 as well as the 6 runs in its backlog. In a
      situation like that, the `collection_state` of cam1 would be `done` with
      `collection_run` being `abc123`, while the `sync_state` would cycle
      through `syncing` and `done` with the `sync_run` updating to whatever run
      was being synced.

### Management logic walkthrough by handler function
Note that much of this logic looks rather complex, but is mostly there to print
appropriate log statments for almost every scenario. Many of the "handled"
scenarios shouldn't happen if collection devices are well-behaved, or don't
require any special action. The following are the boiled-down versions
describing only what these functions DO, without all the fluff logic that they
use to print things

`run_done` (called when postprocessing is done)
  - When a run is finshed, remove it from the list of active runs

`start_run`: called on run/start message
  - add a run to the active run list, setting its devices list to whatever
    devices are currently online
  - start a thread to wait for all the devices to be in the `collecting` state,
    and when that happens send the `all_ready` message. currently it doesn't do
    anything but print a message if the devices time out.

`stop_run`: called on run/stop message
  - change the state of the run to `syncing`, since that shouldbe the next step.

`update_sync_state`: called on logging/sync_state message
  - If syncing is anything but done, just print a message
  - If the sync state is done and the run that's finished syncing is known, it
    only runs the postprocessing if all the run's devices are done syncing.
  - If the sync state is done, but the run is unknown (this shouldn't happen but
    might if something goes wrong and the server misses the start of a run),
    it'll just immediately postprocess it. this could lead to repeatedly
    post-processing unknown runs as multiple data sources finish syncing, but at
    least things will still get procesed.
    - currently it doesn't add these unknown runs to its state, but it probably
      should
  - updates `run_state` to processing if processing is called

`update_collection_state`: called on logging/collection_state message
  - literally just updates internal state based on the message and prints log
    messages, no actual control happens here

`update_status`: called when a device sends an online or offline status update
  (which includes when a device dies unexpectedly since their last will sends
  these messages)
  - If a device came online, just print a message and update internal state
    accordingly
    - Note this does not add devices to runs or anything fancy
  - If a robot associated with a running deployment went offline, it'll send the
    stop command to stop all recording devices (and it will also recieve this
    message and handle it as normal via the stop_run handler)
  - otherwise just update the state and print an appropriate message

`register_device`
  - just adds a new device to the internal list with the type its given
  - *note*: currently if a device tries to register with a type not defined in
    KlogDeviceType, it just won't be registered. It should probably actually be
    added as `unknown`

## Rerun generation notes (`make_rerun.py`)
- first off, yes this file is a mess. see top-level readme issue about it.

- `make-rerun.py` bakes a blueprint into the rerun files it generates. It gets
  that blueprint from `assets`. You can change that blueprint to change how
  future generated rerun files look by default.

- `assets/car.stl` is currently only used for visualizing the quaternion if it
  exists, but this could probably be ported to visualize projected gravity.

- rerun generation doesn't even happen if `kinfer_log.ndjson` isn't found, since
  it currently has most of the data

- it reads joint names from the kinfer file if one exists

- it'll log all the videos it finds. it assumes there is a text file with the
  same name stem as each video file that it can read timetamps from. It also
  assumes the first line of this text file is a comment (which is the case with
  the ffmpeg command that klog-cam is using)

- candump data is logged to a separate timeline in rerun, so when you open the
  file you'll need to switch. Everything else is logged on `time` timeline.

- the entity path structure that you log joints with is 100% up for debate.
  don't feel super locked in to what I've done. Just know that if you change the
  entity path structure, you'll want to update the blueprint to match
