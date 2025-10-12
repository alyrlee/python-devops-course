#!/usr/bin/env python3
"""
Flask Web Application
A web interface for the Python DevOps project
"""

from flask import Flask, render_template, request, jsonify
import json
import sys
import os

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from cli.lambda_function import lambda_handler
from cli.helloclick import tokenize
from cli.gcli import search
from aws.cloudwatch_monitor import CloudWatchMonitor

app = Flask(__name__)

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/api/lambda', methods=['POST'])
def api_lambda():
    """Lambda function API endpoint"""
    try:
        data = request.get_json()
        name = data.get('name', 'World')
        
        # Call the Lambda function
        result = lambda_handler({'name': name}, {})
        
        return jsonify({
            'success': True,
            'result': result,
            'message': 'Lambda function executed successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Error executing Lambda function'
        }), 500

@app.route('/api/tokenize', methods=['POST'])
def api_tokenize():
    """Tokenize text API endpoint"""
    try:
        data = request.get_json()
        phrase = data.get('phrase', '')
        
        if not phrase:
            return jsonify({
                'success': False,
                'error': 'No phrase provided',
                'message': 'Please provide a phrase to tokenize'
            }), 400
        
        # Tokenize the phrase
        words = phrase.split()
        
        return jsonify({
            'success': True,
            'original': phrase,
            'tokenized': words,
            'count': len(words),
            'message': 'Text tokenized successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Error tokenizing text'
        }), 500

@app.route('/api/cloudwatch', methods=['GET'])
def api_cloudwatch():
    """CloudWatch metrics API endpoint"""
    try:
        monitor = CloudWatchMonitor()
        
        # Get function info
        function_info = monitor.get_lambda_function_info('python-devops-lambda')
        
        # Get metrics
        metrics = monitor.get_lambda_metrics('python-devops-lambda', 24)
        
        # Get recent logs
        logs = monitor.get_lambda_logs('python-devops-lambda', 1)
        
        return jsonify({
            'success': True,
            'function_info': function_info,
            'metrics': metrics,
            'recent_logs': logs[:5],  # Last 5 logs
            'message': 'CloudWatch data retrieved successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Error retrieving CloudWatch data'
        }), 500

@app.route('/api/health')
def api_health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Python DevOps Web API',
        'version': '1.0.0'
    })

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return jsonify({
        'success': False,
        'error': 'Not Found',
        'message': 'The requested resource was not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    return jsonify({
        'success': False,
        'error': 'Internal Server Error',
        'message': 'An internal server error occurred'
    }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
