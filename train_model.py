import pandas as pd
import pickle
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split

def main():
    # 1. Load interactions
    interactions = pd.read_csv("interactions.csv")

    # 2. Convert to Surprise dataset (user_id, song_id, like)
    reader = Reader(rating_scale=(0, 1))  # 'like' is 0 or 1
    data = Dataset.load_from_df(interactions[['user_id', 'song_id', 'like']], reader)

    # 3. Split train/test
    trainset, testset = train_test_split(data, test_size=0.2)

    # 4. Train model
    algo = SVD(n_factors=20, n_epochs=20, random_state=42)
    algo.fit(trainset)

    # 6. Save trained model to disk
    with open("recommendation_model.pkl", "wb") as f:
        pickle.dump(algo, f)

    print("Model trained and saved as recommendation_model.pkl")

if __name__ == "__main__":
    main()
