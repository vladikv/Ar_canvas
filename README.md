<div align="center">

# 🖐️ AR Canvas

**Draw in the air. Sculpt in 3D. No mouse. No keyboard. Just your hand.**
</div>

---

## ✨ What is this?

AR Canvas turns your webcam into an augmented reality studio.  
Point your finger → draw glowing strokes in the air.  
Switch gesture → grab a 3D cube and spin it with your hand.  
Everything renders live on top of your camera feed — no extra hardware needed.

---

## 🎥 Demo

> _Point your index finger to draw. Make a fist to pause. Show three fingers to enter 3D mode._

```
☞  Index finger   →  Draw on screen
✊  Fist           →  Pause / stop drawing
✋  Open palm      →  Clear canvas
☞☞☞ Three fingers →  Switch to 3D mode
🤌  Pinch          →  Grab and move 3D object
```

---

## 🚀 Features

### ✏️ Drawing Mode
| Brush | Effect |
|-------|--------|
| `normal` | Solid smooth line |
| `neon` | Glowing layered light effect |
| `spray` | Scattered paint particles |
| `marker` | Semi-transparent wide stroke |
| `dotted` | Dotted line pattern |
| `eraser` | Erase strokes |

- 🎨 **8 colors** — cyan, red, green, blue, yellow, magenta, orange, white
- ✨ **Particle system** — sparks trail your brush with gravity
- 💾 **Save** your drawing with `S`

### 📦 3D Mode
- 3 shapes: **Cube · Sphere · Pyramid**
- Grab with pinch gesture → **move** anywhere on screen
- Rotate on **X / Y axes** by moving your hand
- **Two-hand scale** — spread hands to grow, bring together to shrink
- Auto-spin when not grabbed
- Cycle shapes with `N`

---

## 📁 Project Structure

```
ar_canvas/
├── main.py                  # Entry point
├── hand_tracker.py          # MediaPipe wrapper (21 landmarks)
├── gesture_detector.py      # Gesture recognition logic
├── modes/
│   ├── drawing_mode.py      # Canvas, brushes, particles
│   └── ar_mode.py           # 3D object management
├── objects3d/
│   ├── cube.py              # Cube geometry + projection
│   ├── sphere.py            # Sphere geometry + projection
│   └── pyramid.py           # Pyramid geometry + projection
├── effects/
│   ├── brushes.py           # All brush rendering functions
│   └── particles.py         # Particle system with gravity
└── ui/
    └── toolbar.py           # HUD, color palette, hints bar
```


## ⌨️ Keyboard Controls

| Key | Action |
|-----|--------|
| `M` | Toggle Draw / 3D mode |
| `B` | Cycle brush type |
| `C` | Cycle color |
| `N` | Next 3D shape |
| `+` / `-` | Brush size |
| `S` | Save drawing as PNG |
| `Q` | Quit |

---

## 🤌 Gesture Reference

| Gesture | Action |
|---------|--------|
| ☞ Index finger | Draw / move in 3D |
| ✊ Fist | Pause drawing |
| ✋ Open palm | Clear canvas |
| ☞☞☞ Three fingers | Enter 3D mode |
| 🤌 Pinch | Grab 3D object |
| 🤌 Pinch + move | Rotate 3D object |
| Two hands apart | Scale 3D object |

---

## 🛠️ Tech Stack

| Library | Purpose |
|---------|---------|
| `opencv-python` | Camera capture and rendering |
| `mediapipe` | Real-time hand landmark detection |
| `numpy` | Matrix math, 3D projections |
| `pygame` | Window management |

---

## 🗺️ Roadmap

- [ ] AI sketch-to-3D conversion
- [ ] More 3D shapes (torus, star, custom OBJ)
- [ ] Color picker gesture
- [ ] Record drawing timelapse video
- [ ] Gesture control OS integration (see [GestureOS](#))

---

<div align="center">
Built with 🖐️ and Python
</div>
