#!/usr/bin/env python3
"""
Run the deployment dashboard
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from web.deployment_api import app

if __name__ == '__main__':
    print("🚀 Starting Deployment Dashboard...")
    print("📊 Dashboard will be available at: http://localhost:5001")
    print("🔗 API endpoints:")
    print("   - GET  /api/deployments - Get all deployment statuses")
    print("   - GET  /api/deployments/<env> - Get specific environment status")
    print("   - POST /api/deployments/<env>/status - Update environment status")
    print("   - GET  /api/health - Health check")
    print("   - GET  /api/summary - Deployment summary")
    print("\nPress Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
