# klog-cam

Data source module for collecting video with normal webcams.

## Installation
  - First install klog-sync (see its readme) as it's a dependency.
  - `pip install -e klog-cam`
  - `klog-cam-cli setup` will bring up an interactive fzf selection of detected
    v4l cameras. <TAB> to add to selection, <ENTER> to finish. You'll then be
    asked for the directory to use for logs, and it'll create a config for you.

## Usage
  - `klog-cam` offers the standard daemon-control systemd bindings
  - `klog-cam-cli` offers manual camera control and utilities through the following commands:
    - `klog-cam-cli record <RUN_ID>`: start recording for provided run id.
    - `klog-cam-cli stop`: stop running recordings and convert videos
    - `setup`: helper for creating a config--discovers cameras and interactively
      selects them
    - `preview <TARGET_IP_OR_HOSTNAME>`: streams video over UDP to provided ip
      address on port 1234
    - `adjust <TARGET_IP_OR_HOSTNAME>`: opens ncurses frontend to v4l2-ctl for
      easy camera configurationi, while simultaneously streaming udp preview to provided ip

### Notes
  - For the preview: there's probably a lot of ways to view a video udp stream,
    but I use `mpv` with this command:

  ```
  mpv --no-cache --untimed --no-demuxer-thread \
  --video-sync=audio --vd-lavc-threads=1 \
  udp://0.0.0.0:1234
  ```

## Known issues & needed improvements
  - The setup of installed entrypoints here is rather strange, I know. 
    `klog-cam` is the standard systemd-binding command that works
    just like `klog-sync` and `klog-server`. I wanted to also offer manual video
    start/stop as well as the extra, non-daemon commands, so in my haste I just
    add another entrypoint, `klog-cam-cli` that calls the `cli` module. I'm
    certain there's a nice way to update systemd_utils such that you can add these
    commands on top of the ones it provides. The only complication is the desire
    to use the same words (start and stop), but I'm sure there's a good solution
    to that too.

  - Regardless of the above, all commands here should use argparse (or similar)
    so they self-document.

  - The preview feature could definitely use some love if it's getting used. If
    there's multiple cameras it previews one, then when killed moves to the next,
    but doesn't die properly afterwards when killed with ctrl-c. Requires violence
    (killall ffmpeg or similar). It also drops a lot of frames.
