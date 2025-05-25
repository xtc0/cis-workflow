# infra.ah_configuration.group

## Description

An Ansible Role to create groups in Automation Hub.

## Variables

|Variable Name|Default Value|Required|Description|Example|
|:---:|:---:|:---:|:---:|:---:|
|`ah_host`|""|yes|URL to the Automation Hub or Galaxy Server. (alias: `ah_hostname`)|127.0.0.1|
|`ah_username`|""|yes|Admin User on the Automation Hub or Galaxy Server.||
|`ah_password`|""|yes|Automation Hub Admin User's password on the Automation Hub Server.  This should be stored in an Ansible Vault at vars/tower-secrets.yml or elsewhere and called from a parent playbook.||
|`ah_validate_certs`|`true`|no|Whether or not to validate the Ansible Automation Hub Server's SSL certificate.||
|`ah_request_timeout`|`10`|no|Specify the timeout Ansible should use in requests to the Galaxy or Automation Hub host.||
|`ah_path_prefix`|""|no|API path used to access the api. Either galaxy, automation-hub, or custom||
|`ah_configuration_async_dir`|`null`|no|Sets the directory to write the results file for async tasks. The default value is set to `null` which uses the Ansible Default of `/root/.ansible_async/`.||
|`ah_groups`|`see below`|yes|Data structure describing your groups, described below.||

### Secure Logging Variables

The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add group task does not include sensitive information.
ah_configuration_group_secure_logging defaults to the value of ah_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of automation hub configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`ah_configuration_group_secure_logging`|`False`|no|Whether or not to include the sensitive Namespace role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`ah_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables

The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`ah_configuration_async_retries`|50|no|This variable sets the number of retries to attempt for the role globally.|
|`ah_configuration_group_async_retries`|`ah_configuration_async_retries`|no|This variable sets the number of retries to attempt for the role.|
|`ah_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`ah_configuration_group_async_delay`|`ah_configuration_async_delay`|no|This sets the delay between retries for the role.|

## Data Structure

### Group Variables

|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`name`|""|yes|str|Group Name. Must be lower case containing only alphanumeric characters and underscores.|
|`perms`|""|yes|str|The list of permissions to add to or remove from the given group. See below for options.|
|`state`|`present`|no|str|Desired state of the group.|
<!-- |`new_name`|""|yes|str|Setting this option will change the existing name (looked up via the name field.| -->
#### perms

The module accepts the following roles:

- For user management, `add_user`, `change_user`, `delete_user`, and `view_user`.
- For group management, `add_group`, `change_group`, `delete_group`, and `view_group`.
- For collection namespace management, `add_namespace`, `change_namespace`, `upload_to_namespace`, and `delete_namespace`.
- For collection content management, `modify_ansible_repo_content`, and `delete_collection`.
- For remote repository configuration, `change_collectionremote` and `view_collectionremote`.
- For container image management, only with private automation hub v4.3.2
  or later, `change_containernamespace_perms`, `change_container`,
  `change_image_tag`, `create_container`, `push_container`, and `delete_containerrepository`.
- For task management, `change_task`, `view_task`, and `delete_task`.
- You can also grant or revoke all permissions with `*` or `all`.

### Standard Project Data Structure

#### Yaml Example

```yaml
---
ah_groups:
  - name: group1
    state: present
```

## Playbook Examples

### Standard Role Usage

```yaml
---
- name: Add group to Automation Hub
  hosts: localhost
  connection: local
  gather_facts: false
  vars:
    ah_validate_certs: false
  # Define following vars here, or in ah_configs/ah_auth.yml
  # ah_host: ansible-ah-web-svc-test-project.example.com
  pre_tasks:
    - name: Include vars from ah_configs directory
      ansible.builtin.include_vars:
        dir: ./vars
        extensions: ["yml"]
      tags:
        - always
  roles:
    - ../../group
```

## License

[GPLv3+](https://github.com/redhat-cop/ah_configuration#licensing)

## Author

[Tom Page](https://github.com/Tompage1994/)
