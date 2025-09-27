AI-Powered Job Recommender System
## Overview

An intelligent job recommender system leveraging Large Language Models (LLMs) to analyze resumes, identify skill gaps, suggest career roadmaps, and fetch tailored job openings from multiple online portals.

![Screenshot](screenshot.png)  
*A screenshot of the application's main interface, showing resume analysis and job results.*

---

## 📄 Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Tech Stack & Architecture](#tech-stack--architecture)
- [Technology Used](#technology-used)
- [System Architecture](#system-architecture)
- [Setup and Installation](#setup-and-installation)
    - [Prerequisites](#prerequisites)
    - [Backend Setup](#backend-setup)
    - [Frontend Setup](#frontend-setup)
    - [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Environment Variables](#environment-variables)
- [Project Structure](#project-structure)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## 🌟 Introduction

This project transforms the job search process into a streamlined, personalized experience. By uploading a PDF resume, users receive an AI-powered analysis including a professional summary, identified skill gaps, and a strategic career roadmap. The system automatically queries multiple job portals (Indeed, Google Jobs, Glassdoor, Naukri) and presents relevant opportunities in a modern web interface.

Originally built with Streamlit, the application now features a scalable, decoupled architecture with a Python/FastAPI backend and a vanilla HTML, CSS, and JavaScript frontend.

---

## ✨ Features

- **📄 PDF Resume Upload:** Simple, intuitive interface for uploading resumes in PDF format.
- **🤖 AI-Powered Analysis:** Utilizes the Groq LLM API for high-speed text analysis to:
    - Generate a concise, professional summary.
    - Identify critical skill gaps and missing qualifications.
    - Create a personalized career development roadmap.
- **🔍 Multi-Source Job Scraping:** Fetches job listings concurrently from multiple platforms using Apify actors:
    - Indeed
    - Google Jobs
    - Glassdoor
    - Naukri (India)
- **✨ Modern & Responsive UI:** Clean, user-friendly interface built with Bootstrap 5, compatible with all devices.
- **🔗 Decoupled Architecture:** Independent frontend and backend for maintainability, scalability, and deployment flexibility.

---

## 🛠️ Tech Stack & Architecture

### Technology Used

**Backend:**
- Python: Core programming language
- FastAPI: High-performance ASGI framework for APIs
- Groq: LLM provider for fast, free AI-powered text generation
- Apify Client: Interacts with web scraping actors
- PyMuPDF (fitz): Efficient PDF text extraction
- Uvicorn: ASGI server for FastAPI

**Frontend:**
- HTML5: Markup language
- CSS3: Custom styling
- Bootstrap 5: Responsive design and UI components
- JavaScript (ES6): API calls, DOM manipulation, interactivity
- marked.js: Parses Markdown responses from LLM into styled HTML

---

## 🏗️ System Architecture

The application follows a client-server model. The frontend is a static web app communicating with the backend via REST API. The backend handles PDF processing, Groq LLM interaction, and Apify web scrapers orchestration.

```mermaid
graph TD
        A[User's Browser (Frontend)] -->|1. Uploads PDF| B(FastAPI Backend)
        B -->|2. Sends Resume Text| C{Groq LLM API}
        C -->|3. Returns Analysis (Summary, Gaps, Roadmap)| B
        A -->|4. Clicks 'Find Jobs' with Keywords| B
        B -->|5. Sends Keywords to Scrapers| D(Apify Cloud)
        subgraph D [Apify Cloud]
                D1[Indeed Actor]
                D2[Google Jobs Actor]
                D3[Glassdoor Actor]
                D4[Naukri Actor]
        end
        D -->|6. Returns Job Listings| B
        B -->|7. Sends Final JSON Response to Client| A
```

---

## 🚀 Setup and Installation

Follow these steps to run the project locally.

### Prerequisites

- Python 3.10+
- pip (package manager)
- Apify Account (API Token)
- Groq Account (API Key)

### Backend Setup

1. **Clone the repository:**
     ```bash
     git clone https://github.com/encoder43/AI_based_Job_Recommender_System.git
     cd AI_based_Job_Recommender_System
     ```

2. **Navigate to backend directory:**
     ```bash
     cd backend
     ```

3. **Create and activate a virtual environment:**
     - *Windows:*
         ```bash
         python -m venv venv
         .\venv\Scripts\activate
         ```
     - *macOS/Linux:*
         ```bash
         python3 -m venv venv
         source venv/bin/activate
         ```

4. **Install dependencies:**
     ```bash
     pip install -r requirements.txt
     ```

5. **Create `.env` file in `backend/` directory:**
     ```
     GROQ_API_KEY="your_groq_api_key_here"
     APIFY_API_TOKEN="your_apify_api_token_here"
     ```

### Frontend Setup

The frontend is a static site. Use a simple HTTP server to run it.

---

## ▶️ Running the Application

**Start Backend Server:**
```bash
uvicorn main:app --reload
```
Backend API: [http://127.0.0.1:8000](http://127.0.0.1:8000)

**Start Frontend Server:**
```bash
cd ../frontend
python -m http.server 8001
```
Frontend: [http://127.0.0.1:8001](http://127.0.0.1:8001)

---

## 📡 API Endpoints

| Endpoint            | Method | Body (JSON)                | Description                                                                 |
|---------------------|--------|----------------------------|-----------------------------------------------------------------------------|
| `/`                 | GET    | -                          | Health check endpoint                                                        |
| `/analyze-resume/`  | POST   | multipart/form-data (file) | Accepts PDF, returns summary, skill gaps, roadmap, suggested keywords        |
| `/fetch-jobs/`      | POST   | `{ "keywords": "..." }`    | Accepts keywords, returns job listings from all configured scraper services  |

---

## 🔑 Environment Variables

Add these to your `.env` file in the backend directory:

| Variable         | Description                        | Example                        |
|------------------|------------------------------------|--------------------------------|
| GROQ_API_KEY     | API key from Groq Console          | gsk_xxxxxxxxxxxxxxxxxxxxxxxx   |
| APIFY_API_TOKEN  | API token from Apify Console       | apify_api_xxxxxxxxxxxxxxxxxxxx |

---

## 📂 Project Structure

```
AI_based_Job_Recommender_System/
├── backend/
│   ├── src/
│   │   ├── __init__.py
│   │   ├── helper.py        # PDF extraction & Groq LLM calls
│   │   └── job_api.py       # Apify actor (scraper) logic
│   ├── main.py              # FastAPI server and API endpoints
│   ├── requirements.txt
│   └── .env                 # API keys (not in git)
└── frontend/
        ├── css/
        │   └── style.css        # Custom styles
        ├── js/
        │   └── main.js          # Client-side logic, API calls
        └── index.html           # Main page structure
```

---

## 📈 Future Improvements

- **User Authentication:** Save resume analysis history and favorite jobs.
- **Database Integration:** Store results in a database (PostgreSQL, MongoDB).
- **More Job Sources:** Integrate additional job platforms.
- **Advanced Filtering:** UI controls for location, salary, company, etc.
- **Containerization:** Dockerize frontend and backend for deployment.

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/AmazingFeature`).
3. Make changes and commit (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📜 License

Distributed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 📫 Contact

- **encoder43** - [GitHub Profile](https://github.com/encoder43)
- **Project Link:** [AI_based_Job_Recommender_System](https://github.com/encoder43/AI_based_Job_Recommender_System)

