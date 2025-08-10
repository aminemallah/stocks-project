import subprocess
import time
import sys

def run_script(script_path):
    while True:
        try:
            result = subprocess.run([sys.executable, script_path], check=False)
            if result.returncode == 0:
                print("Script executed successfully!")
                break
            else:
                print(f"Script failed with exit code {result.returncode}. Retrying in 60 seconds...")
                time.sleep(300)
                
        except Exception as e:
            print(f"Error running script: {e}. Retrying in 60 seconds...")
            time.sleep(300)

if __name__ == "__main__":
    script_to_run = "scripts/x_fetch_followers.py"
    run_script(script_to_run)