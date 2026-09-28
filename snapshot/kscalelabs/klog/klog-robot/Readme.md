# Klog-robot

This package provides the `klog-deploy` executable, which is a wrapper aronud
any deployment command you like.

## Installation & usage
- First install & configure `klog-sync`
- Then install the package `pip install -e klog-deploy`
- Configure it, based on default yaml configuration file
  - it'll yell at you if you don't have a config file when you run, and will
    hopefully help you create one

- You can now run `klog-deploy` to see a list of the options it supports. To
  deploy with data collection, run `klog-deploy whatever-command-to-deploy`

- The options do have a little quirk: if you pass `--notes` or `--name`, they
  absorb the next argument as the notes or name if it's not another option. So
  if you want to pass them without values (so you're asked for them
  interactively after the run), you should do e.g.
  `klog-deploy --name --notes -- your-command` to avoid the first word of your
  command getting eaten up as notes

## Expectations of the firmware
`klog-deploy` is stupid. it doesn't care what command you throw after it,
it'll still do the same thing, so you can deploy however you like. It does,
however, have some expectations built in that are based on the current
firmware.

- If your commmand has a `.kinfer` file anywhere in it, that file will be copied
  to the run directory
- It expects the firmware to create an `events.log` file in the working
  directory. It moves this to the run directory and calls it `kinfer-log.ndjson`
  - it expects the last line of this file to be garbage (this is due to how the
    firmware currentyl does file logging)
