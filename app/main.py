from app.monitor import get_process_stats, load_config
from app.utils import sort_processes, filter_processes, detect_anomalies, mark_child_processes
import argparse
import time


def main():
    config = load_config()
    interval = config.get("refresh_interval", 5)

    parser = argparse.ArgumentParser(description="Process Monitoring CLI")
    parser.add_argument("--sort", help="Sort by field: pid, name, cpu_percent, memory_percent")
    parser.add_argument("--desc", action="store_true", help="Sort descending")
    parser.add_argument("--filter", help="Filter by name (case-insensitive)")
    parser.add_argument("--anomaly", action="store_true", help="Show only processes exceeding CPU/MEM threshold")
    args = parser.parse_args()

    print(f"\nFetching process stats --- Press Ctrl+C to stop.\n")

    try:
        while True:
            stats = get_process_stats()

            stats = mark_child_processes(stats)

            if args.filter:
                stats = filter_processes(stats, args.filter)

            if args.sort:
                stats = sort_processes(stats, args.sort, reverse=args.desc)

            if args.anomaly:
                stats = detect_anomalies(stats)


            #print("=" * 60)
            print(f"{'PID':<8} {'NAME':<25} {'CPU%':<8} {'MEM%':<8} {'CHILD':<6}")
            print("-" * 70)

            for proc in stats:
                print(f"{proc['pid']:<8} {proc['name'][:24]:<25} {proc['cpu_percent']:<8.2f} {proc['memory_percent']:<8.2f} {str(proc.get('is_child', False)):<6}")

            print("=" * 70 + "\n")
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\nStopped monitoring.")


if __name__ == "__main__":
    main()
