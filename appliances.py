"""
Appliance monitoring system with simulated usage patterns.
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class Appliance:
    """Represents a home appliance with its properties."""
    name: str
    power_consumption: float  # in watts
    is_on: bool = False
    usage_hours_per_day: float = 0.0
    last_used: Optional[datetime] = None
    category: str = "general"  # heating, cooling, lighting, entertainment, kitchen


class ApplianceMonitor:
    """Monitors appliance usage patterns and generates simulated data."""
    
    def __init__(self):
        self.appliances: Dict[str, Appliance] = {}
        self.usage_history: List[Dict] = []
        self._initialize_default_appliances()
    
    def _initialize_default_appliances(self):
        """Initialize with common household appliances."""
        default_appliances = [
            Appliance("Air Conditioner", 3500, False, 6.0, category="cooling"),
            Appliance("Refrigerator", 150, True, 24.0, category="kitchen"),
            Appliance("Washing Machine", 2000, False, 1.5, category="kitchen"),
            Appliance("Television", 150, False, 4.0, category="entertainment"),
            Appliance("LED Lights", 50, False, 8.0, category="lighting"),
            Appliance("Laptop", 50, False, 6.0, category="entertainment"),
            Appliance("Electric Heater", 2000, False, 3.0, category="heating"),
            Appliance("Microwave", 1000, False, 0.5, category="kitchen"),
            Appliance("Dishwasher", 1800, False, 1.5, category="kitchen"),
            Appliance("Gaming Console", 200, False, 2.0, category="entertainment"),
        ]
        
        for appliance in default_appliances:
            self.appliances[appliance.name.lower()] = appliance
    
    def simulate_daily_usage(self, days: int = 7) -> List[Dict]:
        """Simulate appliance usage for the past N days."""
        history = []
        base_date = datetime.now() - timedelta(days=days)
        
        for day in range(days):
            date = base_date + timedelta(days=day)
            daily_usage = {}
            total_energy = 0
            
            for name, appliance in self.appliances.items():
                # Simulate usage with some randomness
                if appliance.name == "Refrigerator":
                    # Refrigerator runs continuously
                    hours = 24
                else:
                    # Other appliances have variable usage
                    base_hours = appliance.usage_hours_per_day
                    hours = max(0, base_hours + random.uniform(-1, 1))
                
                energy_kwh = (appliance.power_consumption * hours) / 1000
                daily_usage[appliance.name] = {
                    'hours': round(hours, 2),
                    'energy_kwh': round(energy_kwh, 2),
                    'cost': round(energy_kwh * 0.15, 2)  # $0.15 per kWh
                }
                total_energy += energy_kwh
            
            history.append({
                'date': date.strftime('%Y-%m-%d'),
                'appliances': daily_usage,
                'total_energy_kwh': round(total_energy, 2),
                'total_cost': round(total_energy * 0.15, 2)
            })
        
        self.usage_history = history
        return history
    
    def get_current_status(self) -> Dict:
        """Get current status of all appliances."""
        status = {}
        for name, appliance in self.appliances.items():
            status[appliance.name] = {
                'is_on': appliance.is_on,
                'power_consumption_watts': appliance.power_consumption,
                'category': appliance.category
            }
        return status
    
    def get_appliance(self, name: str) -> Optional[Appliance]:
        """Get an appliance by name (case-insensitive)."""
        return self.appliances.get(name.lower())
    
    def turn_on(self, name: str) -> bool:
        """Turn on an appliance."""
        appliance = self.get_appliance(name)
        if appliance:
            appliance.is_on = True
            appliance.last_used = datetime.now()
            return True
        return False
    
    def turn_off(self, name: str) -> bool:
        """Turn off an appliance."""
        appliance = self.get_appliance(name)
        if appliance:
            appliance.is_on = False
            return True
        return False
    
    def get_weekly_summary(self) -> Dict:
        """Get weekly energy usage summary."""
        if not self.usage_history:
            self.simulate_daily_usage(7)
        
        weekly_data = self.usage_history[-7:] if len(self.usage_history) >= 7 else self.usage_history
        
        total_energy = sum(day['total_energy_kwh'] for day in weekly_data)
        total_cost = sum(day['total_cost'] for day in weekly_data)
        avg_daily = total_energy / len(weekly_data) if weekly_data else 0
        
        # Calculate per-appliance totals
        appliance_totals = {}
        for day in weekly_data:
            for app_name, app_data in day['appliances'].items():
                if app_name not in appliance_totals:
                    appliance_totals[app_name] = {'energy': 0, 'cost': 0, 'hours': 0}
                appliance_totals[app_name]['energy'] += app_data['energy_kwh']
                appliance_totals[app_name]['cost'] += app_data['cost']
                appliance_totals[app_name]['hours'] += app_data['hours']
        
        return {
            'total_energy_kwh': round(total_energy, 2),
            'total_cost': round(total_cost, 2),
            'avg_daily_energy_kwh': round(avg_daily, 2),
            'avg_daily_cost': round(avg_daily * 0.15, 2),
            'appliance_breakdown': appliance_totals
        }

