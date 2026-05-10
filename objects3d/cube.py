import cv2
import numpy as np


class Cube:
    def __init__(self, x=320, y=240, size=100):
        self.x    = float(x)
        self.y    = float(y)
        self.size = float(size)

        self.rot_x = 30.0
        self.rot_y = 45.0
        self.rot_z = 0.0

        self.edge_color = (0, 255, 255)
        self.face_color = (0, 100, 100)
        self.alpha      = 0.35
        self.thickness  = 2
        self.grabbed    = False
        self.spin_y     = 0.5

    def _rotation_matrix(self):
        rx, ry, rz = np.radians(self.rot_x), np.radians(self.rot_y), np.radians(self.rot_z)
        Rx = np.array([[1,0,0],[0,np.cos(rx),-np.sin(rx)],[0,np.sin(rx),np.cos(rx)]])
        Ry = np.array([[np.cos(ry),0,np.sin(ry)],[0,1,0],[-np.sin(ry),0,np.cos(ry)]])
        Rz = np.array([[np.cos(rz),-np.sin(rz),0],[np.sin(rz),np.cos(rz),0],[0,0,1]])
        return Rz @ Ry @ Rx

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

    def _get_geometry(self):
        s = self.size / 2
        verts = np.array([
            [-s,-s,-s],[s,-s,-s],[s,s,-s],[-s,s,-s],  # back face
            [-s,-s, s],[s,-s, s],[s,s, s],[-s,s, s],  # front face
        ], dtype=float)
        faces = [
            [0,1,2,3],[4,5,6,7],
            [0,1,5,4],[2,3,7,6],
            [0,3,7,4],[1,2,6,5],
        ]
        return verts, faces

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