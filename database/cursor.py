import sqlite3

import atexit

from Config import Config

conn = sqlite3.connect(Config.database)

cursor = conn.cursor()

create_table_query = '''
CREATE TABLE IF NOT EXISTS QuestionAnswers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    username TEXT NOT NULL,
    is_answer_correct BOOLEAN NOT NULL 
);
'''

# Execute the SQL statement to create the table
cursor.execute(create_table_query)

# Commit changes and close the connection
conn.commit()


@atexit.register
def close_connection():
    conn.close()
