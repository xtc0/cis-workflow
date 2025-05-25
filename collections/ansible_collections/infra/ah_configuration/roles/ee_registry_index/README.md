# infra.ah_configuration.ee_registry_index

## Description

An Ansible Role to index EE Registries in Automation Hub.

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
|`ah_ee_registries`|`see below`|yes|Data structure describing your ee_registries, described below. (Note this is the same as for the `ee_registries` role and the variable can be combined). Note that this role will only do anything if the `index` suboption of this variable is set to true.||

### Secure Logging Variables

The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add ee_registry task does not include sensitive information.
ah_configuration_ee_registry_secure_logging defaults to the value of ah_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of automation hub configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`ah_configuration_ee_registry_secure_logging`|`False`|no|Whether or not to include the sensitive Registry role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`ah_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables

The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`ah_configuration_async_retries`|50|no|This variable sets the number of retries to attempt for the role globally.|
|`ah_configuration_ee_registry_index_async_retries`|`ah_configuration_async_retries`|no|This variable sets the number of retries to attempt for the role.|
|`ah_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`ah_configuration_ee_registry_index_async_delay`|`ah_configuration_async_delay`|no|This sets the delay between retries for the role.|

## Data Structure

### EE Registry Variables

|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`name`|""|yes|str|Registry name. Must be lower case containing only alphanumeric characters and underscores.|
|`index`|false|no|bool|Whether to index the ee_registry. Bu default it will not index unless this is set to true.|
|`wait`|true|no|str|Whether to wait for the indexing to complete|
|`interval`|`ah_configuration_ee_registry_index_async_delay`|no|str|The interval which the indexing task will be checked for completion|
|`timeout`|""|no|str|How long to wait for the indexing task to complete|

### Standard Project Data Structure

#### Yaml Example

```yaml
---
ah_ee_registries:
  - name: myreg
    url: https://quay.io/my/registry
    interval: 10
    wait: true
    timeout: 300
```

## Playbook Examples

### Standard Role Usage

```yaml
---
- name: Index ee_registry in Automation Hub
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
    - ee_registry_index
```

## License

[GPLv3+](https://github.com/redhat-cop/ah_configuration#licensing)

## Author

[Tom Page](https://github.com/Tompage1994/)
