# 🕵️‍♂️ Spyfall Game

A web-based multiplayer party game inspired by the popular game **Spyfall**. Built with **Python (Flask)** and **Socket.IO** for real-time communication.

---

## 🎯 Game Concept

One of the players is secretly assigned the role of the **Spy**, while others know a shared **location**. The players must ask each other questions to determine who the spy is — meanwhile, the spy tries to figure out the location without getting caught.

---

## 💡 Features

- Real-time multiplayer gameplay via WebSockets (Flask-SocketIO)
- Clean UI with responsive layout (HTML/CSS/JS)
- Multiple views:
  - Lobby / Room
  - Game screen with timer
  - Rules page
  - Game over screen
- Timer and voting logic
- Location selection from predefined list
- Ready for deployment on **Render**

---

## 🧱 Tech Stack

- **Backend:** Flask + Flask-SocketIO  
- **Frontend:** HTML + CSS + JavaScript  
- **Deployment:** Gunicorn, Render  
- **Real-time Communication:** WebSockets (via SocketIO)

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/spyfall_game.git
cd spyfall_game
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the server locally

```bash
python server.py
```

Then open `http://localhost:5000` in your browser.

---

## 🌍 Deployment

The app is deployed on [Render](https://render.com/) and uses:

- `gunicorn` as WSGI server
- `requirements.txt` for dependency management
- `render.yaml` (if used) for configuration

Make sure your **DNS is properly configured** if you use a custom domain.

---

## 📁 Project Structure

```bash
spyfall-game/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── templates/
│   ├── index.html
│   ├── game.html
│   ├── room.html
│   ├── rules.html
│   └── game_over.html
├── server.py
├── locations.py
├── requirements.txt
└── README.md
```

---

## 📜 License

This project is provided as-is. For personal or educational use only.