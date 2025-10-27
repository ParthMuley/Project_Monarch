# monarch_core/cli.py
import argparse
import os
from .monarch import Monarch # Relative import for sibling module
from dotenv import load_dotenv

# Define base directory (one level up from this script)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(BASE_DIR, 'configs')
DATA_DIR = os.path.join(BASE_DIR, 'data')

def main():
    load_dotenv(override=True) # Load .env file from the root

    parser = argparse.ArgumentParser(
        prog="Project Monarch",
        description="An autonomous, multi-guild agent organization.",
        epilog="Provide a detailed task prompt for the agent army to execute."
    ) # Keep parser setup
    parser.add_argument(
        "--prompt",  # Use a flag
        type=str,
        required=True,  # Make it mandatory
        help="The main task or prompt you want the agent army to work on."
    )

    args = parser.parse_args()

    # Pass the correct paths to Monarch
    monarch_controller = Monarch(
        army_file=os.path.join(DATA_DIR, "army.json"),
        guild_config_file=os.path.join(CONFIG_DIR, "guilds.json"),
        main_config_file=os.path.join(CONFIG_DIR, "config.json")
    )

    print("\n" + "="*50)
    print(f"\n[USER JOB]: {args.prompt}")
    final_product, _ = monarch_controller.execute_job(args.prompt)

    # --- ADD THIS PRINT LOGIC BACK ---
    print("\n--------------------------")
    if final_product:
        print("\n--- MONARCH'S FINAL DELIVERABLE ---")
        print(final_product)
    else:
        print("The job could not be completed.")
    # --- END OF ADDED LOGIC ---

    # ... (rest of the print and save logic) ...
    monarch_controller.save_army()
    monarch_controller.save_configs()

if __name__ == "__main__":
    main()