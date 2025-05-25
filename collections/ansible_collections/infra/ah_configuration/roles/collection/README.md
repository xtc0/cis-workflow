# infra.ah_configuration.collection

## Description

An Ansible Role to update, or destroy Automation Hub Collections.

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
|`ah_collections`|`see below`|yes|Data structure describing your collections, described below.||

These are the sub options for the vars `ah_collections` which are dictionaries with the options you want. See examples for details.
|Variable Name|Default Value|Required|Description|Example|
|:---:|:---:|:---:|:---:|:---:|
|`namespace`|""|yes|Namespace name. Must be lower case containing only alphanumeric characters and underscores.|"awx"|
|`name`|""|yes|Collection name. Must be lower case containing only alphanumeric characters and underscores.||
|`version`|""|no|Collection Version. Must be lower case containing only alphanumeric characters and underscores. If not provided and 'auto_approve' true, will be derived from the path.||
|`path`|""|no|Collection artifact file path.||
|`wait`|"true"|no|Waits for the collection to be uploaded||
|`auto_approve`|"true"|no|Approves a collection and requires version to be set.||
|`timeout`|"true"||Maximum time to wait for the collection approval||
|`interval`|"true"|10|Interval at which approval is checked||
|`overwrite_existing`|"false"|no|Overwrites an existing collection and requires version to be set.||
|`state`|"present"|no|Desired state of the resource||

The `ah_configuration_async_dir` variable sets the directory to write the results file for async tasks.
The default value is set to  `null` which uses the Ansible Default of `/root/.ansible_async/`.

### Secure Logging Variables

The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add repository task does not include sensitive information.
ah_configuration_repository_secure_logging defaults to the value of ah_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of automation hub configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`ah_configuration_collection_secure_logging`|`False`|no|Whether or not to include the sensitive collection role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`ah_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

## Data Structure

### Standard Project Data Structure

#### Yaml Example

```yaml
---
ah_collections:
  - namespace: 'awx'
    name: 'awx'
    path: /var/tmp/collections/awx_awx-15.0.0.tar.gz
    state: present

  - namespace: test_collection
    name: test
    version: 4.1.2
    state: absent
```

## Playbook Examples

### Standard Role Usage

```yaml
---
- name: Add collection
  hosts: localhost
  connection: local
  gather_facts: false
  vars:
    ah_validate_certs: false
  # Define following vars here, or in ah_configs/ah_auth.yml
  # ah_host: ansible-ah-web-svc-test-project.example.com
  # ah_token: changeme
  pre_tasks:
    - name: Include vars from ah_configs directory
      ansible.builtin.include_vars:
        dir: ./vars
        extensions: ["yml"]
      tags:
        - always
  roles:
    - ../../collection
```

## License

[GPLv3+](https://github.com/redhat-cop/ah_configuration#licensing)

## Author

[Inderpal Tiwana](https://github.com/inderpaltiwana/)
