# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.utils.display import Display
import os

display = Display()


class FilterModule(object):
    """
        Ansible file jinja2 tests
    """

    def filters(self):
        return {
            'dict_from_list': self.dict_from_list,
            'append_checksum': self.append_checksum,
            'installed_modules': self.installed_modules,
        }

    def dict_from_list(self, data, search):
        """
        """
        display.v(f"dict_from_list({data}, {search})")

        if(isinstance(data, dict)):
            result = data.get(search, {})
        else:
            result = next((item for item in data if item.get('name') == search), {})

        display.v(f"result : {result}")

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

        display.v(f"result : {result}")

        return result

    def installed_modules(self, data):
        """
        """
        _data = data.copy()
        if isinstance(data, dict):
            for t, v in _data.items():
                # display.v(f"  - {t}")
                # display.v(f"    {v}")
                if v.get("download", None):
                    _ = v.pop("download")
                if v.get("src", None):
                    _ = v.pop("src")

        # display.v(f"result : {_data}")

        return _data
