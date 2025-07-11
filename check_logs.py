import os

def check_log_folder():
    log_dir = os.path.expanduser("~/.pypop/logs")
    if not os.path.exists(log_dir):
        print("❌ Log folder does not exist. No logs found yet.")
        return
    
    files = sorted(os.listdir(log_dir))
    if not files:
        print("⚠️ No log files found in ~/.pypop/logs/")
        return
    
    print(f"✅ Found {len(files)} log files in ~/.pypop/logs/")
    for f in files[-2:]:  # Show last 2 logs
        path = os.path.join(log_dir, f)
        print(f"\n📄 Log: {f}")
        with open(path, "r") as file:
            content = file.read()
            print(content[:500] + ('...' if len(content) > 500 else ''))  # Preview

if __name__ == "__main__":
    check_log_folder()
