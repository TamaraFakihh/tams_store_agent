# ================================================================
# Tam’s Store Agent — Full Implementation (Gemini API Version)
# ================================================================

import os, time, json, sqlite3
from pathlib import Path
from dotenv import load_dotenv
from pypdf import PdfReader
import google.generativeai as genai
import gradio as gr

# ------------------------------------------------
# 1. Environment + Directories
# ------------------------------------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
genai.configure(api_key=GEMINI_API_KEY)

ROOT = Path(__file__).parent
ME_DIR = ROOT / "me"
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)
DB_PATH = DATA_DIR / "tam_store.db"

# ------------------------------------------------
# 2. Read Business Files
# ------------------------------------------------
def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""

def read_pdf(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        reader = PdfReader(path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception:
        return ""

BUSINESS_SUMMARY = read_text(ME_DIR / "business_summary.txt")
BUSINESS_PDF_TEXT = read_pdf(ME_DIR / "about_business.pdf")

# ------------------------------------------------
# 3. Database Initialization
# ------------------------------------------------
def init_db():
    """Create relational schema: leads (PK) -> feedback (FK)."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            message TEXT
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            lead_id INTEGER NOT NULL,
            timestamp INTEGER NOT NULL,
            question TEXT,
            PRIMARY KEY (lead_id, timestamp),
            FOREIGN KEY (lead_id) REFERENCES leads(id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        );
    """)
    conn.commit()
    conn.close()

# ------------------------------------------------
# 4. Tool Functions
# ------------------------------------------------
def record_customer_interest(email: str, name: str, message: str) -> str:
    """Insert or update a lead in the leads table."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    now = int(time.time())
    cur.execute("SELECT id FROM leads WHERE email = ?", (email.strip(),))
    existing = cur.fetchone()

    if existing:
        cur.execute(
            "UPDATE leads SET name=?, message=?, timestamp=? WHERE email=?",
            (name.strip(), message.strip(), now, email.strip()),
        )
        lead_id = existing[0]
        print(f"[DB] Updated existing lead {lead_id} — {name} <{email}>")
    else:
        cur.execute(
            "INSERT INTO leads (timestamp, name, email, message) VALUES (?, ?, ?, ?)",
            (now, name.strip(), email.strip(), message.strip()),
        )
        lead_id = cur.lastrowid
        print(f"[DB] New lead added {lead_id} — {name} <{email}>")

    conn.commit()
    conn.close()
    return f"Thanks, {name}! We’ve saved your interest — our style team will reach out soon 💌"

def record_feedback(email: str, question: str) -> str:
    """Insert feedback linked to an existing lead (creates placeholder if needed)."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT id FROM leads WHERE email = ?", (email.strip(),))
    lead = cur.fetchone()

    if not lead:
        cur.execute(
            "INSERT INTO leads (timestamp, name, email, message) VALUES (?, ?, ?, ?)",
            (int(time.time()), "Anonymous", email.strip(), "Auto-created from feedback"),
        )
        lead_id = cur.lastrowid
        print(f"[DB] Placeholder lead created for {email}")
    else:
        lead_id = lead[0]

    timestamp = int(time.time() * 1000)  # milliseconds precision
    cur.execute(
        "INSERT INTO feedback (lead_id, timestamp, question) VALUES (?, ?, ?)",
        (lead_id, timestamp, question.strip()),
    )
    conn.commit()
    conn.close()
    print(f"[DB] Feedback logged from lead {lead_id} ({email}) — {question[:60]}...")
    return "Thank you! We’ve saved your feedback for follow-up 👗"

# ------------------------------------------------
# 5. System Prompt
# ------------------------------------------------
SYSTEM_PROMPT = f"""
You are **Tam’s Store**, a contemporary fashion brand and clothing boutique.

Your goals:
- Speak with the friendly, polished tone of a boutique stylist.
- Use the official business info below to answer questions about products,
  sizing, sustainability, or policies.
- When a user shows shopping interest, politely ask for their **name** and **email**
  and then call `record_customer_interest`.
- When you can’t answer something, call `record_feedback`.
- Always remain professional, fashion-savvy, and concise.

# Business Summary
{BUSINESS_SUMMARY}

# Brand Profile
{BUSINESS_PDF_TEXT}
""".strip()

# ------------------------------------------------
# 6. Gemini Chat Logic
# ------------------------------------------------
model = genai.GenerativeModel("models/gemini-2.5-flash")


def generate_response(user_message, history):
    """
    Simulate Gemini 'function calling' invisibly.
    Detects when the assistant text includes or implies a tool call,
    executes it silently, and returns only the natural-language part.
    """
    full_context = SYSTEM_PROMPT + "\n\nConversation so far:\n"
    for u, a in history:
        full_context += f"User: {u}\nAssistant: {a}\n"
    full_context += f"User: {user_message}\nAssistant:"

    # Add safety message when user includes personal info (Gemini may block emails)
    if "@" in user_message:
        user_message += " (Note: this email is shared for business contact purposes only.)"

    try:
        # Generate Gemini response
        response = model.generate_content(full_context)

        # ✅ Safely extract text
        if response.candidates and response.candidates[0].content.parts:
            text = response.text.strip()
        else:
            print("⚠️ Empty Gemini response (finish_reason likely 12 — filtered or null).")
            return "💭 Sorry, I wasn’t able to generate a proper reply this time. Could you please rephrase that?"
    except Exception as e:
        print("❌ Gemini error:", e)
        return "⚠️ Something went wrong while processing your message."

    # ✅ --- Handle simulated customer interest logging
    if "record_customer_interest" in text:
        import re
        name = re.search(r"name=['\"]?([\w\s]+)['\"]?", text)
        email = re.search(r"email=['\"]?([\w@\.\-]+)['\"]?", text)
        msg = user_message
        if name and email:
            record_customer_interest(email.group(1), name.group(1), msg)
        # remove the raw tool call from reply
        text = re.sub(r"record_customer_interest.*", "", text).strip()
        return text + "\n\n💌 Thanks! Your interest has been saved."

    # ✅ --- Handle simulated feedback logging
    elif "record_feedback" in text or "feedback=" in text:
        record_feedback("anonymous@example.com", user_message)
        # remove the raw tool call from reply
        import re
        text = re.sub(r"record_feedback.*", "", text).strip()
        return text + "\n\n💖 Your feedback has been noted for follow-up."

    # ✅ --- Normal text (no tool detected)
    else:
        return text



# ------------------------------------------------
# 7. Gradio Chat Interface
# ------------------------------------------------
def respond(user_msg, history):
    try:
        reply = generate_response(user_msg, history)
    except Exception as e:
        reply = f"⚠️ Something went wrong: {e}"
    return reply

with gr.Blocks(title="Tam’s Store — Fashion Assistant") as demo:
    gr.Markdown("## 👗 Tam’s Store — Fashion Assistant\nWelcome to Tam’s boutique assistant! Ask anything about collections, sizing, or policies.")
    gr.ChatInterface(
        fn=respond,
        type="tuples",
        examples=[
            "Hi! I'm interested in your winter collection.",
            "Do you offer petite sizes?",
            "Can you tell me about your sustainability practices?",
            "My name is Lara, my email is lara@example.com — please contact me for a fitting.",
        ]
    )


if __name__ == "__main__":
    demo.launch()
