from objects3d.cube import Cube
from objects3d.sphere import Sphere
from objects3d.pyramid import Pyramid


class ARMode:
    SHAPES = ['cube', 'sphere', 'pyramid']

    def __init__(self, width, height):
        self.width  = width
        self.height = height

        cx, cy = width // 2, height // 2
        self.objects = {
            'cube':    Cube(cx, cy, 120),
            'sphere':  Sphere(cx, cy, 120),
            'pyramid': Pyramid(cx, cy, 120),
        }

        self.shape_idx   = 0
        self.prev_tip    = None
        self.prev_scale  = None

    # ─────────────────────────── Properties ───────────────────────────

    @property
    def shape_name(self):
        return self.SHAPES[self.shape_idx]

    @property
    def obj(self):
        return self.objects[self.shape_name]

    # ─────────────────────────── Update ───────────────────────────

    def update(self, gesture, index_tip, two_hand_dist):
        """Call every frame with gesture data"""
        self.obj.auto_spin()

        # Handle two-hand scaling first (independent of gesture)
        if two_hand_dist is not None:
            self.obj.grab()  # Keep grabbed while scaling
            if self.prev_scale is not None:
                delta = (two_hand_dist - self.prev_scale) * 0.5
                if abs(delta) > 0.1:  # Only scale if change is significant
                    self.obj.scale(delta)
            self.prev_scale = two_hand_dist
        else:
            self.prev_scale = None

        # Handle main gestures
        if gesture == 'draw' and index_tip:
            # Point with index finger - move object
            self.obj.grab()
            self.obj.move(*index_tip)
            self.prev_tip = index_tip

        elif gesture == 'pinch' and index_tip:
            self.obj.grab()
            self.obj.move(*index_tip)

            # Rotate by hand movement
            if self.prev_tip:
                dx = index_tip[0] - self.prev_tip[0]
                dy = index_tip[1] - self.prev_tip[1]
                self.obj.rotate(dx, dy)
            self.prev_tip = index_tip

        elif gesture == 'next':
            self.next_shape()
            self.prev_tip   = None
            self.prev_scale = None

        elif gesture == 'clear':
            self._reset()

        else:
            self.obj.release()
            self.prev_tip   = None

    def _reset(self):
        cx, cy = self.width // 2, self.height // 2
        self.obj.move(cx, cy)
        self.obj.rot_x = 30.0
        self.obj.rot_y = 45.0
        self.obj.rot_z = 0.0
        self.obj.release()
        self.prev_tip   = None
        self.prev_scale = None

    # ─────────────────────────── Render ───────────────────────────

    def render(self, frame):
        """Draw active 3D object onto frame"""
        return self.obj.draw(frame)

    # ─────────────────────────── Controls ───────────────────────────

    def next_shape(self):
        self.shape_idx = (self.shape_idx + 1) % len(self.SHAPES)
        self._reset()

    def add_shape(self, shape_type='cube'):
        """Add a new shape to the scene"""
        cx, cy = self.width // 2, self.height // 2
        new_obj = None
        
        if shape_type == 'cube':
            new_obj = Cube(cx, cy, 120)
        elif shape_type == 'sphere':
            new_obj = Sphere(cx, cy, 120)
        elif shape_type == 'pyramid':
            new_obj = Pyramid(cx, cy, 120)
        
        if new_obj:
            self.objects[f'{shape_type}_{len(self.objects)}'] = new_obj
            print(f"✓ Added {shape_type}")

    def remove_shape(self):
        """Remove the current active shape"""
        if len(self.objects) > 1:  # Keep at least one shape
            del self.objects[self.shape_name]
            self.shape_idx = 0
            print("✓ Removed shape")

    def list_shapes(self):
        """Get list of all shapes"""
        return list(self.objects.keys())