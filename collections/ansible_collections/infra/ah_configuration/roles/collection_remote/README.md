# collection_remote

## Description

An Ansible Role to create a Collection Remote Repository.

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
|`ah_collection_remotes`|`see below`|yes|Data structure describing your collection remote repository, described below.||

The `ah_configuration_async_dir` variable sets the directory to write the results file for async tasks.
The default value is set to  `null` which uses the Ansible Default of `/root/.ansible_async/`.

### Secure Logging Variables

The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to False as normally the add repository task does not include sensitive information.
ah_configuration_repository_secure_logging defaults to the value of ah_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of automation hub configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`ah_configuration_collection_remote_secure_logging`|`False`|no|Whether or not to include the sensitive Namespace role tasks in the log.  Set this value to `True` if you will be providing your sensitive values from elsewhere.|
|`ah_configuration_secure_logging`|`False`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables

The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`ah_configuration_async_retries`|50|no|This variable sets the number of retries to attempt for the role globally.|
|`ah_configuration_collection_remote_async_retries`|`ah_configuration_async_retries`|no|This variable sets the number of retries to attempt for the role.|
|`ah_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`ah_configuration_collection_remote_async_delay`|`ah_configuration_async_delay`|no|This sets the delay between retries for the role.|

## Data Structure

### Collection Remote Variables

|Variable Name|Default Value|Required|Description|Example|
|:---:|:---:|:---:|:---:|:---:|
|`name`|``|yes| Repository name. Probably one of community, validated, or rh-certified||
|`url`|`https://cloud.redhat.com/api/automation-hub/`|no|(`ah_repository_certified`)Remote URL for the repository.|`https://console.redhat.com/api/automation-hub/content/`|
|`url`|`https://galaxy.ansible.com/api/`|no|(`ah_repository_community`)Remote URL for the repository.||
|`auth_url`|`https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token`|no|(`ah_repository_certified`)Remote URL for the repository authentication if separate.||
|`token`|``|no|Token to authenticate to the remote repository.||
|`policy`|`immediate`|no|The policy to use when downloading content. Can be one of `immediate`, `When syncing, download all metadata and content now.`.||
|`requirements`|``|no|Requirements, a list of collections in [requirements file format](https://docs.ansible.com/ansible/latest/collections_guide/collections_installing.html#install-multiple-collections-with-a-requirements-file) to limit thedownload from remote. This will only download provided collections. This is only the list under collections. See examples for usuage.||
|`requirements_file`|``|no|A yaml requirements file to download from remote. In requirements file format. Exclusive with `requirements` ||
|`username`|``|no|Username to authenticate to the remote repository.||
|`password`|``|no|Password to authenticate to the remote repository.||
|`tls_validation`|`True`|no|Whether to use TLS validation against the remote repository|True|
|`client_key`|``|no|A PEM encoded private key file used for authentication||
|`client_cert`|``|no|A PEM encoded client certificate used for authentication||
|`ca_cert`|``|no|A PEM encoded CA certificate used for authentication||
|`client_key_path`|``|no|Path to a PEM encoded private key file used for authentication||
|`client_cert_path`|``|no|Path to a PEM encoded client certificate used for authentication||
|`ca_cert_path`|``|no|Path to a PEM encoded CA certificate used for authentication||
|`download_concurrency`|`10`|no| Number of concurrent collections to download.||
|`max_retries`|`0`|no|Retries to use when running sync. Default is 0 which does not limit.||
|`rate_limit`|`8`|no|Limits total download rate in requests per second.||
|`signed_only`|`False`|no|Only download signed collections|False|
|`sync_dependencies`|`True`|no|Whether to download depenencies when syncing collections.|False|
|`proxy_url`|``|no|The URL for the proxy. Defaults to global `proxy_url` variable.||
|`proxy_username`|``|no|The username for the proxy authentication. Defaults to global `proxy_username` variable.||
|`proxy_password`|``|no|The password for the proxy authentication. Defaults to global `proxy_password` variable.||
|`state`|`present`|no|Desired state of the collection_remote. Either `present` or `absent`.||

### Standard Project Data Structure

#### Yaml Example

```yaml
---
ah_collection_remotes:
  - name: community-infra
    url: https://beta-galaxy.ansible.com/
    requirements:
      - name: infra.ee_utilities
      - name: infra.controller_configuration
```

## Playbook Examples

### Standard Role Usage

```yaml
---
- name: Add repository to Automation Hub
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
    - ../../collection_remote
```

## License

[GPLv3+](https://github.com/redhat-cop/ah_configuration#licensing)
