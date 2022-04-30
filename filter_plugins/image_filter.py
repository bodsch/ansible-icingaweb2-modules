# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.utils.display import Display

# import json
import os

# https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html
# https://blog.oddbit.com/post/2019-04-25-writing-ansible-filter-plugins/

display = Display()


class FilterModule(object):
    """
        Ansible file jinja2 tests
    """

    def filters(self):
        return {
            'type': self.var_type,
            'dict_from_list': self.dict_from_list,
            'append_checksum': self.append_checksum,
        }

    def var_type(self, var):
        """
          Get the type of a variable
        """
        return type(var).__name__

    def dict_from_list(self, data, search):
        """
        """
        display.v("dict_from_list({}, {})".format(data, search))

        result = next((item for item in data if item.get('name') == search), {})

        display.v("result : {}".format(result))

        return result

    def append_checksum(self, data, checksums):
        """
        """
        for c in checksums.get("results"):
            path = c.get("stat", {}).get("path", None)
            checksum = c.get("stat", {}).get("checksum", None)

            for d, _ in data.items():
                file_name = "{}.zip".format(d)
                if path.endswith(file_name) and len(file_name) == len(os.path.basename(path)):
                    data[d]['checksum'] = checksum
                    break

        result = data

        display.v("result : {}".format(result))

        return result
