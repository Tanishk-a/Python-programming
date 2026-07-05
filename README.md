# Python Programming Projects

A comprehensive collection of Python programs featuring chatbots, face recognition, ERP systems, student management tools, and various learning projects.

## 📂 Project Structure

```
python-programming/
├── Chatbot.py              # Main chatbot implementation
├── chatbacked.py           # Chatbot backend logic
├── chatbot.html            # Chatbot web interface
├── Final_faceregonitioncode.py   # Face recognition using OpenCV
├── app.py                  # Flask application
├── database.py             # Database management module
├── erpbackend.py          # ERP system backend
├── main.py                # Main application entry point
├── view.py                # View layer for MVC pattern
├── console.py             # Console utilities
├── StudentDetails.csv     # Student database
├── Employees_Report.xlsx  # Employee report
├── erp_project/           # Django ERP project
├── TrainingImage/         # Training images for face recognition
├── PYTHON BASICS TO ADVANCED/  # Learning materials
│   ├── studentreportcard.py
│   ├── erp_system.py
│   └── other basics
└── style.css, index.html  # Web interface files
```

## 🚀 Features

### Chatbot System
- Interactive chatbot with natural language processing
- Web interface for user interaction
- Backend logic for conversation management

### Face Recognition
- Real-time face detection and recognition using OpenCV
- Training with custom face datasets
- Integration with existing applications

### ERP System
- Complete Enterprise Resource Planning system
- Student and Employee management
- Report generation and data analysis

### Educational Projects
- From basics to advanced Python concepts
- Student report card generation
- Database management examples

## 🛠️ Technologies Used

- **Python 3.x** - Core language
- **OpenCV** - Computer vision and face recognition
- **Flask/Django** - Web framework
- **SQLite/SQL** - Database management
- **HTML/CSS** - Web interface
- **Pandas** - Data analysis and manipulation

## 📋 Requirements

```bash
pip install opencv-python
pip install flask
pip install django
pip install pandas
pip install numpy
```

## 🚀 Getting Started

### Clone the Repository
```bash
git clone https://github.com/Tanishk-a/Python-programming.git
cd Python-programming
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Chatbot
```bash
python Chatbot.py
# Or access via web interface
python app.py
# Open browser to http://localhost:5000
```

### Run Face Recognition
```bash
python Final_faceregonitioncode.py
```

### Run ERP System
```bash
cd erp_project
python manage.py runserver
```

## 📊 Project Components

### 1. Chatbot Module
- Natural language understanding
- Response generation
- User interaction logging

### 2. Face Recognition Module
- Real-time face detection
- Face encoding and comparison
- Attendance tracking capability

### 3. ERP System
- Student information management
- Employee records management
- Report generation
- Data analytics

### 4. Database
- CSV data storage
- Excel report generation
- SQL database integration

## 🎓 Learning Resources

The repository includes progressively advanced Python concepts:
- Variables and data types
- Functions and logic
- File handling and databases
- Web development
- Computer vision
- ERP concepts

## 📝 Usage Examples

### Using the Chatbot
```python
from Chatbot import ChatbotEngine
bot = ChatbotEngine()
response = bot.get_response("Hello")
print(response)
```

### Face Recognition
```python
import cv2
from Final_faceregonitioncode import FaceRecognizer
recognizer = FaceRecognizer()
recognizer.train()
recognizer.predict(image)
```

## 🤝 Contributing

Feel free to fork this repository and submit pull requests for any improvements.

## 📄 License

This project is open source and available for educational purposes.

## 👤 Author

**Tanishka Minghlani**
- GitHub: [@Tanishk-a](https://github.com/Tanishk-a)

## 📞 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

⭐ If you find this repository helpful, please give it a star!
