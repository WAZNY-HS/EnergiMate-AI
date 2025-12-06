"""
Prediction and rules engine for suggesting when to turn devices on/off.
"""

from datetime import datetime, time
from typing import List, Dict, Optional
from appliances import ApplianceMonitor, Appliance


class EnergyPredictor:
    """Uses rules and patterns to predict optimal device usage."""
    
    def __init__(self, monitor: ApplianceMonitor):
        self.monitor = monitor
        self.electricity_rate = 0.15  # $0.15 per kWh
        self.peak_hours = (time(17, 0), time(21, 0))  # 5 PM - 9 PM
    
    def is_peak_hour(self, current_time: Optional[datetime] = None) -> bool:
        """Check if current time is during peak hours."""
        if current_time is None:
            current_time = datetime.now()
        
        current = current_time.time()
        peak_start, peak_end = self.peak_hours
        
        if peak_start <= peak_end:
            return peak_start <= current <= peak_end
        else:  # Handles overnight peak hours
            return current >= peak_start or current <= peak_end
    
    def suggest_device_actions(self) -> List[Dict]:
        """Generate suggestions for turning devices on/off based on rules."""
        suggestions = []
        current_time = datetime.now()
        is_peak = self.is_peak_hour(current_time)
        
        for name, appliance in self.monitor.appliances.items():
            suggestion = None
            
            # Rule 1: Turn off devices that are on but shouldn't be
            if appliance.is_on:
                # Refrigerator should stay on
                if appliance.name == "Refrigerator":
                    continue
                
                # Check if device has been on for too long
                if appliance.last_used:
                    hours_on = (current_time - appliance.last_used).total_seconds() / 3600
                    if hours_on > appliance.usage_hours_per_day:
                        suggestion = {
                            'action': 'turn_off',
                            'appliance': appliance.name,
                            'reason': f'Device has been on for {hours_on:.1f} hours, exceeding typical daily usage of {appliance.usage_hours_per_day} hours',
                            'potential_savings': self._calculate_savings(appliance, 'off'),
                            'priority': 'high'
                        }
            
            # Rule 2: Suggest turning off high-consumption devices during peak hours
            if appliance.is_on and is_peak and appliance.power_consumption > 1000:
                if appliance.name != "Refrigerator":
                    suggestion = {
                        'action': 'turn_off',
                        'appliance': appliance.name,
                        'reason': f'Peak hours detected (5 PM - 9 PM). High consumption device should be turned off to save on peak rates',
                        'potential_savings': self._calculate_savings(appliance, 'off', peak_multiplier=1.5),
                        'priority': 'medium'
                    }
            
            # Rule 3: Suggest optimal times for high-consumption appliances
            if not appliance.is_on and appliance.power_consumption > 1000:
                if not is_peak:
                    suggestion = {
                        'action': 'turn_on',
                        'appliance': appliance.name,
                        'reason': f'Current time is off-peak. Good time to use high-consumption device',
                        'potential_savings': self._calculate_savings(appliance, 'on', peak_multiplier=0.7),
                        'priority': 'low'
                    }
            
            # Rule 4: Check for idle devices
            if appliance.is_on and appliance.last_used:
                idle_hours = (current_time - appliance.last_used).total_seconds() / 3600
                if idle_hours > 2 and appliance.name not in ["Refrigerator"]:
                    suggestion = {
                        'action': 'turn_off',
                        'appliance': appliance.name,
                        'reason': f'Device appears to be idle for {idle_hours:.1f} hours',
                        'potential_savings': self._calculate_savings(appliance, 'off'),
                        'priority': 'high'
                    }
            
            if suggestion:
                suggestions.append(suggestion)
        
        # Sort by priority (high -> medium -> low)
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        suggestions.sort(key=lambda x: priority_order.get(x['priority'], 3))
        
        return suggestions
    
    def _calculate_savings(self, appliance: Appliance, action: str, 
                          hours: float = 1.0, peak_multiplier: float = 1.0) -> Dict:
        """Calculate potential savings from an action."""
        if action == 'turn_off':
            # Savings from turning off
            energy_saved = (appliance.power_consumption * hours) / 1000  # kWh
            cost_saved = energy_saved * self.electricity_rate * peak_multiplier
        else:  # turn_on (scheduling for off-peak)
            # Savings from using off-peak rates
            energy_used = (appliance.power_consumption * hours) / 1000
            peak_cost = energy_used * self.electricity_rate * 1.5
            off_peak_cost = energy_used * self.electricity_rate * 0.7
            cost_saved = peak_cost - off_peak_cost
            energy_saved = 0  # No energy saved, just cost
        
        return {
            'energy_kwh': round(energy_saved, 3),
            'cost_dollars': round(cost_saved, 2),
            'hours': hours
        }
    
    def predict_weekly_savings(self) -> Dict:
        """Predict potential weekly savings if all suggestions are followed."""
        weekly_suggestions = []
        total_energy_saved = 0
        total_cost_saved = 0
        
        # Simulate following suggestions for a week
        for day in range(7):
            daily_suggestions = self.suggest_device_actions()
            for suggestion in daily_suggestions:
                if suggestion['action'] == 'turn_off':
                    appliance = self.monitor.get_appliance(suggestion['appliance'])
                    if appliance:
                        savings = suggestion['potential_savings']
                        total_energy_saved += savings['energy_kwh']
                        total_cost_saved += savings['cost_dollars']
        
        return {
            'estimated_weekly_energy_saved_kwh': round(total_energy_saved, 2),
            'estimated_weekly_cost_saved': round(total_cost_saved, 2),
            'estimated_monthly_cost_saved': round(total_cost_saved * 4, 2),
            'estimated_yearly_cost_saved': round(total_cost_saved * 52, 2)
        }

