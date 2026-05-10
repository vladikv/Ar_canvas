import time
import cv2
import keyboard
import threading
from hand_tracker import HandTracker
from gesture_detector import GestureDetector
from modes.drawing_mode import DrawingMode
from modes.ar_mode import ARMode
from ui.toolbar import Toolbar
from voice_controller import VoiceController

# ─────────────────────────── Config ───────────────────────────

WIDTH, HEIGHT = 1280, 720
FPS           = 30
MODE_DRAW     = 'draw'
MODE_3D       = '3d'


def voice_listen_thread(voice):
    """Run voice listening in a separate thread"""
    text = voice.listen()
    if text:
        command = voice.parse_command(text)
        if command:
            print(f"✓ Command: {command[0]}")


def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, FPS)

    tracker  = HandTracker(max_hands=2)
    detector = GestureDetector()
    drawing  = DrawingMode(WIDTH, HEIGHT)
    ar       = ARMode(WIDTH, HEIGHT)
    toolbar  = Toolbar(WIDTH, HEIGHT)

    mode      = MODE_DRAW
    prev_time = time.time()
    prev_keys = set()  # Track pressed keys to avoid repeats
    
    # Voice control
    voice = VoiceController()
    voice_command = None
    position_history = []  # For gesture detection

    print("AR Canvas started!")
    print("Controls:")
    print("  M = Toggle draw/3D mode")
    print("  V = Start/Stop voice listening")
    print("  B = Next brush type")
    print("  C = Next color")
    print("  N = Next 3D shape")
    print("  P = Add shape (3D)")
    print("  D = Delete shape (3D)")
    print("  +/- = Adjust brush thickness")
    print("  S = Save drawing")
    print("  R = Clear canvas")
    print("  Q or ESC = Quit")
    print()
    print("Gestures:")
    print("  Peace ✌️ = Line ruler")
    print("  OK 👌 = Fill area")
    print("  Wave 👋 = Scroll menu")
    print()
    print("Press V to enable voice control 🎤")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)

        # ── Hand tracking ──
        all_landmarks = tracker.process(frame)

        lm0 = all_landmarks[0] if len(all_landmarks) > 0 else None
        lm1 = all_landmarks[1] if len(all_landmarks) > 1 else None

        gesture   = detector.get_gesture(lm0)
        index_tip = detector.get_index_tip(lm0)
        two_hand_dist = detector.get_two_hand_distance(lm0, lm1)

        # Track position for gesture detection
        if index_tip:
            position_history.append(index_tip)
            if len(position_history) > 20:
                position_history.pop(0)

        # Handle new gestures
        if gesture == 'peace':
            # V gesture - enable ruler
            cv2.putText(frame, "Ruler mode (V gesture)", (20, 100),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        
        if gesture == 'ok':
            # OK gesture - fill area
            cv2.putText(frame, "Fill mode (OK gesture)", (20, 100),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        # ── Mode switching via gesture ──
        if gesture == 'mode_3d':
            mode = MODE_3D
        elif gesture == 'stop' and mode == MODE_3D:
            mode = MODE_DRAW

        # ── Active mode update ──
        if mode == MODE_DRAW:
            drawing.update(gesture, index_tip)
            frame = drawing.render(frame)
        else:
            ar.update(gesture, index_tip, two_hand_dist)
            frame = drawing.render(frame)   # keep drawing visible underneath
            frame = ar.render(frame)

        # ── Hand skeleton ──
        tracker.draw(frame)

        # ── UI ──
        frame = toolbar.draw(frame, mode, drawing, ar)

        # ── FPS ──
        now  = time.time()
        fps  = 1.0 / max(now - prev_time, 1e-9)
        prev_time = now
        toolbar.draw_fps(frame, fps)

        cv2.imshow('AR Canvas', frame)

        # ── Keyboard (using keyboard library for reliability) ──
        current_keys = set()
        key_list = ['q', 'esc', 'm', 'b', 'c', 'n', 'v', 'p', 'd', 'x', '+', '=', '-', 's', 'r']
        
        for key in key_list:
            if keyboard.is_pressed(key):
                current_keys.add(key)
        
        # Only trigger on new key presses (not held down)
        new_keys = current_keys - prev_keys
        
        for key in new_keys:
            if key == 'q' or key == 'esc':
                print("Exiting...")
                raise KeyboardInterrupt()
            elif key == 'v':
                # Voice control toggle
                print("🎤 Слухаю голос...")
                threading.Thread(target=voice_listen_thread, args=(voice,), daemon=True).start()
            elif key == 'm':
                mode = MODE_3D if mode == MODE_DRAW else MODE_DRAW
                print(f"✓ Mode: {mode.upper()}")
            elif key == 'b':
                drawing.next_brush()
                print(f"✓ Brush: {drawing.brush_name}")
            elif key == 'c':
                drawing.next_color()
                print(f"✓ Color: {drawing.color_name}")
            elif key == 'n':
                ar.next_shape()
                if mode == MODE_DRAW:
                    mode = MODE_3D
                print(f"✓ Shape: {ar.shape_name.upper()}")
            elif key == 'p' and mode == MODE_3D:
                # Add new shape
                ar.add_shape('cube')
                print("✓ Додано новий куб")
            elif key == 'd' and mode == MODE_3D:
                # Delete active shape
                ar.remove_shape()
                print("✓ Видалено фігуру")
            elif key == 'x' and mode == MODE_3D:
                # Reset all shapes
                ar._reset()
                print("✓ Скинуто все")
            elif key in ('+', '='):
                drawing.increase_thickness()
                print(f"✓ Thickness: {drawing.thickness}")
            elif key == '-':
                drawing.decrease_thickness()
                print(f"✓ Thickness: {drawing.thickness}")
            elif key == 's':
                drawing.save('my_drawing.png')
                print("✓ Збережено!")
            elif key == 'r':
                drawing.clear()
                print("✓ Очищено!")
        
        prev_keys = current_keys
        cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()
    print("AR Canvas closed.")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass