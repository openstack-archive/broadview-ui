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

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import forms
from horizon import tables
from horizon import views

from broadview_lib.config.bst import GetBSTThresholds

from openstack_dashboard.dashboards.broadview.thresholdspanel import forms as bst_forms

import json
import sys

from openstack_dashboard.dashboards.broadview import switches
from openstack_dashboard.dashboards.broadview import common

from oslo_log import log as logging

LOG = logging.getLogger(__name__)

def getIngressPortPriorityGroupRange(data):
    ports = set()
    priority_groups = set() 

    d = data.getIngressPortPriorityGroup() 
    for x in d:
        for y in x:
            ports.add(int(y.getPort()))
            priority_groups.add(int(y.getPriorityGroup()))

    return {"ports": sorted(list(ports)),
            "priority_groups": sorted(list(priority_groups))}

def getEgressPortServicePoolRange(data):
    ports = set()
    service_pools = set() 

    d = data.getEgressPortServicePool() 
    for x in d:
        for y in x:
            ports.add(int(y.getPort()))
            service_pools.add(int(y.getServicePool()))

    return {"ports": sorted(list(ports)),
            "service_pools": sorted(list(service_pools))}

def getIngressPortServicePoolRange(data):
    ports = set()
    service_pools = set() 

    d = data.getIngressPortServicePool() 
    for x in d:
        for y in x:
            ports.add(int(y.getPort()))
            service_pools.add(int(y.getServicePool()))

    return {"ports": sorted(list(ports)),
            "service_pools": sorted(list(service_pools))}

def getEgressUcQueueRange(data):
    queues = set()

    d = data.getEgressUcQueue() 
    for x in d:
        for y in x:
            queues.add(int(y.getQueue()))

    return {"queues": sorted(list(queues))}

def getEgressUcQueueGroupRange(data):
    queue_groups = set()

    d = data.getEgressUcQueueGroup() 
    for x in d:
        for y in x:
            queue_groups.add(int(y.getQueueGroup()))

    return {"queue_groups": sorted(list(queue_groups))}

def getEgressMcQueueRange(data):
    queues = set()

    d = data.getEgressMcQueue() 
    for x in d:
        for y in x:
            queues.add(int(y.getQueue()))

    return {"queues": sorted(list(queues))}

def getIngressServicePoolRange(data):
    service_pools = set()

    d = data.getIngressServicePool() 
    for x in d:
        for y in x:
            service_pools.add(int(y.getServicePool()))

    return {"service_pools": sorted(list(service_pools))}

def getEgressServicePoolRange(data):
    service_pools = set()

    d = data.getEgressServicePool() 
    for x in d:
        for y in x:
            service_pools.add(int(y.getServicePool()))

    return {"service_pools": sorted(list(service_pools))}

def getEgressCPUQueueRange(data):
    queues = set()

    d = data.getEgressCPUQueue() 
    for x in d:
        for y in x:
            queues.add(int(y.getQueue()))

    return {"queues": sorted(list(queues))}

def getEgressRQEQueueRange(data):
    queues = set()

    d = data.getEgressRQEQueue() 
    for x in d:
        for y in x:
            queues.add(int(y.getQueue()))

    return {"queues": sorted(list(queues))}

def getDeviceRange(data):
    return {}

def getThresholdRanges(realm, data):
    ret = None

    dispatch = [{"include_ingress_port_priority_group":
                 getIngressPortPriorityGroupRange},  
                {"include_ingress_port_service_pool": 
                 getIngressPortServicePoolRange},  
                {"include_egress_port_service_pool": 
                 getEgressPortServicePoolRange},  
                {"include_egress_uc_queue": 
                 getEgressUcQueueRange},  
                {"include_egress_uc_queue_group": 
                 getEgressUcQueueGroupRange},  
                {"include_egress_mc_queue": 
                 getEgressMcQueueRange},  
                {"include_ingress_service_pool": 
                 getIngressServicePoolRange},  
                {"include_egress_service_pool": 
                 getEgressServicePoolRange},  
                {"include_egress_cpu_queue": 
                 getEgressCPUQueueRange},  
                {"include_egress_rqe_queue": 
                 getEgressRQEQueueRange},  
                {"include_device":
                 getDeviceRange}]
        
    for x in dispatch:
        if realm in x:
            ret = x[realm](data)
            break
    return ret 

def getBSTSwitchThresholds(host, port):
    thresholds = [ "include_ingress_port_priority_group", \
                   "include_ingress_port_service_pool", \
                   "include_egress_port_service_pool", \
                   "include_egress_uc_queue", \
                   "include_egress_uc_queue_group", \
                   "include_egress_mc_queue", \
                   "include_ingress_service_pool", \
                   "include_egress_service_pool", \
                   "include_egress_cpu_queue", \
                   "include_egress_rqe_queue", \
                   "include_device"] 
    ret = []
    first = None
    x = switches.getBSTSwitches()
    for y in x:
        try:
            # the agent doesn't seem to be able to pass back large
            # amounts of data without truncating it, so get the data 
            # in multiple requests.  TODO file a bug on this

            for thresh in thresholds:
                swdata = {}
                o = GetBSTThresholds(y["ip"], int(y["port"]))
                
                o.setIncludeIngressPortPriorityGroup("include_ingress_port_priority_group" in thresh)
                o.setIncludeIngressPortServicePool("include_ingress_port_service_pool" in thresh)
                o.setIncludeIngressServicePool("include_ingress_service_pool" in thresh)
                o.setIncludeEgressPortServicePool("include_egress_port_service_pool" in thresh)
                o.setIncludeEgressServicePool("include_egress_service_pool" in thresh)
                o.setIncludeEgressUcQueue("include_egress_uc_queue" in thresh)
                o.setIncludeEgressUcQueueGroup("include_egress_uc_queue_group" in thresh)
                o.setIncludeEgressMcQueue("include_egress_mc_queue" in thresh)
                o.setIncludeEgressCPUQueue("include_egress_cpu_queue" in thresh)
                o.setIncludeEgressRQEQueue("include_egress_rqe_queue" in thresh)
                o.setIncludeDevice("include_device" in thresh)

                status, rep = o.send(30)

                if status == 200:
                    j = json.dumps(o.getJSON())
                    swdata["realm"] = thresh
                    swdata["data"] = j  
                    swdata["host"] = y["ip"]
                    swdata["port"] = y["port"]
                    ranges = getThresholdRanges(thresh, rep)
                    swdata["ranges"] = ranges
                else:
                    LOG.info("getBSTSwitchThresholds: failure {}".format(status)) 
                if len(swdata):
                    ret.append(swdata)

        except:
            LOG.info("getBSTSwitchThresholds: exception {}".format(sys.exc_info()[0]))
    return ret

class ThresholdsUpdateView(forms.ModalFormView):

    form_class = bst_forms.BSTThresholdsForm
    form_id = "edit_thresholds"
    page_title = _("Configure BST Thresholds")
    submit_url = reverse_lazy('horizon:broadview:thresholdspanel:index')
    cancel_url = reverse_lazy('horizon:broadview:thresholdspanel:index')
    success_url = reverse_lazy('horizon:broadview:thresholdspanel:update')
    template_name = 'broadview/thresholdspanel/form.html'

    def __init__(self):
        super(ThresholdsUpdateView, self).__init__()
        self._thresholds = None

    def get_initial(self):
        initial = super(ThresholdsUpdateView, self).get_initial()
        return initial

    def get_context_data(self, **kwargs):
        host = None
        port = None
        host_port = None

        try:
            host_port = self.kwargs['host_port']
        except:
            pass

        if host_port:
            host, port = common.getHostPort(host_port)

        context = super(ThresholdsUpdateView, self).get_context_data(**kwargs)

        if not self._thresholds:
            self._thresholds = getBSTSwitchThresholds(host, port)

        context["bst_switches"] = self._thresholds
        return context

    def get_success_url(self, **kwargs):
        if self.host_port:
           kwargs["host_port"] = self.host_port

        return reverse('horizon:broadview:thresoldspanel:update', kwargs=kwargs)
