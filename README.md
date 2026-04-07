# Endpoint Security Monitor

A lightweight security monitoring agent that analyzes system logs in real-time and detects suspicious activities such as brute force attacks.

## Features
- Real-time log monitoring
- Failed login detection
- Brute force detection (rule-based)
- Modular architecture (collectors, detectors)

## Tech Stack
- Python (Agent)
- (Future) Spring Boot (Backend)
- (Future) React (Dashboard)

## DIT
uvicorn backend.main:app --reload
npm run dev