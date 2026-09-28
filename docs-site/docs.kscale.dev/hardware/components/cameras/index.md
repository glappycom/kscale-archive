<!-- preserved from https://docs.kscale.dev/hardware/components/cameras via https://web.archive.org/web/20241014234509id_/https://docs.kscale.dev/hardware/components/cameras -->

# Cameras - K-Scale Labs Docs

Hardware

Components

Cameras

⚠️

This documentation is under construction and incomplete. We are in the process of choosing a camera that works well with our robots.

# Cameras

## Sensing

The preferred camera to use with the [Seeed Studio J501 carrier board](/hardware/components/mcu) is the [3MP SG3S-ISX031C-GMSL2F (opens in a new tab)](https://www.sensing-world.com/en/pd.jsp?id=23) from Sensing.

* [Camera Datasheet (opens in a new tab)](https://autosensee.feishu.cn/file/NvhcbDq4Wo0e4DxG1d7cP19QnIf)
* [GMSL Extension Board (opens in a new tab)](https://www.seeedstudio.com/reServer-Industrial-J501-GMSL-extension-board-p-5949.html)

This camera comes with several different possible lenses. We are using the 118 degree horizontal field of view lens.

![Sensing Cameras](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fsensing-cameras.5421a9fe.png&w=3840&q=75)

## Arducam

We have experimented with the ArduCAM

* [18MP Color Camera (opens in a new tab)](https://www.arducam.com/product/arducam-pivariety-18mp-ar1820hs-color-camera-module-for-rpi-cam-b0367)
* [Fisheye Lens (opens in a new tab)](https://www.arducam.com/product/arducam-180-degree-fisheye-1-2-3-m12-mount-with-lens-adapter-for-raspberry-pi-high-quality-camera/)

These are MIPI cameras, as oppose to USB cameras, and have higher data transfer rates.
ArduCAM makes open source cameras and have a wide selection of lenses which is important
for us as we do not have neck actuation.

Here is an example of using OpenCV to capture a frame:

```
import cv2
import numpy as np
from v4l2py import Device
 
resolution = (4896, 3684)
 
with Device.from_id(camera_id) as cam:
    for i, frame in enumerate(cam):
        print(f"Frame #{i}: {len(frame)} bytes")
        bayer = np.frombuffer(frame.data, dtype=np.uint16).reshape(resolution[::-1])
        img = cv2.cvtColor(bayer, cv2.COLOR_BayerGB2RGB)
        cv2.imshow("frame", img)
 
        # The camera image is (W, H) by default, but we display as (H, W).
        img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        cv2.imwrite(f"frame_{i}.png", img)
```

The driver source code for the ArduCAM lives [here (opens in a new tab)](https://github.com/ArduCAM/MIPI_Camera).
The driver used for the python implementation is [v4l2py (opens in a new tab)](https://github.com/tiagocoutinho/v4l2py/tree/master).

## From Physics to Pixels

1. Light enters the camera through the lens.
2. Photons hit the image sensor, typically a CCD (Charge-Coupled Device) or CMOS (Complementary Metal-Oxide-Semiconductor) sensor.
3. Each photodiode in the CMOS sensor has a filter on it, Red Green or Blue (together called CFA, color filter array). Comparing their intensity gives us colored images. (also see step 8)
4. Each sensor pixel contains a photodiode that converts photons into electrical charges.
5. The accumulated charge is proportional to the light intensity.
6. An ADC (Analog-to-Digital Converter) converts the analog signal to digital values.
7. These digital values represent the brightness and color information for each pixel.
8. Demosaicing algorithms interpolate the full RGB information for each pixel.
   (eg. a pixel in the sensor with a blue filter will have its red and green values extrapolated from the nearby pixels which have those filters).
9. Additional processing may include noise reduction, sharpening, and color correction.
10. The resulting digital image is now ready for display or further processing by neural networks or other algorithms.

### Bayer Filter Mosaic

The Bayer filter mosaic is a color filter array (CFA) used in most digital camera sensors. It's named after its inventor, Bryce Bayer of Eastman Kodak. Here's how it works:

* The mosaic consists of a repeating 2x2 pattern of color filters placed over the sensor's pixels.
* Each 2x2 square contains two green filters, one red filter, and one blue filter.
* The pattern typically looks like this:

![Bayer Filter Mosaic](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fbayer.0885c264.png&w=640&q=75)

* There are twice as many green filters because the human eye is more sensitive to green light.
* Each pixel only captures one color of light (red, green, or blue).

This arrangement allows a single sensor to capture color information, but requires interpolation (demosaicing) to reconstruct a full-color image.

### Encoding

### Advanced Processing: HDR and Color Spaces

#### High Dynamic Range (HDR)

HDR imaging captures a wider range of light intensities than standard sensors. It often involves taking multiple exposures and combining them:

* Underexposed image captures highlights
* Overexposed image captures shadows
* Software merges these to create a single image with more detail in both bright and dark areas

#### Color Space Conversion

After demosaicing, the image data is typically in the camera's native RGB color space. Common conversions include:

* RGB to YUV: Used in many video compression algorithms
* RGB to sRGB: Standard color space for most displays
* RGB to Adobe RGB: Wider color gamut, often used in professional photography

### Key Terms

* **RGB (Red, Green, Blue)**: Additive color model used in digital imaging and displays.
* **YUV**: Color encoding system that separates brightness (Y) from color information (U and V).
  + Y: Luma (brightness)
  + U and V: Chrominance (color) components
* **sRGB**: Standard RGB color space for most consumer devices and the web.
* **Color Gamut**: The range of colors a device can capture or display.
* **Bitmap**: a grid of pixels, as opposed to vector image.

[Motor Control](/hardware/components/motor_control "Motor Control")[Speaker](/hardware/components/speaker "Speaker")
