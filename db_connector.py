import mysql.connector
from mysql.connector import Error
import os
import time
import sqlite3
from pathlib import Path

class DatabaseConnector:
    """Utility class to handle database operations for the Alumni Tracer app"""
    
    def __init__(self, max_retries=1):
        """Initialize database connection parameters"""
        # Database configuration - in production, use environment variables
        self.config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',  # Add your MySQL password here
            'database': 'alumni_db'  # Name of your database
        }
        
        self.connected = False
        self.max_retries = max_retries
        self.db_type = 'mysql'  # Default to MySQL
        
        # Initialize connection and create tables if needed
        try:
            self._initialize_database()
        except Error as e:
            print(f"MySQL database initialization error: {e}")
            print("Falling back to SQLite local database...")
            try:
                self._initialize_sqlite_database()
                self.db_type = 'sqlite'
                self.connected = True
                print("SQLite database initialized successfully. Data will be saved locally.")
            except Exception as e:
                print(f"SQLite fallback failed: {e}")
                print("You can still use the app, but data will not be saved.")
    
    def _initialize_database(self):
        """Initialize MySQL database and create tables if they don't exist"""
        conn = None
        cursor = None
        
        try:
            # First connect without specifying database to create it if needed
            print("Attempting to connect to MySQL server...")
            conn = mysql.connector.connect(
                host=self.config['host'],
                user=self.config['user'],
                password=self.config['password'],
                connection_timeout=5  # 5 second timeout
            )
            
            cursor = conn.cursor()
            
            # Create database if not exists
            print(f"Creating database {self.config['database']} if it doesn't exist...")
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.config['database']}")
            
            # Close initial connection
            cursor.close()
            conn.close()
            
            # Connect to the database
            print(f"Connecting to {self.config['database']} database...")
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor()
            
            # Create users table if not exists
            print("Creating users table if it doesn't exist...")
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    year_graduated VARCHAR(10),
                    strand VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            self.connected = True
            print("MySQL database initialized successfully")
            
        except Error as e:
            print(f"Error initializing MySQL database: {e}")
            # For MySQL server connection errors, provide more helpful message
            if "Can't connect to MySQL server" in str(e):
                print("\nPossible reasons for connection failure:")
                print("1. MySQL server is not installed")
                print("2. MySQL service is not running")
                print("3. MySQL server is using a different port")
                print("4. Credentials are incorrect\n")
                print("Solution: Make sure MySQL server is installed and running.")
            raise e
        
        finally:
            if cursor:
                try:
                    cursor.close()
                except:
                    pass
            if conn:
                try:
                    conn.close()
                except:
                    pass
    
    def _initialize_sqlite_database(self):
        """Initialize SQLite database as a fallback"""
        # Create database directory if it doesn't exist
        db_dir = Path(__file__).parent / "data"
        db_dir.mkdir(exist_ok=True)
        
        # SQLite database path
        self.sqlite_db_path = db_dir / "alumni_local.db"
        
        # Connect to SQLite database
        conn = sqlite3.connect(str(self.sqlite_db_path))
        cursor = conn.cursor()
        
        # Create users table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                name TEXT NOT NULL,
                year_graduated TEXT,
                strand TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        cursor.close()
        conn.close()
        print(f"SQLite database initialized at: {self.sqlite_db_path}")
    
    def register_user(self, email, password, name, year_graduated=None, strand=None):
        """Register a new user in the database"""
        if not self.connected:
            return False, "Database not connected. User information will not be saved."
            
        if self.db_type == 'mysql':
            return self._register_user_mysql(email, password, name, year_graduated, strand)
        else:
            return self._register_user_sqlite(email, password, name, year_graduated, strand)
    
    def _register_user_mysql(self, email, password, name, year_graduated=None, strand=None):
        """Register a new user in MySQL database"""
        conn = None
        cursor = None
        
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor()
            
            # Check if email already exists
            cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                return False, "Email already registered"
            
            # Insert new user
            query = """
                INSERT INTO users (email, password, name, year_graduated, strand)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (email, password, name, year_graduated, strand))
            conn.commit()
            
            return True, "Registration successful"
            
        except Error as e:
            print(f"Error registering user: {e}")
            return False, f"Registration failed: {str(e)}"
            
        finally:
            if cursor:
                try:
                    cursor.close()
                except:
                    pass
            if conn:
                try:
                    conn.close()
                except:
                    pass
    
    def _register_user_sqlite(self, email, password, name, year_graduated=None, strand=None):
        """Register a new user in SQLite database"""
        try:
            conn = sqlite3.connect(str(self.sqlite_db_path))
            cursor = conn.cursor()
            
            # Check if email already exists
            cursor.execute("SELECT email FROM users WHERE email = ?", (email,))
            if cursor.fetchone():
                return False, "Email already registered"
            
            # Insert new user
            query = """
                INSERT INTO users (email, password, name, year_graduated, strand)
                VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(query, (email, password, name, year_graduated, strand))
            conn.commit()
            
            return True, "Registration successful (saved locally)"
            
        except sqlite3.Error as e:
            print(f"Error registering user in SQLite: {e}")
            return False, f"Registration failed: {str(e)}"
            
        finally:
            if conn:
                conn.close()
    
    def authenticate_user(self, email, password):
        """Authenticate a user with email and password"""
        if not self.connected:
            # For demo purposes, allow a hardcoded test account when DB is not available
            if email == "test@example.com" and password == "password":
                user = {
                    "id": 0,
                    "email": email,
                    "name": "Test User",
                    "year_graduated": "2023",
                    "strand": "STEM"
                }
                return True, "Test account authenticated (offline mode)", user
            return False, "Database not connected. Cannot authenticate.", None
            
        if self.db_type == 'mysql':
            return self._authenticate_user_mysql(email, password)
        else:
            return self._authenticate_user_sqlite(email, password)
    
    def _authenticate_user_mysql(self, email, password):
        """Authenticate a user against MySQL database"""
        conn = None
        cursor = None
        
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor(dictionary=True)
            
            # Check credentials
            query = "SELECT * FROM users WHERE email = %s AND password = %s"
            cursor.execute(query, (email, password))
            user = cursor.fetchone()
            
            if user:
                return True, "Authentication successful", user
            else:
                return False, "Invalid email or password", None
                
        except Error as e:
            print(f"Error authenticating user: {e}")
            return False, f"Authentication failed: {str(e)}", None
            
        finally:
            if cursor:
                try:
                    cursor.close()
                except:
                    pass
            if conn:
                try:
                    conn.close()
                except:
                    pass
    
    def _authenticate_user_sqlite(self, email, password):
        """Authenticate a user against SQLite database"""
        try:
            conn = sqlite3.connect(str(self.sqlite_db_path))
            conn.row_factory = sqlite3.Row  # This enables name-based access to columns
            cursor = conn.cursor()
            
            # Check credentials
            query = "SELECT * FROM users WHERE email = ? AND password = ?"
            cursor.execute(query, (email, password))
            row = cursor.fetchone()
            
            if row:
                # Convert sqlite3.Row to dict
                user = dict(zip([column[0] for column in cursor.description], row))
                return True, "Authentication successful", user
            else:
                return False, "Invalid email or password", None
                
        except sqlite3.Error as e:
            print(f"Error authenticating user in SQLite: {e}")
            return False, f"Authentication failed: {str(e)}", None
            
        finally:
            if conn:
                conn.close()

# Create an instance for import
db = DatabaseConnector()
