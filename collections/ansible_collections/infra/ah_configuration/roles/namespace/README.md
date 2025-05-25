# infra.ah_configuration.namespace

## Description

An Ansible Role to create Namespaces in Automation Hub.

## Variables

|Variable Name|Default Value|Required|Description|Example|
|:---:|:---:|:---:|:---:|:---:|
|`ah_host`|""|yes|URL to the Automation Hub or Galaxy Server. (alias: `ah_hostname`)|127.0.0.1|
|`ah_username`|""|yes|Admin User on the Automation Hub or Galaxy Server.||
|`ah_password`|""|yes|Automation Hub Admin User's password on the Automation Hub Server.  This should be stored in an Ansible Vault at vars/tower-secrets.yml or elsewhere and called from a parent playbook.||
|`ah_token`|""|yes|Tower Admin User's token on the Automation Hub Server.  This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook.||
|`ah_validate_certs`|`true`|no|Whether or not to validate the Ansible Automation Hub Server's SSL certificate.||
|`ah_request_timeout`|`10`|no|Specify the timeout Ansible should use in requests to the Galaxy or Automation Hub host.||
|`ah_path_prefix`|""|no|API path used to access the api. Either galaxy, automation-hub, or custom||
|`ah_configuration_async_dir`|`null`|no|Sets the directory to write the results file for async tasks. The default value is set to `null` which uses the Ansible Default of `/root/.ansible_async/`.||
|`ah_namespaces`|`see below`|yes|Data structure describing your namespaces, described below.||

### Secure Logging Variables

The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add namespace task does not include sensitive information.
ah_configuration_namespace_secure_logging defaults to the value of ah_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of automation hub configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`ah_configuration_namespace_secure_logging`|`False`|no|Whether or not to include the sensitive Namespace role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`ah_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables

The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`ah_configuration_async_retries`|50|no|This variable sets the number of retries to attempt for the role globally.|
|`ah_configuration_namespace_async_retries`|`ah_configuration_async_retries`|no|This variable sets the number of retries to attempt for the role.|
|`ah_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`ah_configuration_namespace_async_delay`|`ah_configuration_async_delay`|no|This sets the delay between retries for the role.|

## Data Structure

### Namespace Variables

|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`name`|""|yes|str|Namespace name. Must be lower case containing only alphanumeric characters and underscores.|
|`new_name`|""|yes|str|Setting this option will change the existing name (looked up via the name field.|
|`description`|""|yes|str|Description to use for the Namespace.|
|`company`|""|no|str|Namespace owner company name.|
|`email`|"password"|yes|str|Namespace contact email.|
|`avatar_url`|"public"|yes|str|Namespace logo URL.|
|`resources`|""|no|str|Namespace resource page in Markdown format.|
|`links`|[]|no|list|A list of dictionaries of Name and url values for links related the Namespace. See below for details.|
|`groups`|[]|yes|list|A list of dictionaries of the Names of groups that own the Namespace.|
|`state`|`present`|no|str|Desired state of the namespace.|

#### Links

|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`name`|""|yes|str|Link Text.|
|`description`|""|yes|str|Link URL.|

### Standard Project Data Structure

#### Yaml Example

```yaml
---
ah_namespaces:
  - name: abc15
    company: Redhat
    email: user@example.com
    avatar_url: https://static.redhat.com/libs/redhat/brand-assets/latest/corp/logo.svg
    description: string
    resources: "# Redhat\nA Namespace test with changes"
    links:
      - name: "New_Google"
        url: "http://www.google.com"
    groups:
      - name: system:partner-engineers
        object_roles:
          - "change_namespace"
          - "upload_to_namespace"
```

## Playbook Examples

### Standard Role Usage

```yaml
---
- name: Add namespace to Automation Hub
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
    - ../../namespace
```

## License

[GPLv3+](https://github.com/redhat-cop/ah_configuration#licensing)

## Author

[Sean Sullivan](https://github.com/sean-m-sullivan/)
