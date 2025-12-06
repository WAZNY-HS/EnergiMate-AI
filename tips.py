"""
Energy-saving tips system with weekly recommendations.
"""

from typing import List, Dict
from datetime import datetime
import random


class EnergyTips:
    """Provides energy-saving tips and recommendations."""
    
    def __init__(self):
        self.tips_database = self._load_tips()
        self.weekly_tips = []
        self.last_updated = None
    
    def _load_tips(self) -> Dict[str, List[str]]:
        """Load categorized energy-saving tips."""
        return {
            'general': [
                "Unplug devices when not in use - many devices consume 'phantom' energy even when turned off",
                "Use power strips to easily turn off multiple devices at once",
                "Replace incandescent bulbs with LED bulbs - they use 75% less energy",
                "Set your thermostat 2-3 degrees higher in summer and lower in winter",
                "Use natural light during the day instead of artificial lighting",
                "Close curtains during hot days to keep your home cooler",
                "Open windows for natural ventilation instead of using AC when possible",
                "Use ceiling fans to help circulate air and reduce AC usage",
                "Seal windows and doors to prevent air leaks",
                "Regularly clean or replace air filters in HVAC systems"
            ],
            'appliances': [
                "Run your dishwasher only when it's full",
                "Use cold water for laundry - 90% of energy goes to heating water",
                "Clean the lint filter in your dryer after every load",
                "Don't open the refrigerator door frequently - each opening wastes energy",
                "Use a microwave instead of an oven for small meals - it's more efficient",
                "Defrost your freezer regularly to maintain efficiency",
                "Use the right-sized pot on stove burners - smaller pots waste energy",
                "Cook multiple items in the oven at once when possible",
                "Use a toaster oven for small items instead of a full oven",
                "Air dry dishes instead of using the dishwasher's heat dry cycle"
            ],
            'heating_cooling': [
                "Install a programmable thermostat to automatically adjust temperature",
                "Use zone heating/cooling - only heat or cool rooms you're using",
                "Maintain your HVAC system with regular professional checkups",
                "Use window coverings strategically - open in winter, closed in summer",
                "Insulate your home properly - good insulation can save 20-30% on energy",
                "Use a space heater for small areas instead of heating the whole house",
                "Keep air vents unobstructed by furniture",
                "Replace old HVAC systems with energy-efficient models",
                "Use exhaust fans in bathrooms and kitchens only when necessary",
                "Consider using a heat pump instead of traditional heating/cooling"
            ],
            'electronics': [
                "Enable power-saving modes on computers and devices",
                "Turn off monitors when not in use",
                "Use a smart power strip that cuts power to devices in standby mode",
                "Stream content on smaller devices when possible - TVs use more energy",
                "Adjust screen brightness - lower brightness uses less energy",
                "Unplug chargers when not actively charging devices",
                "Use sleep mode on computers instead of leaving them fully on",
                "Consider using a laptop instead of a desktop - laptops use less energy",
                "Turn off gaming consoles completely instead of leaving them in standby",
                "Use energy-efficient settings on all electronic devices"
            ],
            'seasonal': [
                "In summer: Use fans and natural ventilation before turning on AC",
                "In winter: Let sunlight in during the day, close curtains at night",
                "In spring/fall: Open windows instead of using HVAC systems",
                "Use weatherstripping to seal gaps around doors and windows",
                "Plant trees strategically to provide shade in summer",
                "Use a clothesline instead of a dryer when weather permits",
                "Adjust water heater temperature - 120°F is usually sufficient",
                "Use cold water for most laundry and dishwashing",
                "Take shorter showers to reduce water heating costs",
                "Insulate your water heater and pipes to reduce heat loss"
            ]
        }
    
    def get_weekly_tips(self, count: int = 5) -> List[Dict]:
        """Get a selection of weekly energy-saving tips."""
        if not self.weekly_tips or self._should_refresh_tips():
            self._generate_weekly_tips(count)
            self.last_updated = datetime.now()
        
        return self.weekly_tips
    
    def _should_refresh_tips(self) -> bool:
        """Check if tips should be refreshed (weekly)."""
        if self.last_updated is None:
            return True
        
        days_since_update = (datetime.now() - self.last_updated).days
        return days_since_update >= 7
    
    def _generate_weekly_tips(self, count: int):
        """Generate a new set of weekly tips."""
        all_tips = []
        for category, tips in self.tips_database.items():
            for tip in tips:
                all_tips.append({
                    'tip': tip,
                    'category': category.replace('_', ' ').title()
                })
        
        # Randomly select tips, ensuring variety
        selected = random.sample(all_tips, min(count, len(all_tips)))
        self.weekly_tips = selected
    
    def get_tips_by_category(self, category: str) -> List[str]:
        """Get tips for a specific category."""
        category_key = category.lower().replace(' ', '_')
        return self.tips_database.get(category_key, [])
    
    def get_personalized_tip(self, appliance_name: str) -> str:
        """Get a personalized tip based on a specific appliance."""
        appliance_tips = {
            'air conditioner': "Set your AC to 78°F when you're home and higher when away. Each degree can save 3-5% on cooling costs.",
            'refrigerator': "Keep your refrigerator at 37-40°F and freezer at 0-5°F. Don't overfill - air needs to circulate.",
            'washing machine': "Wash clothes in cold water - it saves energy and is gentler on fabrics. Only run full loads.",
            'television': "Enable auto-brightness and power-saving modes. Turn off completely when not watching.",
            'lights': "Switch to LED bulbs - they last 25 times longer and use 75% less energy than incandescent bulbs.",
            'laptop': "Use battery saver mode and reduce screen brightness. Unplug the charger when battery is full.",
            'heater': "Use a space heater only for the room you're in. Close doors to contain heat.",
            'microwave': "Use microwave for reheating - it's 3-4 times more efficient than an oven.",
            'dishwasher': "Run only when full, use energy-saving mode, and skip the heat dry cycle.",
            'gaming console': "Enable auto-shutdown after inactivity. Turn off completely instead of leaving in standby mode."
        }
        
        name_lower = appliance_name.lower()
        for key, tip in appliance_tips.items():
            if key in name_lower:
                return tip
        
        return "Unplug devices when not in use to avoid phantom energy consumption."

