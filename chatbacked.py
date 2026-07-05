import flask 
import flask_cors
import google.genai as genai 
import pyttsx3
import threading

# ============================================
# CONFIGURATION
# ============================================

GOOGLE_API_KEY = "AIzaSyC5AxDtzF6Mtks9-a_ohoktc0OibmOXhWY"

# Flask App
app = flask.Flask(__name__)
flask_cors.CORS(app)

# ============================================
# VOICE ASSISTANT CLASS
# ============================================

class VoiceAssistant:
    def __init__(self):
        self.tts_rate = 175
        self.tts_volume = 1.0
        self.selected_voice_id = None

        try:
            temp_engine = pyttsx3.init()
            self.voices = temp_engine.getProperty('voices')

            if self.voices:
                self.selected_voice_id = self.voices[0].id

            temp_engine.stop()

        except Exception:
            self.voices = []

        self.client = genai.Client(api_key=GOOGLE_API_KEY)
        self.model, self.chat_session = self.create_chat_model(
            [
                "gemini-3-flash-preview",
            ],
            generation_config={
                "temperature": 0.7,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 300,
            }
        )

    def create_chat_model(self, model_names, generation_config):
        last_error = None
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
                last_error = e
                print(f"Model not available: {model_name} -> {e}")

        raise RuntimeError(
            "Unable to initialize a supported Google GenerativeModel. "
            "Please verify your API access and model availability."
        )

    def speak(self, text):
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', self.tts_rate)
            engine.setProperty('volume', self.tts_volume)

            if self.selected_voice_id:
                engine.setProperty('voice', self.selected_voice_id)

            engine.say(text)
            engine.runAndWait()
            engine.stop()

        except Exception as e:
            print("TTS Error:", e)

    def get_response(self, user_message):
        try:
            response = self.chat_session.send_message(user_message)
            return response.text

        except Exception as e:
            return f"Error: {str(e)}"


# Global assistant instance
assistant = VoiceAssistant()

# ============================================
# ROUTES
# ============================================

@app.route('/')
def home():
    return """
    <h1>🤖 Chatbot Backend Running</h1>
    <p>Status: <span style='color:green;'>ONLINE</span></p>
    <p>API Endpoint: <code>http://localhost:5000/api/chat</code></p>
    """

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = flask.request.get_json()

        if not data:
            return flask.jsonify({
                "success": False,
                "error": "No JSON data received"
            }), 400

        user_message = data.get("message", "").strip()

        if not user_message:
            return flask.jsonify({
                "success": False,
                "error": "No message provided"
            }), 400

        bot_reply = assistant.get_response(user_message)

        return flask.jsonify({
            "success": True,
            "reply": bot_reply
        })

    except Exception as e:
        return flask.jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/speak', methods=['POST'])
def speak():
    try:
        data = flask.request.get_json()

        if not data:
            return flask.jsonify({
                "success": False,
                "error": "No JSON data received"
            }), 400

        text = data.get("text", "").strip()

        if not text:
            return flask.jsonify({
                "success": False,
                "error": "No text provided"
            }), 400

        thread = threading.Thread(
            target=assistant.speak,
            args=(text,),
            daemon=True
        )
        thread.start()

        return flask.jsonify({
            "success": True,
            "message": "Speaking started"
        })

    except Exception as e:
        return flask.jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    return flask.jsonify({
        "status": "online",
        "message": "Chatbot backend is running!"
    })


# ============================================
# RUN SERVER
# ============================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🚀 CHATBOT BACKEND SERVER STARTING...")
    print("=" * 60)
    print("✓ Server URL: http://localhost:5000")
    print("✓ Chat API: http://localhost:5000/api/chat")
    print("✓ Speak API: http://localhost:5000/api/speak")
    print("✓ Health API: http://localhost:5000/api/health")
    print("✓ Press Ctrl+C to stop")
    print("=" * 60 + "\n")

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )