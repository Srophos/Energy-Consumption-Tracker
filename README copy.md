# ⚡ Energy Tracker - Professional CI/CD Pipeline

A web application to track daily energy consumption and calculate monthly electricity bills with a professional CI/CD pipeline demonstrating automated testing, containerized deployment, and AWS infrastructure.

## 🚀 Features

- **Daily Energy Entry**: Track appliance usage with power rating and hours used
- **Monthly Dashboard**: View consumption breakdown and calculated bills
- **Automated CI/CD**: GitHub Actions pipeline with quality gates
- **Containerized Deployment**: Docker containers for staging and production
- **Environment Isolation**: Separate staging and production databases
- **Automated Testing**: Unit, integration, and system tests with 80%+ coverage
- **Security Scanning**: Automated vulnerability detection
- **Health Monitoring**: Built-in health checks for deployment verification
- **Automated Rollback**: Automatic revert on failed deployments

## 🏗️ Architecture

### Tech Stack
- **Backend**: Python Flask 3.0
- **Database**: SQLite
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **Deployment**: AWS EC2
- **Registry**: Docker Hub

### System Architecture
```
┌─────────────────────────────────────────────────────────┐
│                     GitHub Repository                    │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │
│  │ Feature │  │ Develop │  │  Main   │  │  Tests  │   │
│  │ Branches│  │ Branch  │  │ Branch  │  │         │   │
│  └────┬────┘  └────┬────┘  └────┬────┘  └─────────┘   │
└───────┼───────────┼────────────┼────────────────────────┘
        │           │            │
        ▼           ▼            ▼
   ┌────────────────────────────────────┐
   │      GitHub Actions Pipeline       │
   │  ┌──────────────────────────────┐  │
   │  │ 1. Lint  2. Security         │  │
   │  │ 3. Test  4. Build Docker     │  │
   │  │ 5. Push  6. Deploy           │  │
   │  │ 7. Health Check 8. Rollback  │  │
   │  └──────────────────────────────┘  │
   └────────────┬──────────┬────────────┘
                │          │
         develop│          │main
                ▼          ▼
        ┌───────────────────────────┐
        │      AWS EC2 Instance     │
        │  ┌──────────────────────┐ │
        │  │ Staging (Port 5001)  │ │
        │  │ - Docker Container   │ │
        │  │ - staging.db         │ │
        │  └──────────────────────┘ │
        │  ┌──────────────────────┐ │
        │  │Production (Port 5000)│ │
        │  │ - Docker Container   │ │
        │  │ - production.db      │ │
        │  └──────────────────────┘ │
        └───────────────────────────┘
```

## 📋 Prerequisites

- Python 3.11+
- Docker
- AWS EC2 instance (t2.micro or larger)
- GitHub account
- Docker Hub account

## 🛠️ Local Development Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/energy-tracker.git
cd energy-tracker
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python run.py
```

Visit `http://localhost:5000` in your browser.

### 5. Run Tests
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

## 🐳 Docker Deployment

### Build Docker Image
```bash
docker build -t energy-tracker:latest .
```

### Run Container
```bash
docker run -d \
  --name energy-tracker \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  -e DATABASE=/app/data/production.db \
  -v $(pwd)/data:/app/data \
  energy-tracker:latest
```

### Health Check
```bash
curl http://localhost:5000/health
```

## ⚙️ CI/CD Pipeline Setup

### 1. GitHub Secrets Configuration

Navigate to your repository → Settings → Secrets and variables → Actions, and add:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `DOCKERHUB_USERNAME` | Docker Hub username | `johndoe` |
| `DOCKERHUB_TOKEN` | Docker Hub access token | Generate from Docker Hub settings |
| `EC2_HOST` | EC2 instance public IP | `54.123.45.67` |
| `EC2_USER` | EC2 SSH username | `ubuntu` |
| `EC2_SSH_KEY` | EC2 private SSH key | Contents of your `.pem` file |

### 2. AWS EC2 Setup

**Launch EC2 Instance:**
```bash
# Instance type: t2.micro (Free tier eligible)
# AMI: Ubuntu 24.04 LTS
# Security Group: Allow ports 22, 5000, 5001
```

**Connect and Install Docker:**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Create data directories
mkdir -p ~/data/staging ~/data/production
```

### 3. Branch Strategy

| Branch | Purpose | CI/CD Actions | Deployment |
|--------|---------|---------------|------------|
| `feature/*` | Development | Lint + Security + Tests | None |
| `develop` | Staging | All + Build Docker | Staging (Port 5001) |
| `main` | Production | All + Build Docker | Production (Port 5000) |

### 4. Pipeline Stages

1. **Linting**: Code style validation (Black, isort, Flake8)
2. **Security Scan**: Vulnerability detection (Bandit, Safety)
3. **Unit Tests**: Business logic verification (Pytest)
4. **Build Docker**: Create containerized artifact
5. **Push to Registry**: Store versioned image in Docker Hub
6. **Deploy**: Deploy to appropriate environment
7. **Health Check**: Verify deployment success
8. **Approval/Rollback**: Manual gate or automatic rollback

## 📊 Database Schema

### energy_entries
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| date | TEXT | Entry date (YYYY-MM-DD) |
| appliance | TEXT | Appliance name |
| power_watts | INTEGER | Power rating in watts |
| hours_used | REAL | Hours of usage |
| energy_kwh | REAL | Calculated energy (kWh) |
| created_at | TIMESTAMP | Creation timestamp |

### billing_rates
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| rate_per_kwh | REAL | Billing rate per kWh |
| effective_date | TEXT | Rate effective date |
| created_at | TIMESTAMP | Creation timestamp |

## 🧪 Testing Strategy

### Test Coverage
- **Unit Tests (70%)**: Individual functions and calculations
- **Integration Tests (20%)**: API routes and database operations
- **System Tests (10%)**: Health checks and deployment verification

### Running Tests
```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_routes.py -v

# With coverage report
pytest tests/ --cov=app --cov-report=term-missing

# Coverage threshold check
coverage report --fail-under=80
```

## 🔒 Security Measures

| Measure | Implementation |
|---------|----------------|
| Secrets Management | GitHub Secrets for credentials |
| SSH Authentication | Key-based (no passwords) |
| Network Security | Security Groups restrict access |
| Dependency Scanning | Safety tool checks vulnerabilities |
| Code Scanning | Bandit detects security issues |

## 🚀 Deployment Workflow

### Staging Deployment
```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "Add new feature"

# Push to trigger CI (no deployment)
git push origin feature/new-feature

# Merge to develop for staging
git checkout develop
git merge feature/new-feature
git push origin develop  # Deploys to staging
```

### Production Deployment
```bash
# Merge develop to main
git checkout main
git merge develop
git push origin main  # Triggers production deployment (requires approval)
```

## 📈 Monitoring and Rollback

### Health Check Endpoint
```bash
# Staging
curl http://your-ec2-ip:5001/health

# Production
curl http://your-ec2-ip:5000/health
```

### Manual Rollback
```bash
ssh ubuntu@your-ec2-ip

# Stop current container
docker stop energy-tracker-production
docker rm energy-tracker-production

# Run backup version
docker run -d \
  --name energy-tracker-production \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  -v ~/data/production:/app/data \
  your-dockerhub-username/energy-tracker:main-backup
```

## 🔧 Environment Variables

| Variable | Staging | Production |
|----------|---------|------------|
| `FLASK_ENV` | development | production |
| `DEBUG` | True | False |
| `DATABASE` | staging.db | production.db |
| `PORT` | 5001 | 5000 |

## 📝 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Display daily entry form |
| `/` | POST | Save entry and redirect to dashboard |
| `/dashboard?month=X&year=Y` | GET | Display monthly consumption |
| `/health` | GET | Health check for monitoring |

## 🎯 Success Criteria

- ✅ Automated unit testing on every commit (all branches)
- ✅ Containerized artifact creation on production branch merge
- ✅ Separate staging and production environments
- ✅ Manual approval gate for production deployments
- ✅ Automated rollback on deployment failures
- ✅ Security scanning and vulnerability detection
- ✅ Minimum 80% test coverage achieved

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- Flask documentation
- Docker best practices
- GitHub Actions documentation
- AWS EC2 deployment guides
