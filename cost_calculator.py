"""
Cost calculation and savings estimation system.
"""

from typing import Dict, List
from appliances import ApplianceMonitor
from predictor import EnergyPredictor


class CostCalculator:
    """Calculates energy costs and potential savings."""
    
    def __init__(self, monitor: ApplianceMonitor, predictor: EnergyPredictor):
        self.monitor = monitor
        self.predictor = predictor
        self.electricity_rate = 0.15  # $0.15 per kWh (default)
    
    def calculate_current_costs(self) -> Dict:
        """Calculate current energy costs based on usage history."""
        if not self.monitor.usage_history:
            self.monitor.simulate_daily_usage(7)
        
        weekly_summary = self.monitor.get_weekly_summary()
        
        return {
            'weekly_cost': weekly_summary['total_cost'],
            'weekly_energy_kwh': weekly_summary['total_energy_kwh'],
            'daily_avg_cost': weekly_summary['avg_daily_cost'],
            'daily_avg_energy_kwh': weekly_summary['avg_daily_energy_kwh'],
            'monthly_estimate': round(weekly_summary['total_cost'] * 4, 2),
            'yearly_estimate': round(weekly_summary['total_cost'] * 52, 2),
            'appliance_breakdown': weekly_summary['appliance_breakdown']
        }
    
    def estimate_savings_from_suggestions(self) -> Dict:
        """Estimate savings if all suggestions are followed."""
        suggestions = self.predictor.suggest_device_actions()
        predictions = self.predictor.predict_weekly_savings()
        
        total_suggestions = len(suggestions)
        high_priority = sum(1 for s in suggestions if s['priority'] == 'high')
        
        return {
            'weekly_energy_saved_kwh': predictions['estimated_weekly_energy_saved_kwh'],
            'weekly_cost_saved': predictions['estimated_weekly_cost_saved'],
            'monthly_cost_saved': predictions['estimated_monthly_cost_saved'],
            'yearly_cost_saved': predictions['estimated_yearly_cost_saved'],
            'total_suggestions': total_suggestions,
            'high_priority_suggestions': high_priority,
            'savings_percentage': self._calculate_savings_percentage()
        }
    
    def _calculate_savings_percentage(self) -> float:
        """Calculate percentage of potential savings."""
        current_costs = self.calculate_current_costs()
        savings = self.predictor.predict_weekly_savings()
        
        if current_costs['weekly_cost'] > 0:
            percentage = (savings['estimated_weekly_cost_saved'] / current_costs['weekly_cost']) * 100
            return round(percentage, 1)
        return 0.0
    
    def get_cost_breakdown_by_appliance(self) -> List[Dict]:
        """Get cost breakdown sorted by highest consuming appliances."""
        costs = self.calculate_current_costs()
        breakdown = []
        
        for app_name, data in costs['appliance_breakdown'].items():
            percentage = (data['cost'] / costs['weekly_cost']) * 100 if costs['weekly_cost'] > 0 else 0
            breakdown.append({
                'appliance': app_name,
                'weekly_cost': round(data['cost'], 2),
                'weekly_energy_kwh': round(data['energy'], 2),
                'weekly_hours': round(data['hours'], 2),
                'percentage_of_total': round(percentage, 1)
            })
        
        # Sort by cost (highest first)
        breakdown.sort(key=lambda x: x['weekly_cost'], reverse=True)
        return breakdown
    
    def project_future_savings(self, months: int = 12) -> Dict:
        """Project savings over a period of months."""
        savings = self.estimate_savings_from_suggestions()
        monthly_savings = savings['monthly_cost_saved']
        
        cumulative = 0
        monthly_projection = []
        
        for month in range(1, months + 1):
            cumulative += monthly_savings
            monthly_projection.append({
                'month': month,
                'monthly_savings': round(monthly_savings, 2),
                'cumulative_savings': round(cumulative, 2)
            })
        
        return {
            'monthly_savings': monthly_savings,
            'total_over_period': round(cumulative, 2),
            'monthly_breakdown': monthly_projection
        }

