 # MQTT Protocol Spec 
 A few notes:
  - Device names are just hostnames at the moment.


## Run start & stop
  `logging/run/start`
    {
      "robot": "<robot>"
      "run_id": "<ID>"
    }
    - All data sources & syncers subscribe
    - Sent by the robot to kick off recording

  `logging/run/stop`
    {
      "run_id": "<ID>"
    }
    - All data sources & syncers subsribe
    - Sent by the robot on run end
    - If the robot dies mid-run, the server will send this to stop other devices
      collecting

## Existence & health of devices on the network
  - `device/checkhealth/<name>`
    - request a status report from a device. Sent by the server. Currently
      unused and thus untested, but in theory devices should respond to it.

  - `device/scan`
    {"from": "klog-server"}
    - The content of this is currently ignored by devices and could be anything
    - send by the server, requests that all devices re-register. Currently
      unused and thus untested, but devices should simply go through their
      registration process again (as they do on startup) when they recieve this.
    - Meant for casesb where the server goes offline but data sources stay up.
      Seting `retain=True` on registration messages makes this largely
      unnecessary though, thus its lack of use.

  - `device/status/<name>`
    {
     "device": "<NAME>",
     "status": "online|offline",
     ["disconnect_type": "normal|unexpected"]
    }
    - Sent by data sources, used by the server to track what devices are online
    - The `online` message is handled by the server but not sent by the devices
      at the moment.
    - Devices send this message with `offline` status when they are killed with
      e.g. ctrl-c or exit expectedly (such as `klog-robot` when a deployment
      ends). Devices have this message with "unexepected" disconnect type set as
      their "last will" (an mqtt feature that automatically sends a
      preconfigured message if a device goes offline from the mqtt network), so
      the server knows if devices die.

  - `device/register/<NAME>`
    {"device": "<NAME>", "type": "klog-cam|klog-kbot|<something-else>",
    ["description": "<descrip>"]}
    - Sent by data sources to let the server know that they exist and what type
      of data source they are. Currently only "klog-kbot" and "klog-cam" are
      supported, but the "data-source decoder" system (see main Readme) should
      make it easy to add support for more device types.
    - should be retained, so the server can pick up devices again if it goes
      offline and comes back up. (This logic is broken, see main readme)

  - `device/registered/<name>`
    {
      "device": "<NAME>"
      "status": "confirmed|failed"
      ["failure_type": "<type>"]
    }
    - Sent by the server back to devices to let them know if they've been
      sucessfully registered.
    - should *NOT* be retained so devices re-register whenever they come back
      online

## Logging state of data sources
  - `logging/collection_state/<device>`
    - retain not necessary if we assume server is always online
    {
     "device": "<NAME>",
     "collection_state": "starting|collecting|done|failed",
     "run_id": <ID>,
     ["failure_type": "<type>"]
    }
  - `logging/sync_state/<device>`
    {
      "device": "<NAME>",
      "sync_state": "syncing|paused|done|failed",
      "run_id": "<ID>"
      ["failure_type": "<type>"]
    }

  - `logging/all_ready`
    - whether or not all registered logging devices are collecting
    {
      "run_id": "<ID>"
      "status": true|false
      "devices": ["<dev1>", "<dev2>", "<dev3>"]
    }
