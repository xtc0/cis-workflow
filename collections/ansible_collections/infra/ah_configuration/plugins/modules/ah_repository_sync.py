#!/usr/bin/python
# coding: utf-8 -*-

# (c) 2020, Sean Sullivan <@sean-m-sullivan>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["deprecated"],
    "supported_by": "community",
}


DOCUMENTATION = """
---
module: ah_repository_sync
author: "Tom Page (@Tompage1994)"
short_description: Configure a repository.
description:
    - Configure an Automation Hub remote Repository. See
      U(https://www.ansible.com/) for an overview.
deprecated:
  why: The endpoint has been removed and is not supported in AAP 2.4 onwards. It's functionality has been replaced by collection_remote_sync.
  alternative: collection_repository_sync
  removed_in: 3.0.0
  removed_from_collection: infra.ah_configuration
options:
    name:
      description:
        - Repository name. Probably one of community or rh-certified.
      required: True
      type: str
    wait:
      description:
        - Wait for the repository to finish syncing before returning.
      required: false
      default: True
      type: bool
    interval:
      description:
        - The interval to request an update from Automation Hub.
      required: False
      default: 1
      type: float
    timeout:
      description:
        - If waiting for the project to update this will abort after this
          amount of seconds
      type: int
extends_documentation_fragment: infra.ah_configuration.auth
"""


EXAMPLES = """
- name: Sync rh-certified repo without waiting
  infra.ah_configuration.ah_repository_sync:
    name: rh-certified
    wait: false

- name: Sync community repo and wait up to 60 seconds
  infra.ah_configuration.ah_repository_sync:
    name: community
    wait: true
    timeout: 60
"""

from ..module_utils.ah_module import AHModule
import time


def main():
    # Any additional arguments that are not fields of the item can be added here
    argument_spec = dict(
        name=dict(required=True),
        wait=dict(default=True, type="bool"),
        interval=dict(default=1.0, type="float"),
        timeout=dict(default=None, type="int"),
    )

    # Create a module for ourselves
    module = AHModule(argument_spec=argument_spec)
    module.warn("This role 'repository_sync' and module 'ah_repository_sync' will be removed when support for AAP 2.3 ends in May of 2024. "
                "The module and role collection_repository_sync replaced it."
                )

    # Extract our parameters
    name = module.params.get("name")
    wait = module.params.get("wait")
    interval = module.params.get("interval")
    timeout = module.params.get("timeout")

    sync_endpoint = "api/{0}/content/{1}/v3/sync".format(module.path_prefix, name)
    config_endpoint = "{0}/config".format(sync_endpoint)

    repository = module.get_only(config_endpoint, name_or_id=name, key="req_url")

    if repository is None:
        module.fail_json(msg="Unable to find repository")

    result = module.post_endpoint(sync_endpoint)
    if result["status_code"] != 200:
        module.fail_json(msg="Failed to update project, see response for details", response=result)

    module.json_output["changed"] = True
    module.json_output["task"] = result["json"]["task"]

    if not wait:
        module.exit_json(**module.json_output)

    # Grab our start time to compare against for the timeout
    start = time.time()

    result = module.get_only(config_endpoint, name_or_id=name, key="req_url")

    while not result["last_sync_task"]["finished_at"]:
        if timeout and timeout < time.time() - start:
            module.json_output["msg"] = "Monitoring of {0} - {1} aborted due to timeout".format("repository_sync", name)
            module.wait_sync_output(result)
            module.fail_json(**module.json_output)

        time.sleep(interval)

        result = module.get_only(config_endpoint, name_or_id=name, key="req_url")
        module.json_output["status"] = result["last_sync_task"]["state"]

    if result["last_sync_task"]["state"] == "failed":
        module.json_output["msg"] = "The {0} - {1}, failed".format("repository_sync", name)
        module.wait_sync_output(result)
        module.fail_json(**module.json_output)

    module.wait_sync_output(result)

    module.exit_json(**module.json_output)


if __name__ == "__main__":
    main()
