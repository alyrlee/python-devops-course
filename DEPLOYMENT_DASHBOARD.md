# 🚀 Deployment Dashboard

A modern, responsive web interface for monitoring deployment status across all environments.

## Features

- **Real-time Status**: View deployment status for all environments (ephemeral, dev, staging, prod)
- **Visual Indicators**: Color-coded status badges (success, failure, pending)
- **Environment Details**: Region, last deployed time, duration, commit hash
- **Summary Statistics**: Overview of successful, failed, and pending deployments
- **Responsive Design**: Works on desktop and mobile devices
- **API Integration**: RESTful API for deployment status management

## Quick Start

### 1. Install Dependencies

```bash
pip install flask
```

### 2. Run the Dashboard

```bash
python run_dashboard.py
```

### 3. Access the Dashboard

Open your browser and navigate to:
- **Dashboard**: http://localhost:5000
- **API Health**: http://localhost:5000/api/health

## API Endpoints

### Get All Deployments
```bash
curl http://localhost:5000/api/deployments
```

### Get Specific Environment
```bash
curl http://localhost:5000/api/deployments/ephemeral
```

### Update Environment Status
```bash
curl -X POST http://localhost:5000/api/deployments/ephemeral/status \
  -H "Content-Type: application/json" \
  -d '{"status": "success", "commit": "abc1234"}'
```

### Get Summary Statistics
```bash
curl http://localhost:5000/api/summary
```

## Environment Statuses

- **🟢 Success**: Deployment completed successfully
- **🔴 Failure**: Deployment failed
- **🟡 Pending**: Deployment in progress

## Dashboard Features

### Environment Cards
Each environment shows:
- Environment name and status
- AWS region
- Last deployment time
- Deployment duration
- Commit hash
- Direct link to environment

### Summary Statistics
- Total deployments
- Successful deployments
- Failed deployments
- Pending deployments

### Real-time Updates
- Refresh button to update status
- Last updated timestamp
- Automatic data fetching from API

## Customization

### Adding New Environments
Edit `src/web/deployment_api.py` and add new environments to `DEPLOYMENT_DATA`:

```python
"new-env": {
    "name": "New Environment",
    "status": "success",
    "region": "us-west-2",
    "url": "http://localhost:5001/environments/new-env",
    "lastDeployed": "2024-01-15 14:30:00",
    "duration": "2m 15s",
    "commit": "abc1234",
    "branch": "main",
    "deployedBy": "GitHub Actions"
}
```

### Styling
The dashboard uses modern CSS with:
- Gradient backgrounds
- Card-based layout
- Responsive grid system
- Smooth animations
- Color-coded status indicators

## Integration with CI/CD

The dashboard can be integrated with your CI/CD pipeline by:

1. **Updating Status**: POST to `/api/deployments/<env>/status` when deployments complete
2. **Webhook Integration**: Set up webhooks to automatically update status
3. **GitHub Actions**: Use the API to update deployment status from workflows

## Development

### File Structure
```
src/web/
├── deployment_api.py          # Flask API server
├── templates/
│   └── deployment-dashboard.html  # Dashboard HTML template
└── run_dashboard.py           # Dashboard runner script
```

### Adding New Features
1. Update the Flask API in `deployment_api.py`
2. Modify the HTML template in `templates/deployment-dashboard.html`
3. Add new API endpoints as needed
4. Update the JavaScript for new functionality

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Kill existing process
   lsof -ti:5000 | xargs kill -9
   ```

2. **Template Not Found**
   ```bash
   # Ensure templates directory exists
   mkdir -p src/web/templates
   ```

3. **API Not Responding**
   ```bash
   # Check if Flask is running
   curl http://localhost:5000/api/health
   ```

## Production Deployment

For production use:

1. **Use a Production WSGI Server**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 src.web.deployment_api:app
   ```

2. **Set Environment Variables**:
   ```bash
   export FLASK_ENV=production
   export FLASK_DEBUG=False
   ```

3. **Use a Reverse Proxy** (nginx/Apache) for SSL and load balancing

4. **Database Integration**: Replace in-memory data with a real database

## License

This project is part of the Python DevOps Course and is available under the MIT License.
