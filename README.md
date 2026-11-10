
# AI Helmet and Cap Detection

## Project Description

AI Helmet and Cap Detection is a Python-based
web application developed using Streamlit and
Google Gemini API.

The application accepts short video uploads
and analyzes visible people to determine
whether they appear to wear:

- Safety helmets
- Ordinary caps
- No visible headwear
- Unclear / not visible

## Technologies Used

- Python
- Streamlit
- Google Gemini API
- Google AI Studio
- GitHub

## Project Structure

helmet-detection-ai/
|
|-- app.py
|-- requirements.txt
|-- README.md

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/helmet-detection-ai.git
```

Open the project directory:

```bash
cd helmet-detection-ai
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure your Gemini API key.

Windows PowerShell:

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

Linux / macOS:

```bash
export GEMINI_API_KEY="YOUR_API_KEY"
```

Run the application:

```bash
streamlit run app.py
```

## Features

- Video upload
- Video preview
- AI-powered visual analysis
- Helmet and cap classification
- Detection summary
- Streamlit user interface

## Limitations

AI results are estimates and can be incorrect.
This application is not a certified safety
inspection system.

## Developer

Developed with Python, Streamlit and Gemini AI.
