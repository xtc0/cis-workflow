
Task: Create an AAP workflow with approval - use case: 2 CIS hardening rules (RHEL9)

Rule 1: Ensure cramfs kernel module is not available

Rule 2: Ensure permissions on /etc/ssh/sshd_config are configured


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

