import cv2
import mediapipe as mp
import numpy as np


class HandTracker:
    # Finger tip landmark indices
    FINGER_TIPS = [4, 8, 12, 16, 20]
    WRIST = 0

    def __init__(self, max_hands=2, detection_confidence=0.7, tracking_confidence=0.7):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_draw_styles = mp.solutions.drawing_styles

        self.hands = self.mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )

        self.results = None
        self.landmarks = []

    def process(self, frame):
        """Process frame and detect hands"""
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb)
        self.landmarks = []

        if self.results.multi_hand_landmarks:
            h, w, _ = frame.shape
            for hand_lms in self.results.multi_hand_landmarks:
                points = []
                for lm in hand_lms.landmark:
                    points.append((int(lm.x * w), int(lm.y * h), lm.z))
                self.landmarks.append(points)

        return self.landmarks

    def draw(self, frame):
        """Draw hand skeleton on frame"""
        if self.results and self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame,
                    hand_lms,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_draw_styles.get_default_hand_landmarks_style(),
                    self.mp_draw_styles.get_default_hand_connections_style()
                )
        return frame

    def get_finger_tip(self, hand_index=0, finger=1):
        """
        Returns fingertip coordinates
        finger: 0=thumb, 1=index, 2=middle, 3=ring, 4=pinky
        """
        if hand_index < len(self.landmarks):
            tip_id = self.FINGER_TIPS[finger]
            return self.landmarks[hand_index][tip_id][:2]
        return None

    def get_fingers_up(self, hand_index=0):
        """
        Returns list [thumb, index, middle, ring, pinky]
        1 = raised, 0 = folded
        """
        if hand_index >= len(self.landmarks):
            return []

        lm = self.landmarks[hand_index]
        fingers = []

        # Thumb (compare by X axis)
        if lm[4][0] < lm[3][0]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Other 4 fingers (compare by Y axis — lower value = higher on screen)
        for tip_id in self.FINGER_TIPS[1:]:
            if lm[tip_id][1] < lm[tip_id - 2][1]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    def get_gesture(self, hand_index=0):
        """
        Recognizes gesture and returns name:
        - 'draw'    → index finger only (drawing mode)
        - 'stop'    → fist (pause)
        - 'clear'   → open palm (clear canvas)
        - 'mode_3d' → three fingers (3D mode)
        - 'pinch'   → pinch gesture (grab object)
        - 'unknown' → unrecognized gesture
        """
        fingers = self.get_fingers_up(hand_index)
        if not fingers:
            return 'unknown'

        total = sum(fingers)

        # Fist — all fingers folded
        if total == 0:
            return 'stop'

        # Open palm — all fingers raised
        if total == 5:
            return 'clear'

        # Only index finger — drawing
        if fingers == [0, 1, 0, 0, 0]:
            return 'draw'

        # Three fingers up — 3D mode
        if fingers == [0, 1, 1, 1, 0]:
            return 'mode_3d'

        # Pinch — thumb and index finger close together
        if hand_index < len(self.landmarks):
            lm = self.landmarks[hand_index]
            thumb_tip = np.array(lm[4][:2])
            index_tip = np.array(lm[8][:2])
            dist = np.linalg.norm(thumb_tip - index_tip)
            if dist < 40:
                return 'pinch'

        return 'unknown'

    def get_pinch_distance(self, hand_index=0):
        """Distance between thumb and index finger (for scaling)"""
        if hand_index >= len(self.landmarks):
            return None
        lm = self.landmarks[hand_index]
        thumb = np.array(lm[4][:2])
        index = np.array(lm[8][:2])
        return float(np.linalg.norm(thumb - index))

    def get_two_hand_distance(self):
        """Distance between index fingers of both hands (for 3D scaling)"""
        if len(self.landmarks) < 2:
            return None
        p1 = np.array(self.landmarks[0][8][:2])
        p2 = np.array(self.landmarks[1][8][:2])
        return float(np.linalg.norm(p1 - p2))

    def hand_count(self):
        """Number of detected hands"""
        return len(self.landmarks)