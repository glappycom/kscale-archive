<!-- preserved from https://docs.kscale.dev/discuss/679c5231e60d8300114cc103 via https://web.archive.org/web/20250621015136id_/https://docs.kscale.dev/discuss/679c5231e60d8300114cc103 -->

# Discussions

[Ask a Question](/discuss-new)

[Back to All](/discuss)

0

## get error when enable --show\_viewer True

5 months ago by hua\_

ces/zbot/robot\_fixed.urdf')>, material: <gs.materials.Rigid>.  
[Genesis] [12:28:50] [INFO] Building scene <5412285>...  
[Genesis] [12:28:56] [INFO] Compiling simulation kernels...  
[Genesis] [12:29:03] [INFO] Building visualizer...  
libGL error: MESA-LOADER: failed to open iris: /usr/lib/dri/iris\_dri.so: cannot open shared object file: No such file or directory (search paths /usr/lib/x86\_64-linux-gnu/dri:$${ORIGIN}/dri:/usr/lib/dri, suffix \_dri)  
libGL error: failed to load driver: iris  
libGL error: MESA-LOADER: failed to open swrast: /usr/lib/dri/swrast\_dri.so: cannot open shared object file: No such file or directory (search paths /usr/lib/x86\_64-linux-gnu/dri:$${ORIGIN}/dri:/usr/lib/dri, suffix \_dri)  
libGL error: failed to load driver: swrast  
Exception in thread Thread-2 (\_init\_and\_start\_app):  
Traceback (most recent call last):  
File "/home/zzh/miniconda3/envs/genesis/lib/python3.11/threading.py", line 1045, in \_bootstrap\_inner  
self.run()  
File "/home/zzh/miniconda3/envs/genesis/lib/python3.11/threading.py", line 982, in run  
self.\_target(\_self.\_args, **self.\_kwargs)  
File "/home/zzh/miniconda3/envs/genesis/lib/python3.11/site-packages/genesis/ext/pyrender/viewer.py", line 1138, in \_init\_and\_start\_app  
super(Viewer, self).**init**(  
File "/home/zzh/miniconda3/envs/genesis/lib/python3.11/site-packages/pyglet/window/xlib/**init**.py", line 167, in** init **super().**init**(\_args,** kwargs)  
File "/home/zzh/miniconda3/envs/genesis/lib/python3.11/site-packages/pyglet/window/**init**.py", line 533, in **init**  
context = config.create\_context(gl.current\_context)  
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  
File "/home/zzh/miniconda3/envs/genesis/lib/python3.11/site-packages/pyglet/gl/xlib.py", line 117, in create\_context  
return XlibContext(self, share)  
^^^^^^^^^^^^^^^^^^^^^^^^  
File "/home/zzh/miniconda3/envs/genesis/lib/python3.11/site-packages/pyglet/gl/xlib.py", line 152, in **init**  
raise gl.ContextException(msg)  
pyglet.gl.ContextException: Could not create GL context

Add Comment
