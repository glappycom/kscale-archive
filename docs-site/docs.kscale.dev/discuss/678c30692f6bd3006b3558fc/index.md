<!-- preserved from https://docs.kscale.dev/discuss/678c30692f6bd3006b3558fc via https://web.archive.org/web/20250621005322id_/https://docs.kscale.dev/discuss/678c30692f6bd3006b3558fc -->

# Inconsistent feet collision boxes in Mujoco XML

There are inconsistent collision properties for the feet in the XML provided in the mujoco playground, leads to robot not being able to stand, it's not representative of reality.

<https://github.com/kscalelabs/mujoco_playground/blob/master/playground/resources/zbot/zbot.xml>

See FOOT1 and FOOT2 below

```
  <default class="collision">
    <geom group="3"/>
    <default class="FOOT1">
      <geom size="0.08 0.0275 0.006" pos="0 -0.043 0.0133277" type="box" contype="1" conaffinity="1"/>
      <site size="0.08 0.0275 0.006" pos="0 -0.043 0.0133277" type="box"/>
    </default>
    <default class="FOOT2">
      <geom size="0.027 0.0325" pos="0 9.61687e-05 0.0388277" type="cylinder"/>
    </default>
```

Can't upload pics but these shapes are very different.

> This Wayback capture is the ReadMe.io JavaScript shell. The article body was not in the archived HTML.
