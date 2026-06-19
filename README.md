# Pico Shutter

A wireless camera shutter trigger using a Raspberry Pi Pico 2 W. Your phone connects to the Pico's open WiFi hotspot and a simple webpage lets you trigger the shutter by shorting the mic pin on a wired headphone jack -- exactly like pressing the middle button on Apple EarPods.

Works on iPhone and Android.

---

## What You Need

- Raspberry Pi Pico 2 W
- TRRS male to male 3.5mm aux cable (must be 4 pole -- 2 black rings on the plug)
- 2 alligator clips
- 1k ohm resistor (optional but recommended for pin protection)
- USB-C to 3.5mm adapter that supports mic and remote control (not audio only)
- Lightning to 3.5mm adapter if using an older iPhone

---

## Important Note on Adapters

Many cheap USB-C to 3.5mm adapters are audio only and will not work. You need one that specifically supports microphone and remote control buttons. Look for packaging that says "works with inline mic" or "supports headset with mic". The Apple USB-C to 3.5mm adapter and Google USB-C to 3.5mm adapter are both confirmed to work.

---

## Wiring

### Identifying the TRRS plug segments

Count from the plastic housing outward:

```
[PLASTIC]--[SLEEVE]--[GAP]--[RING2]--[GAP]--[RING1]--[GAP]--[TIP]
               |                |
           Mic/Remote        Ground
```

- SLEEVE = segment closest to the plastic housing = Mic/Remote
- RING2 = second segment from the plastic = Ground

### Alligator clip connections

| Alligator clip | TRRS segment | Pico 2 W pin |
|---|---|---|
| Clip 1 | SLEEVE (Mic/Remote) | GP0 - Pin 1 (top left corner) |
| Clip 2 | RING2 (Ground) | GND - Pin 3 |

### Pico 2 W pin reference

```
        +-----[USB]-----+
GP0  1 *|               |
GND  3 *|               |
        ...             ...
        +---------------+
```

Pins 1 and 3 are on the left side near the USB connector.

Optionally put a 1k ohm resistor in series on GP0 for protection.

---

## Setup

1. Flash MicroPython onto your Pico 2 W from micropython.org/download/RPI_PICO2_W
2. Copy main.py to the root of the Pico using Thonny
3. Plug one end of the TRRS cable into your phone via adapter
4. Attach alligator clips to the other end as described above
5. Connect alligator clips to GP0 and GND on the Pico
6. Power the Pico via USB

---

## Connecting

1. On your phone go to Settings -> WiFi
2. Connect to PicoShutter (no password required)
3. Open your phone browser and go to 192.168.4.1
4. The shutter page will load automatically

---

## Using

1. Open your phone camera app
2. Switch to the browser with the shutter page open
3. Tap the SHUTTER button on the webpage
4. The Pico briefly shorts the mic pin to ground for 100ms which triggers the camera

### What the button does

| Camera mode | Result |
|---|---|
| Photo | Takes a photo |
| Video | Starts or stops recording |

---

## Troubleshooting

**WiFi not showing up**
- Make sure the Pico is powered and main.py is on it
- Check the Thonny console for errors

**Page not loading**
- Make sure you are connected to PicoShutter WiFi not your home WiFi
- Type 192.168.4.1 manually in the browser address bar

**Shutter not firing**
- Check your USB-C to 3.5mm adapter supports mic and remote -- audio only adapters will not work
- Check alligator clips are on the correct TRRS segments
- Make sure the cable is fully plugged into the phone adapter
- Check GP0 and GND pins are correct on the Pico
- Try a different TRRS cable -- some cables only have 3 poles (TRS) even if they look the same
