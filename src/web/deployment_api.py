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
        "url": "https://ephemeral.example.com",
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
        "url": "https://dev.example.com",
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
        "url": "https://staging.example.com",
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
        "url": "https://prod.example.com",
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
