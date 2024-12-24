# Flask Question-Answer API

A robust question-answer system built with Flask, OpenAI, and PostgreSQL, deployed on AWS ECS. The system processes user questions through OpenAI's API and stores Q&A pairs in PostgreSQL.

## Quick Start

1. Clone the repository:
   ```bash
   git clone git@github.com:savannahtech/insait-tofunmi.git flask-api
   cd flask-api
   ```

2. Set up and run the project:
   ```bash
   make setup  # Creates .env file from template
   # Edit .env with your configurations
   make build  # Builds Docker containers
   make run    # Starts the application
   ```

3. Access the API documentation at http://localhost:5000/api/docs

## Configuration

1. Configure your `.env` file with the following variables:
   ```env
   POSTGRES_USER=your_db_user
   POSTGRES_PASSWORD=your_db_password
   POSTGRES_DB=your_db_name
   SECRET_KEY=your_secret_key
   OPENAI_API_KEY=your_openai_api_key
   DATABASE_URL=postgresql://your_db_user:your_db_password@localhost:5435/your_db_name
   ```

## Development Commands

```bash
# Build and start containers
make build
make run

# Database operations
make migrate-init    # Initialize migrations
make migrate        # Create new migration
make upgrade        # Apply migrations

# Testing
make test          # Run pytest suite

# Maintenance
make clean         # Remove containers and cleanup
make logs          # View application logs
```

## Deployment

### Container Registry
- Docker images are stored on DockerHub
- Registry: [oluwatofunmi/question-answer](https://hub.docker.com/repository/docker/oluwatofunmi/question-answer/general)

### CI/CD Pipeline
- Automated deployments via GitHub Actions
- Pipeline: [GitHub Actions Workflow](https://github.com/21toffy/flask-api/actions/workflows/cicd.yaml)
- Triggers on:
  - Push to main branch
  - Merge requests to main

### Production Deployment
- Deployed on AWS ECS Fargate
- API URL: http://98.81.125.248:5000/api/docs/
- Note: Currently using HTTP (not HTTPS)

## Testing

The project uses pytest for testing. Tests cover:
- API endpoints
- Database interactions
- Core functionality

Run tests with:
```bash
make test
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests: `make test`
4. Submit a pull request

