import cv2
import numpy as np
from effects.brushes import Brushes
from effects.particles import ParticleSystem


class DrawingMode:
    COLORS = {
        'cyan':    (0, 255, 255),
        'red':     (0, 0,   255),
        'green':   (0, 255,   0),
        'blue':    (255, 100,  0),
        'yellow':  (0, 220, 255),
        'white':   (255, 255, 255),
        'magenta': (255, 0,  255),
        'orange':  (0, 165, 255),
    }
    COLOR_NAMES  = list(COLORS.keys())
    BRUSH_NAMES  = ['normal', 'neon', 'spray', 'eraser', 'marker', 'dotted']

    def __init__(self, width, height):
        self.width  = width
        self.height = height

        # Canvas with alpha channel
        self.canvas = np.zeros((height, width, 4), dtype=np.uint8)

        self.color_idx = 0
        self.brush_idx = 0
        self.thickness = 5
        self.prev_point = None

        self.particles = ParticleSystem(width, height)

    # ─────────────────────────── Properties ───────────────────────────

    @property
    def color(self):
        return self.COLORS[self.COLOR_NAMES[self.color_idx]]

    @property
    def brush_name(self):
        return self.BRUSH_NAMES[self.brush_idx]

    @property
    def color_name(self):
        return self.COLOR_NAMES[self.color_idx]

    # ─────────────────────────── Drawing ───────────────────────────

    def update(self, gesture, index_tip):
        """Call every frame with current gesture and fingertip position"""
        if gesture == 'draw' and index_tip:
            if self.prev_point:
                self._apply_brush(self.prev_point, index_tip)
                self.particles.emit(*index_tip, self.color)
            self.prev_point = index_tip
        elif gesture == 'clear':
            self.clear()
            self.prev_point = None
        else:
            self.prev_point = None

    def _apply_brush(self, p1, p2):
        name = self.brush_name
        if name == 'normal':
            Brushes.normal(self.canvas, p1, p2, self.color, self.thickness)
        elif name == 'neon':
            Brushes.neon(self.canvas, p1, p2, self.color, self.thickness)
        elif name == 'spray':
            Brushes.spray(self.canvas, p2, self.color, self.thickness)
        elif name == 'eraser':
            Brushes.eraser(self.canvas, p1, p2, self.thickness)
        elif name == 'marker':
            Brushes.marker(self.canvas, p1, p2, self.color, self.thickness)
        elif name == 'dotted':
            Brushes.dotted(self.canvas, p1, p2, self.color, self.thickness)

    def clear(self):
        self.canvas = np.zeros((self.height, self.width, 4), dtype=np.uint8)
        self.particles.clear()

    # ─────────────────────────── Compositing ───────────────────────────

    def render(self, frame):
        """Overlay canvas and particles onto camera frame"""
        self.particles.update(self.canvas)
        alpha = self.canvas[:, :, 3] / 255.0
        for c in range(3):
            frame[:, :, c] = (
                frame[:, :, c] * (1 - alpha) +
                self.canvas[:, :, c] * alpha
            ).astype(np.uint8)
        return frame

    # ─────────────────────────── Controls ───────────────────────────

    def next_color(self):
        self.color_idx = (self.color_idx + 1) % len(self.COLOR_NAMES)

    def next_brush(self):
        self.brush_idx = (self.brush_idx + 1) % len(self.BRUSH_NAMES)

    def increase_thickness(self):
        self.thickness = min(30, self.thickness + 2)

    def decrease_thickness(self):
        self.thickness = max(1, self.thickness - 2)

    def save(self, path='drawing.png'):
        import cv2
        cv2.imwrite(path, self.canvas)
        print(f"Drawing saved: {path}")