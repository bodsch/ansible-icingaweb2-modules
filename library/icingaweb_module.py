#!/usr/bin/env python3

# -*- coding: utf-8 -*-

# (c) 2020, Bodo Schulz <bodo@boone-schulz.de>
# BSD 2-clause (see LICENSE or https://opensource.org/licenses/BSD-2-Clause)

from __future__ import absolute_import, division, print_function
import os

from ansible.module_utils.basic import AnsibleModule


__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '0.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = """
---
module: icingawweb_module.py
author:
    - 'Bodo Schulz'
short_description: enable / disable icingaweb modules.
description: ''
"""

EXAMPLES = """
- name: disable modules
  become: true
  icingaweb_module:
    state: absent
    modules: dark_lord
"""


class IcingaWeb2Modules(object):
    """
    Main Class to implement the Icinga2 API Client
    """
    module = None

    def __init__(self, module):
        """
          Initialize all needed Variables
        """
        self.module = module

        self.state = module.params.get("state")
        self.install_directory = module.params.get("install_directory")
        self.modules = module.params.get("modules")
        self.checksums = module.params.get("checksums")

    def run(self):
        res = dict(
            changed=False,
            failed=False,
        )

        if os.path.isdir(self.install_directory):
            """
            """
            changed = False

            self.module.log(msg=f"  - modules: '{len(self.modules)}' - checksums: '{self.checksums}'")

            if len(self.modules) > 0 and len(self.checksums) > 0:
                """
                """
                _modules = self.modules.copy()

                for module in _modules:
                    checksum = None
                    module_checksum = None

                    checksum_file = os.path.join(
                        self.install_directory,
                        module,
                        ".checksum"
                    )

                    self.module.log(msg=f"Module: {module}")
                    self.module.log(msg=f"- checksum_file : '{checksum_file}'")

                    if os.path.exists(checksum_file):
                        with open(checksum_file) as f:
                            checksum = f.readlines()[0]

                        if checksum is not None:
                            module_checksum = self.checksums.get(module, {}).get("checksum")

                        module_version = _modules.get(module, {}).get("version")
                        installed_version = self.checksums.get(module, {}).get("version")

                        self.module.log(msg=f"- module_version      : '{module_version}'")
                        self.module.log(msg=f"- installed_version   : '{installed_version}'")

                        version_compare_git = module_version in ["master", "main"]
                        version_compare = module_version != installed_version
                        checksum_compare = (checksum is not None and module_checksum is not None and module_checksum == checksum)

                        self.module.log(msg=f"- version_compare_git : '{version_compare_git}'")
                        self.module.log(msg=f"- version_compare     : '{version_compare}'")
                        self.module.log(msg=f"- checksum_compare    : '{checksum_compare}'")

                        if version_compare_git:
                            self.modules[module]['download'] = True
                            changed = True
                        else:
                            if not version_compare and not checksum_compare:
                                self.module.log(msg="- download == TRUE")
                                self.modules[module]['download'] = True
                                changed = True
                            else:
                                self.module.log(msg="- download == FALSE")
                                self.modules[module]['download'] = False

            else:
                _modules = self.modules.copy()

                for module in _modules:
                    self.modules[module]['download'] = True
                    changed = True

            res['changed'] = changed
            res['modules'] = self.modules
        else:
            msg = f"{self.install_directory} is no directory"

            res['ansible_module_results'] = msg
            res['failed'] = True
            module.log(msg=msg)

        return res

    def create_link(self, source, destination, force=False):
        module.log(msg="create_link({}, {}, {})".format(source, destination, force))

        if(force):
            os.remove(destination)
            os.symlink(source, destination)
        else:
            os.symlink(source, destination)

        pass


# ===========================================
# Module execution.
#


def main():
    """
    """
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(
                default="verify",
                choices=["verify", "absent", "present"]
            ),
            install_directory=dict(
                required=True,
                type="path",
                # default='/usr/share/icingaweb2/modules'
            ),
            modules=dict(
                required=True,
                type=dict
            ),
            checksums=dict(
                required=True,
                type=dict
            ),
        ),
        supports_check_mode=False,
    )

    icingaweb = IcingaWeb2Modules(module)
    result = icingaweb.run()

    module.log(msg="= result : '{}'".format(result))

    module.exit_json(**result)


# import module snippets
if __name__ == '__main__':
    main()
