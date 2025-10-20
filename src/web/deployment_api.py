#!/usr/bin/env python3
"""
Deployment API for the Python DevOps Course application
Provides endpoints for deployment status and dashboard
"""

import os
from datetime import datetime
from flask import Flask, render_template, jsonify, request
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

app = Flask(__name__)

# Sample deployment data - in a real app, this would come from a database
DEPLOYMENT_DATA = {
    "ephemeral": {
        "name": "Ephemeral",
        "status": "success",
        "region": "us-east-1",
        "url": "http://localhost:5001/environments/ephemeral",
        "lastDeployed": "2024-01-15 14:30:00",
        "duration": "2m 15s",
        "commit": "abc1234",
        "branch": "dev",
        "deployedBy": "GitHub Actions"
    },
    "dev": {
        "name": "Development",
        "status": "success",
        "region": "us-east-1",
        "url": "http://localhost:5001/environments/dev",
        "lastDeployed": "2024-01-15 14:25:00",
        "duration": "3m 45s",
        "commit": "def5678",
        "branch": "dev",
        "deployedBy": "GitHub Actions"
    },
    "staging": {
        "name": "Staging",
        "status": "pending",
        "region": "us-east-1",
        "url": "http://localhost:5001/environments/staging",
        "lastDeployed": "2024-01-15 14:20:00",
        "duration": "4m 30s",
        "commit": "ghi9012",
        "branch": "main",
        "deployedBy": "GitHub Actions"
    },
    "prod": {
        "name": "Production",
        "status": "failure",
        "region": "us-west-2",
        "url": "http://localhost:5001/environments/prod",
        "lastDeployed": "2024-01-15 14:15:00",
        "duration": "5m 10s",
        "commit": "jkl3456",
        "branch": "main",
        "deployedBy": "GitHub Actions"
    }
}

@app.route('/')
def dashboard():
    """Serve the deployment dashboard"""
    return render_template('deployment-dashboard.html')

@app.route('/environments/<environment>')
def environment_page(environment):
    """Serve environment-specific pages"""
    if environment not in DEPLOYMENT_DATA:
        return f"Environment '{environment}' not found", 404
    
    env_data = DEPLOYMENT_DATA[environment]
    
    # Create a simple environment page
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{env_data['name']} Environment</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                background: white;
                border-radius: 12px;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
                overflow: hidden;
            }}
            .header {{
                background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }}
            .content {{
                padding: 30px;
            }}
            .status-badge {{
                display: inline-block;
                padding: 8px 16px;
                border-radius: 20px;
                font-weight: 600;
                text-transform: uppercase;
                margin: 10px 0;
            }}
            .status-badge.success {{
                background: #27ae60;
                color: white;
            }}
            .status-badge.failure {{
                background: #e74c3c;
                color: white;
            }}
            .status-badge.pending {{
                background: #f39c12;
                color: white;
            }}
            .info-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin: 20px 0;
            }}
            .info-card {{
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                border-left: 4px solid #3498db;
            }}
            .info-label {{
                color: #7f8c8d;
                font-weight: 500;
                margin-bottom: 5px;
            }}
            .info-value {{
                color: #2c3e50;
                font-weight: 600;
                font-size: 1.1rem;
            }}
            .back-btn {{
                background: #3498db;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                cursor: pointer;
                font-size: 1rem;
                text-decoration: none;
                display: inline-block;
                margin-top: 20px;
            }}
            .back-btn:hover {{
                background: #2980b9;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 {env_data['name']} Environment</h1>
                <div class="status-badge {env_data['status']}">{env_data['status']}</div>
            </div>
            <div class="content">
                <div class="info-grid">
                    <div class="info-card">
                        <div class="info-label">Region</div>
                        <div class="info-value">{env_data['region']}</div>
                    </div>
                    <div class="info-card">
                        <div class="info-label">Last Deployed</div>
                        <div class="info-value">{env_data['lastDeployed']}</div>
                    </div>
                    <div class="info-card">
                        <div class="info-label">Duration</div>
                        <div class="info-value">{env_data['duration']}</div>
                    </div>
                    <div class="info-card">
                        <div class="info-label">Commit</div>
                        <div class="info-value">{env_data['commit']}</div>
                    </div>
                    <div class="info-card">
                        <div class="info-label">Branch</div>
                        <div class="info-value">{env_data['branch']}</div>
                    </div>
                    <div class="info-card">
                        <div class="info-label">Deployed By</div>
                        <div class="info-value">{env_data['deployedBy']}</div>
                    </div>
                </div>
                <a href="/" class="back-btn">← Back to Dashboard</a>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

@app.route('/api/deployments')
def get_deployments():
    """Get deployment status for all environments"""
    return jsonify(DEPLOYMENT_DATA)

@app.route('/api/deployments/<environment>')
def get_deployment(environment):
    """Get deployment status for a specific environment"""
    if environment not in DEPLOYMENT_DATA:
        return jsonify({"error": "Environment not found"}), 404
    
    return jsonify(DEPLOYMENT_DATA[environment])

@app.route('/api/deployments/<environment>/status', methods=['POST'])
def update_deployment_status(environment):
    """Update deployment status for an environment"""
    if environment not in DEPLOYMENT_DATA:
        return jsonify({"error": "Environment not found"}), 404
    
    data = request.get_json()
    if not data or 'status' not in data:
        return jsonify({"error": "Status is required"}), 400
    
    # Update the deployment data
    DEPLOYMENT_DATA[environment].update({
        "status": data['status'],
        "lastDeployed": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "commit": data.get('commit', DEPLOYMENT_DATA[environment]['commit']),
        "branch": data.get('branch', DEPLOYMENT_DATA[environment]['branch']),
        "deployedBy": data.get('deployedBy', 'Manual Update')
    })
    
    return jsonify(DEPLOYMENT_DATA[environment])

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

@app.route('/api/summary')
def get_summary():
    """Get deployment summary statistics"""
    stats = {}
    for env_data in DEPLOYMENT_DATA.values():
        status = env_data['status']
        stats[status] = stats.get(status, 0) + 1
    
    return jsonify({
        "total": len(DEPLOYMENT_DATA),
        "successful": stats.get('success', 0),
        "failed": stats.get('failure', 0),
        "pending": stats.get('pending', 0),
        "last_updated": datetime.now().isoformat()
    })

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    os.makedirs(templates_dir, exist_ok=True)
    
    # Move the HTML file to templates directory
    html_file = os.path.join(os.path.dirname(__file__), 'deployment-dashboard.html')
    template_file = os.path.join(templates_dir, 'deployment-dashboard.html')
    if os.path.exists(html_file) and not os.path.exists(template_file):
        os.rename(html_file, template_file)
    
    app.run(debug=True, host='0.0.0.0', port=5001)
