# main.py
import argparse
from monarch import Monarch

def main():
    """
    Main function to run the Monarch CLI.
    """
    # 1. Set up the argument parser
    parser = argparse.ArgumentParser(
        prog="Project Monarch",
        description="An autonomous, multi-guild agent organization.",
        epilog="Provide a detailed task prompt for the agent army to execute."
    )

    # 2. Define the command-line arguments
    parser.add_argument(
        "prompt",  # The name of the argument
        type=str,
        help="The main task or prompt you want the agent army to work on."
    )

    # 3. Parse the arguments from the command line
    args = parser.parse_args()

    # 4. Initialize and run the Monarch system
    monarch_controller = Monarch()
    print("\n" + "="*50)
    print(f"\n[USER JOB]: {args.prompt}")

    final_product, _ = monarch_controller.execute_job(args.prompt)

    print("\n--------------------------")
    if final_product:
        print("\n--- MONARCH'S FINAL DELIVERABLE ---")
        print(final_product)
    else:
        print("The job could not be completed.")

    print("\n" + "="*50)
    monarch_controller.save_army()
    monarch_controller.save_configs()

if __name__ == "__main__":
    main()