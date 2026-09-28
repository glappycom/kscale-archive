<!-- preserved from https://docs.kscale.dev/hardware/components/lcd via https://web.archive.org/web/20241015003646id_/https://docs.kscale.dev/hardware/components/lcd -->

# LCD for Eyes - K-Scale Labs Docs

Hardware

Components

LCD

⚠️

This documentation is under construction and incomplete. We are in the process
of choosing a microphone that works well with our robots.

# LCD for Eyes

At the moment, we are using the this LCD from waveshare: [https://www.waveshare.com/product/rp2040-lcd-1.28.htm (opens in a new tab)](https://www.waveshare.com/product/rp2040-lcd-1.28.htm)
It is an 1.28in circular display connected to a waveshare RP2040 microcontroller. It also has an IMU built in.

We selected it for its compact form factor and having the onboard microcontroller helps simplify the firmware code on the Jetson.

It can be programmed using the Pico SDK in C or with CircuitPython or MicroPython.

### Implementation with C

For the eye animation, we chose the C library LVGL. Waveshare includes a useful library for initiating and interacting with the LCD
[/lib/LCD (opens in a new tab)](https://github.com/waveshareteam/RP2040-Touch-LCD-1.28/tree/main/c/lib/LCD) and how to use it.
An example of how to build an eye emotion animation on top of the library:

```
void Grinning_Emotion_Init_Anim(void)
{
    if (anim_enabled) return;
 
    lv_obj_clean(lv_scr_act()); // Get current screen and clean it
    lv_obj_set_style_bg_color(lv_scr_act(), lv_color_white(), 0 );
 
    lv_obj_t *arcPointer = lv_arc_create(lv_scr_act());
 
 
    lv_obj_set_size(arcPointer, 175, 175);
    lv_arc_set_bg_angles(arcPointer, 190, 350);
    lv_arc_set_angles(arcPointer, 0, 0);
    lv_obj_remove_style(arcPointer, NULL, LV_PART_KNOB);
    lv_obj_set_style_arc_color(arcPointer, lv_palette_main(LV_PALETTE_BROWN), 0);
    lv_obj_center(arcPointer);
    lv_obj_set_style_arc_width(arcPointer, 19, LV_PART_MAIN);
 
 
    // Define animation
    lv_anim_t a;
    lv_anim_init(&a);
 
    //Params of animation
    lv_anim_set_var(&a, arcPointer);
    lv_anim_set_time(&a, 3000);
    // lv_anim_set_repeat_count(&a, LV_ANIM_REPEAT_INFINITE);
    lv_anim_set_path_cb(&a, lv_anim_path_ease_in_out);
    // lv_anim_set_playback_time(&a, 1000);
 
 
    // Direct to callback to apply value
    lv_anim_set_exec_cb(&a, arc_start_angle_cb);
    lv_anim_set_values(&a, 205, 190);
    lv_anim_start(&a);
    lv_anim_set_exec_cb(&a, arc_end_angle_cb);
    lv_anim_set_values(&a, 335, 350);
    lv_anim_start(&a);
 
    anim_enabled = true;
    logo_enabled = false;
}
```

For reading the data from the IMU, use the QMI8658 library on the Waveshare demo repo [/lib/QMI8658 (opens in a new tab)](https://github.com/waveshareteam/RP2040-Touch-LCD-1.28/tree/main/c/lib/QMI8658).
See the full sample code at their github repo, a short snippet is included below

```
#include "QMI8658.h"
 
QMI8658_init(); //located in LCD_1in28_LVGL_test.c
 
//...
add_repeating_timer_ms(50, repeating_imu_data_update_timer_callback, NULL, &imu_data_update_timer);
add_repeating_timer_ms(100, repeating_imu_diff_timer_callback, NULL, &imu_diff_timer);
add_repeating_timer_ms(1,   repeating_lvgl_timer_callback, NULL, &lvgl_timer);
 
char label_text[64];
float acc[3], gyro[3];
unsigned int tim_count = 0;
 
QMI8658_read_xyz(acc, gyro, &tim_count);
```

### CircuitPython

An alternative choice is to flash the RP2040 with CircuitPython and then write Python code to load onto it. An example open source implementation is located [here (opens in a new tab)](https://github.com/aedile/circuit_python_wsRP2040128).
You can display an animation with the below functionalities:

```
hardware = wsRP2040128()
hardware.draw_circle('eye', 115, 120, 100, hardware.color('white'))
hardware.sprites['eye'].x = 80
 
sleep_time = 0.01
moving_pos = True
 
while True:
    if(hardware.sprites['eye'].x < 80):
        moving_pos = True
        hardware.sprites['eye'].x = 80
    if(hardware.sprites['eye'].x >170):
        moving_pos = False
        hardware.sprites['eye'].x = 170
 
    if moving_pos:
        hardware.sprites['eye'].x += 2
    else:
        hardware.sprites['eye'].x -= 2
 
    if(hardware.time + sleep_time) < time.monotonic():
        hardware.update()
        hardware.time = time.monotonic()
 
    time.sleep(sleep_time)
```

[Microphone](/hardware/components/microphone "Microphone")[Firmware ↗](/hardware/components/lcd# "Firmware ↗")
