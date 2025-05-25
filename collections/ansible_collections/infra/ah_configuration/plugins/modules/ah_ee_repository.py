#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Herve Quatremain <hquatrem@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# You can consult the UI API documentation directly on a running private
# automation hub at https://hub.example.com/pulp/api/v3/docs/


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: ah_ee_repository
short_description: Manage private automation hub execution environment repositories/containers
description:
  - Update and delete execution environment repositories (also known as containers).
  - Grant group access to repositories.
version_added: '0.4.3'
author: Herve Quatremain (@herve4m)
options:
  name:
    description:
      - Name of the repository to remove or modify.
    required: true
    type: str
  description:
    description:
      - Text that describes the repository.
    type: str
  registry:
    description:
      - The remote registry that the repository belongs in.
    type: str
  upstream_name:
    description:
      - The name of the image upstream.
    type: str
  include_tags:
    description:
      - The tags to pull in.
    type: list
    elements: str
    default: []
  exclude_tags:
    description:
      - The tags to avoid pulling in.
    type: list
    elements: str
    default: []
  readme:
    description:
      - README text in Markdown format for the repository.
      - Mutually exclusive with the C(readme_file) option.
    type: str
  readme_file:
    description:
      - Path to a README file in Markdown format to associate with the repository.
      - Mutually exclusive with the C(readme) option.
    type: path
  state:
    description:
      - If C(absent), then the module deletes the repository.
      - The module does not fail if the repository does not exist because the state is already as expected.
      - If C(present), then the module sets the description and README file for the repository.
    type: str
    default: present
    choices: [absent, present]
notes:
  - Supports C(check_mode).
  - Only works with private automation hub v4.3.2 or later for local repositories and v4.4.0 for remote repositories.
  - The module cannot be use to create repositories.
    Use C(podman push) for example to create repositories.
extends_documentation_fragment: infra.ah_configuration.auth_ui
"""

EXAMPLES = r"""
- name: Ensure the repository description and README are set
  infra.ah_configuration.ah_ee_repository:
    name: ansible-automation-platform-20-early-access/ee-supported-rhel8
    state: present
    description: Supported execution environment
    readme: |
      # My execution environment

      * bullet 1
      * bullet 2
    ah_host: hub.example.com
    ah_username: admin
    ah_password: Sup3r53cr3t

- name: Ensure the repository README is set
  infra.ah_configuration.ah_ee_repository:
    name: ansible-automation-platform-20-early-access/ee-supported-rhel8
    state: present
    readme_file: README.md
    ah_host: hub.example.com
    ah_username: admin
    ah_password: Sup3r53cr3t

- name: Ensure the repository is removed
  infra.ah_configuration.ah_ee_repository:
    name: ansible-automation-platform-20-early-access/ee-supported-rhel8
    state: absent
    ah_host: hub.example.com
    ah_username: admin
    ah_password: Sup3r53cr3t

- name: Add a remote repository from quayio registry
  infra.ah_configuration.ah_ee_repository:
    name: myrepo
    upstream_name: repo
    registry: quayio
    include_tags:
      - latest
      - 0.0.1
    state: present
    ah_host: hub.example.com
    ah_username: admin
    ah_password: Sup3r53cr3t
"""

RETURN = r""" # """

import os
import os.path

from ..module_utils.ah_api_module import AHAPIModule
from ..module_utils.ah_ui_object import AHUIEERepository, AHUIEERegistry, AHUIEERemote
from ..module_utils.ah_pulp_object import AHPulpEERepository, AHPulpEENamespace


def delete_empty_namespace(module, repository_name):
    """Delete the namespace of the given repository name.

    :param module: The API object that the function uses to access the API.
    :type module: :py:class:``ah_api_module.AHAPIModule``
    :param repository_name: Name of the repository for which the namespace must
                            be deleted if empty.
    :type repository_name: str
    """
    namespace_name = repository_name.split("/", 1)[0]
    repos = AHPulpEERepository.get_repositories_in_namespace(module, namespace_name)
    if len(repos) == 0:
        namespace_pulp = AHPulpEENamespace(module)
        namespace_pulp.get_object(namespace_name)
        namespace_pulp.delete(auto_exit=False)


def main():
    argument_spec = dict(
        name=dict(required=True),
        description=dict(),
        registry=dict(),
        upstream_name=dict(),
        include_tags=dict(type="list", elements="str", default=[]),
        exclude_tags=dict(type="list", elements="str", default=[]),
        readme=dict(),
        readme_file=dict(type="path"),
        state=dict(choices=["present", "absent"], default="present"),
    )

    # Create a module for ourselves
    module = AHAPIModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        mutually_exclusive=[
            ("readme", "readme_file"),
        ],
        required_by={"registry": "upstream_name"},
    )

    # Extract our parameters
    name = module.params.get("name")
    description = module.params.get("description")
    registry = module.params.get("registry")
    readme = module.params.get("readme")
    readme_file = module.params.get("readme_file")
    state = module.params.get("state")

    # Authenticate
    module.authenticate()

    # Only recent versions support execution environment
    vers = module.get_server_version()
    if vers < "4.3.2":
        module.fail_json(msg="This module requires private automation hub version 4.3.2 or later. Your version is {vers}".format(vers=vers))
    elif vers < "4.4.0" and registry:
        module.fail_json(
            msg="This module requires private automation hub version 4.4.0 or later to create remote repositories. Your version is {vers}".format(vers=vers)
        )

    # Process the object from the Pulp API (delete or create)
    repository_pulp = AHPulpEERepository(module)

    # API (GET): /pulp/api/v3/distributions/container/container/?name=<name>
    repository_pulp.get_object(name)

    # Process the object from the UI API
    repository_ui = AHUIEERepository(module)

    # Get the repository details from its name.
    # API (GET): /api/galaxy/_ui/v1/execution-environments/repositories/<name>/
    repository_ui.get_object(name, vers)

    # Removing the repository
    if state == "absent":
        repository_pulp.delete()

    changed = False

    if registry:
        remote_pulp = AHPulpEERepository(module)
        remote_pulp.get_object(name)
    else:
        remote_pulp = None

    # If registry is set this is a remote repository
    if registry:

        # Get the registry id
        registry_obj = AHUIEERegistry(module)
        registry_obj.get_object(registry, vers)

        new_fields = {}
        for field_name in (
            "upstream_name",
            "include_tags",
            "exclude_tags",
        ):
            field_val = module.params.get(field_name)
            new_fields[field_name] = field_val

        remote = AHUIEERemote(module)
        if vers > "4.7.0":
            new_fields["registry"] = registry_obj.data['id']
            remote.name_field = "id"
            registry_obj.id_field = "id"
        else:
            new_fields["registry"] = registry_obj.id
        if repository_ui.exists:
            if vers > "4.7.0":
                remote.get_object(repository_ui.data["pulp"]["repository"]["remote"]["id"], vers)
            else:
                remote.get_object(repository_ui.data["pulp"]["repository"]["remote"]["pulp_id"], vers)
        new_fields["name"] = name
        remote_changed = remote.create_or_update(new_fields, auto_exit=False)
        changed = changed or remote_changed

    else:
        if not repository_pulp.exists:
            module.fail_json(
                msg="The {repository} repository does not exist and registry is not set so it is assumed this is a local image.".format(repository=name)
            )

    repository_pulp.get_object(name)
    repository_ui.get_object(name, vers)

    # If a README file is given, verify that it exists and then read it.
    if readme_file is not None:
        if not os.path.isfile(readme_file):
            module.fail_json(msg="The {file} file does not exist or is not a file.".format(file=readme_file))

        if not os.access(readme_file, os.R_OK):
            module.fail_json(msg="You do not have read access to the {file} file.".format(file=readme_file))

        # Read in the file contents
        try:
            with open(readme_file, "r") as f:
                readme = f.read()
        except Exception as e:
            module.fail_json(msg="Cannot read {file}: {error}".format(file=readme_file, error=e))

    if description is not None and repository_pulp.update({"description": description, "base_path": name}, auto_exit=False):
        changed = True

    if readme is None:
        json_output = {
            "name": name,
            "type": repository_pulp.object_type,
            "changed": changed,
        }
        module.exit_json(**json_output)
    # API (GET): /api/automation-hub/v3/plugin/execution-environments/repositories/{{ content_path }}/_content/readme/
    # API (GET): /api/galaxy/_ui/v1/execution-environments/repositories/<name>/_content/readme/
    # API (PUT): /api/galaxy/_ui/v1/execution-environments/repositories/<name>/_content/readme/
    updated = repository_ui.update_readme(readme, auto_exit=False)
    json_output = {
        "name": name,
        "type": repository_ui.object_type,
        "changed": changed or updated,
    }
    module.exit_json(**json_output)


if __name__ == "__main__":
    main()
