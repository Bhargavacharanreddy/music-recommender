import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd
import os
import json
from kafka import KafkaProducer

# Load songs metadata
songs_df = pd.read_csv("songs.csv")

# Load model
with open("recommendation_model.pkl", "rb") as f:
    model = pickle.load(f)

# Kafka producer
BROKER_URL = os.getenv("KAFKA_BROKER_URL", "localhost:9092")
producer = KafkaProducer(
    bootstrap_servers=[BROKER_URL],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

app = FastAPI()

class LikeRequest(BaseModel):
    user_id: int
    song_id: int

@app.get("/recommend/{user_id}")
def recommend_song(user_id: int):
    """
    For demo: 
    - We read from interactions.csv to see which songs the user already liked.
    - Then we ask the model for a predicted 'like' score for songs the user hasn't liked yet.
    """
    import pandas as pd
    interactions = pd.read_csv("interactions.csv")
    user_liked_songs = interactions.loc[
        (interactions['user_id'] == user_id) & (interactions['like'] == 1),
        'song_id'
    ]
    user_songs = set(user_liked_songs)

    predictions = []
    for song_id in songs_df['song_id']:
        if song_id not in user_songs:
            est_rating = model.predict(uid=user_id, iid=song_id).est
            predictions.append((song_id, est_rating))

    predictions.sort(key=lambda x: x[1], reverse=True)

    if predictions:
        best_song_id, best_score = predictions[0]
        song_info = songs_df[songs_df['song_id'] == best_song_id].to_dict('records')[0]
        return {
            "recommended_song_id": best_song_id,
            "predicted_like_score": best_score,
            "song_info": song_info
        }
    else:
        return {"message": "No recommendation available."}

@app.post("/like")
def user_likes_song(req: LikeRequest):
    """
    Publish "like" event to Kafka. 
    The Kafka consumer will pick it up and update user_profile in the local DB.
    """
    event_data = {"user_id": req.user_id, "song_id": req.song_id}
    producer.send("song_likes", event_data)
    producer.flush()
    return {
        "status": "ok",
        "message": f"Like event published for user {req.user_id}, song {req.song_id}"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
