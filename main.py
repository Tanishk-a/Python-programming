import tkinter as tk
from tkinter import messagebox, font
import speech_recognition as sr 
import pyttsx3 
import google.genai as genai 
import threading
from datetime import datetime

# ============================================
# CONFIGURATION
# ============================================

GOOGLE_API_KEY = "AIzaSyC5AxDtzF6Mtks9-a_ohoktc0OibmOXhWY"

COLORS = {
    'bg_gradient_top': '#0f0c29',
    'primary': '#667eea',
    'primary_hover': '#764ba2',
    'accent': '#f093fb',
    'success': '#4facfe',
    'danger': '#fa709a',
    'warning': '#feca57',
    'text_light': '#ffffff',
    'card_bg': '#1f1f3a',
    'user_bubble': '#667eea',
    'assistant_bubble': '#4facfe',
    'input_bg': '#2a2a4e',
}

# ============================================
# VOICE ASSISTANT
# ============================================

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.tts_rate = 175
        self.tts_volume = 1.0
        self.selected_voice_id = None
        self.is_listening = False

        try:
            temp_engine = pyttsx3.init()
            self.voices = temp_engine.getProperty("voices")
            if self.voices:
                self.selected_voice_id = self.voices[0].id
            temp_engine.stop()
        except:
            self.voices = []

        self.client = genai.Client(api_key=GOOGLE_API_KEY)
        self.model, self.chat_session = self.create_chat_model(
            [
                "gemini-3-flash-preview",
            ],
            generation_config={
                "temperature": 0.7,
                "top_p": 0.9,
                "max_output_tokens": 300,
            }
        )

    def create_chat_model(self, model_names, generation_config=None):
        if generation_config is None:
            generation_config = {
                "temperature": 0.7,
                "top_p": 0.9,
                "max_output_tokens": 300,
            }

        for model_name in model_names:
            try:
                chat_session = self.client.chats.create(
                    model=model_name,
                    config=generation_config,
                    history=[]
                )
                print(f"Using model: {model_name}")
                return model_name, chat_session
            except Exception as e:
                print(f"Model not available: {model_name} -> {e}")

        self.model = None
        self.chat_session = None
        raise RuntimeError(
            "Unable to initialize a supported Google GenerativeModel. "
            "Please verify your API access and model availability."
        )

    def set_voice(self, voice_index):
        if 0 <= voice_index < len(self.voices):
            self.selected_voice_id = self.voices[voice_index].id

    def speak(self, text):
        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", self.tts_rate)
            engine.setProperty("volume", self.tts_volume)

            if self.selected_voice_id:
                engine.setProperty("voice", self.selected_voice_id)

            engine.say(text)
            engine.runAndWait()
            engine.stop()

        except Exception as e:
            print("TTS Error:", e)

    def listen(self):
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=10
                )
                return self.recognizer.recognize_google(audio)
        except:
            return None

    def get_response(self, user_message):
        try:
            response = self.chat_session.send_message(user_message)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"

# ============================================
# GUI APPLICATION
# ============================================

class ModernVoiceAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.assistant = VoiceAssistant()
        self.message_count = 0
        self.last_input_was_voice = False

        self.setup_window()
        self.setup_ui()

    def setup_window(self):
        self.root.title("NEXUS AI Assistant")
        self.root.geometry("1000x700")
        self.root.configure(bg=COLORS['bg_gradient_top'])

    def setup_ui(self):
        main_container = tk.Frame(self.root, bg=COLORS['bg_gradient_top'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        title_font = font.Font(family="Segoe UI", size=28, weight="bold")

        title = tk.Label(
            main_container,
            text="✨ NEXUS AI",
            font=title_font,
            bg=COLORS['card_bg'],
            fg=COLORS['text_light']
        )
        title.pack(fill=tk.X, pady=10)

        control_frame = tk.Frame(main_container, bg=COLORS['card_bg'])
        control_frame.pack(fill=tk.X, pady=10)

        self.voice_var = tk.StringVar()
        voice_options = [f"Voice {i+1}" for i in range(len(self.assistant.voices))]

        if voice_options:
            self.voice_var.set(voice_options[0])

        voice_menu = tk.OptionMenu(
            control_frame,
            self.voice_var,
            *voice_options,
            command=self.change_voice
        )
        voice_menu.pack(side=tk.LEFT, padx=10)

        export_btn = tk.Button(
            control_frame,
            text="💾 Export",
            command=self.export_chat,
            bg=COLORS['success']
        )
        export_btn.pack(side=tk.RIGHT, padx=5)

        clear_btn = tk.Button(
            control_frame,
            text="🗑️ Clear",
            command=self.clear_chat,
            bg=COLORS['danger']
        )
        clear_btn.pack(side=tk.RIGHT, padx=5)

        chat_container = tk.Frame(main_container, bg=COLORS['card_bg'])
        chat_container.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(chat_container, bg=COLORS['card_bg'], highlightthickness=0)

        scrollbar = tk.Scrollbar(chat_container, orient="vertical", command=self.canvas.yview)

        self.scrollable_frame = tk.Frame(self.canvas, bg=COLORS['card_bg'])

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        input_frame = tk.Frame(main_container, bg=COLORS['card_bg'])
        input_frame.pack(fill=tk.X, pady=10)

        self.text_entry = tk.Entry(
            input_frame,
            font=("Segoe UI", 12),
            bg=COLORS['input_bg'],
            fg="white",
            insertbackground="white"
        )

        self.text_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, ipady=10)
        self.text_entry.bind("<Return>", lambda e: self.send_text_message())

        send_btn = tk.Button(
            input_frame,
            text="📤 Send",
            command=self.send_text_message,
            bg=COLORS['primary']
        )
        send_btn.pack(side=tk.LEFT, padx=5)

        self.voice_btn = tk.Button(
            input_frame,
            text="🎤 Speak",
            command=self.start_voice_input,
            bg=COLORS['accent']
        )
        self.voice_btn.pack(side=tk.LEFT, padx=5)

        self.status_label = tk.Label(
            main_container,
            text="🟢 Ready to chat",
            bg=COLORS['card_bg'],
            fg=COLORS['success']
        )
        self.status_label.pack(fill=tk.X)

        self.add_message("assistant", "Hello! I'm NEXUS AI Assistant ✨")

    def add_message(self, sender, message):
        bubble_frame = tk.Frame(self.scrollable_frame, bg=COLORS['card_bg'])
        bubble_frame.pack(fill=tk.X, pady=8, padx=10)

        timestamp = datetime.now().strftime("%H:%M")

        if sender == "user":
            container = tk.Frame(bubble_frame, bg=COLORS['card_bg'])
            container.pack(anchor="e")

            tk.Label(
                container,
                text=timestamp,
                font=("Segoe UI", 8),
                bg=COLORS['card_bg'],
                fg=COLORS['text_light']
            ).pack(anchor="e")

            tk.Label(
                container,
                text=message,
                font=("Segoe UI", 11),
                bg=COLORS['user_bubble'],
                fg="white",
                wraplength=500,
                justify=tk.LEFT,
                padx=15,
                pady=10
            ).pack(anchor="e")

        else:
            container = tk.Frame(bubble_frame, bg=COLORS['card_bg'])
            container.pack(anchor="w")

            header = tk.Frame(container, bg=COLORS['card_bg'])
            header.pack(anchor="w")

            tk.Label(
                header,
                text=f"🤖 NEXUS • {timestamp}",
                font=("Segoe UI", 9, "bold"),
                bg=COLORS['card_bg'],
                fg=COLORS['accent']
            ).pack(side=tk.LEFT)

            speaker_btn = tk.Button(
                header,
                text="🔊",
                command=lambda msg=message: self.replay_audio(msg),
                bg=COLORS['card_bg'],
                fg=COLORS['accent'],
                relief=tk.FLAT
            )
            speaker_btn.pack(side=tk.LEFT, padx=10)

            tk.Label(
                container,
                text=message,
                font=("Segoe UI", 11),
                bg=COLORS['assistant_bubble'],
                fg="white",
                wraplength=500,
                justify=tk.LEFT,
                padx=15,
                pady=10
            ).pack(anchor="w")

        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def replay_audio(self, message):
        self.status_label.config(text="🔊 Playing audio...")
        threading.Thread(target=self.assistant.speak, args=(message,), daemon=True).start()

    def send_text_message(self):
        message = self.text_entry.get().strip()

        if not message:
            return

        self.text_entry.delete(0, tk.END)
        self.last_input_was_voice = False
        self.add_message("user", message)
        self.status_label.config(text="🔄 Processing...")

        threading.Thread(target=self.process_message, args=(message,), daemon=True).start()

    def start_voice_input(self):
        if self.assistant.is_listening:
            return

        self.assistant.is_listening = True
        self.voice_btn.config(text="🎤 Listening...")
        self.status_label.config(text="🎤 Listening...")

        threading.Thread(target=self.voice_input_thread, daemon=True).start()

    def voice_input_thread(self):
        text = self.assistant.listen()
        self.assistant.is_listening = False

        self.root.after(0, lambda: self.voice_btn.config(text="🎤 Speak"))

        if text:
            self.last_input_was_voice = True
            self.root.after(0, lambda: self.add_message("user", text))
            self.process_message(text)
        else:
            self.root.after(0, lambda: self.status_label.config(text="⚠️ Couldn't hear you"))

    def process_message(self, message):
        response = self.assistant.get_response(message)

        self.root.after(0, lambda: self.add_message("assistant", response))

        if self.last_input_was_voice:
            threading.Thread(target=self.assistant.speak, args=(response,), daemon=True).start()

        self.root.after(0, lambda: self.status_label.config(text="🟢 Ready to chat"))

    def change_voice(self, choice):
        index = int(choice.split()[-1]) - 1
        self.assistant.set_voice(index)

    def clear_chat(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.add_message("assistant", "Chat cleared! Ready for fresh conversation ✨")

    def export_chat(self):
        filename = f"nexus_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write("NEXUS AI Chat Export\n")

            messagebox.showinfo("Export", f"Chat exported as {filename}")

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernVoiceAssistantGUI(root)
    root.mainloop()