
# Task: Create an AAP workflow with approval - use case: 2 CIS hardening rules (RHEL9)

To see list of CIS rules for RHEL 9, go to https://downloads.cisecurity.org/#/, under "Red Hat Enterprise Linux", select "Download PDF" for CIS Red Hat Enterprise Linux 9 Benchmark v2.0.0. Document called CIS_Red_Hat_Enterprise_Linux_9_Benchmark_v2.0.0.pdf will then be downloaded. This document containes the full list of CIS rules from which we will choose 2 to implement.

### Rule 1: Ensure cramfs kernel module is not available

### Rule 2: Ensure permissions on /etc/ssh/sshd_config are configured



Process for cramfs:

< Scan >
- If the cramfs kernel module is available in ANY installed kernel, verify:
- An entry including /bin/true or /bin/false exists in a file within the /etc/modprobe.d/ directory
- The module is deny listed in a file within the /etc/modprobe.d/ directory
- The module is not loaded in the running kernel

< Harden >
- Create a file ending in .conf with install cramfs /bin/false in the /etc/modprobe.d/ directory
- Create a file ending in .conf with blacklist cramfs in the /etc/modprobe.d/ directory
- Run modprobe -r cramfs 2>/dev/null; rmmod cramfs 2>/dev/null to remove cramfs from the kernel


Process for sshd_config:

< Scan >
- Run the following script and verify /etc/ssh/sshd_config and files ending in .conf in the /etc/ssh/sshd_config.d directory are:
- Mode 0600 or more restrictive
- Owned by the root user
- Group owned by the group root.

< Harden >
- Run the following script to set ownership and permissions on /etc/ssh/sshd_config and files ending in .conf in the /etc/ssh/sshd_config.d directory
  

## Example use case: CIS Workflow with Approvals
Security engineers want to ensure that RHEL 9 systems comply with key CIS benchmarks.  
This AAP workflow:


1. Runs a **scan playbook** to check for non-compliance.
2. Runs a **harden playbook** to fix issues for:
   - Ensure `cramfs` module is not available
   - Ensure permissions on `/etc/ssh/sshd_config` are configured correctly

## 1. Testing Non-Compliance For Cramfs (cramfs kernel module is now available)
```bash
# Remove deny rules and blacklist
sudo rm -f /etc/modprobe.d/cramfs_install.conf
sudo rm -f /etc/modprobe.d/cramfs_blacklist.conf

# Load the cramfs module
sudo modprobe cramfs

# Confirm it's loaded (optional)
lsmod | grep cramfs
```
After using these commands, cramfs would become available. By doing so, this would violate CIS rules and hence would trigger a failed task when running scan playbook (scan.yml).

## 2. Testing Non-Compliance For /etc/ssh/sshd_config
```bash
# Change permissions to less restrictive
sudo chmod 0644 /etc/ssh/sshd_config
```

After using these commands, permissions for /etc/ssh/sshd_config would change and become non-compliant. This would violate CIS rules and hence would trigger a failed task when running scan playbook (scan.yml).

## 3. After configuring for Non-Compliance, Trigger harden.yml

When non-compliance is picked up in scan.yml, certain tasks would fail for scan.yml. These tasks would then be corrected by harden playbook (harden.yml).

