import tkinter as tk
from tkinter import scrolledtext, messagebox, font
import speech_recognition as sr 
import pyttsx3
import google.genai as genai     
import threading
from datetime import datetime

# ============================================
# CONFIGURATION
# ============================================

GOOGLE_API_KEY = "AIzaSyCs_A_V9j77NZjr9-iqdE7HIvqKSn_bF4"

# Modern Color Palette
COLORS = {
    'bg_gradient_top': '#0f0c29',
    'bg_gradient_mid': '#302b63',
    'bg_gradient_bot': '#24243e',
    'primary': '#667eea',
    'primary_hover': '#764ba2',
    'accent': '#f093fb',
    'success': '#4facfe',
    'danger': '#fa709a',
    'warning': '#feca57',
    'text_light': '#ffffff',
    'text_dark': '#1a1a2e',
    'card_bg': '#1f1f3a',
    'card_border': '#2d2d5f',
    'user_bubble': '#667eea',
    'assistant_bubble': '#4facfe',
    'input_bg': '#2a2a4e',
}

# ============================================
# VOICE ASSISTANT CLASS
# ============================================

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        # Don't keep a persistent TTS engine - create fresh each time
        self.tts_rate = 175
        self.tts_volume = 1.0
        self.selected_voice_id = None

        # Get available voices once
        temp_engine = pyttsx3.init()
        self.voices = temp_engine.getProperty('voices')
        if self.voices:
            self.selected_voice_id = self.voices[0].id
        temp_engine.stop()
        del temp_engine

        self.client = genai.Client(api_key=GOOGLE_API_KEY)
        self.model, self.chat_session = self.create_chat_model(
            [
                "gemini-3-flash-preview",
            ],
            generation_config={
                "temperature": 0.7,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 200,
            }
        )
        self.is_listening = False

    def create_chat_model(self, model_names, generation_config=None):
        if generation_config is None:
            generation_config = {
                "temperature": 0.7,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 200,
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

        raise RuntimeError(
            "Unable to initialize a supported Google GenerativeModel. "
            "Please verify your API access and model availability."
        )

    def set_voice(self, voice_index):
        if 0 <= voice_index < len(self.voices):
            self.selected_voice_id = self.voices[voice_index].id
    
    def speak(self, text):
        """Create fresh TTS engine each time to avoid Windows bug"""
        try:
            # Create fresh engine
            engine = pyttsx3.init()
            engine.setProperty('rate', self.tts_rate)
            engine.setProperty('volume', self.tts_volume)
            
            if self.selected_voice_id:
                engine.setProperty('voice', self.selected_voice_id)
            
            # Speak
            engine.say(text)
            engine.runAndWait()
            
            # Clean up
            engine.stop()
            del engine
            
        except Exception as e:
            print(f"TTS Error: {e}")
    
    def listen(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                text = self.recognizer.recognize_google(audio)
                return text
            except:
                return None
    
    def get_response(self, user_message):
        try:
            response = self.chat_session.send_message(user_message)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"

# ============================================
# MODERN GUI APPLICATION
# ============================================

class ModernVoiceAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.assistant = VoiceAssistant()
        self.message_count = 0
        self.is_dark_mode = True
        self.last_input_was_voice = False  # Track if last input was voice
        
        self.setup_window()
        self.setup_ui()
        
    def setup_window(self):
        self.root.title("NEXUS AI Assistant")
        self.root.geometry("1000x700")
        self.root.configure(bg=COLORS['bg_gradient_top'])
        self.root.minsize(800, 600)
        
        # Center window
        self.center_window()
        
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_gradient_frame(self, parent):
        """Create a frame with gradient-like effect"""
        frame = tk.Frame(parent, bg=COLORS['card_bg'], highlightthickness=0)
        return frame
        
    def setup_ui(self):
        # Main container with padding
        main_container = tk.Frame(self.root, bg=COLORS['bg_gradient_top'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # ===== HEADER WITH GRADIENT EFFECT =====
        header_frame = self.create_gradient_frame(main_container)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Title with modern font
        title_font = font.Font(family="Segoe UI", size=28, weight="bold")
        title_label = tk.Label(
            header_frame,
            text="✨ NEXUS AI",
            font=title_font,
            bg=COLORS['card_bg'],
            fg=COLORS['text_light']
        )
        title_label.pack(pady=20)
        
        subtitle = tk.Label(
            header_frame,
            text="Your Intelligent Voice Companion",
            font=("Segoe UI", 11),
            bg=COLORS['card_bg'],
            fg=COLORS['accent']
        )
        subtitle.pack(pady=(0, 15))
        
        # ===== CONTROL BAR =====
        control_frame = self.create_gradient_frame(main_container)
        control_frame.pack(fill=tk.X, pady=(0, 15), ipady=10)
        
        # Left controls
        left_controls = tk.Frame(control_frame, bg=COLORS['card_bg'])
        left_controls.pack(side=tk.LEFT, padx=15)
        
        tk.Label(
            left_controls,
            text="🎙️ Voice:",
            font=("Segoe UI", 10),
            bg=COLORS['card_bg'],
            fg=COLORS['text_light']
        ).pack(side=tk.LEFT, padx=5)
        
        self.voice_var = tk.StringVar()
        voice_options = [f"Voice {i+1}" for i in range(len(self.assistant.voices))]
        
        voice_menu = tk.OptionMenu(left_controls, self.voice_var, *voice_options, command=self.change_voice)
        voice_menu.config(
            bg=COLORS['primary'],
            fg=COLORS['text_light'],
            font=("Segoe UI", 9),
            activebackground=COLORS['primary_hover'],
            activeforeground=COLORS['text_light'],
            highlightthickness=0,
            bd=0,
            width=10
        )
        voice_menu.pack(side=tk.LEFT, padx=5)
        
        if voice_options:
            self.voice_var.set(voice_options[0])
        
        # Right controls
        right_controls = tk.Frame(control_frame, bg=COLORS['card_bg'])
        right_controls.pack(side=tk.RIGHT, padx=15)
        
        # Theme toggle
        self.theme_btn = self.create_modern_button(
            right_controls,
            "🌙 Dark",
            self.toggle_theme,
            COLORS['warning']
        )
        self.theme_btn.pack(side=tk.LEFT, padx=5)
        
        # Export button
        export_btn = self.create_modern_button(
            right_controls,
            "💾 Export",
            self.export_chat,
            COLORS['success']
        )
        export_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        clear_btn = self.create_modern_button(
            right_controls,
            "🗑️ Clear",
            self.clear_chat,
            COLORS['danger']
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # ===== CHAT AREA =====
        chat_container = self.create_gradient_frame(main_container)
        chat_container.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Custom scrollbar
        canvas = tk.Canvas(chat_container, bg=COLORS['card_bg'], highlightthickness=0)
        scrollbar = tk.Scrollbar(chat_container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg=COLORS['card_bg'])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=15)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10))
        
        self.canvas = canvas
        
        # Welcome message
        self.add_message("assistant", "Hello! I'm NEXUS, your AI voice assistant. Click the microphone or type to chat with me! ✨")
        
        # ===== INPUT AREA =====
        input_container = self.create_gradient_frame(main_container)
        input_container.pack(fill=tk.X, ipady=10)
        
        input_inner = tk.Frame(input_container, bg=COLORS['card_bg'])
        input_inner.pack(fill=tk.X, padx=15, pady=10)
        
        # Text input with modern styling
        self.text_entry = tk.Entry(
            input_inner,
            font=("Segoe UI", 12),
            bg=COLORS['input_bg'],
            fg=COLORS['text_light'],
            relief=tk.FLAT,
            insertbackground=COLORS['text_light']
        )
        self.text_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=12, padx=(0, 10))
        self.text_entry.bind("<Return>", lambda e: self.send_text_message())
        
        # Send button
        send_btn = self.create_modern_button(
            input_inner,
            "📤 Send",
            self.send_text_message,
            COLORS['primary'],
            width=10
        )
        send_btn.pack(side=tk.LEFT, padx=5)
        
        # Voice button with animation
        self.voice_btn = self.create_modern_button(
            input_inner,
            "🎤 Speak",
            self.start_voice_input,
            COLORS['accent'],
            width=10
        )
        self.voice_btn.pack(side=tk.LEFT, padx=5)
        
        # ===== STATUS BAR =====
        status_frame = tk.Frame(main_container, bg=COLORS['card_bg'], height=40)
        status_frame.pack(fill=tk.X)
        
        self.status_label = tk.Label(
            status_frame,
            text="🟢 Ready to chat",
            font=("Segoe UI", 10),
            bg=COLORS['card_bg'],
            fg=COLORS['success']
        )
        self.status_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        self.stats_label = tk.Label(
            status_frame,
            text="💬 Messages: 0",
            font=("Segoe UI", 10),
            bg=COLORS['card_bg'],
            fg=COLORS['accent']
        )
        self.stats_label.pack(side=tk.RIGHT, padx=20, pady=10)
        
    def create_modern_button(self, parent, text, command, color, width=None):
        """Create a modern styled button"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg=COLORS['text_light'],
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            activebackground=color,
            activeforeground=COLORS['text_light'],
            bd=0,
            padx=15,
            pady=8
        )
        
        if width:
            btn.config(width=width)
        
        # Hover effects
        def on_enter(e):
            btn.config(bg=self.lighten_color(color))
        
        def on_leave(e):
            btn.config(bg=color)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def lighten_color(self, color):
        """Lighten a hex color"""
        color = color.lstrip('#')
        r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        r = min(255, r + 30)
        g = min(255, g + 30)
        b = min(255, b + 30)
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def add_message(self, sender, message):
        """Add a modern chat bubble with speaker button"""
        bubble_frame = tk.Frame(self.scrollable_frame, bg=COLORS['card_bg'])
        bubble_frame.pack(fill=tk.X, pady=8, padx=10)
        
        timestamp = datetime.now().strftime("%H:%M")
        
        if sender == "user":
            # User message (right aligned)
            container = tk.Frame(bubble_frame, bg=COLORS['card_bg'])
            container.pack(anchor="e", padx=10)
            
            time_label = tk.Label(
                container,
                text=timestamp,
                font=("Segoe UI", 8),
                bg=COLORS['card_bg'],
                fg=COLORS['text_light'],
                justify=tk.RIGHT
            )
            time_label.pack(anchor="e")
            
            msg_bubble = tk.Frame(container, bg=COLORS['user_bubble'], bd=0)
            msg_bubble.pack(anchor="e", pady=2)
            
            msg_label = tk.Label(
                msg_bubble,
                text=message,
                font=("Segoe UI", 11),
                bg=COLORS['user_bubble'],
                fg=COLORS['text_light'],
                wraplength=500,
                justify=tk.LEFT,
                padx=15,
                pady=10
            )
            msg_label.pack()
            
        else:
            # Assistant message (left aligned) with speaker button
            container = tk.Frame(bubble_frame, bg=COLORS['card_bg'])
            container.pack(anchor="w", padx=10)
            
            header = tk.Frame(container, bg=COLORS['card_bg'])
            header.pack(anchor="w", fill=tk.X)
            
            tk.Label(
                header,
                text="🤖 NEXUS",
                font=("Segoe UI", 9, "bold"),
                bg=COLORS['card_bg'],
                fg=COLORS['accent']
            ).pack(side=tk.LEFT)
            
            tk.Label(
                header,
                text=f" • {timestamp}",
                font=("Segoe UI", 8),
                bg=COLORS['card_bg'],
                fg=COLORS['text_light']
            ).pack(side=tk.LEFT)
            
            # Speaker button to replay audio
            speaker_btn = tk.Button(
                header,
                text="🔊",
                font=("Segoe UI", 12),
                bg=COLORS['card_bg'],
                fg=COLORS['accent'],
                relief=tk.FLAT,
                cursor="hand2",
                bd=0,
                padx=8,
                command=lambda msg=message: self.replay_audio(msg)
            )
            speaker_btn.pack(side=tk.RIGHT)
            
            # Hover effect for speaker button
            def on_enter(e):
                speaker_btn.config(fg=COLORS['primary'])
            def on_leave(e):
                speaker_btn.config(fg=COLORS['accent'])
            
            speaker_btn.bind("<Enter>", on_enter)
            speaker_btn.bind("<Leave>", on_leave)
            
            msg_bubble = tk.Frame(container, bg=COLORS['assistant_bubble'], bd=0)
            msg_bubble.pack(anchor="w", pady=2)
            
            msg_label = tk.Label(
                msg_bubble,
                text=message,
                font=("Segoe UI", 11),
                bg=COLORS['assistant_bubble'],
                fg=COLORS['text_light'],
                wraplength=500,
                justify=tk.LEFT,
                padx=15,
                pady=10
            )
            msg_label.pack()
        
        # Auto scroll
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)
        
        # Update stats (only if label exists)
        self.message_count += 1
        if hasattr(self, 'stats_label'):
            self.stats_label.config(text=f"💬 Messages: {self.message_count}")
    
    def replay_audio(self, message):
        """Replay a message audio when speaker button clicked"""
        self.status_label.config(text="🔊 Playing audio...", fg=COLORS['accent'])
        threading.Thread(target=self.speak_message, args=(message,), daemon=True).start()
    
    def speak_message(self, message):
        """Speak a message and update status"""
        self.assistant.speak(message)
        self.root.after(0, lambda: self.status_label.config(
            text="🟢 Ready to chat",
            fg=COLORS['success']
        ))
    
    def send_text_message(self):
        message = self.text_entry.get().strip()
        if not message:
            return
        
        self.text_entry.delete(0, tk.END)
        self.add_message("user", message)
        self.status_label.config(text="🔄 Processing...", fg=COLORS['warning'])
        
        # Mark that this was a TEXT input (don't auto-speak)
        self.last_input_was_voice = False
        
        threading.Thread(target=self.process_message, args=(message,), daemon=True).start()
    
    def start_voice_input(self):
        if self.assistant.is_listening:
            return
        
        self.voice_btn.config(text="🎤 Listening...", state=tk.DISABLED, bg=COLORS['danger'])
        self.status_label.config(text="🎤 Listening...", fg=COLORS['danger'])
        
        threading.Thread(target=self.voice_input_thread, daemon=True).start()
    
    def voice_input_thread(self):
        self.assistant.is_listening = True
        text = self.assistant.listen()
        self.assistant.is_listening = False
        
        self.root.after(0, lambda: self.voice_btn.config(
            text="🎤 Speak",
            state=tk.NORMAL,
            bg=COLORS['accent']
        ))
        
        if text:
            # Mark that this was a VOICE input (auto-speak response)
            self.last_input_was_voice = True
            
            self.root.after(0, lambda: self.add_message("user", text))
            self.process_message(text)
        else:
            self.root.after(0, lambda: self.status_label.config(
                text="⚠️ Couldn't hear you",
                fg=COLORS['warning']
            ))
            self.root.after(2000, lambda: self.status_label.config(
                text="🟢 Ready to chat",
                fg=COLORS['success']
            ))
    
    def process_message(self, message):
        response = self.assistant.get_response(message)
        self.root.after(0, lambda: self.add_message("assistant", response))
        
        # Only auto-speak if the question was asked by VOICE
        if self.last_input_was_voice:
            # Show speaking status
            self.root.after(0, lambda: self.status_label.config(
                text="🔊 Speaking...",
                fg=COLORS['accent']
            ))
            
            # Speak in thread
            threading.Thread(target=self.speak_with_callback, args=(response,), daemon=True).start()
        else:
            # Text input - just show ready status (no auto-speak)
            self.root.after(0, lambda: self.status_label.config(
                text="🟢 Ready to chat",
                fg=COLORS['success']
            ))
    
    def speak_with_callback(self, text):
        """Speak and update status when done"""
        self.assistant.speak(text)
        self.root.after(0, lambda: self.status_label.config(
            text="🟢 Ready to chat",
            fg=COLORS['success']
        ))
    
    def change_voice(self, choice):
        voice_index = int(choice.split()[-1]) - 1
        self.assistant.set_voice(voice_index)
    
    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        if self.is_dark_mode:
            self.theme_btn.config(text="🌙 Dark")
        else:
            self.theme_btn.config(text="☀️ Light")
    
    def clear_chat(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.add_message("assistant", "Chat cleared! Ready for a fresh start! ✨")
        self.message_count = 0
    
    def export_chat(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"nexus_chat_{timestamp}.txt"
        
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("=== NEXUS AI CHAT EXPORT ===\n\n")
                for widget in self.scrollable_frame.winfo_children():
                    # Extract text from message bubbles
                    for child in widget.winfo_children():
                        for subchild in child.winfo_children():
                            if isinstance(subchild, tk.Label):
                                text = subchild.cget('text')
                                if text and text not in ["🤖 NEXUS"]:
                                    f.write(f"{text}\n")
                    f.write("\n")
            
            self.status_label.config(text=f"✓ Exported to {filename}", fg=COLORS['success'])
            messagebox.showinfo("Success", f"Chat exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

# ============================================
# RUN APPLICATION
# ============================================

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernVoiceAssistantGUI(root)
    root.main()
