# Assignment 10: Secure User Model with FastAPI

## 📋 Overview

This project implements a secure user authentication system using FastAPI, SQLAlchemy, and Pydantic. It includes password hashing, database validation, comprehensive testing, and automated CI/CD deployment to Docker Hub.

## 🔗 Links

- **GitHub Repository**: [Your Repository URL]
- **Docker Hub Repository**: [https://hub.docker.com/r/twin632/assignment10](https://hub.docker.com/r/twin632/assignment10)
- **Pull Docker Image**: 
  ```bash
  docker pull twin632/assignment10:latest
  ```

## 🏗️ Architecture

### User Model (SQLAlchemy)
- **Fields**: `id`, `username`, `email`, `password_hash`, `first_name`, `last_name`, `is_active`, `is_verified`, `created_at`, `updated_at`
- **Constraints**: Unique username and email
- **Security**: Bcrypt password hashing

### Pydantic Schemas
- **UserCreate**: Validates user registration data with password requirements
- **UserResponse**: Returns safe user data (excludes password_hash)
- **UserLogin**: Validates login credentials

### Password Security
- Minimum 6 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit
- Hashed using bcrypt before storage

## 🚀 Running Tests Locally

### Prerequisites
- Python 3.10+
- PostgreSQL installed and running
- Git

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd <your-repo-name>
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Set Up PostgreSQL Database
```bash
# Create a test database
createdb mytestdb

# Or using psql
psql -U postgres
CREATE DATABASE mytestdb;
\q
```

### 5. Configure Environment Variables
```bash
# Create a .env file or set environment variable
export DATABASE_URL=postgresql://user:password@localhost:5432/mytestdb

# On Windows PowerShell
$env:DATABASE_URL="postgresql://user:password@localhost:5432/mytestdb"
```

### 6. Run All Tests
```bash
# Run all tests with coverage
pytest --cov=app --cov-report=term-missing -v

# Run only unit tests
pytest tests/unit/ -v

# Run only integration tests
pytest tests/integration/ -v

# Run with detailed output
pytest -vv --tb=short
```

### 7. Run Specific Test Files
```bash
# Test user model
pytest tests/integration/test_user.py -v

# Test authentication
pytest tests/integration/test_user_auth.py -v

# Test schemas
pytest tests/unit/test_schema_base.py -v

# Test database
pytest tests/unit/test_database.py -v
```

### Expected Output
```
========================= test session starts =========================
collected 45 items

tests/unit/test_database.py ......                              [ 13%]
tests/unit/test_schema_base.py ..................              [ 53%]
tests/integration/test_user.py ................                [ 89%]
tests/integration/test_user_auth.py .....                      [100%]

---------- coverage: platform linux, python 3.10.x -----------
Name                          Stmts   Miss  Cover   Missing
-----------------------------------------------------------
app/__init__.py                   0      0   100%
app/database.py                  21      0   100%
app/models/user.py               87      0   100%  
app/schemas/base.py              28      0   100%
app/schemas/user.py              15      0   100%
-----------------------------------------------------------
TOTAL                           151      2    99%

========================= 45 passed in 5.23s ==========================
```

## 🐳 Running with Docker

### Pull and Run from Docker Hub
```bash
# Pull the latest image
docker pull twin632/assignment10:latest

# Run the container
docker run -d -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:password@host:5432/db \
  --name fastapi-app \
  twin632/assignment10:latest

# Check logs
docker logs fastapi-app

# Access the application
curl http://localhost:8000/health

# Stop and remove
docker stop fastapi-app && docker rm fastapi-app
```

### Build Locally
```bash
# Build the image
docker build -t assignment10:local .

# Run locally built image
docker run -d -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:password@localhost:5432/mytestdb \
  assignment10:local
```

### Docker Compose (Optional)
```bash
# If you have docker-compose.yml
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

The CI/CD pipeline automatically:

1. **Test Stage**
   - Spins up a PostgreSQL container
   - Runs unit tests with coverage
   - Runs integration tests with real database
   - Uploads test results and coverage reports

2. **Security Stage**
   - Builds Docker image
   - Scans for vulnerabilities using Trivy
   - Fails on CRITICAL or HIGH severity issues

3. **Deploy Stage**
   - Builds multi-platform image (amd64, arm64)
   - Pushes to Docker Hub with tags:
     - `twin632/assignment10:latest`
     - `twin632/assignment10:<commit-sha>`

### Triggering the Pipeline
```bash
# Push to main branch
git add .
git commit -m "Your commit message"
git push origin main

# Or create a pull request
git checkout -b feature/new-feature
git push origin feature/new-feature
# Then create PR on GitHub
```

### Viewing Pipeline Results
1. Go to your GitHub repository
2. Click on the **Actions** tab
3. View workflow runs and logs
4. Check Docker Hub for pushed images


## 🧪 Test Coverage

Current test coverage: **~99%**

### Unit Tests (23 tests)
- Pydantic schema validation
- Password validation rules
- Database connection and session management
- Model method testing

### Integration Tests (22 tests)
- User registration and authentication
- Database constraints (unique email/username)
- Password hashing and verification
- Token creation and validation
- Transaction rollback scenarios

## 🔐 Security Features

- ✅ Non-root Docker user (`appuser`)
- ✅ Bcrypt password hashing
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ Input validation (Pydantic)
- ✅ Unique constraints on email/username
- ✅ JWT token authentication
- ✅ Automated vulnerability scanning (Trivy)
- ✅ Environment variable configuration
- ✅ Health check endpoint

## 🛠️ Technologies Used

- **FastAPI**: Modern web framework
- **SQLAlchemy**: ORM for database operations
- **Pydantic**: Data validation
- **PostgreSQL**: Relational database
- **Pytest**: Testing framework
- **Docker**: Containerization
- **GitHub Actions**: CI/CD automation
- **Trivy**: Security scanning

## 📝 API Endpoints

- `GET /health` - Health check endpoint
- `POST /register` - User registration
- `POST /login` - User authentication
- `GET /users/me` - Get current user profile


