# Klog

A system for collecting  and automatically postprocessing data from (optionally
distributed) sources during policy deployments. The term is also used to refer
to the physical computer in the kscale garage which hosts the data (and is the
hostname for that computer).

## Overview
Klog is made up of modules (I use that term not as a technical python term but
merely as a descriptor, they're each their own python package):

  - `klog-server`: the master of the house and the keeper of the data. This
    daemon runs on the server (currently Scott's desktop in the garage). It
    keeps track of what devices are online and  what deployments are active (though
    for the moment we only do one deployment at a time, this should in theory
    support deploying on multiple robots at once). When data from deployments
    finishes syncing to it, it postprocesses the data (currently just puts it
    into rerun, but ultimately should probably decode into some standardized
    format for all sources).

  - `klog-sync`: mover of data and avid blaster of network bandwidth (probably).
    - This daemon runs on each "data source" alongside whatever is collecting
      the data (at the moment, that means it runs on the camera modules and on
      the robot). Whenever a deployment is *not* active, it uses rsync to
      transfer locally stored run data to klog. If deployments are done faster
      than it can sync the data, it simply builds up a backlog which it works
      through whenever you aren't deploying. The server doesn't know or care
      that this isn't the same module as whatever data source it's running
      alongside, so it sends messages with the same "device" field.

  - `klog-cam`: a "data source." Broadly that means it collects data during a
    a run and syncs it to klog afterwards.
      *note: `klog-cam` also happens to be the only
      non-robot data source that exists right now, but the idea is for the system
      to be extensible--it should be easy to add new data sources and have the
      data they produce be processed in whatever way you define.*
    - Concretely, it's a daemon which runs on a linux computer with one or more
      v4l2-controlled cameras connected and records video during deployments. Any
      number of these camera nodes can be set up (if only we had a whole bunch of
      raspberry pis lying around in the garage, they'd be perfect for this).
    - At time of writing there are 2 `klog-cam` nodes set up, one mounted to the
      kgantry with 2 cameras, a top view and a corner view, and another with one
      camera that simply lives on a tripod.

  - `klog-robot`: our other "data source," but a slightly special one in that
    it has the power to start and stop runs.
    - installs the `klog-deploy` executable which is a simple wrapper around
      commands. Throw it in front of whatever you're running to deploy, and
      it'll collect data about the run. see the `klog-robot` readme for details

  - "What's `deploy` and `remotes.yaml`?", I hear you asking... (tldr you can ignore them if you want)
    - not really part of the project, just a little thing I cooked up to make it
      easier to develop for a distributed system like this. I'ts so short you
      may as well just look at `deploy` to see how it works and what it does
    - essentially you just define which devices on the network need which
      modules and  run deploy to rsync them.

## Installation & usage
All the pieces use MQTT to talk to each other--so they need an MQTT broker.
  - I have `mosquitto` running on klog for this. Youll need to configure all
    the pieces with the ip (or hostname) of the mqtt broker, and the port it's
    listening on.
    - Since all the devices are on tailscale you can use `klog` as the mqtt host
    - It's using port 1883 which is the default

The pieces (see individual readmes for installation details):
  - `klog-server` needs to be configured and running on the data server (klog)
  - `klog-robot` needs to be installed on the robot, so you can run `klog-deploy`
    to start data collection
  - `klog-sync` needs to be installed, configured, and running on the robot and
    all data sources.
  - `klog-cam` needs to be installed on any computers you want to plug cameras
    into and have collect data, and configured with the cameras you want to use

All these pieces have yaml config files that allow you to configure the mqtt
broker and host (**except klog-cam**, see known issues). They each have default
configs in their package directories for reference of the parameters they need.

**Once all the daemons are running, just run e.g.
`klog-deploy ./faux-rtos --policy-scale 1.0` on the robot, and you'll be
collecting data!**

### Where the latest versions are instaled right now
- `kbotv2-no11`: `klog` conda environment
- `klog`: `klog` conda environment (note for some reason on login you don't even
  land in base, run `bash` and then you'll have access to conda. this needs
  fixing of course)
- `klog-cam1`: `klog` conda environment
- `klog-cam2`: in `~/.venv` environment (I know, I know. I just wanted to make
  sure it worked.)

### Systemd Bindings
`klog-sync`, `klog-cam`, and `klog-server` all use `systemd_utils` to provide
subcommand "bindings" to systemd. After installing one of these packages, run 
the `install` subcommand (e.g. `klog-sync install`) to install the systemd
service (into ~/.config/systemd/user). Afterwards you'll have access to the
following subcommands:
`start` is equivalent to `systemctl --user start <service>`
`stop` -> `systemctl --user stop <service>`
`restart` ...
`enable` ...
`disable` ...
`journal` will show live output from the service (equvilent to `journalctl` with some options)

### Important Notes & Gotchas
- If things aren't working as you expect, your most valuable debugging
  tool will be watching `klog-server journal`, as it reports most everything 
  that happens. (Including every mqtt message sent to any topic, useful as
  many of my early bugs were simple due to devices not properly following the
  protocol I defined). Failing that, you can also watch the `journal` entries
  for the `klog-cam` and `klog-sync` instances.

- Since all the daemons are run as user services, they stop running when the
  user is logged out unless you do `loginctl enable-linger <username>`. I've
  done this on the devices I've installed things on, but it needs to be done on
  new devices. Maybe there's a better way around this.

- By default, raspberrypi os doesn't have systemd's journald set up with
  persistent storage, meaning commands like `klog-cam journal` will show nothing
  useful. To set this up, you'll need to put `Storage=persistent` in the
  `[Journal]` section of `/etc/systemd/journald.conf` and reboot (logging out
  and back in might also apply the change).

- The clocks on the robot, cameras, and klog need to be synchronized. I've
  installed `chrony` on all of them, which is a plug-and-play NTP client. You
  can also probably configure systemd-timesyncd (which is builtin) or synchronize a
  different way, as long as new devices are synchronized somehow.

- For some reason, klog-cam2's network connection is *insanely* slow, so it
  takes a very long time to sync. Before worrying that things aren't syncing
  properly, take a look at `klog-sync journal` on klog-cam2. It should show live
  progress of the rsync transfer.
  *note: this live progress might not actually work in systemd-journald so you
  may not see the progress output. If this is the case, the utility `progress`
  is extremely useful--it just shows the status of current rsync (and other
  long-running process) commands.

### Directory structure
This same structure is mirrored on each data collection device, and is how data
is stored.
- log_dir (`/mnt/klog1` on the server) (referred to as the "log directory")
  - <run_id> (these are referred to as "run directory")
    - metadata.json
    - kinfer_log.ndjson
    - klog-cam0-1.mp4
    - ...
  - <run_id>
    - ...
  - <run_id>
    - ...

### Random gluey bits and pieces: how to "browse" the data
  - I have `python -m http.server` running in a tmux server on klog, in the log
    directory (`/mnt/klog1`) to allow us to send around links to the folders
    with all the run data. Obviously should be replaced with an actual
    interface.

  - Until run logs are automatically sent in discord (probably via an mqtt
    message sent to the discord bot from klog-server), I've been just sending
    out links to runs manually in response to people's policy submissions. When
    a run completes, I run `getlink` on my laptop (which actually just calls
    `getlog` on klog). This shows me runs most-recent-first. I select the
    latest run, it prints out the link, and I send this in the discord. Please
    automate this for the sake of Scott and anyone else who does deployments.

  - The `getlog` script in `klog-server/klog_server/scripts` is the closest
    thing to a searchable/browsable interface for the data that exists right
    now. It just uses fzf to let you look through & filter runs, and prints out
    the run_ids of the ones you select (with <TAB>) while browsing. Please
    replace this asap
    - `getlog`, `getlink`, and `getrr` (in `scripts_to_get_the_data`) all just
      ssh into klog, call this script, and then rsync back the whole directory (getlog),
      just the rerun file (getrr), or just print the link to the run (getlink).
      These are *NOT* guaranteed to work, as I just wrote them as convenience
      scripts for myself. Again, should be replaced asap.

## The big TODO: "data source & decoder" architecture for easy extensibility
The ultimate form of this system is flexible and ultra-extensible. It should
be easy to add new data sources which log data in any form they like, and have
this be handled properly. The way this should probably be achieved at a high
level:
  - The server-side has a registry of "decoders," which are functions which
    convert data from whatever form a data source stores it in (ndjson, video,
    binary, whatever) to some useful format.
  - When devices register with the server, they specify:
    - What files they will provide for each run
    - What decoder should be used to deal with these files
  - When a run finishes, as data sources finish syncing, the server can run
    the appropriate decoder on each source's data
  - When all sources are done syncing, it can do final processing (like putting
    everything into rerun, if that wasn't part of the decoding logic)
  - Then it can tell the deployment discord bot (or any similar system) that
    processing is done, so the data can be sent in the discord and added to
    @alik's policy evaluation notion.

This type of system will be ideal for when @greg goes bananas with logging and
can produce a gigabyte of data per second. He can log things as raw bytes,
flatbuffers, or whatever is fast, and as long as he writes a decoder for it and
drops it on the server side, things should "just work"

Implementation details are of course up to whoever does this, but a few things
that are in my head:
  - I imagine decoders take a list of the files produced by their corresponding data
    source, which can be guaranteed to exist by the server (it can throw an error
    and not call the decoder if it gets a sync done message but doesn't see the
    right files)
  - I've pondered but not decided on what I think the contracts around what
    decoders produce should be. Options as I see them:
    - Decoders are expected to turn data into some human-readable form, doesn't
      matter what, and are optionally allowed to directly log their data to
      rerun however they see fit (they can be passed a rerun sink)
    - Decoders are expected to turn data into some standardized format which can
      be used to synthesize all the sources into one object. Decoders could
      optionally log to rerun, OR this standard format could include some sort
      of metadata defining how things should be logged to rerun, and the server
      could handle actually putting it in rerun
    - There's other options here. These were just a few of my thoughts
  - Worth considering whether this is implemented by just adding more defined
    data source types the server knows about, or whether this is done in a
    slightly more modular, plugin-style way where devices can just give the name
    of their decoder, and the server dynamically checks if that decoder is in
    its bank of decoders, using it if so (so all you have to do to add a new
    data source is drop a decoder file in a folder on the server side)

## Other Known issues & Needed Fixes
As I write this it's looking more and more like these should just become github
issues lol. Feel free.

### [feature] klog-cam should use the same config logic as other modules
- **klog-cam's mqtt broker & port are hardcoded in `main.py`**
  - This is because too much of its logic happens in bash, so python doesn't even
    touch its config file. Once that's fixed and python actually handles the
    config, this'll be easy to fix, it can just work the same way as klog-sync
    and klog-robot
- while you're at it, it'd be super nice to support configurable "nicknames" for
  each camera. currently they're auto-named the hostname plus a number.

### [potential bug] klog-sync may falsely report `failed` when it means `paused`
  - tke a look at `SyncManager.py`, the logic looks right to me but I think I've
    seen this issue. Needs further investigation

### [improvement] klog-sync should handle not being able to enforce size limits better
  - currently it just dies.

### [cleanup] use type aliases everywhere
  - in klog-server's `StateManager.py`, I define some type aliases for
    readability (like `RunId`, `DevId`). I use these elsewhere only
    inconsistently.

### [cleanup] register unknown devices
- this will go along with the "data-source decoder" update but currently devices
  of unknown type are just not registered with the server (see klog-server
  readme)

### [cleanup|QOL] Move klog-cam logic out of bash
- There's currently far too much logic going on in `klog_cam_start` and
  `klog_cam_stop` (and the other scripts as well). The config parsing and error
  checking done in those scripts should be done in python, and the ffmpeg
  command can just be a `subprocess` call. Python can be in charge of managing
  those processes and killing them when the run ends, no need for the process
  naming BS. You'll also be able to eliminate the system dependencies on lsof
  and yq.

### [potential bug] videos sometimes(?) not getting logged into rerun
- I've seen an issue where sometimes™ some or all of the videos fail to be added
  to the rerun file, despite `make_rerun.py` showing the output messages about
  videos being added. I haven't yet been able to identify the source of this.
  I'm blindly hoping this was tied to the dropped frames issue and will
  magically be fixed now, but condolances if it comes back, it may be annoying
  to debug. Wish I had more advice here.

### [feature|cleanup|QOL] klog-robot needs help
- the `klog-deploy` script has its expectations about the firmware's
  data-production behavior baked in. see `klog-robot` readme for details, but
  essentially there should be a clearer contract between the firmware and
  the robot data source module. `klog-deploy` also captures the output of the
  command you run, and that output is currently not parsed at all.
- this file is also partially a holdover from the "2 random python scripts"
  days, so it's also a mess. Just breaking this up into setup and breakdown
  functions would go a long way.
- Once you start core-pinning the firmware, should also pin the candump process
  to a different core
- could definitely rework/augment the cli options
- it's worth at least considering whether this should be reworked to be another
  daemon, so that literally all that needs to happen at deployment time is
  sending the start and stop mqtt commands, and the daemon could capture
  everything it needs to. This would require some changes to how the firmware
  logs things (i.e. not just throwing `events.log` in the working directory),
  and maybe it's better to stick with the wrapper for now.
- could be nice to add a way of noting runs that were cancelled before the
  policy was run--one way is to run with `--notes` and then let blank notes be
  the marker of an abandoned run, but it'd be super cool to auto-detect this and
  put it in the run_info
- rename `metadata.json` to something else (maybe `run_info.json`)
  - there's too many `metadata.json`s in this world.
  - this'll also require `make_rerun.py` on the server side to deal with this

### [potential bug] file permission issues when running things as services
- I've encountered some issues with `klog-cam`, `klog-sync`, and `klog-server`
  not having the file permissions they need (or not having their PATHs set up
  correctly) when run as systemd services. I'm pretty sure this is fixed now,
  but if you see permission errors or stupid things like `rsync not found`,
  first try running the module normally in the foreground (e.g. just `klog-sync`)
  and seee if you have the same issue. If not, you'll need to tweak
  `systemd_utils.py` to fix systemd unit file stuff.

### [sysadmin] migrate klog to ZFS
- so there's a shared pool with multiple drives, and possibly redundancy
- currently `/mnt/klog1` is hardcoded several places, so when you do this just
  ripgrep for that to change

### [sysadmin|feature] make file permissions on klog more secure
- currently the `dpsh` user has full acces to everything. But there's already a
  `data` user whose purpose was to be in charge of data, so `dpsh` could only
  have read-access. this should actually happen (klog-server will need to run as
  `data`).

### [improvments] rerun generation todos
- The output from the firmware should be parsed, at the very least for
  loglevels. Currently only timestamps are parsed
- The firmware outputs a git hash of its version near the start of a run. this
  should probably be parsed and stored.

### [bug] The persistent registration logic is likely slightly broken
- Data source registration messages are retained, but device status: offline
  messages are not. Things will work correctly if the server goes offline and
  comes back up while the same devices are online, but if a data source goes
  offline while the server is down, the server will still get its registration
  message when it comes back up and will think the device is active
  - Could probably fix this by just actually using the `devices/scan` message
    when the server starts up

### [potential bug] untested mqtt protocol features
- Some of the messages I've defined in Mqtt_spec.md aren't being used right now,
  which means they haven't been tested. These are not guaranteed to be correctly
  implemented on the server or device sides.
- All such message types are marked as such in Mqtt_spec


### [missing features] needs a browsable interface
- while my collection of bash scripts technically gets the job done, there
  should definitely be a more user-friendly way to browse through `klog` data.
  This may become less relevant as @alik adds to his policy leaderboard, but
  would still be very nice.

### [cleanup] all checks are probably failing
- Much of this was written with the goal of getting it to work, so I wasn't
  careful about having all my static checks pass. I probably do things the
  linter isn't happy about, like only use type hints when I felt it was useful,
  or not having docstrings for every function, or hinting things as
  `str | None` and then calling methods on them because I *promise* it won't be
  `None` when I call it. So there's some cleanup to be done to make the static
  checking gods happy.


### [cleanup] move video conversion to server-side
- Though the conversion from mkv to mp4 is very quick since as-is it doesn't
  re-encode (`-v:c copy`), on principle all postprocessing should happen on the
  klog-server side rather than the data source side. This will likely naturally
  be part of the "data source and decoder" change

### [QOL] improve klog-cam preview
- see klog-cam readme

### [cleanup|QOL] klog-cam cli improvements (argparse, entrypoints)
- see klog-cam readme

### [maybe bug] dropped video segments
- I've seen some issues with missing sections of video (a few seconds long). I
  haven't root-caused this but I'm reasonably confident it's fixed now after I
  removed `mpdecimate` and added `thread-queue-size 512` to ffmpeg command. My
  sincerest condolances if it comes back. My only advice is that chatgpt is
  pretty good at ffmpeg.

### [QOL] Improve reporting  in systemd_utils
- The output of these commands is terse to nonexistent. should have far richer
  output.

### [cleanup] rewrite `make_rerun.py`
- this file is a complete shit show. It's a holdover from ye olden days when
  this project was just 2 random python scripts floating around and it's a mess.
  Probably not worth cleaning it up in isolation, though, will naturally become
  obsolete as part of the "data source & decoder" architecture change.

### [cleanup|QOL] Shared dependencies / monorepo packaging / general packaging
- This repo is currently just 3 completely separate python packages sitting in a
  directory together. It should probably be repackaged in some fancy way that
  allows shared dependencies but doesn't force you to install all the pieces.
  Example of why this would be nice:
  - `klog-sync`, `klog-cam`, and `klog-server` all use `systemd-utils.py`, which
    is currently just symlinked in all their directories.
  - `klog-cam` and `klog-robot` both have similar logic to register with the
    server, as well as to send offline messages. Could be worth pulling these
    out into a sharable unit.
- Just could use another set of eyes on the setup of pyproject.toml and
  setup.py. It's possible or even likely there are silly non-critical mistakes
  here

### [cleanup] Config Files
- The config file management is pretty bad as of now. The `config.py` files are
  all nearly identical except for the parameters they take and the name of the
  file they look for, this could  definitely be consolidated to a nice
  shared config parser. There may already be a library for this as well.
  klog-sync/config.py is particularly a mess.

- I can't think of a good reason for klog-sync to have its own config file. It
  should almost certainly be unified with whatever data source it's runnning
  alongside.

- The interactive config prompting is largely untested and does not have
  thorough error handling. Very likely to break.

- Each module has an example config in its source directory, but these should be
  installed in the users ~/.config on package install, probably as e.g.
  `klog-sync-example.yaml`

### [quickfix] Rename klog-robot to klog-kbot
- Future proof so there can be a klog-zbot!

# Only semi-related: Things to harrass rerun people about
Feature requests that would make life easier for us

## Better text support
  - Looks like of the 3 views you can use on text logs, only one (text log i
    think) supports scrolling with the cursor
  - Ability to filter lines by some criteria

## Viewer
  - Ability to chang which data points you "step" through when using arrow
    keys--currently looks like it just uses the finest resolution, so the arrow
    keys get pretty cooked if you want to step through a 30fps video but you
    have a ~2000Hz candump in there

## Logging data
  - Ability to log an entire vector at once, while letting each item get its own
    entity path (and ideally name) so you can move them around and show/hide
    them individually (without using the silly colored dots)

