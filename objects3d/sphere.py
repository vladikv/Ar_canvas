import cv2
import numpy as np


class Sphere:
    def __init__(self, x=320, y=240, size=100):
        self.x    = float(x)
        self.y    = float(y)
        self.size = float(size)

        self.rot_x = 0.0
        self.rot_y = 0.0
        self.rot_z = 0.0

        self.edge_color = (255, 100, 0)
        self.face_color = (100, 40,  0)
        self.alpha      = 0.35
        self.thickness  = 1
        self.grabbed    = False
        self.spin_y     = 0.5

        self.rings = 8
        self.segs  = 12

    def _rotation_matrix(self):
        rx, ry, rz = np.radians(self.rot_x), np.radians(self.rot_y), np.radians(self.rot_z)
        Rx = np.array([[1,0,0],[0,np.cos(rx),-np.sin(rx)],[0,np.sin(rx),np.cos(rx)]])
        Ry = np.array([[np.cos(ry),0,np.sin(ry)],[0,1,0],[-np.sin(ry),0,np.cos(ry)]])
        Rz = np.array([[np.cos(rz),-np.sin(rz),0],[np.sin(rz),np.cos(rz),0],[0,0,1]])
        return Rz @ Ry @ Rx

    def _get_geometry(self):
        verts = []
        r = self.size / 2
        for i in range(self.rings + 1):
            lat = np.pi * i / self.rings - np.pi / 2
            for j in range(self.segs):
                lon = 2 * np.pi * j / self.segs
                verts.append([
                    np.cos(lat) * np.cos(lon) * r,
                    np.sin(lat) * r,
                    np.cos(lat) * np.sin(lon) * r,
                ])
        faces = []
        for i in range(self.rings):
            for j in range(self.segs):
                a = i * self.segs + j
                b = i * self.segs + (j + 1) % self.segs
                c = (i + 1) * self.segs + (j + 1) % self.segs
                d = (i + 1) * self.segs + j
                faces.append([a, b, c, d])
        return np.array(verts, dtype=float), faces

    def _project(self, vertices):
        R   = self._rotation_matrix()
        fov = 600.0
        pts = []
        for v in vertices:
            rv = R @ v
            z  = rv[2] + fov
            if z == 0: z = 0.001
            pts.append((int(rv[0] * fov / z + self.x),
                        int(rv[1] * fov / z + self.y)))
        return pts

    def draw(self, frame):
        verts, faces = self._get_geometry()
        pts = self._project(verts)
        h, w = frame.shape[:2]
        overlay = frame.copy()

        b, g, r = self.face_color
        for face in faces:
            poly = np.array([pts[i] for i in face], dtype=np.int32)
            if all(0 <= p[0] < w and 0 <= p[1] < h for p in poly):
                cv2.fillPoly(overlay, [poly], (b, g, r))

        cv2.addWeighted(overlay, self.alpha, frame, 1 - self.alpha, 0, frame)

        eb, eg, er = self.edge_color
        for face in faces:
            for k in range(len(face)):
                cv2.line(frame, pts[face[k]], pts[face[(k+1) % len(face)]],
                         (eb, eg, er), self.thickness)
        return frame

    def rotate(self, dx, dy):
        self.rot_y += dx * 0.5
        self.rot_x += dy * 0.5

    def scale(self, delta):
        self.size = max(30, min(400, self.size + delta))

    def move(self, x, y):
        self.x, self.y = float(x), float(y)

    def auto_spin(self):
        if not self.grabbed:
            self.rot_y += self.spin_y

    def grab(self):
        self.grabbed = True
        self.spin_y  = 0.0

    def release(self):
        self.grabbed = False
        self.spin_y  = 0.5