# delete-vmware-snapshots
### Delete VMWare snapshots from VCenter after the specified snapshot age is reached

This script uses Hashicorp Vault along with a set of environment variables that must be present on the local system for storage and retrieval of secrets such as usernames, API keys, URLs, etc.

This repo contains a custom module entitled 'get_secrets.py' that should help to streamline the auth process somewhat. Details will need to be modified on a per-site basis.

Also in the repo is an additional custom module named send_email.py.

The main script (delete_vmware_snapshots.py) deletes VMWare snapshots from VCenter older than a specified number of days.

The ```max_snapshot_age``` variable can be edited as necessary to increase or decrease the number of snapshots to be deleted.

Results are emailed in tabular format as an attachment to a specified user or users.
