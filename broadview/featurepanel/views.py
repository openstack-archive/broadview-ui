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

from openstack_dashboard.dashboards.broadview.featurepanel import forms as bst_forms

import subprocess
import json
import sys

from openstack_dashboard.dashboards.broadview import switches
from openstack_dashboard.dashboards.broadview import common

from oslo_log import log as logging

LOG = logging.getLogger(__name__)

def getBSTSwitchFeatures(host, port):
    ret = []
    first = None
    x = switches.getBSTSwitches()
    for y in x:
        try:
            output = subprocess.Popen(\
                ["bv-bstctl.py", "get-feature", "timeout:30", "host:{}".format(y["ip"]), \
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
            LOG.info("getBSTSwitchFeatures: unable to execute bv-bstctl {}".format(sys.exc_info()[0]))

    # if we found a switch matching the specified host, port, put it at the
    # head of the list

    if first:
        ret.insert(0, first)
    return ret

class FeatureUpdateView(forms.ModalFormView):

    form_class = bst_forms.BSTFeatureForm
    form_id = "edit_feature"
    page_title = _("Configure BST Feature")
    submit_url = reverse_lazy('horizon:broadview:featurepanel:index')
    cancel_url = reverse_lazy('horizon:broadview:featurepanel:index')
    success_url = reverse_lazy('horizon:broadview:featurepanel:update')
    template_name = 'broadview/featurepanel/form.html'

    def get_initial(self):
        initial = super(FeatureUpdateView, self).get_initial()
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
            
        switch = getBSTSwitchFeatures(host, port)
        if len(switch):
            switch = switch[0]
            try:
                initial["enable"] = "yes" if switch["bst-enable"] else "no"
            except:
                LOG.info("get_initial: unable to initialize enable")
                
            try:
                initial["send_async_reports"] = "yes" if switch["send-async-reports"] else "no"
            except:
                LOG.info("get_initial: unable to initialize send_async_reports")
                
            try:
                initial["stat_in_percentage"] = "yes" if switch["stat-in-percentage"] else "no"
            except:
                LOG.info("get_initial: unable to initialize stat_in_percentage")
                
            try:
                initial["stat_units_in_cells"] = "yes" if switch["stat-units-in-cells"] else "no"
            except:
                LOG.info("get_initial: unable to initialize stat_units_in_cells")
                
            try:
                initial["send_snapshot_on_trigger"] = "yes" if switch["send-snapshot-on-trigger"] else "no"
            except:
                LOG.info("get_initial: unable to initialize send_snapshot_on_trigger")
                
            try:
                initial["async_full_reports"] = "yes" if switch["async-full-reports"] else "no"
            except:
                LOG.info("get_initial: unable to initialize async_full_reports")
                
            try:
                initial["collection_interval"] = int(switch["collection-interval"])
            except:
                LOG.info("get_initial: unable to initialize collection_interval")
                
            try:
                initial["trigger_rate_limit"] = int(switch["trigger-rate-limit"])
            except:
                LOG.info("get_initial: unable to initialize trigger_rate_limit")
                
            try:
                initial["trigger_rate_limit_interval"] = int(switch["trigger-rate-limit-interval"])
            except:
                LOG.info("get_initial: unable to initialize trigger_rate_limit_interval")
        
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

        context = super(FeatureUpdateView, self).get_context_data(**kwargs)
        features = getBSTSwitchFeatures(host, port)
        context["bst_switches"] = common.hyphen2underscore(features)
        return context

    def get_success_url(self, **kwargs):
        if self.host_port:
           kwargs["host_port"] = self.host_port

        return reverse('horizon:broadview:featurepanel:update', kwargs=kwargs)
