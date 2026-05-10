import numpy as np


class GestureDetector:
    """
    Interprets raw hand landmarks into named gestures.
    Works with landmark data produced by HandTracker.
    """

    FINGER_TIPS = [4, 8, 12, 16, 20]

    # ─────────────────────────── Fingers ───────────────────────────

    def get_fingers_up(self, landmarks):
        """
        Returns [thumb, index, middle, ring, pinky]
        1 = raised, 0 = folded
        """
        if not landmarks:
            return []

        lm = landmarks
        fingers = []

        # Thumb — compare by X axis
        fingers.append(1 if lm[4][0] < lm[3][0] else 0)

        # Other fingers — compare by Y axis
        for tip_id in self.FINGER_TIPS[1:]:
            fingers.append(1 if lm[tip_id][1] < lm[tip_id - 2][1] else 0)

        return fingers

    # ─────────────────────────── Gestures ───────────────────────────

    def get_gesture(self, landmarks):
        """
        Returns gesture name:
        - 'draw'      index finger only
        - 'stop'      fist
        - 'clear'     open palm
        - 'mode_3d'   three fingers (index, middle, ring)
        - 'pinch'     thumb + index close together
        - 'next'      pinky only (cycle shape)
        - 'peace'     V gesture (index + middle)
        - 'ok'        OK gesture (thumb + index close, others up)
        - 'wave'      open hand moving
        - 'unknown'   anything else
        """
        if not landmarks:
            return 'unknown'

        fingers = self.get_fingers_up(landmarks)
        if not fingers:
            return 'unknown'

        total = sum(fingers)

        # Peace gesture (V) - index + middle only
        if fingers == [0, 1, 1, 0, 0]:
            return 'peace'

        # OK gesture - thumb + index close, others up
        if fingers == [1, 1, 1, 1, 1]:
            if self._pinch_distance(landmarks) < 50:
                return 'ok'

        if total == 0:
            return 'stop'

        if total == 5:
            return 'clear'

        if fingers == [0, 1, 0, 0, 0]:
            return 'draw'

        if fingers == [0, 1, 1, 1, 0]:
            return 'mode_3d'

        if fingers == [0, 0, 0, 0, 1]:
            return 'next'

        # Pinch check
        if self._pinch_distance(landmarks) < 40:
            return 'pinch'

        return 'unknown'

    # ─────────────────────────── Distances ───────────────────────────

    def _pinch_distance(self, landmarks):
        thumb = np.array(landmarks[4][:2])
        index = np.array(landmarks[8][:2])
        return float(np.linalg.norm(thumb - index))

    def get_pinch_distance(self, landmarks):
        """Public pinch distance (thumb ↔ index)"""
        if not landmarks:
            return None
        return self._pinch_distance(landmarks)

    def get_two_hand_distance(self, lm_left, lm_right):
        """Distance between index fingertips of two hands"""
        if not lm_left or not lm_right:
            return None
        p1 = np.array(lm_left[8][:2])
        p2 = np.array(lm_right[8][:2])
        return float(np.linalg.norm(p1 - p2))

    def get_index_tip(self, landmarks):
        """Returns (x, y) of index fingertip"""
        if not landmarks:
            return None
        return landmarks[8][:2]

    def is_hand_moving_fast(self, prev_pos, curr_pos, threshold=30):
        """Detect if hand is moving fast (for wave detection)"""
        if not prev_pos or not curr_pos:
            return False
        dist = np.linalg.norm(np.array(curr_pos) - np.array(prev_pos))
        return dist > threshold

    def detect_circular_motion(self, position_history):
        """Detect circular motion (minimum 4 points)"""
        if len(position_history) < 4:
            return False
        
        # Check if points form a rough circle
        # Simple approximation: check if hand returns near starting point
        dist_start_end = np.linalg.norm(
            np.array(position_history[-1]) - np.array(position_history[0])
        )
        return dist_start_end < 50  # Points close together = circle