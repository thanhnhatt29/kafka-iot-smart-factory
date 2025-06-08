import subprocess
import argparse
import threading
import time

def start_producer_instance(script_path, instance_num):
    """Starts a single producer instance and prints status."""
    print(f"Starting {script_path} instance {instance_num}...")
    try:
        # Use Popen to start the process without blocking
        process = subprocess.Popen(['python', script_path])
        return process
    except FileNotFoundError:
        print(f"Error: Script not found at {script_path}")
        return None
    except Exception as e:
        print(f"Error starting {script_path} instance {instance_num}: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run multiple producer instances in parallel")
    parser.add_argument('--count', type=int, default=1, help="Number of instances per producer type")
    args = parser.parse_args()

    producer_scripts = [
        'producer/temperature_producer.py',
        'producer/humidity_producer.py',
        'producer/vibration_producer.py'
    ]

    all_processes = []

    print(f"Starting {args.count} instance(s) for each producer type in parallel...")

    # Start all producer instances
    for script in producer_scripts:
        for i in range(args.count):
            process = start_producer_instance(script, i + 1)
            if process:
                all_processes.append(process)

    print(f"\n{len(all_processes)} producer instances have been started.")
    print("Waiting for all producers to complete...")

    # Wait for all started processes to complete
    for process in all_processes:
        try:
            # Using wait() is often sufficient if you don't need stdout/stderr
            process.wait()
            # Or use communicate() if you need to capture output/errors later
            # stdout, stderr = process.communicate()
            # if process.returncode != 0:
            #    print(f"A producer instance exited with error code {process.returncode}.")
            #    if stderr:
            #       print(f"Error output: {stderr.decode()}")
        except Exception as e:
            print(f"Error waiting for a process: {e}")


    print("\n✅ All producer instances have completed.")