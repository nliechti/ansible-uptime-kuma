#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Lucas Held <lucasheld@hotmail.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r'''
---
extends_documentation_fragment:
  - lucasheld.uptime_kuma.uptime_kuma

module: proxy_info
version_added: 0.0.0
author: Lucas Held (@lucasheld)
short_description: TODO
description: TODO

options:
  id:
    description: The proxy id.
    type: int
  host:
    description: TODO
    type: str
  port:
    description: TODO
    type: int
'''

EXAMPLES = r'''
- name: list proxies
  lucasheld.uptime_kuma.proxy_info:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
  register: result
'''

RETURN = r'''
'''

import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.lucasheld.uptime_kuma.plugins.module_utils.common import common_module_args, get_proxy_by_host_port
from ansible.module_utils.basic import missing_required_lib

try:
    from uptime_kuma_api import UptimeKumaApi
    HAS_UPTIME_KUMA_API = True
except ImportError:
    HAS_UPTIME_KUMA_API = False


def run(api, params, result):
    id_ = params.get("id")

    host = params.get("host")
    port = params.get("port")

    if id_:
        proxy = api.get_proxy(id_)
        result["proxies"] = [proxy]
    elif host and port:
        proxy = get_proxy_by_host_port(api, host, port)
        result["proxies"] = [proxy]
    else:
        result["proxies"] = api.get_proxies()


def main():
    module_args = dict(
        id=dict(type="int"),
        host=dict(type="str"),
        port=dict(type="int"),
    )
    module_args.update(common_module_args)

    module = AnsibleModule(module_args, supports_check_mode=True)
    params = module.params

    if not HAS_UPTIME_KUMA_API:
        module.fail_json(msg=missing_required_lib("uptime_kuma_api"))

    api = UptimeKumaApi(params["api_url"])
    api.login(params["api_username"], params["api_password"])

    result = {
        "changed": False
    }

    try:
        run(api, params, result)

        api.disconnect()
        module.exit_json(**result)
    except Exception as e:
        api.disconnect()
        error = traceback.format_exc()
        module.fail_json(msg=error, **result)


if __name__ == '__main__':
    main()