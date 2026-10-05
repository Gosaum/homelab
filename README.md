# Homelab

This repository is an infrastructure-as-code project that provisions a Raspberry Pi 3 server with Ansible and deploys containerized services with Docker Compose. It configures secure remote access through Tailscale, installs and configures Docker, and runs a Nginx web server behind a Caddy reverse proxy.

This repository documents my setup and is not meant to be a generic template, even though you can always adapt it to your needs. It reflects my own hardware and network, and some values specific to them might therefore be hard-coded. This approach is a choice that allows me to spend less time generalizing and documenting, and more time experimenting and learning.

## Services and network

```text
Client device
  |
  | HTTP (80) / HTTPS (443)
  | over LAN or tailnet
  v
Caddy container (reverse proxy)
  | 
  | HTTP (80) over Docker network
  | with Docker internal DNS
  v
Nginx container (web server)
```

## Ansible provisioning

Ansible is used to configure the Raspberry Pi host before the containers are deployed. The playbook takes care of the initial system setup, installs the packages required by the project, and applies the host-level configuration needed to run the services reliably.

- **Install Tailscale and join the tailnet**: provides secure remote access for managing the server with Ansible.
- **Add additional SSH users**: creates additional users and configures their SSH keys and permissions.
- **Harden the SSH server**: disables root login and password-based authentication.
- **Install and configure Docker**: installs docker and configures its behavior to help limit disk usage.
- **Copy and run the services**: copies the files, builds the containers and starts them with Docker Compose.
- **Clean up afterwards**: removes unused Docker images left behind by rebuilds to reclaim space on the host.

## Repository Structure

```text
homelab/
├── README.md
│
├── ansible/
│   ├── ansible.cfg         # configure ansible
│   ├── inventory.yml       # define ansible managed hosts
│   ├── ...
│   ├── playbooks/
│   │   ├── deploy.yml      # services deployment playbook
│   │   └── setup.yml       # server setup playbook
│   └── host_vars/
│       └── rpi3/           # host configuration variables
│           ├── vars.yml    # store values
│           └── vault.yml   # store encrypted secrets
│
├── services/
│   ├── compose.yml         # define and manage services and volumes
│   ├── caddy/              # caddy configuration
│   └── webserver/          # website src and nginx configuration
│
└── LICENSE
```

## Getting started

**[ 0 ] Prerequisites**

- A Raspberry Pi 3 Model B and a microSD card, mine is a SanDisk 16GB
- A machine with Ansible installed and set up
- An SSH key Ansible will use to connect to the host
- A free Tailnet account with MagicDNS and HTTPS Certificates enabled

*Note: to generate the SSH key, I ran `ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_ansible -C "ansible"`.*

**[ 1 ] Clone the repository**

```bash
git clone https://github.com/Gosaum/homelab
cd homelab/ansible
```

**[ 2 ] Set up Ansible**

Install the required Ansible collections:

```bash
ansible-galaxy collection install -r requirements.yml
```

Set a password for the Ansible vault:

```bash
umask 077 && cat > .vault_pass
# Enter your password and press Ctrl+D.
```

Create the vault that will hold the secrets:

```bash
rm -f host_vars/rpi3/vault.yml
ansible-vault create host_vars/rpi3/vault.yml
```

The vault should contain the sudo password that will be used by the `ansible` user.

Generate a reusable Tailscale auth key from the Tailscale admin console and add it to the vault:

```yaml
ansible_become_password: "xxxxxxxx" # Sudo password for the ansible user
tailscale_authkey: "tskey-auth-xxxxxxxx" # Tailscale auth key
```

**[ 3 ] Configure SSH users (optional)**

Edit `host_vars/rpi3/vars.yml` and add users:

```yaml
additional_ssh_users:
  guest:
    admin: true
    ssh_keys:
      - ssh-ed25519 xxxxxxxx key1
      - ssh-ed25519 xxxxxxxx key2
```

Add as many as you like. If you don't want any additional user, leave the list empty:

```yaml
additional_ssh_users: []
```

Pre-hash their password with `mkpasswd --method=sha-512` and add them to the vault as well:

```bash
ansible-vault edit host_vars/rpi3/vault.yml
```

```yaml
ssh_users_passwords:
  guest01: "$6$b1cd..."
  guest02: "$6$ab8f..."
  ...
```

**[ 4 ] Flash and power on**

Using Raspberry Pi Imager, flash Ubuntu Server 24.04.5 LTS (64-bit) on the microSD card with `rpi3-server` as the hostname, `ansible` as the username and `ssh-ed25519 AAAA... ansible` (the SSH key Ansible will use, see prerequisites) as an authorized SSH key. Configure the Wi-Fi. Power on the Raspberry Pi and wait a few minutes.

**[ 5 ] Run the setup playbook**

Find the Pi's IPv4 address on the LAN (your machine must be on the same network):

```bash
ping -4 rpi3-server.local
```

From the `ansible/` directory, run the playbook against that address:

```bash
ansible-playbook playbooks/setup.yml -e ansible_host=<IP>
```

Once it completes, check connectivity:

```bash
ansible rpi3 -m ping
```

Without the `-e` flag, ansible is using the Tailscale hostname, which only works if Tailscale has successfully been installed on the host.

Finally, deploy the services:

```bash
ansible-playbook playbooks/deploy.yml
```

The website should now be reachable at `https://rpi3-server.<domain>/`.