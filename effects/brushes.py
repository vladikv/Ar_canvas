import cv2
import numpy as np


class Brushes:
    @staticmethod
    def normal(canvas, p1, p2, color, thickness):
        """Solid line brush"""
        b, g, r = color
        cv2.line(canvas, p1, p2, (b, g, r, 255), thickness)

    @staticmethod
    def neon(canvas, p1, p2, color, thickness):
        """Glowing neon brush with layered transparency"""
        b, g, r = color
        layers = [
            (thickness * 5, 40),
            (thickness * 3, 100),
            (thickness,     255),
        ]
        for t, alpha in layers:
            cv2.line(canvas, p1, p2, (b, g, r, alpha), t)

    @staticmethod
    def spray(canvas, point, color, thickness):
        """Spray paint brush with random scatter"""
        x, y = point
        b, g, r = color
        h, w = canvas.shape[:2]
        for _ in range(30):
            ox = x + int(np.random.randn() * thickness * 3)
            oy = y + int(np.random.randn() * thickness * 3)
            ox = np.clip(ox, 0, w - 1)
            oy = np.clip(oy, 0, h - 1)
            canvas[oy, ox] = (b, g, r, 255)

    @staticmethod
    def eraser(canvas, p1, p2, thickness):
        """Eraser — clears pixels to transparent"""
        cv2.line(canvas, p1, p2, (0, 0, 0, 0), thickness * 6)

    @staticmethod
    def marker(canvas, p1, p2, color, thickness):
        """Semi-transparent marker brush"""
        b, g, r = color
        overlay = canvas.copy()
        cv2.line(overlay, p1, p2, (b, g, r, 180), thickness * 2)
        cv2.addWeighted(overlay, 0.5, canvas, 0.5, 0, canvas)

    @staticmethod
    def dotted(canvas, p1, p2, color, thickness):
        """Dotted line brush"""
        b, g, r = color
        dist  = int(np.linalg.norm(np.array(p2) - np.array(p1)))
        steps = max(dist // 10, 1)
        for i in range(steps + 1):
            t  = i / steps
            cx = int(p1[0] + (p2[0] - p1[0]) * t)
            cy = int(p1[1] + (p2[1] - p1[1]) * t)
            cv2.circle(canvas, (cx, cy), thickness, (b, g, r, 255), -1)