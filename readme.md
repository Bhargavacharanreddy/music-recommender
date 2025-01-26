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




---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/music-recommender.git
cd music-recommender
```


### 2. Set Up the Virtual Environment
Set up a Python virtual environment to isolate project dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Start Kafka and Zookeeper
This project uses Kafka and Zookeeper, which are started using Docker Compose:

Ensure Docker Desktop is running.
Start Kafka and Zookeeper with:
```bash
docker compose up -d
```

Verify that Kafka and Zookeeper are running:
```bash

docker compose ps
```

### 4. Train the Model
Train the recommendation model on the historical interaction dataset:
```bash
python train_model.py
```
This will create a file named recommendation_model.pkl, which stores the trained collaborative filtering model.

### 5. Start the Kafka Consumer
The Kafka consumer listens to user feedback events and updates the user profile in the SQLite database:

Open a new terminal window or tab.
Activate the virtual environment:
```bash
source venv/bin/activate
```

Run the consumer:
```bash
python kafka_consumer.py
```
You should see a message indicating the consumer is listening to the song_likes topic.

### 6. Run the FastAPI Backend
The FastAPI backend provides REST endpoints for recommendations and user feedback:

Open another terminal window or tab.
Activate the virtual environment:
```bash
source venv/bin/activate
```

Start the FastAPI server:
```bash
python app.py
```
The server will be available at: http://localhost:8000

### 7. Test the Endpoints
You can test the functionality using curl, Postman, or any other REST client.

Recommend a Song
Retrieve a song recommendation for a user:

```bash
curl http://localhost:8000/recommend/101
```

Example Response:
```
{
  "recommended_song_id": 3,
  "predicted_like_score": 0.87,
  "song_info": {
    "song_id": 3,
    "title": "Song C",
    "artist": "Artist X",
    "genre": "Rock"
  }
}
```

Like a Song
Send feedback indicating that a user likes a song:

```
curl -X POST -H "Content-Type: application/json" \
-d '{"user_id": 101, "song_id": 3}' \
http://localhost:8000/like
```

Example Response:
```

{
  "status": "ok",
  "message": "Like event published for user 101, song 3"
}
```

### Project Structure
```bash
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
```

# Future Improvements
## Incremental Model Updates:

### Use a machine learning algorithm capable of incremental learning (e.g., real-time updates based on user feedback).
### Additional Features:

### Incorporate more user and song metadata (e.g., user demographics, song embeddings, or artist popularity) to improve recommendations.
### Scalable Storage:

### Migrate the SQLite database to Amazon DynamoDB or Amazon RDS for better scalability.
### Cloud Integration:

### Deploy the model on Amazon SageMaker and use Amazon MSK (Managed Kafka) for better reliability and performance.
### Model Retraining Pipelines:

### Automate model retraining with tools like Apache Airflow or AWS Step Functions.


# License
This project is open-source and available under the MIT License.