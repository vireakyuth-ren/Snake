import sqlite3

# def get_high_scores():
#     conn = sqlite3.connect('highscore.db')
#     c = conn.cursor()
#     c.execute("SELECT score FROM highscore ORDER BY score DESC")
    
#     high_scores = c.fetchall()
#     conn.close()
#     return [score[0] for score in high_scores]

def get_highscores_and_names():
    conn = sqlite3.connect('highscore.db')
    c = conn.cursor()
    c.execute("SELECT score, name FROM highscore ORDER BY score DESC")
    
    high_scores_names = c.fetchall()
    conn.close()
    return high_scores_names

def show_highscores():
    high_scores_names = get_highscores_and_names()
    print("High Scores:")
    for i, (score, name) in enumerate(high_scores_names):
        print(f"{i+1}. {name}: {score}")

# def show_high_scores():
#     high_scores = get_highscores_and_names()
#     print("High Scores:")
#     for idx, score in enumerate(high_scores, start=1):
#         print(f"{idx}. {score}")

if __name__ == "__main__":
    show_highscores()

# def add_name_column():
#     conn = sqlite3.connect('highscore.db')
#     c = conn.cursor()
#     # Add a new column to the existing table
#     try:
#         c.execute("ALTER TABLE highscore ADD COLUMN name TEXT")
#     except sqlite3.OperationalError:
#         # This error occurs if the column already exists
#         pass
#     conn.commit()
#     conn.close()

# conn = sqlite3.connect('highscore.db')
# c = conn.cursor()
# c.execute("DELETE FROM highscore")
# conn.commit()