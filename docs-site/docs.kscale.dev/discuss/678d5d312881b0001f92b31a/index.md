<!-- preserved from https://docs.kscale.dev/discuss/678d5d312881b0001f92b31a via https://web.archive.org/web/20250815185947id_/https://docs.kscale.dev/discuss/678d5d312881b0001f92b31a -->

# Discussions

[Ask a Question](/discuss-new)

[Back to all](/discuss)

0

## Sound isn't implemented

7 months ago by Daniel Ginovker

Noticed the docs are outdated, but even the package code doesn't work

```
Traceback (most recent call last):
  File "/home/wacket/Projects/TeamOne/skillet/examples/squat.py", line 116, in main
    response = kos.sound.play_audio(audio_chunks(), **audio_config)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/wacket/Projects/TeamOne/venv/lib/python3.11/site-packages/pykos/services/sound.py", line 108, in play_audio
    return self.stub.PlayAudio(request_iterator())
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/wacket/Projects/TeamOne/venv/lib/python3.11/site-packages/grpc/_channel.py", line 1536, in __call__
    return _end_unary_response_blocking(state, call, False, None)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/wacket/Projects/TeamOne/venv/lib/python3.11/site-packages/grpc/_channel.py", line 1006, in _end_unary_response_blocking
    raise _InactiveRpcError(state)  # pytype: disable=not-instantiable
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
grpc._channel._InactiveRpcError: <_InactiveRpcError of RPC that terminated with:
        status = StatusCode.UNIMPLEMENTED
        details = ""
        debug_error_string = "UNKNOWN:Error received from peer  {created_time:"2025-01-19T12:01:20.666382568-08:00", grpc_status:12, grpc_message:""}"
>
```

Was using this code

```
        kos = pykos.KOS(ip="192.168.42.1")
        
        # Play audio file properly
        with open("some_file.wav", "rb") as audio_file:
            def audio_chunks():
                while chunk := audio_file.read(4096):  # Read in 4KB chunks
                    yield chunk
            
            # Configure audio parameters for WAV playback
            audio_config = {
                "sample_rate": 44100,  # Standard WAV sample rate
                "bit_depth": 16,       # Standard WAV bit depth
                "channels": 2          # Stereo
            }
            
            response = kos.sound.play_audio(audio_chunks(), **audio_config)
            if not response.success:
                logger.error(f"Failed to play audio: {response.error}")
```

  

Code was based on `lib/python3.11/site-packages/pykos/services/sound.py`

Add Comment
