import speech_recognition as sr
import threading
import pyttsx3


class VoiceController:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000  # Регулировка чувствительности
        
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        
        self.last_command = None
        self.listening = False
        self.running = True

    def speak(self, text):
        """Говорит текст"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except:
            pass

    def listen(self):
        """Слушает голос и возвращает команду"""
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.1)
                print("🎤 Слухаю...")
                audio = self.recognizer.listen(source, timeout=5)
            
            text = self.recognizer.recognize_google(audio, language='uk-UA')
            print(f"Вы сказали: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("❌ Не розібрав речення")
            return None
        except sr.RequestError:
            print("❌ Помилка мікрофону")
            return None
        except Exception as e:
            print(f"❌ Помилка: {e}")
            return None

    def parse_command(self, text):
        """Парсит речь и возвращает команду"""
        if not text:
            return None

        # Команди малювання
        if any(word in text for word in ['очисти', 'clear', 'стерти']):
            return ('clear_canvas', {})
        
        if any(word in text for word in ['зберегти', 'save', 'save drawing']):
            return ('save_drawing', {})
        
        if any(word in text for word in ['наступний колір', 'next color', 'червоний', 'red']):
            return ('next_color', {})
        
        if any(word in text for word in ['синій', 'blue', 'зелений', 'green']):
            color = 'red' if 'червоний' in text else ('blue' if 'синій' in text else 'green')
            return ('set_color', {'color': color})

        if any(word in text for word in ['збільшити', 'increase', 'більше', 'bigger']):
            return ('increase_thickness', {})
        
        if any(word in text for word in ['зменшити', 'decrease', 'менше', 'smaller']):
            return ('decrease_thickness', {})

        # Команди 3D
        if any(word in text for word in ['куб', 'cube', 'додай куб', 'add cube']):
            return ('add_cube', {})
        
        if any(word in text for word in ['сфера', 'sphere', 'куля', 'ball']):
            return ('add_sphere', {})
        
        if any(word in text for word in ['піраміда', 'pyramid']):
            return ('add_pyramid', {})

        if any(word in text for word in ['наступна', 'next shape', 'change shape']):
            return ('next_shape', {})
        
        if any(word in text for word in ['видалити', 'delete', 'remove']):
            return ('delete_object', {})
        
        if any(word in text for word in ['скинути', 'reset', 'reset all']):
            return ('reset_all', {})

        # Переходы между режимами
        if any(word in text for word in ['три д', '3d', 'mode 3d', '3d режим']):
            return ('switch_mode', {'mode': '3d'})
        
        if any(word in text for word in ['малювання', 'draw', 'draw mode', 'режим рисования']):
            return ('switch_mode', {'mode': 'draw'})

        # Система
        if any(word in text for word in ['скасувати', 'undo']):
            return ('undo', {})
        
        if any(word in text for word in ['повторити', 'redo']):
            return ('redo', {})
        
        if any(word in text for word in ['допомога', 'help', 'commands']):
            return ('show_help', {})

        return None

    def execute_command(self, command_tuple):
        """Возвращает обработанную команду для main.py"""
        if not command_tuple:
            return None
        return command_tuple
