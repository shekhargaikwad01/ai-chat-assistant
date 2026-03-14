import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", 5432),
        dbname=os.getenv("DB_NAME", "ai_chat_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD")
    )

def load_all_chats():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT chat_id, title, last_updated FROM chats ORDER BY last_updated DESC")
    chats_rows = cur.fetchall()
    all_chats = {}
    for chat_id, title, last_updated in chats_rows:
        cur.execute(
            "SELECT role, content, has_files FROM messages WHERE chat_id = %s ORDER BY id ASC",
            (chat_id,)
        )
        messages = []
        for role, content, has_files in cur.fetchall():
            msg = {"role": role, "content": content}
            if has_files:
                msg["has_files"] = True
            messages.append(msg)
        all_chats[chat_id] = {
            "title": title,
            "messages": messages,
            "last_updated": last_updated.isoformat() if last_updated else datetime.now().isoformat()
        }
    cur.close()
    conn.close()
    return all_chats

def save_chat(chat_id, title, messages, last_updated=None):
    if not messages:
        return
    conn = get_connection()
    cur = conn.cursor()
    now = last_updated or datetime.now().isoformat()
    cur.execute("""
        INSERT INTO chats (chat_id, title, last_updated)
        VALUES (%s, %s, %s)
        ON CONFLICT (chat_id) DO UPDATE
        SET title = EXCLUDED.title,
            last_updated = EXCLUDED.last_updated
    """, (chat_id, title, now))
    cur.execute("DELETE FROM messages WHERE chat_id = %s", (chat_id,))
    for msg in messages:
        cur.execute("""
            INSERT INTO messages (chat_id, role, content, has_files)
            VALUES (%s, %s, %s, %s)
        """, (
            chat_id,
            msg.get("role"),
            msg.get("content", ""),
            msg.get("has_files", False)
        ))
    conn.commit()
    cur.close()
    conn.close()

def delete_chat(chat_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM chats WHERE chat_id = %s", (chat_id,))
    conn.commit()
    cur.close()
    conn.close()

def rename_chat(chat_id, new_title):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE chats SET title = %s WHERE chat_id = %s",
        (new_title, chat_id)
    )
    conn.commit()
    cur.close()
    conn.close()