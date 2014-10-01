#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2014, William Jimenez <wjimenez5271@gmail.com>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.


DOCUMENTATION = '''
---
module: rundeck
version_added:
short_description: execute rundeck jobs via rundeck api
description:
  - Makes API call to specified Rundeck server to execute job
options: {}
author: William Jimenez
notes:
  - Requires rundeck python module: https://pypi.python.org/pypi/rundeckrun
'''

EXAMPLES = '''
# Execute job on rundeck server
 - name: Execute my rundeck job
   rundeck: rd_host=rundeck.mycompany.net api_token=E4rNvVRV378knO9dp3d73O0cs1kd0kCd job_id=116e2025-7895-444a-88f7-d96b4f19fdb3

'''

try:
    from rundeck.client import Rundeck
except ImportError:
    rundeck_module = False
else:
    rundeck_module = True

def main():
    module = AnsibleModule(
        argument_spec = dict(
            rd_host           = dict(required=True),
            api_token         = dict(required=True),
            job_id            = dict(required=True),
            arguments         = dict(required=False),
        ),
        supports_check_mode=False,
    )
    if not rundeck_module:
        module.fail_json('Rundeck python module required to execute')

    rd_host = module.params['rd_host']
    api_token = module.params['api_token']
    job_id = module.params['job_id']
    try:
        arguments = module.params['arguments']
    except:
        arguments = None

    try:
        rd = Rundeck(rd_host, api_token=api_token)
        rd.run_job(job_id, argString=arguments)
        module.exit_json(changed=True)
    except Exception:
        module.fail_json('Error initiating rundeck job')


# import module snippets
from ansible.module_utils.basic import *
main()
