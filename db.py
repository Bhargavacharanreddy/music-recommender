import sqlite3

def get_connection():
    conn = sqlite3.connect("music_app.db")
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Create a simple user profile table to track liked songs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_profile (
            user_id INTEGER,
            song_id INTEGER,
            PRIMARY KEY (user_id, song_id)
        )
    """)
    conn.commit()
    conn.close()
