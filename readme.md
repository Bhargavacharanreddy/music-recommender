# Music Recommendation System

This is a simple **Music Recommendation System** project that recommends songs to users based on their previous interactions using collaborative filtering.

The project integrates with **Kafka** for real-time user feedback and provides a REST API using **FastAPI**. It also includes a simple machine learning model trained on user-song interactions to predict song recommendations.

---

## Features

1. **Recommend Songs**: Suggests songs to users based on their interaction history.
2. **User Feedback Handling**: Allows users to like songs and updates their profiles in real-time using Kafka.
3. **Machine Learning**: Uses collaborative filtering (SVD algorithm) to train the recommendation model.
4. **SQLite Database**: Tracks user profiles and their liked songs.
5. **FastAPI Backend**: REST API for making recommendations and handling user feedback.

---

## Architecture Overview

- **Data**: 
  - `songs.csv`: Song metadata (ID, title, artist, genre).
  - `interactions.csv`: Historical user-song interactions (user ID, song ID, like/dislike).

- **Kafka**: 
  - `song_likes` topic handles real-time feedback when a user likes a song.

- **SQLite**:
  - Tracks user-song interactions in the `user_profile` table.

- **Backend**:
  - Exposes REST endpoints for recommendations and user feedback.

---

## Prerequisites

1. **Docker Desktop** (for Kafka and Zookeeper setup)
2. **Python 3.9+** (virtual environment recommended)
3. **pip** or **pip3** installed
4. **Kafka Python Library** installed

---


music-recommender/
├── app.py                 # FastAPI backend
├── db.py                  # SQLite database setup and helpers
├── kafka_consumer.py      # Kafka consumer to update the user profile in real-time
├── train_model.py         # Script to train the recommendation model
├── docker-compose.yml     # Kafka and Zookeeper setup
├── songs.csv              # Song metadata
├── interactions.csv       # User interactions dataset
├── recommendation_model.pkl # Trained collaborative filtering model
├── music_app.db           # SQLite database file (auto-created)
├── venv/                  # Python virtual environment (not pushed to GitHub)
└── README.md              # Documentation

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/music-recommender.git
cd music-recommender
