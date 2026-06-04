# HireGenie AI 🧞‍♂️✨

HireGenie AI is an intelligent, automated recruitment platform built to streamline the hiring process. By leveraging the power of Google's Gemini AI, HireGenie automatically parses bulk resume uploads, extracts structured candidate profiles, and algorithmically matches them against your custom job descriptions.

Say goodbye to manual resume screening and let AI build your dream team.

## ✨ Features

- **Multi-Tenant Architecture**: Robust data isolation ensures that recruiters only have access to the jobs and candidates they create.
- **AI-Powered Resume Parsing**: Upload PDFs in bulk. The system automatically extracts text and uses LLMs to structure candidate skills, experience, and contact info.
- **Intelligent Matching Algorithm**: Candidates are automatically scored and matched against active Job Descriptions to find the perfect fit.
- **Modern Glassmorphism UI**: A stunning, premium dark-mode interface built with Bootstrap 5, featuring fluid animations, mesh gradients, and interactive charts.
- **Advanced Security**: Strict email deliverability validation blocks disposable and temporary email addresses during registration to prevent spam accounts.
- **Interactive Dashboard**: Real-time analytics on candidate volume, average match scores, and pending reviews.

## 🛠️ Tech Stack

- **Backend**: Python, Flask, SQLAlchemy (SQLite/PostgreSQL ready)
- **Frontend**: HTML5, Vanilla CSS (Custom Glassmorphism), Bootstrap 5, Jinja2 Templates
- **AI Integration**: Google Gemini API (`google-generativeai`)
- **PDF Processing**: `PyPDF2`
- **Security**: `flask-login`, `Werkzeug`, `email-validator`, `disposable-email-domains`

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- A [Google Gemini API Key](https://aistudio.google.com/)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Mohit8103/hiregenie-ai.git
   cd hiregenie-ai
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   Copy the example environment file and add your credentials:
   ```bash
   cp .env.example .env
   ```
   Open `.env` and fill in your `SECRET_KEY` and `GEMINI_API_KEY`.

5. **Run the Application**
   ```bash
   python run.py
   ```
   The database will automatically initialize on the first run. Access the platform at `http://127.0.0.1:5000/`.

## 🔒 Security Note
This platform incorporates deep email validation utilizing DNS Mail Exchange (MX) lookups and throwaway domain blacklists. When testing registration locally, ensure you are using a valid, non-disposable email address domain or the system will reject the account creation.

## 📄 License
This project is proprietary and confidential. All rights reserved.
