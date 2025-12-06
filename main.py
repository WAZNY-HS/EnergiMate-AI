"""
EnergiMate Ai - Smart Energy Saver Assistant
Main application with interactive CLI interface.
"""

import sys
from datetime import datetime
from appliances import ApplianceMonitor
from predictor import EnergyPredictor
from tips import EnergyTips
from cost_calculator import CostCalculator


class EnergiMateAI:
    """Main application class for EnergiMate Ai."""
    
    def __init__(self):
        self.monitor = ApplianceMonitor()
        self.predictor = EnergyPredictor(self.monitor)
        self.tips = EnergyTips()
        self.calculator = CostCalculator(self.monitor, self.predictor)
        self.running = True
        
        # Initialize with simulated data
        self.monitor.simulate_daily_usage(7)
    
    def print_header(self):
        """Print application header."""
        print("\n" + "="*60)
        print("  🔋 EnergiMate Ai - Smart Energy Saver Assistant")
        print("="*60)
    
    def print_menu(self):
        """Print main menu options."""
        print("\n📋 Available Commands:")
        print("  1. status          - View current appliance status")
        print("  2. usage           - View weekly energy usage summary")
        print("  3. suggestions     - Get energy-saving suggestions")
        print("  4. tips            - View weekly energy-saving tips")
        print("  5. costs           - View cost breakdown and savings")
        print("  6. turnon <name>   - Turn on an appliance")
        print("  7. turnoff <name>  - Turn off an appliance")
        print("  8. appliances      - List all appliances")
        print("  9. help            - Show this menu")
        print("  10. exit           - Exit the application")
        print()
    
    def handle_status(self):
        """Display current appliance status."""
        print("\n📊 Current Appliance Status:")
        print("-" * 60)
        status = self.monitor.get_current_status()
        
        for app_name, app_data in status.items():
            status_icon = "🟢 ON" if app_data['is_on'] else "🔴 OFF"
            print(f"  {app_name:25} {status_icon:8} "
                  f"({app_data['power_consumption']}W, {app_data['category']})")
    
    def handle_usage(self):
        """Display weekly usage summary."""
        print("\n📈 Weekly Energy Usage Summary:")
        print("-" * 60)
        summary = self.monitor.get_weekly_summary()
        
        print(f"  Total Energy Used:     {summary['total_energy_kwh']} kWh")
        print(f"  Total Cost:            ${summary['total_cost']:.2f}")
        print(f"  Average Daily Energy:  {summary['avg_daily_energy_kwh']} kWh")
        print(f"  Average Daily Cost:    ${summary['avg_daily_cost']:.2f}")
        
        print("\n  Top Energy Consumers:")
        breakdown = sorted(
            summary['appliance_breakdown'].items(),
            key=lambda x: x[1]['energy'],
            reverse=True
        )[:5]
        
        for app_name, data in breakdown:
            print(f"    • {app_name:25} {data['energy']:6.2f} kWh (${data['cost']:.2f})")
    
    def handle_suggestions(self):
        """Display energy-saving suggestions."""
        print("\n💡 Energy-Saving Suggestions:")
        print("-" * 60)
        suggestions = self.predictor.suggest_device_actions()
        
        if not suggestions:
            print("  ✅ Great! No immediate actions needed. All appliances are optimized.")
            return
        
        priority_icons = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}
        
        for i, suggestion in enumerate(suggestions, 1):
            icon = priority_icons.get(suggestion['priority'], '⚪')
            action = suggestion['action'].upper().replace('_', ' ')
            savings = suggestion['potential_savings']
            
            print(f"\n  {icon} Suggestion #{i} ({suggestion['priority'].upper()} Priority)")
            print(f"     Action: {action} {suggestion['appliance']}")
            print(f"     Reason: {suggestion['reason']}")
            if savings['energy_kwh'] > 0:
                print(f"     Potential Savings: {savings['energy_kwh']} kWh, ${savings['cost_dollars']:.2f}")
            else:
                print(f"     Potential Savings: ${savings['cost_dollars']:.2f} (off-peak rate)")
    
    def handle_tips(self):
        """Display weekly energy-saving tips."""
        print("\n💚 Weekly Energy-Saving Tips:")
        print("-" * 60)
        tips = self.tips.get_weekly_tips(5)
        
        for i, tip_data in enumerate(tips, 1):
            print(f"\n  Tip #{i} - {tip_data['category']}:")
            print(f"    {tip_data['tip']}")
    
    def handle_costs(self):
        """Display cost breakdown and savings estimates."""
        print("\n💰 Cost Analysis & Savings Potential:")
        print("-" * 60)
        
        # Current costs
        costs = self.calculator.calculate_current_costs()
        print("\n  Current Costs:")
        print(f"    Weekly:  ${costs['weekly_cost']:.2f} ({costs['weekly_energy_kwh']} kWh)")
        print(f"    Monthly: ${costs['monthly_estimate']:.2f}")
        print(f"    Yearly:  ${costs['yearly_estimate']:.2f}")
        
        # Potential savings
        savings = self.calculator.estimate_savings_from_suggestions()
        print("\n  Potential Savings (if suggestions followed):")
        print(f"    Weekly:  ${savings['weekly_cost_saved']:.2f} ({savings['weekly_energy_saved_kwh']} kWh)")
        print(f"    Monthly: ${savings['monthly_cost_saved']:.2f}")
        print(f"    Yearly:  ${savings['yearly_cost_saved']:.2f}")
        print(f"    Savings: {savings['savings_percentage']}% reduction")
        
        # Top cost contributors
        print("\n  Top Cost Contributors:")
        breakdown = self.calculator.get_cost_breakdown_by_appliance()[:5]
        for item in breakdown:
            print(f"    • {item['appliance']:25} ${item['weekly_cost']:6.2f} ({item['percentage_of_total']}%)")
    
    def handle_turn_on(self, args):
        """Handle turn on command."""
        if not args:
            print("❌ Error: Please specify an appliance name.")
            print("   Usage: turnon <appliance_name>")
            return
        
        name = ' '.join(args)
        if self.monitor.turn_on(name):
            appliance = self.monitor.get_appliance(name)
            print(f"✅ Turned ON: {appliance.name}")
        else:
            print(f"❌ Error: Appliance '{name}' not found.")
            print("   Use 'appliances' command to see available appliances.")
    
    def handle_turn_off(self, args):
        """Handle turn off command."""
        if not args:
            print("❌ Error: Please specify an appliance name.")
            print("   Usage: turnoff <appliance_name>")
            return
        
        name = ' '.join(args)
        if self.monitor.turn_off(name):
            appliance = self.monitor.get_appliance(name)
            print(f"✅ Turned OFF: {appliance.name}")
        else:
            print(f"❌ Error: Appliance '{name}' not found.")
            print("   Use 'appliances' command to see available appliances.")
    
    def handle_appliances(self):
        """List all available appliances."""
        print("\n🏠 Available Appliances:")
        print("-" * 60)
        for name, appliance in self.monitor.appliances.items():
            print(f"  • {appliance.name:25} ({appliance.power_consumption}W, {appliance.category})")
    
    def process_command(self, command: str):
        """Process user command."""
        parts = command.strip().lower().split()
        if not parts:
            return
        
        cmd = parts[0]
        args = parts[1:]
        
        if cmd == 'status':
            self.handle_status()
        elif cmd == 'usage':
            self.handle_usage()
        elif cmd == 'suggestions':
            self.handle_suggestions()
        elif cmd == 'tips':
            self.handle_tips()
        elif cmd == 'costs':
            self.handle_costs()
        elif cmd == 'turnon':
            self.handle_turn_on(args)
        elif cmd == 'turnoff':
            self.handle_turn_off(args)
        elif cmd == 'appliances':
            self.handle_appliances()
        elif cmd == 'help':
            self.print_menu()
        elif cmd == 'exit' or cmd == 'quit':
            self.running = False
            print("\n👋 Thank you for using EnergiMate Ai! Stay energy-efficient! 🌱\n")
        else:
            print(f"❌ Unknown command: {cmd}")
            print("   Type 'help' to see available commands.")
    
    def run(self):
        """Main application loop."""
        self.print_header()
        self.print_menu()
        
        while self.running:
            try:
                command = input("EnergiMate> ").strip()
                if command:
                    self.process_command(command)
            except KeyboardInterrupt:
                print("\n\n👋 Thank you for using EnergiMate Ai! Stay energy-efficient! 🌱\n")
                break
            except EOFError:
                print("\n\n👋 Thank you for using EnergiMate Ai! Stay energy-efficient! 🌱\n")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")


def main():
    """Entry point for the application."""
    app = EnergiMateAI()
    app.run()


if __name__ == "__main__":
    main()

