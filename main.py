# main.py
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def run_csp_reminder():
    """Execute the CSP reminder script"""
    print("Running CSP Reminder...")
    print("-" * 40)
    
    # Import and run the CSP reminder module
    try:
        from scripts import csp_reminder
        # If the script has a main function, call it
        if hasattr(csp_reminder, 'main'):
            csp_reminder.main()
        else:
            # If no main function, the script likely runs on import
            print("CSP Reminder executed successfully")
    except Exception as e:
        print(f"Error running CSP Reminder: {e}")

def run_dip_threshold():
    """Execute the dip threshold script"""
    print("\nRunning Dip Threshold Check...")
    print("-" * 40)
    
    # Import and run the dip threshold module
    try:
        from scripts import dip_below_threshold
        # If the script has a main function, call it
        if hasattr(dip_below_threshold, 'main'):
            dip_below_threshold.main()
        else:
            # If no main function, the script likely runs on import
            print("Dip Threshold Check executed successfully")
    except Exception as e:
        print(f"Error running Dip Threshold Check: {e}")

def main():
    """Main function to execute both scripts"""
    print("Starting Stock Analysis Scripts")
    print("=" * 50)
    
    # Run CSP Reminder
    run_csp_reminder()
    
    # Run Dip Threshold Check
    run_dip_threshold()
    
    print("\n" + "=" * 50)
    print("All scripts completed!")

if __name__ == "__main__":
    main()