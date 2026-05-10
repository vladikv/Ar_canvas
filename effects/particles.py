import numpy as np


class ParticleSystem:
    def __init__(self, canvas_width, canvas_height):
        self.width  = canvas_width
        self.height = canvas_height
        self.particles = []

    def emit(self, x, y, color, count=3):
        """Spawn particles at given position"""
        b, g, r = color
        for _ in range(count):
            self.particles.append({
                'x':    float(x),
                'y':    float(y),
                'vx':   np.random.randn() * 2.5,
                'vy':   np.random.randn() * 2.5 - 1.0,
                'life': 1.0,
                'decay': np.random.uniform(0.03, 0.07),
                'color': (b, g, r),
            })

    def update(self, canvas):
        """Update all particles and paint them onto canvas"""
        alive = []
        for p in self.particles:
            p['x']    += p['vx']
            p['y']    += p['vy']
            p['vy']   += 0.12   # gravity
            p['life'] -= p['decay']

            if p['life'] > 0:
                x, y = int(p['x']), int(p['y'])
                if 0 <= x < self.width and 0 <= y < self.height:
                    alpha = int(p['life'] * 255)
                    b, g, r = p['color']
                    canvas[y, x] = (b, g, r, alpha)
                alive.append(p)

        self.particles = alive

    def clear(self):
        self.particles = []