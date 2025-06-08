import subprocess
import argparse

def run_producers(producer_script, num_instances):
    processes = []
    
    for i in range(num_instances):
        print(f"Starting {producer_script} instance {i + 1}...")
        process = subprocess.Popen(['python', producer_script])
        processes.append(process)
    
    for process in processes:
        process.communicate()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run multiple producer instances")
    parser.add_argument('--count', type=int, default=1, help="Number of instances per producer type")
    args = parser.parse_args()

    # Run each type of producer with the specified count
    run_producers('producer/temperature_producer.py', args.count)
    run_producers('producer/humidity_producer.py', args.count)
    run_producers('producer/vibration_producer.py', args.count)

    print("✅ All producers have been started.")
