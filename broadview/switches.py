# (C) Copyright Broadcom Corporation 2016
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from broadview_lib.config.broadviewconfig import BroadViewBSTSwitches
from oslo_log import log as logging

LOG = logging.getLogger(__name__)

def getBSTSwitches():
    ret = []
    x = BroadViewBSTSwitches()
    for y in x:
        if not "ip" in y:
            LOG.warning('getBSTSwitches: switch {} in /etc/broadviewswitches.conf has no ip'.format(y))
            continue
        if not "port" in y:
            LOG.warning('getBSTSwitches: switch {} in /etc/broadviewswitches.conf has no port'.format(y))
            continue
        ret.append(y)
    return ret

def getBSTSwitchChoices():
    ret = []
    x = getBSTSwitches()
    if len(x) == 0:
        LOG.warning('getBSTSwitchChoices: no configured switches in /etc/broadviewswitches.conf')
    for y in x:
        if not "description" in y:
            s = "{}:{}".format(y["ip"], y["port"])
        else:
            s = "{}:{} ({})".format(y["ip"], y["port"], y["description"])
        ret.append((s, s))
    return ret
