#!/usr/bin/env python3
import os
import sys
import subprocess
import time

# === Nmap Scan Puzzle ===

def find_project_root():
    dir_path = os.path.abspath(os.path.dirname(__file__))
    while dir_path != "/":
        if os.path.exists(os.path.join(dir_path, ".ccri_ctf_root")):
            return dir_path
        dir_path = os.path.dirname(dir_path)
    print("❌ ERROR: Could not find project root marker (.ccri_ctf_root).", file=sys.stderr)
    sys.exit(1)

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    input(prompt)

def run_nmap_scan():
    print("\n📡 Running: nmap -sV --version-light -p8000-8100 localhost\n")
    try:
        result = subprocess.run(
            ["nmap", "-sV", "--version-light", "-p8000-8100", "localhost"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )
        return result.stdout
    except FileNotFoundError:
        print("❌ ERROR: nmap is not installed.")
        sys.exit(1)

def extract_open_ports(scan_output):
    ports = []
    for line in scan_output.splitlines():
        if "open" in line:
            try:
                port = line.split("/")[0].strip()
                ports.append(port)
            except Exception:
                continue
    return ports

def fetch_service_name(port):
    try:
        headers = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-D", "-", f"http://localhost:{port}"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )
        for line in headers.stdout.splitlines():
            if "X-Service-Name" in line:
                return line.split(":", 1)[1].strip()
        return "unknown"
    except FileNotFoundError:
        print("❌ ERROR: curl is not installed.")
        sys.exit(1)

def fetch_port_response(port):
    try:
        result = subprocess.run(
            ["curl", "-s", f"http://localhost:{port}"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )
        return result.stdout
    except FileNotFoundError:
        print("❌ ERROR: curl is not installed.")
        sys.exit(1)

def main():
    project_root = find_project_root()
    script_dir = os.path.abspath(os.path.dirname(__file__))
    os.chdir(script_dir)

    clear_screen()
    print("🛰️ Nmap Scan Puzzle")
    print("--------------------------------------\n")
    print("Several simulated services are running locally (inside your CTF app).\n")
    print("🎯 Your goal: Scan localhost (127.0.0.1) for open ports in the range 8000–8100, and find the REAL flag.")
    print("⚠️ Some ports contain random junk responses. Only one flag is correct.\n")
    print("🔧 Under the hood:")
    print("   We'll use 'nmap' to scan the ports and see what services respond.")
    print("   Then we'll query each open port for its reported service name.\n")

    pause()

    scan_output = run_nmap_scan()
    clear_screen()
    print("📝 Nmap Scan Results:")
    print("--------------------------------------")
    print(scan_output)
    print("\n✅ Scan complete.\n")

    pause("📖 Review the scan results above. Press ENTER to explore the open ports interactively...")

    open_ports = extract_open_ports(scan_output)

    if not open_ports:
        print("❌ No open ports found in the range 8000–8100.")
        pause("Press ENTER to exit...")
        sys.exit(1)

    # Build port-to-service map
    port_services = {}
    for port in open_ports:
        service_name = fetch_service_name(port)
        port_services[port] = service_name

    # Interactive exploration
    while True:
        clear_screen()
        print("--------------------------------------")
        print("Open ports detected:")
        for idx, port in enumerate(open_ports, 1):
            service = port_services[port]
            print(f"{idx:2d}. {port} ({service})")
        print(f"{len(open_ports)+1:2d}. Exit\n")

        try:
            choice = int(input(f"Select a port to explore (1-{len(open_ports)+1}): ").strip())
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
            time.sleep(1)
            continue

        if 1 <= choice <= len(open_ports):
            port = open_ports[choice - 1]
            service = port_services[port]
            print(f"\n🌐 Connecting to http://localhost:{port} ...")
            print(f"Service: {service}")
            print("--------------------------------------")
            response = fetch_port_response(port)

            if not response.strip():
                print(f"❌ No response received from port {port}.")
            else:
                print(response)

            print("--------------------------------------\n")

            while True:
                print("Options:")
                print("1. 🔁 Return to port list")
                print("2. 💾 Save this response to nmap_flag_response.txt\n")

                sub_choice = input("Choose an option (1-2): ").strip()
                if sub_choice == "1":
                    break
                elif sub_choice == "2":
                    out_file = os.path.join(script_dir, "nmap_flag_response.txt")
                    with open(out_file, "a") as f:
                        f.write(f"Port: {port}\nService: {service}\nResponse:\n{response}\n")
                        f.write("--------------------------------------\n")
                    print(f"✅ Response saved to {out_file}")
                    time.sleep(1)
                    break
                else:
                    print("❌ Invalid choice. Please select 1 or 2.")
                    time.sleep(1)

        elif choice == len(open_ports)+1:
            print("\n👋 Exiting helper. Return to the CTF portal to submit your flag.")
            break
        else:
            print("❌ Invalid choice. Please select a valid port.")
            time.sleep(1)

if __name__ == "__main__":
    main()
