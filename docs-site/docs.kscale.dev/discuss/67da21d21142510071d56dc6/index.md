<!-- preserved from https://docs.kscale.dev/discuss/67da21d21142510071d56dc6 via https://web.archive.org/web/20250713174404id_/https://docs.kscale.dev/discuss/67da21d21142510071d56dc6 -->

# missing some para of urdf when using urdf2mjcf tool

hello.i use this tool to convert my urdf to mjcf in order to use in mink,but i encounter some problem:when i define a virtual link in the urdf such as"end_effector" but it disappear in the converted xml file? is there any solution to fix it?or mujoco support other way to do that?

the segement is:

<link name="end_effector">
    <visual>
        <geometry>
            <sphere radius="0.01" />
        </geometry>
    </visual>
    <inertial>
        <mass value="0.0" />
    </inertial>
  </link>
  <joint name="ee_gripper" type="fixed" dont_collapse="true">
    <origin
        xyz="0.21 0 0"
        rpy="-1.57079632679 0 -1.57079632679" />
    <parent
        link="link06" />
    <child
        link="end_effector" />
  </joint>

> This Wayback capture is the ReadMe.io JavaScript shell. The article body was not in the archived HTML.
