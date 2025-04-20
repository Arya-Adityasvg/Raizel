# Raizel - AI-Powered Student Assistant

Raizel is an intelligent student assistant that helps students manage their academic information, access course details, and get instant answers to their questions using Google's Generative AI.

## Features

- 🤖 AI-powered chat interface using Google's Gemini Pro model
- 🎤 Voice input support for natural interaction
- 📊 Academic data visualization and management
- 📅 Academic calendar integration
- 📝 Course and subject-wise marks tracking
- 🔍 Intelligent search across academic records
- 📱 Responsive web interface
- 🔒 Secure student authentication

## Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **AI Integration**: Google Generative AI (Gemini Pro)
- **Database**: CSV files for data storage
- **Voice Processing**: Speech Recognition, Text-to-Speech
- **Real-time Communication**: Socket.IO

## Prerequisites

- Python 3.8 or higher
- Google API key for Gemini Pro
- Required Python packages (listed in requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/raizel.git
cd raizel
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Add your Google API key to `.env`

4. Run the application:
```bash
python app.py
```

## Project Structure

```
raizel/
├── app.py                 # Main Flask application
├── google_ai_integration.py  # Google AI integration
├── voice_chatbot.py      # Voice processing module
├── static/               # Static files
│   ├── css/
│   │   └── style.css    # Main stylesheet
│   └── js/
│       └── main.js      # Frontend JavaScript
├── templates/            # HTML templates
│   └── index.html       # Main application template
├── data/                # CSV data files
│   ├── Students_Academic_Records.csv
│   ├── Academic_Calendar.csv
│   ├── SubjectWise_Marks.csv
│   └── Student_Course_Details.csv
├── requirements.txt     # Python dependencies
└── .env                # Environment variables
```

## Usage

1. Start the application:
```bash
python app.py
```

2. Access the web interface at `http://localhost:3000`

3. Login with your student credentials:
   - Registration numbers: REG2023001 to REG2023005

4. Use the chat interface to:
   - Ask questions about your academic records
   - Get course information
   - Check upcoming events
   - Access subject-wise marks

## API Key Setup

1. Get your Google API key:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy the key to your `.env` file

2. Test the API key:
```bash
python test_google_ai.py
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Google Generative AI for providing the AI capabilities
- Flask framework for the web application
- All contributors who have helped shape this project

## Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter)
Project Link: [https://github.com/yourusername/raizel](https://github.com/yourusername/raizel) 