# ChatCBT 💖

This is a warm, supportive chatbot that acts like your best friend trained in Cognitive Behavioral Therapy (CBT) to help you work through negative thoughts one message at a time.

## Overview

Bestie uses structured CBT flows to help users process thoughts gently and effectively.

## How It’s Made

**Tech Stack:**

- **Frontend:** React, TailwindCSS, HTML, CSS, JavaScript
- **Backend:** FastAPI (Python)
- **Model:** HuggingFace Zephyr 7B Beta (via HuggingFace Inference API)
- **Deployment:** Frontend on Vercel, Backend on HuggingFace Spaces

The frontend was built with React and styled using TailwindCSS to create a soft, chat-style UI. Each message bubble is dynamically rendered with a typing animation and a clean delay effect to simulate real-time texting. I added logic to split long responses into smaller, friendlier bubbles and limited the number of questions per message.

The FastAPI backend handles user input, maintains short-term context (last 5 exchanges), and formats the prompt with a message tailored for warm friendly responses. All inference happens via HuggingFace’s hosted Zephyr-7B model.

## Project Structure

```bash
ChatCBT/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── .env
└── frontend/
    ├── src/
    ├── public/
    └── package.json

```

---

## To Run the App Locally:

### 1. Clone the repo

```bash
git clone <https://github.com/sRainapark/ChatCBT.git>
cd ChatCBT
```

### 2. Set up the backend and the frontend

in your terminal: 

```bash
cd backend
python3 -m venv venv
source venv/bin/activate         # for macOS/Linux
pip install -r requirements.txt
```

Create a `.env` file in `backend/` with this line:

```bash
HF_API_TOKEN=your_huggingface_api_key_here
```

The run the server:

```bash
uvicorn app:app --reload --port 8001
```

In a separate terminal window:

```bash
cd frontend
npm install
npm start
```

## Deployment Guide

**Backend on Hugging Face Spaces**

1. Go to https://huggingface.co/spaces.
2. Create a new Space → select `SDK: Docker`.
3. Push your backend folder contents to this space.
4. Include a `Dockerfile`, `app.py`, `requirements.txt`, `.env`.

**Frontend on Vercel**

1. Go to https://vercel.com/ and link your GitHub repo.
2. Set `build` command to `npm run build` and output dir to `build`.
3. Add `REACT_APP_API_URL=https://your-backend-url/chat` to Vercel’s environment variables.

💡 Tip: Use Hugging Face’s `/proxy/username/space-name` URL if CORS issues arise.

## Notes

- This project is still a work in progress with plenty of room for improvement—I'd really appreciate any feedback or suggestions you might have!
- This is NOT a replacement for professional therapy
