import cv2
import numpy as np


class Toolbar:
    def __init__(self, width, height):
        self.width  = width
        self.height = height

    def draw(self, frame, mode, drawing, ar):
        """Render full UI overlay onto frame"""
        self._draw_top_bar(frame, mode, drawing, ar)
        self._draw_bottom_bar(frame)
        self._draw_color_palette(frame, drawing)
        return frame

    # ─────────────────────────── Top bar ───────────────────────────

    def _draw_top_bar(self, frame, mode, drawing, ar):
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (self.width, 64), (15, 15, 15), -1)
        cv2.addWeighted(overlay, 0.65, frame, 0.35, 0, frame)

        # Mode pill
        if mode == 'draw':
            pill_color = (0, 200, 200)
            label      = 'DRAW'
        else:
            pill_color = (200, 80, 0)
            label      = '3D'

        cv2.rectangle(frame, (12, 10), (90, 52), pill_color, -1)
        cv2.rectangle(frame, (12, 10), (90, 52), (255,255,255), 1)
        cv2.putText(frame, label, (22, 42),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,0), 2)

        # Mode-specific info
        if mode == 'draw':
            info = (f'Brush: {drawing.brush_name}   '
                    f'Color: {drawing.color_name}   '
                    f'Size: {drawing.thickness}')
            cv2.putText(frame, info, (105, 38),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (210, 210, 210), 1)
        else:
            info = f'Shape: {ar.shape_name}'
            cv2.putText(frame, info, (105, 38),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (210, 210, 210), 1)

    # ─────────────────────────── Color palette ───────────────────────────

    def _draw_color_palette(self, frame, drawing):
        px = self.width - 20
        for i, name in enumerate(reversed(drawing.COLOR_NAMES)):
            bgr = drawing.COLORS[name]
            cx  = px - i * 30
            cv2.circle(frame, (cx, 32), 10, bgr, -1)
            # Highlight active color
            active_name = drawing.COLOR_NAMES[drawing.color_idx]
            if name == active_name:
                cv2.circle(frame, (cx, 32), 13, (255, 255, 255), 2)

    # ─────────────────────────── Bottom bar ───────────────────────────

    def _draw_bottom_bar(self, frame):
        h = self.height
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, h - 32), (self.width, h), (15,15,15), -1)
        cv2.addWeighted(overlay, 0.65, frame, 0.35, 0, frame)

        hints = ('☞ Index=draw   ✊ Fist=pause   ✋ Palm=clear   '
                 '☞☞☞ 3-fingers=3D   🤙 Pinch=grab   '
                 'M=mode  B=brush  C=color  N=shape  +/-=size  S=save  Q=quit')
        cv2.putText(frame, hints, (10, h - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.38, (160, 160, 160), 1)

    # ─────────────────────────── FPS ───────────────────────────

    def draw_fps(self, frame, fps):
        cv2.putText(frame, f'FPS {int(fps)}', (10, 82),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (80, 255, 80), 1)