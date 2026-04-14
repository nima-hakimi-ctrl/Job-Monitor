import sqlite3
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'jobs.db')

def init_database():
    """Initialize the SQLite database with required tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create jobs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            location TEXT,
            description TEXT,
            url TEXT,
            source TEXT NOT NULL,
            score INTEGER DEFAULT 0,
            posted_date TEXT,
            discovered_date TEXT NOT NULL,
            alerted INTEGER DEFAULT 0
        )
    ''')
    
    # Create index for faster lookups
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_job_id ON jobs(job_id)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_discovered_date ON jobs(discovered_date)
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")

def job_exists(job_id):
    """Check if a job already exists in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM jobs WHERE job_id = ?', (job_id,))
    exists = cursor.fetchone()[0] > 0
    
    conn.close()
    return exists

def save_job(job_data):
    """Save a job to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO jobs (job_id, title, company, location, description, url, source, score, posted_date, discovered_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            job_data['job_id'],
            job_data['title'],
            job_data['company'],
            job_data.get('location', ''),
            job_data.get('description', ''),
            job_data['url'],
            job_data['source'],
            job_data.get('score', 0),
            job_data.get('posted_date', ''),
            datetime.now().isoformat()
        ))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Job already exists
        return False
    finally:
        conn.close()

def mark_as_alerted(job_id):
    """Mark a job as having been alerted."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('UPDATE jobs SET alerted = 1 WHERE job_id = ?', (job_id,))
    conn.commit()
    conn.close()

def get_unalerted_jobs(min_score=3):
    """Get jobs that haven't been alerted yet and meet minimum score."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT job_id, title, company, location, description, url, source, score, discovered_date
        FROM jobs
        WHERE alerted = 0 AND score >= ?
        ORDER BY score DESC, discovered_date DESC
    ''', (min_score,))
    
    jobs = []
    for row in cursor.fetchall():
        jobs.append({
            'job_id': row[0],
            'title': row[1],
            'company': row[2],
            'location': row[3],
            'description': row[4],
            'url': row[5],
            'source': row[6],
            'score': row[7],
            'discovered_date': row[8]
        })
    
    conn.close()
    return jobs

def get_stats():
    """Get database statistics."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM jobs')
    total = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM jobs WHERE alerted = 1')
    alerted = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM jobs WHERE alerted = 0')
    pending = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'total_jobs': total,
        'alerted': alerted,
        'pending': pending
    }

if __name__ == '__main__':
    init_database()
    print("Database setup complete!")
    stats = get_stats()
    print(f"Stats: {stats}")
