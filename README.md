# 🛍️ Tam's Store Agent

An AI-powered conversational assistant built for **Tam's Store**, designed to answer customer queries about products, sizing, sustainability practices, and more.  
This project demonstrates an end-to-end implementation of an **LLM-powered business assistant** integrated with Gradio and deployed on Hugging Face Spaces.

### 🌐 Live Demo

🚀 **Live App:** [Try Tam’s Store Agent on Hugging Face Spaces](https://tamarafakih-tams-store-agent.hf.space/)  

---

---

## 📦 Repository Structure
Tam_Store_Agent/
│
├── data/
│ ├── tam_store.db
│
├── me/
│ ├── about_business.md # Markdown business overview
│ ├── about_business.pdf # Formal business description
│ └── business_summary.txt # Short summary for model grounding
│
├── app.py # Main Python app (Gradio interface)
├── Business_agent.ipynb # Notebook containing agent logic + experiments
├── requirements.txt # Required Python dependencies
├── .env.example # Sample environment variable file
├── .gitignore # Prevents sensitive files from being pushed
└── README.md # Documentation (this file)


---

## 💡 Project Overview

**Tam's Store Agent** is an AI-driven virtual assistant designed to improve customer interaction for a small retail business.  
It responds intelligently to user questions such as:
- "Do you offer petite sizes?"
- "Can you tell me about your sustainability practices?"
- "I'd like to book a fitting appointment."

It leverages **Gradio** for the chat interface and securely integrates an **API key** for model inference using environment variables.

---

## 🧰 Features

- 🧠 **LLM Integration:** Connects to an OpenAI-compatible API key stored in `.env`
- 💬 **Conversational Interface:** Smooth chat powered by Gradio
- 🗂️ **Structured Business Knowledge:** Pulls information from `.txt` and `.md` files
- ⚙️ **Modular Design:** Easily extendable to new business domains
- ☁️ **Deployed on Hugging Face Spaces** (bonus feature)

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/tams_store_agent.git
cd tams_store_agent
```
### 2️⃣ Create a Virtual Environment
```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows
# or
source .venv/bin/activate       # macOS/Linux
```

### 3️⃣ Install Requirements
```bash
pip install -r requirements.txt
```

### 4️⃣ Update the .env File
Update the .env file by replacing the placeholder with your actual API key.
```bash
OPENAI_API_KEY=your_api_key_here
```

### 4️⃣ Run the Application Locally
```bash
python app.py
```
After running, you should see something like:
```bash
Running on local URL: http://127.0.0.1:7860
```
Click the link to open the app in your browser and start chatting with Tam's Store Agent.


## 🌐 Live Demo (Hugging Face Spaces)

The project is deployed live on Hugging Face Spaces 🎉

👉 [Click here to try Tam's Store Agent](https://tamarafakih-tams-store-agent.hf.space/)

This public deployment runs directly on Hugging Face's infrastructure using Gradio and securely loads the API key from Hugging Face Secrets (so no .env file is exposed).  
You can interact with the assistant, test customer queries, and explore its responses live — no local setup needed.

## 🎥 Demo Video

🎬 [Watch Demo Video](https://your-demo-video-link-here)

This short demo showcases the chatbot's interaction flow, API integration, and deployed interface.

## 🧩 Tools Implemented

- **Business Information Tool** – Extracts data from about_business.md and business_summary.txt
- **Customer Query Tool** – Responds to user prompts about store products, sizing, and sustainability

## 🔐 Environment Management

| File | Purpose |
|------|---------|
| `.env` | Stores API key (not uploaded to GitHub) |
| `.env.example` | Template file for environment variables |
| `.gitignore` | Ensures sensitive files are excluded |

The app uses:

```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
```

## 🧾 Submission Checklist
✅ business_summary.txt

✅ about_business.pdf

✅ Business_agent.ipynb

✅ Two working tools implemented

✅ .env (not uploaded)

✅ Runs successfully

✅ Demo video included

✅ (Bonus) Deployed on Hugging Face Spaces

## 🧠 Technical Notes
- Developed in Python 3.11

- Frameworks: gradio, python-dotenv, openai (or equivalent)

- Tested in Visual Studio Code environment

- Compatible with Hugging Face "Gradio" SDK deployment

## 👩‍💻 Author
Tamara Fakih
- 🎓 American University of Beirut (AUB)
- 📧 tmf14@mail.aub.edu
- 💼 EECE503P – AI Starter Kit Project
- 💬 Passionate about applied AI, business automation, and conversational interfaces.

## ⭐ Acknowledgment
This project was completed as part of the EECE503P/AI Starter Kit course under the guidance of Prof. Ammar Mohanna.
Special thanks to the teaching team for their support and feedback during development.





