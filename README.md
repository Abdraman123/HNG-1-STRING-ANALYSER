# Stage 1 - String Analyzer API

A RESTful API service that analyzes strings, computes their properties, and stores them in a PostgreSQL database. Built with FastAPI and SQLAlchemy.

## 🚀 Live Demo

**API Base URL:** https://YOUR-APP.digitalocean.app

**Interactive Documentation:** https://YOUR-APP.digitalocean.app/docs

**Alternative Docs:** https://YOUR-APP.digitalocean.app/redoc

## 📋 Features

- ✅ Analyze and store string properties
- ✅ Compute SHA-256 hash for unique identification
- ✅ Palindrome detection (case-insensitive)
- ✅ Character frequency mapping
- ✅ Word count analysis
- ✅ Query filtering with multiple parameters
- ✅ Natural language query parsing
- ✅ PostgreSQL database persistence
- ✅ CRUD operations (Create, Read, Delete)
- ✅ Comprehensive error handling
- ✅ Auto-generated API documentation

## 🛠️ Tech Stack

- **Language:** Python 3.9+
- **Framework:** FastAPI 0.115.0
- **Database:** PostgreSQL 18
- **ORM:** SQLAlchemy 2.0.23
- **Server:** Uvicorn
- **Validation:** Pydantic
- **Deployment:** DigitalOcean App Platform

## 📁 Project Structure

```
stage1-string-analyzer/
│
├── main.py              # FastAPI app and API endpoints
├── models.py            # Pydantic schemas and SQLAlchemy models
├── services.py          # Business logic and string analysis functions
├── database.py          # Database configuration and session management
├── config.py            # Application settings and environment variables
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not in git)
├── .gitignore          # Git ignore rules
└── README.md           # Project documentation (this file)
```

## 📦 Installation & Local Setup

### Prerequisites

- Python 3.9 or higher
- PostgreSQL 18
- pip (Python package manager)
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/stage1-string-analyzer.git
cd stage1-string-analyzer
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies installed:**
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `sqlalchemy` - Database ORM
- `psycopg2-binary` - PostgreSQL driver
- `python-dotenv` - Environment variable management
- `pydantic` - Data validation

### Step 4: Set Up PostgreSQL Database

**Create Database and User:**

```bash
# Access PostgreSQL
psql -U postgres

# Or using pgAdmin4:
# Right-click Databases → Create → Database
```

**Run these SQL commands:**

```sql
-- Create database
CREATE DATABASE string_analyser;

-- Create user
CREATE USER your_username WITH PASSWORD 'your_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE string_analyser TO your_username;

-- Connect to database
\c string_analyser

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO your_username;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO your_username;
```

### Step 5: Configure Environment Variables

Create `.env` file in project root:

```env
# Database Configuration
DATABASE_URL=postgresql://your_username:your_password@localhost:5432/string_analyser

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

**⚠️ IMPORTANT:** Replace `your_username` and `your_password` with your actual PostgreSQL credentials.

### Step 6: Run the Application

```bash
uvicorn main:app --reload
```

The API will be available at:
- **API:** http://127.0.0.1:8000
- **Interactive Docs:** http://127.0.0.1:8000/docs
- **Alternative Docs:** http://127.0.0.1:8000/redoc

You should see:
```
🚀 String Analyzer API v1.0.0 starting...
📊 Database: localhost:5432/string_analyser
📚 Docs: http://127.0.0.1:8000/docs
```

## 🔌 API Endpoints

### 1. Create/Analyze String

**POST** `/strings`

Analyzes a string and stores its computed properties.

**Request:**
```json
{
  "value": "racecar"
}
```

**Response (201 Created):**
```json
{
  "id": "sha256_hash_value",
  "value": "racecar",
  "properties": {
    "length": 7,
    "is_palindrome": true,
    "unique_characters": 4,
    "word_count": 1,
    "sha256_hash": "abc123...",
    "character_frequency_map": {
      "r": 2,
      "a": 2,
      "c": 2,
      "e": 1
    }
  },
  "created_at": "2025-10-23T10:00:00Z"
}
```

**Error Responses:**
- `409 Conflict` - String already exists
- `400 Bad Request` - Invalid request body
- `422 Unprocessable Entity` - Invalid data type

---

### 2. Get Specific String

**GET** `/strings/{string_value}`

Retrieves a specific string by its value.

**Example:**
```bash
GET /strings/racecar
```

**Response (200 OK):**
```json
{
  "id": "sha256_hash_value",
  "value": "racecar",
  "properties": { /* same as above */ },
  "created_at": "2025-10-23T10:00:00Z"
}
```

**Error Response:**
- `404 Not Found` - String does not exist

---

### 3. Get All Strings with Filtering

**GET** `/strings`

Retrieves all strings with optional query parameters for filtering.

**Query Parameters:**
- `is_palindrome` (boolean) - Filter by palindrome status
- `min_length` (integer) - Minimum string length
- `max_length` (integer) - Maximum string length
- `word_count` (integer) - Exact word count
- `contains_character` (string) - Single character to search for

**Examples:**

```bash
# Get all palindromes
GET /strings?is_palindrome=true

# Get strings with 5-10 characters
GET /strings?min_length=5&max_length=10

# Get strings with exactly 2 words
GET /strings?word_count=2

# Get strings containing 'a'
GET /strings?contains_character=a

# Combine filters
GET /strings?is_palindrome=true&word_count=1
```

**Response (200 OK):**
```json
{
  "data": [
    {
      "id": "hash1",
      "value": "noon",
      "properties": { /* ... */ },
      "created_at": "2025-10-23T10:00:00Z"
    }
  ],
  "count": 1,
  "filters_applied": {
    "is_palindrome": true,
    "word_count": 1
  }
}
```

**Error Response:**
- `400 Bad Request` - Invalid query parameter values

---

### 4. Natural Language Filtering

**GET** `/strings/filter-by-natural-language`

Filter strings using plain English queries.

**Query Parameter:**
- `query` (string) - Natural language query

**Supported Query Patterns:**

| Query | Parsed Filters |
|-------|---------------|
| "all single word palindromic strings" | `word_count=1, is_palindrome=true` |
| "strings longer than 10 characters" | `min_length=11` |
| "strings containing the letter z" | `contains_character=z` |
| "palindromic strings that contain the first vowel" | `is_palindrome=true, contains_character=a` |

**Example:**
```bash
GET /strings/filter-by-natural-language?query=all%20single%20word%20palindromic%20strings
```

**Response (200 OK):**
```json
{
  "data": [ /* array of matching strings */ ],
  "count": 3,
  "interpreted_query": {
    "original": "all single word palindromic strings",
    "parsed_filters": {
      "word_count": 1,
      "is_palindrome": true
    }
  }
}
```

**Error Responses:**
- `400 Bad Request` - Unable to parse query
- `422 Unprocessable Entity` - Conflicting filters

---

### 5. Delete String

**DELETE** `/strings/{string_value}`

Deletes a string by its value.

**Example:**
```bash
DELETE /strings/test
```

**Response:**
- `204 No Content` - Successfully deleted (empty response)

**Error Response:**
- `404 Not Found` - String does not exist

---

## 🧪 Testing

### Using Interactive Docs (Recommended)

1. Open http://127.0.0.1:8000/docs
2. Click on any endpoint
3. Click "Try it out"
4. Fill in parameters
5. Click "Execute"
6. View response

### Using cURL

```bash
# Create a string
curl -X POST "http://127.0.0.1:8000/strings" \
  -H "Content-Type: application/json" \
  -d '{"value":"racecar"}'

# Get a string
curl "http://127.0.0.1:8000/strings/racecar"

# Get palindromes
curl "http://127.0.0.1:8000/strings?is_palindrome=true"

# Natural language query
curl "http://127.0.0.1:8000/strings/filter-by-natural-language?query=all%20palindromic%20strings"

# Delete a string
curl -X DELETE "http://127.0.0.1:8000/strings/test"
```

### Using Python requests

```python
import requests

BASE_URL = "http://127.0.0.1:8000"

# Create string
response = requests.post(f"{BASE_URL}/strings", json={"value": "hello"})
print(response.json())

# Get string
response = requests.get(f"{BASE_URL}/strings/hello")
print(response.json())

# Get with filters
response = requests.get(f"{BASE_URL}/strings", params={"is_palindrome": True})
print(response.json())
```

### Test Data Examples

```json
{"value": "racecar"}
{"value": "A man a plan a canal Panama"}
{"value": "hello world"}
{"value": "noon"}
{"value": "test string"}
{"value": "madam"}
{"value": "python"}
```

---

## 🔍 Key Implementation Details

### String Analysis Properties

**1. Length**
- Simple character count: `len(string)`

**2. Palindrome Detection**
- Case-insensitive
- Ignores spaces and special characters
- "A man a plan a canal Panama" → True

**3. Unique Characters**
- Count of distinct characters
- "hello" → 4 unique chars (h, e, l, o)

**4. Word Count**
- Words separated by whitespace
- "hello world" → 2 words

**5. SHA-256 Hash**
- Unique identifier for each string
- Same string always produces same hash
- Used as primary key in database

**6. Character Frequency Map**
- Dictionary mapping each character to its count
- "hello" → `{"h": 1, "e": 1, "l": 2, "o": 1}`

### Database Schema

**Table: `strings`**

| Column | Type | Constraints |
|--------|------|-------------|
| id | VARCHAR | PRIMARY KEY |
| value | VARCHAR | UNIQUE, NOT NULL |
| length | INTEGER | NOT NULL |
| is_palindrome | BOOLEAN | NOT NULL |
| unique_characters | INTEGER | NOT NULL |
| word_count | INTEGER | NOT NULL |
| sha256_hash | VARCHAR | NOT NULL |
| character_frequency_map | JSON | NOT NULL |
| created_at | TIMESTAMP | DEFAULT now() |

### Natural Language Processing

Uses regex-based keyword matching to parse queries:

- **Palindrome:** "palindrome", "palindromic" → `is_palindrome=true`
- **Word count:** "single word" → `word_count=1`
- **Length:** "longer than X" → `min_length=X+1`
- **Contains:** "containing letter X" → `contains_character=X`

---

## 🌐 Deployment

### DigitalOcean Deployment Steps

**1. Set Up PostgreSQL Database**

1. Go to DigitalOcean Dashboard
2. Databases → Create Database Cluster
3. Choose PostgreSQL 18
4. Select plan and region
5. Create database
6. Copy connection string

**2. Deploy Application**

1. App Platform → Create App
2. Connect GitHub repository
3. DigitalOcean auto-detects Python
4. Configure build settings (uses requirements.txt)

**3. Configure Environment Variables**

In App Settings → Environment Variables:

```
DATABASE_URL = [Your DigitalOcean PostgreSQL connection string]
DEBUG = False
```

**4. Deploy and Test**

- Wait for deployment (~5 minutes)
- Test live URL
- Verify database connectivity

### Environment Variables for Production

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:port/db` |
| `DEBUG` | Debug mode (False in production) | `False` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |

---

## 🛡️ Error Handling

The API uses appropriate HTTP status codes:

- `200 OK` - Successful GET request
- `201 Created` - Successful POST request
- `204 No Content` - Successful DELETE request
- `400 Bad Request` - Invalid request parameters
- `404 Not Found` - Resource not found
- `409 Conflict` - Duplicate string
- `422 Unprocessable Entity` - Invalid data type
- `500 Internal Server Error` - Server error

All error responses include descriptive messages:

```json
{
  "detail": "String already exists in the system"
}
```

---

## 🐛 Troubleshooting

### Issue: Database Connection Failed

**Error:** `could not connect to server`

**Solutions:**
1. Verify PostgreSQL is running: `sudo systemctl status postgresql`
2. Check DATABASE_URL in .env is correct
3. Test connection: `psql -U username -d database -h localhost`

### Issue: Table Does Not Exist

**Error:** `relation "strings" does not exist`

**Solution:**
```bash
# Restart the app to create tables
uvicorn main:app --reload
```

Or manually create:
```python
from database import engine, Base
Base.metadata.create_all(bind=engine)
```

### Issue: Import Errors

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Use different port
uvicorn main:app --reload --port 8001

# Or kill process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID [PID] /F

# Mac/Linux:
lsof -ti:8000 | xargs kill -9
```

---

## 📊 Project Stats

- **Total Endpoints:** 5
- **Lines of Code:** ~600
- **Files:** 8
- **Dependencies:** 6
- **Database Tables:** 1
- **Test Coverage:** Manual testing via Swagger UI

---

## 🎓 What I Learned

### Technical Skills
- ✅ PostgreSQL database integration
- ✅ SQLAlchemy ORM usage
- ✅ CRUD operations
- ✅ Query parameter filtering
- ✅ Natural language processing basics
- ✅ SHA-256 cryptographic hashing
- ✅ JSON data storage in PostgreSQL
- ✅ Database session management
- ✅ Proper HTTP status codes
- ✅ Error handling strategies

### Best Practices
- ✅ Modular code organization
- ✅ Separation of concerns (models, services, endpoints)
- ✅ Environment-based configuration
- ✅ Database connection pooling
- ✅ Input validation with Pydantic
- ✅ Auto-generated API documentation
- ✅ Proper use of database transactions

---

## 🤝 Contributing

This is a task submission for HNG Internship Stage 1. Feedback and suggestions are welcome!

## 📝 License

This project is created for the HNG Internship program.

## 👤 Author

**ABDUR-RAHMAN AJANI**
- Email: ajaniabdulrahman@gmail.com

## 🙏 Acknowledgments

- [HNG Internship](https://hng.tech/internship) for the practical challenge
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent framework
- [SQLAlchemy](https://www.sqlalchemy.org/) for the powerful ORM
- [PostgreSQL](https://www.postgresql.org/) for reliable database

## 🔗 Important Links

- **HNG Internship:** https://hng.tech/internship
- **FastAPI Documentation:** https://fastapi.tiangolo.com/
- **SQLAlchemy Documentation:** https://docs.sqlalchemy.org/

---

**Built with ❤️ for HNG Internship Stage 1**

*If you found this helpful, please star ⭐ the repository!*