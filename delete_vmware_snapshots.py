import contextlib
import os
import time
from datetime import date, timedelta

from rich.console import Console
from rich.table import Table
from vmwc import VMWareClient

from get_secrets import get_secrets
from send_email import send_email

max_snapshot_age = <CHANGEME>  # in days
filename = "vm_snapshots.txt"
url = os.getenv("VAULT_URL")
token = os.getenv("VMWARE_TOKEN")
path = os.getenv("VMWARE_PATH")

# Needed for email
subject = "Deleted VCenter Snapshots"
sender = "<CHANGEME>"
recipient = ["<CHANGEME>"] 
body = f"Deleted VCenter Snapshots - older than {max_snapshot_age} days"


secrets = get_secrets(url=url, token=token, path=path)

HOST = secrets['data']['host']
USERNAME = secrets['data']['username']
PASSWORD = secrets['data']['password']

today = date.today()
time_delta = today - timedelta(days=max_snapshot_age)

table = Table()
table.show_lines = True
table.add_column("VIRTUAL MACHINE NAME", justify="left")
table.add_column("SNAPSHOT NAME", justify="left")
table.add_column("SNAPSHOT DATE", justify="left")


with open(filename, 'w') as f:
    with VMWareClient(HOST, USERNAME, PASSWORD) as vm_client:
        for vm in vm_client.get_virtual_machines():
            for snapshot in vm.get_snapshots():
                if snapshot.timestamp.date() <= time_delta and not vm.name.startswith("replica") and not 'Gold' in snapshot.name:
                    table.add_row(vm.name, snapshot.name, str(snapshot.timestamp.date()))
                    with contextlib.suppress(Exception):
                        snapshot.delete()
                        time.sleep(2)

                   
console = Console(record=True)
console.print(table)
console.save_text(filename)


send_email(subject, sender, recipient, body, filename)

with contextlib.suppress(FileNotFoundError):
    os.remove(filename)
