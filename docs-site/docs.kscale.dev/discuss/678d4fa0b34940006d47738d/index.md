<!-- preserved from https://docs.kscale.dev/discuss/678d4fa0b34940006d47738d via https://web.archive.org/web/20250815180603id_/https://docs.kscale.dev/discuss/678d4fa0b34940006d47738d -->

# Discussions

[Ask a Question](/discuss-new)

[Back to all](/discuss)

0

## right ankle actuator issue

7 months ago by Yoyo

**problem:**

my custom script is not able to run. while running move\_all\_joints\_a\_little.py, I believe while testing all the actuators it countered a faulty one and stopped. we suspect it is related to actuator id issue like yesterday

**error:**

INFO 2025-01-19 11:13:49 [**main**] Attempting to move joint: right\_ankle\_pitch  
INFO 2025-01-19 11:13:49 [root] Configuring right\_ankle\_pitch (ID: 45)  
ERROR 2025-01-19 11:13:49 [**main**] Failed to move joint right\_ankle\_pitch: <\_InactiveRpcError of RPC that terminated with:  
status = StatusCode.CANCELLED  
details = "Received RST\_STREAM with error code 8"  
debug\_error\_string = "UNKNOWN:Error received from peer {grpc\_message:"Received RST\_STREAM with error code 8", grpc\_status:1, created\_time:"2025-01-19T19:13:49.4308968+00:00"}"

> ERROR 2025-01-19 11:13:49 [**main**] Traceback:  
> Traceback (most recent call last):  
> File "D:\Projects\khacks\_dancing\_robot\skillet\skillet\examples\move\_all\_joints\_a\_little.py", line 35, in main

```
move_joint_a_little(joint_name, MOVE_DEGREES)
```

File "D:\Projects\khacks\_dancing\_robot\skillet\skillet\examples\move\_joint\_a\_little.py", line 83, in move\_joint\_a\_little  
configure\_joint(kos, joint\_name)  
File "D:\Projects\khacks\_dancing\_robot\skillet\skillet\examples\move\_joint\_a\_little.py", line 32, in configure\_joint  
result = kos.actuator.configure\_actuator(  
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  
File "C:\Users\DELL\anaconda3\envs\khacks\Lib\site-packages\pykos\services\actuator.py", line 140, in configure\_actuator  
return self.stub.ConfigureActuator(request)  
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  
File "C:\Users\DELL\anaconda3\envs\khacks\Lib\site-packages\grpc\_channel.py", line 1181, in **call**  
return \_end\_unary\_response\_blocking(state, call, False, None)  
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  
File "C:\Users\DELL\anaconda3\envs\khacks\Lib\site-packages\grpc\_channel.py", line 1006, in \_end\_unary\_response\_blocking  
raise \_InactiveRpcError(state) # pytype: disable=not-instantiable  
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  
grpc.\_channel.\_InactiveRpcError: <\_InactiveRpcError of RPC that terminated with:  
status = StatusCode.CANCELLED  
details = "Received RST\_STREAM with error code 8"  
debug\_error\_string = "UNKNOWN:Error received from peer {grpc\_message:"Received RST\_STREAM with error code 8", grpc\_status:1, created\_time:"2025-01-19T19:13:49.4308968+00:00"}"

INFO 2025-01-19 11:13:49 [**main**] Continuing with next joint...  
ERROR 2025-01-19 11:13:49 [**main**] === Failed Joints ===  
ERROR 2025-01-19 11:13:49 [**main**] Failed to move 1 joints: right\_ankle\_pitch

**what we tried:**

* pinging 192.168.42.1
* ssh and restarting kos servers 3 times
* unplug and plugging in the power source

Add Comment
