"""
EnergiMate Ai - Flask Backend API
RESTful API for the Smart Energy Saver Assistant
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from appliances import ApplianceMonitor
from predictor import EnergyPredictor
from tips import EnergyTips
from cost_calculator import CostCalculator

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)  # Enable CORS for frontend

# Initialize core components
monitor = ApplianceMonitor()
predictor = EnergyPredictor(monitor)
tips = EnergyTips()
calculator = CostCalculator(monitor, predictor)

# Initialize with simulated data
monitor.simulate_daily_usage(7)


@app.route('/')
def index():
    """Serve the main HTML page."""
    return app.send_static_file('index.html')


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get current status of all appliances."""
    try:
        status = monitor.get_current_status()
        return jsonify({
            'success': True,
            'data': status
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/usage', methods=['GET'])
def get_usage():
    """Get weekly energy usage summary."""
    try:
        summary = monitor.get_weekly_summary()
        return jsonify({
            'success': True,
            'data': summary
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/suggestions', methods=['GET'])
def get_suggestions():
    """Get energy-saving suggestions."""
    try:
        suggestions = predictor.suggest_device_actions()
        return jsonify({
            'success': True,
            'data': suggestions
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/tips', methods=['GET'])
def get_tips():
    """Get weekly energy-saving tips."""
    try:
        count = request.args.get('count', 5, type=int)
        tips_data = tips.get_weekly_tips(count)
        return jsonify({
            'success': True,
            'data': tips_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/costs', methods=['GET'])
def get_costs():
    """Get cost analysis and savings estimates."""
    try:
        costs = calculator.calculate_current_costs()
        savings = calculator.estimate_savings_from_suggestions()
        breakdown = calculator.get_cost_breakdown_by_appliance()
        
        return jsonify({
            'success': True,
            'data': {
                'current_costs': costs,
                'potential_savings': savings,
                'breakdown': breakdown
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/appliances', methods=['GET'])
def get_appliances():
    """Get list of all appliances."""
    try:
        appliances_list = []
        for name, appliance in monitor.appliances.items():
            appliances_list.append({
                'name': appliance.name,
                'power_consumption': appliance.power_consumption,
                'category': appliance.category,
                'is_on': appliance.is_on
            })
        return jsonify({
            'success': True,
            'data': appliances_list
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/appliances/<appliance_name>/turnon', methods=['POST'])
def turn_on_appliance(appliance_name):
    """Turn on an appliance."""
    try:
        success = monitor.turn_on(appliance_name)
        if success:
            appliance = monitor.get_appliance(appliance_name)
            return jsonify({
                'success': True,
                'message': f'{appliance.name} turned on successfully',
                'data': {
                    'name': appliance.name,
                    'is_on': appliance.is_on
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Appliance "{appliance_name}" not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/appliances/<appliance_name>/turnoff', methods=['POST'])
def turn_off_appliance(appliance_name):
    """Turn off an appliance."""
    try:
        success = monitor.turn_off(appliance_name)
        if success:
            appliance = monitor.get_appliance(appliance_name)
            return jsonify({
                'success': True,
                'message': f'{appliance.name} turned off successfully',
                'data': {
                    'name': appliance.name,
                    'is_on': appliance.is_on
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Appliance "{appliance_name}" not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/daily-usage', methods=['GET'])
def get_daily_usage():
    """Get daily usage history."""
    try:
        days = request.args.get('days', 7, type=int)
        history = monitor.simulate_daily_usage(days)
        return jsonify({
            'success': True,
            'data': history
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("🔋 Starting EnergiMate Ai Server...")
    print("📱 Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)

