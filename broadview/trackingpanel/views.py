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

from openstack_dashboard.dashboards.broadview.trackingpanel import forms as bst_forms

import subprocess
import json
import sys

from openstack_dashboard.dashboards.broadview import switches
from openstack_dashboard.dashboards.broadview import common

from oslo_log import log as logging

LOG = logging.getLogger(__name__)

def getBSTSwitchTracking(host, port):
    ret = []
    first = None
    x = switches.getBSTSwitches()
    for y in x:
        try:
            output = subprocess.Popen(\
                ["bv-bstctl.py", "get-tracking", "timeout:30", "host:{}".format(y["ip"]), \
                "port:{}".format(y["port"])], \
                stdout=subprocess.PIPE).communicate()[0]
            output = json.loads(output)
            output["host"] = y["ip"]
            output["port"] = y["port"]
            if output:
                if host == y["ip"] and port == y["port"]:
                    first = output
                else:
                    ret.append(output)
        except:
            LOG.info("getBSTSwitchTracking: unable to execute bv-bstctl {}".format(sys.exc_info()[0]))
    # if we found a switch matching the specified host, port, put it at the
    # head of the list

    if first:
        ret.insert(0, first)
    return ret

class TrackingUpdateView(forms.ModalFormView):

    form_class = bst_forms.BSTTrackingForm
    form_id = "edit_feature"
    page_title = _("Configure BST Tracking")
    submit_url = reverse_lazy('horizon:broadview:trackingpanel:index')
    cancel_url = reverse_lazy('horizon:broadview:trackingpanel:index')
    success_url = reverse_lazy('horizon:broadview:trackingpanel:update')
    template_name = 'broadview/trackingpanel/form.html'

    def get_initial(self):
        initial = super(TrackingUpdateView, self).get_initial()
        host_port = None
        host = None
        port = None

        try:
            host_port = self.kwargs['host_port']
        except:
            pass

        if host_port:
            host, port = common.getHostPort(host_port)
            self.host_port = host_port
            
        switch = getBSTSwitchTracking(host, port)
        if len(switch):
            switch = switch[0]
            try:
                initial["track_peak_stats"] = "yes" if switch["track-peak-stats"] else "no"
            except:
                LOG.info("get_initial: unable to initialize track_peak_stats")
                
            try:
                initial["track_ingress_port_priority_group"] = "yes" if switch["track-ingress-port-priority-group"] else "no"
            except:
                LOG.info("get_initial: unable to initialize track_ingress_port_priority_group")
                
            try:
                initial["track_ingress_port_service_pool"] = "yes" if switch["track-ingress-port-service-pool"] else "no"
            except:
                LOG.info("get_initial: unable to initialize track_ingress_port_service_pool")
                
            try:
                initial["track_ingress_service_pool"] = "yes" if switch["track-ingress-service-pool"] else "no"
            except:
                LOG.info("get_initial: unable to initialize track_ingress_service_pool")
                
            try:
                initial["track_egress_port_service_pool"] = "yes" if switch["track-egress-port-service-pool"] else "no"
            except:
                LOG.info("get_initial: unable to initialize track_egress_port_service_pool")
                
            try:
                initial["track_egress_service_pool"] = "yes" if switch["track-egress-service-pool"] else "no"
            except:
                LOG.info("get_initial: unable to initialize track_egress_service_pool")
                
            try:
                initial["track_egress_uc_queue"] = "yes" if switch["track-egress-uc-queue"] else "no"
            except:
                LOG.info("get_initial: unable to initialize track_egress_uc_queue")
                
            try:
                initial["track_egress_uc_queue_group"] = "yes" if switch["track-egress-uc-queue-group"] else "no"
            except:
                LOG.info("get_initial: unable to initialize track_egress_uc_queue_group")
                
            try:
                initial["track_egress_mc_queue"] = "yes" if switch["track-egress-mc-queue"] else "no"
            except:
                LOG.info("get_initial: unable to initialize track_egress_mc_queue")
                
            try:
                initial["track_egress_cpu_queue"] = "yes" if switch["track-egress-cpu-queue"] else "no"
            except:
                LOG.info("get_initial: unable to initialize track_egress_cpu_queue")
                
            try:
                initial["track_egress_rqe_queue"] = "yes" if switch["track-egress-rqe-queue"] else "no"
            except:
                LOG.info("get_initial: unable to initialize track_egress_rqe_queue")
                
            try:
                initial["track_device"] = "yes" if switch["track-device"] else "no"
            except:
                LOG.info("get_initial: unable to initialize track_device")
                
        
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

        context = super(TrackingUpdateView, self).get_context_data(**kwargs)
        features = getBSTSwitchTracking(host, port)
        context["bst_switches"] = common.hyphen2underscore(features)
        return context

    def get_success_url(self, **kwargs):
        if self.host_port:
           kwargs["host_port"] = self.host_port

        return reverse('horizon:broadview:trackingpanel:update', kwargs=kwargs)
