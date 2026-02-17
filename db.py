import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("job_portal.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    # ---------------- CREATE TABLES ----------------
    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            user_type TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs(
            job_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            location TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications(
            app_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            job_id INTEGER
        )
        """)

        self.conn.commit()

        # Insert sample jobs (only once)
        self.cursor.execute("SELECT COUNT(*) FROM jobs")
        if self.cursor.fetchone()[0] == 0:
            self.insert_sample_jobs()

    # ---------------- SAMPLE JOBS ----------------
    def insert_sample_jobs(self):
        jobs = [
            ("Python Developer", "Google", "Bangalore"),
            ("Web Developer", "Amazon", "Hyderabad"),
            ("Data Analyst", "Infosys", "Chennai"),
            ("Software Engineer", "TCS", "Pune")
        ]
        self.cursor.executemany(
            "INSERT INTO jobs (title, company, location) VALUES (?, ?, ?)",
            jobs
        )
        self.conn.commit()

    # ---------------- REGISTER USER ----------------
    def insert(self, name, email, password, user_type):
        try:
            self.cursor.execute(
                "INSERT INTO users (name, email, password, user_type) VALUES (?, ?, ?, ?)",
                (name, email, password, user_type)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    # ---------------- LOGIN ----------------
    def login(self, email, password):
        self.cursor.execute(
            "SELECT id, name FROM users WHERE email=? AND password=?",
            (email, password)
        )
        row = self.cursor.fetchone()

        if row:
            return {"id": row[0], "name": row[1]}
        return None

    # ---------------- GET ALL JOBS ----------------
    def get_all_jobs(self):
        self.cursor.execute("SELECT * FROM jobs")
        rows = self.cursor.fetchall()

        jobs = []
        for row in rows:
            jobs.append({
                "job_id": row[0],
                "title": row[1],
                "company": row[2],
                "location": row[3]
            })
        return jobs

    # ---------------- SEARCH JOB ----------------
    def search_job(self, keyword):
        self.cursor.execute(
            "SELECT * FROM jobs WHERE title LIKE ? OR company LIKE ?",
            (f"%{keyword}%", f"%{keyword}%")
        )
        rows = self.cursor.fetchall()

        jobs = []
        for row in rows:
            jobs.append({
                "job_id": row[0],
                "title": row[1],
                "company": row[2],
                "location": row[3]
            })
        return jobs

    # ---------------- APPLY JOB ----------------
    def apply_job(self, user_id, job_id):
        self.cursor.execute(
            "SELECT * FROM applications WHERE user_id=? AND job_id=?",
            (user_id, job_id)
        )
        if self.cursor.fetchone() is None:
            self.cursor.execute(
                "INSERT INTO applications (user_id, job_id) VALUES (?, ?)",
                (user_id, job_id)
            )
            self.conn.commit()

    # ---------------- DELETE APPLICATION ----------------
    def delete_application(self, user_id, job_id):
        self.cursor.execute(
            "DELETE FROM applications WHERE user_id=? AND job_id=?",
            (user_id, job_id)
        )
        self.conn.commit()
