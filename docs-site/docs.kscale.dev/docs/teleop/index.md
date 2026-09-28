<!-- preserved from https://docs.kscale.dev/docs/teleop via https://web.archive.org/web/20250420214048id_/https://docs.kscale.dev/docs/teleop -->

# Teleoperation

Details about running the teleoperation flow

## Requirements

* linuks-kbot v0.0.4+
* kos-kbot 0.1.3+

# Teleop

## Starting WebRTC stream

bash

```
docker run --rm -it --network=host \
  --device=/dev/video45 \
  --add-host xr.kscale.ai:10.33.20.104 \
  --add-host host.docker.internal:127.0.0.1 \
  ghcr.io/kscalelabs/gst-rs-webrtc:latest \
  gst-launch-1.0 \
    webrtcsink name=ws \
    meta="meta,name=kbot-$(cat /sys/class/net/wlan0/address | tr -d ':')" \
    enable-control-data-channel=true \
    signaller::uri="wss://xr.kscale.ai:8585" \
    v4l2src device=/dev/video45 io-mode=2 ! \
    video/x-raw,format=YUY2,width=1280,height=1080,framerate=30/1 ! \
    videoconvert ! \
    videoflip method=vertical-flip ! \
    video/x-raw,format=I420 ! ws.
```

## Teleop script

To start the teleop data channel over WebRTC, see the script [here](https://github.com/kscalelabs/gst-rs-webrtc/blob/master/robot_data_channel.py) .

## VR Headset link

View the VR headset teleoperation portal [here](https://kscale.ai/webrtcflask/www/stereo-video.html)

# Data collection

## Starting a recording

Python

```
rec_uuid = kos.process_manager.start_kclip("pick up the blue cup")
```

## Stopping a recording

Python

```
rec_uuid = kos.process_manager.stop_kclip()
```

## Exploring krec

Python

```
import krec

rec = krec.extract_from_video('recording_20250319_193701_real_test_1_9c85a9a4-f5b4-437c-9425-d0a2ec732570.krec.mkv')

>>> rec
KRec(frames=1337, header=KRecHeader(uuid='9c85a9a4-f5b4-437c-9425-d0a2ec732570', task='real test 1', robot_platform='KBot', robot_serial='00000000', configs=0))

>>> print(rec.display_frame(300))
Frame 300
=========

Video timestamp: 8919177055
Video frame number: 108
Inference step: 4739

Actuator States (10)
---------------
ID 11: online=true, pos=Some(89.11151123046875), vel=Some(-2.9900929927825928), torque=Some(4.183113098144531), temp=Some(24.0), volt=None, curr=None
ID 12: online=true, pos=Some(16.007286071777344), vel=Some(-1.101572871208191), torque=Some(-0.4971389770507813), temp=Some(24.0), volt=None, curr=None
ID 13: online=true, pos=Some(-22.379470825195313), vel=Some(-71.89730072021484), torque=Some(0.8313884735107422), temp=Some(24.0), volt=None, curr=None
ID 14: online=true, pos=Some(-65.06756591796875), vel=Some(-8.578498840332031), torque=Some(-0.8412456512451172), temp=Some(28.0), volt=None, curr=None
ID 15: online=true, pos=Some(-6.245880126953125), vel=Some(-3.038723945617676), torque=Some(0.0313873291015625), temp=Some(26.0), volt=None, curr=None
ID 21: online=true, pos=Some(0.8899463415145874), vel=Some(0.6119849681854248), torque=Some(0.2481117248535156), temp=Some(22.0), volt=None, curr=None
ID 22: online=true, pos=Some(-2.4664306640625), vel=Some(6.067502975463867), torque=Some(-0.022891998291015625), temp=Some(22.0), volt=None, curr=None
ID 23: online=true, pos=Some(-3.241006851196289), vel=Some(-12.502197265625), torque=Some(0.20570755004882813), temp=Some(25.0), volt=None, curr=None
ID 24: online=true, pos=Some(3.8343043327331543), vel=Some(1.500018835067749), torque=Some(-0.0002593994140625), temp=Some(23.0), volt=None, curr=None
ID 25: online=true, pos=Some(6.383166790008545), vel=Some(-2.730982780456543), torque=Some(-0.2679634094238281), temp=Some(26.0), volt=None, curr=None

Actuator Commands
----------------
ID 11: pos=90.703125, vel=0, torque=0
ID 12: pos=15.908203, vel=0, torque=0
ID 13: pos=-25.751953, vel=0, torque=0
ID 14: pos=-66.26953, vel=0, torque=0
ID 15: pos=-6.2402344, vel=0, torque=0
ID 21: pos=0.9667969, vel=0, torque=0
ID 22: pos=-2.4609375, vel=0, torque=0
ID 23: pos=-3.1640625, vel=0, torque=0
ID 24: pos=7.3828125, vel=0, torque=0
ID 25: pos=6.328125, vel=0, torque=0
```

Updated 27 days ago

---

[KOS](/docs/kos)[KOS Sim](/docs/kos-sim)

* [Table of Contents](#)
* + - [Requirements](#requirements)
  + [Teleop](#teleop)
  + - [Starting WebRTC stream](#starting-webrtc-stream)
    - [Teleop script](#teleop-script)
    - [VR Headset link](#vr-headset-link)
  + [Data collection](#data-collection)
  + - [Starting a recording](#starting-a-recording)
    - [Stopping a recording](#stopping-a-recording)
    - [Exploring krec](#exploring-krec)
