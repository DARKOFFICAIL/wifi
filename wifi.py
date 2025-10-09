# DARK_OFFICAIL Network Monitor
import os
import socket
import requests
import subprocess
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def banner():
    art = """
██████╗  █████╗ ██████╗ ██╗  ██╗    ███╗   ██╗ █████╗ ██████╗ 
██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝    ████╗  ██║██╔══██╗██╔══██╗
██████╔╝███████║██████╔╝█████╔╝     ██╔██╗ ██║███████║██████╔╝
██╔═══╝ ██╔══██║██╔══██╗██╔═██╗     ██║╚██╗██║██╔══██║██╔══██╗
██║     ██║  ██║██║  ██║██║  ██╗    ██║ ╚████║██║  ██║██║  ██║
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝    ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝
         Network Monitor By DARK_OFFICAIL
    """
    console.print(Panel(art, style="bold magenta"))

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "Unknown"

def get_external_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except Exception:
        return "Unknown"

def scan_devices():
    console.print("\n[bold cyan]Scanning connected devices...[/bold cyan]")
    devices = []
    try:
        result = subprocess.check_output("arp -a", shell=True).decode()
        lines = result.split('\n')
        for line in lines:
            if line:
                devices.append(line)
    except Exception:
        devices.append("Could not scan devices.")
    table = Table(title="Connected Devices (ARP)")
    table.add_column("Device Info")
    for d in devices:
        table.add_row(d)
    console.print(table)

def internet_speed():
    console.print("\n[bold cyan]Testing Internet Speed...[/bold cyan]")
    try:
        import speedtest
    except ImportError:
        console.print("[yellow]Speedtest module not found. Installing...[/yellow]")
        os.system("pip install speedtest-cli")
        import speedtest
    st = speedtest.Speedtest()
    download = st.download() / 1_000_000
    upload = st.upload() / 1_000_000
    table = Table(title="Internet Speed (Mbps)")
    table.add_column("Type")
    table.add_column("Speed")
    table.add_row("Download", f"{download:.2f}")
    table.add_row("Upload", f"{upload:.2f}")
    console.print(table)

def active_connections():
    console.print("\n[bold cyan]Active Internet Connections...[/bold cyan]")
    try:
        result = subprocess.check_output("netstat -tunp", shell=True).decode()
    except Exception:
        result = "Cannot get active connections."
    table = Table(title="Active Connections")
    table.add_column("Connection Info")
    for line in result.split('\n'):
        if line.strip():
            table.add_row(line)
    console.print(table)

def main():
    banner()
    console.print("[bold green]IP Information:[/bold green]")
    console.print(f"[bold yellow]Local IP:[/bold yellow] {get_local_ip()}")
    console.print(f"[bold yellow]External IP:[/bold yellow] {get_external_ip()}")
    scan_devices()
    internet_speed()
    active_connections()
    console.print(Panel("[bold green]Network Monitor Finished![/bold green]\n[bold magenta]By DARK_OFFICAIL 💀[/bold magenta]", title="Status"))

if __name__ == "__main__":
    main()
