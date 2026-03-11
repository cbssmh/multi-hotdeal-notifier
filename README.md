# Multi Hotdeal Notifier

A Python-based automation system that monitors multiple hot deal communities and sends notifications to Discord when new posts are detected.

This project is designed as a **multi-source monitoring system**, not just a simple crawler.  
It independently tracks several sites, stores post history in SQLite, and detects only newly posted deals without duplicates.

---

# Architecture

```
Hotdeal Sites
     │
     ▼
Crawler Modules
     │
     ▼
SQLite Database
     │
     ▼
Notification System
     │
     ▼
Discord Webhook
```

---

# Overview

The system periodically crawls multiple hot deal communities and compares the latest posts with previously stored records.

If a new post is detected, the system sends a notification through a **Discord Webhook** and stores the post in the database.

The service is designed to run continuously on a server using **Oracle Cloud VM and systemd**.

---

# Features

- Monitor multiple hot deal communities
- Extract latest posts from each site
- Store post history using SQLite
- Detect new posts by comparing with previous records
- Send notifications through Discord Webhooks
- Scheduled execution using APScheduler
- Environment variable configuration with `.env`
- Modular crawler architecture for easy site expansion
- Cloud deployment on Oracle Cloud VM
- Background service operation using systemd

---

# Supported Sites

Currently supported communities:

- FMKorea Hotdeal
- Ruliweb Hotdeal
- Eomisae Popular Deals
- PPOMPPU Hotdeal

---

# Tech Stack

## Backend

- Python

## Libraries

- requests
- BeautifulSoup4
- APScheduler
- python-dotenv

## Storage

- SQLite

---

# Project Structure

```
multi-hotdeal-notifier/
├── app.py
├── config.py
├── db.py
├── notifier.py
├── scheduler.py
├── run.py
├── requirements.txt
├── sites.json
├── .env.example
├── .gitignore
├── README.md
└── crawlers/
    ├── __init__.py
    ├── eomisae.py
    ├── fmkorea.py
    ├── ppomppu.py
    └── ruliweb.py
```

The project uses a **modular crawler architecture** where each site has its own crawler module.

---

# Setup

## 1. Create virtual environment

```
python -m venv venv
```

## 2. Activate virtual environment

### Windows

```
venv\Scripts\activate
```

### Mac / Linux

```
source venv/bin/activate
```

## 3. Install dependencies

```
pip install -r requirements.txt
```

---

# Environment Variables

Copy `.env.example` to `.env` and configure values.

```
cp .env.example .env
```

Example:

```
DISCORD_WEBHOOK_URL=your_discord_webhook_url
CHECK_INTERVAL_MINUTES=10
```

| Variable | Description |
|--------|-------------|
| DISCORD_WEBHOOK_URL | Discord webhook URL for notifications |
| CHECK_INTERVAL_MINUTES | Interval for checking new posts |

---

# Running the Project

## One-time check

```
python app.py
```

## Run scheduled monitoring

```
python run.py
```

Example output:

```
Scheduler started: checking every 10 minutes
[CHECK] Starting site monitoring
```

---

# System Workflow

```
sites.json
     │
     ▼
Crawler (per site)
     │
     ▼
Collect latest posts
     │
     ▼
Compare with SQLite database
     │
 ┌───┴──────────────┐
 │                  │
No new post     New post detected
 │                  │
 ▼                  ▼
Ignore          Send Discord Webhook
                     │
                     ▼
               Save to SQLite
```

---

# Design Considerations

Instead of attempting to detect identical products across communities,  
the system focuses on detecting **new posts per site**.

Different communities often present the same deal with different:

- titles
- discount descriptions
- emphasis points
- additional information

Therefore each site's new post is treated as an independent information source.

---

# Limitations

Some sites may return blocking responses depending on request frequency.

In particular, **FMKorea may occasionally block requests**, requiring additional stability improvements.

---

# Future Improvements

- Support for additional hot deal communities
- Keyword-based notification filtering
- Exclusion keyword support
- Rich Discord embed messages
- Docker-based deployment

---

# Author

cbssmh
