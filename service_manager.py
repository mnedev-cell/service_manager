import subprocess
import sys
SERVICE_NAME = 'ping_service'
ENABLE_SERVICE = False  # Set to True to enable the service, False to disable it


def check_service_status(service_name):
    """Check the status of a systemd service."""
    try:
        result = subprocess.run(['sudo', 'systemctl', 'status', service_name],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if 'Active: active' in result.stdout:
            print(f"{service_name} is running.")
        elif 'inactive' in result.stdout:
            print(f"{service_name} is not running.")
        else:
            print(f"Unknown status for {service_name}.")
    except Exception as e:
        print(f"Error checking service status: {e}")
        sys.exit(1)


def enable_service(service_name):
    """Enable and start the service."""
    try:
        subprocess.run(['sudo', 'systemctl', 'enable', service_name], check=True)
        subprocess.run(['sudo', 'systemctl', 'start', service_name], check=True)
        print(f"{service_name} has been enabled and started.")
    except Exception as e:
        print(f"Error enabling service: {e}")


def disable_service(service_name):
    """Disable and stop the service."""
    try:
        subprocess.run(['sudo', 'systemctl', 'disable', service_name], check=True)
        subprocess.run(['sudo', 'systemctl', 'stop', service_name], check=True)
        print(f"{service_name} has been disabled and stopped.")
    except Exception as e:
        print(f"Error disabling service: {e}")


def main():
    """Main function to manage service based on configuration."""
    check_service_status(SERVICE_NAME)

    if ENABLE_SERVICE:
        enable_service(SERVICE_NAME)
    else:
        disable_service(SERVICE_NAME)


if __name__ == "__main__":
    main()