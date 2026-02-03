import pymysql
from pymysql.cursors import DictCursor
from dotenv import load_dotenv
import os

# Carica variabili d'ambiente da file .env
load_dotenv()

class DatabaseWrapper:
    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_NAME")
        self.port = int(os.getenv("DB_PORT", 3306))
        self.conn = None

    def connect(self):
        """Crea la connessione al database"""
        if self.conn is None:
            self.conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                cursorclass=DictCursor
            )
        return self.conn

    def close(self):
        """Chiude la connessione"""
        if self.conn:
            self.conn.close()
            self.conn = None

    def create_tables(self):
        """Crea le tabelle necessarie per le consegne"""
        conn = self.connect()
        cursor = conn.cursor()
        
        create_deliveries = """
        CREATE TABLE IF NOT EXISTS deliveries (
            id INT AUTO_INCREMENT PRIMARY KEY,
            tracking_code VARCHAR(50) NOT NULL UNIQUE,
            recipient_name VARCHAR(100) NOT NULL,
            address VARCHAR(255) NOT NULL,
            time_slot VARCHAR(50),
            status ENUM('READY','OUT_FOR_DELIVERY','DELIVERED','FAILED') DEFAULT 'READY',
            priority ENUM('LOW','MEDIUM','HIGH') DEFAULT 'LOW',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_deliveries)
        conn.commit()
        cursor.close()
