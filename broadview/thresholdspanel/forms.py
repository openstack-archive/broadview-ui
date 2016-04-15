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

from django.utils.text import normalize_newlines
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from horizon import forms
from openstack_dashboard.dashboards.broadview import switches 
import subprocess
import json
import sys

from oslo_log import log as logging

LOG = logging.getLogger(__name__)

def updateBSTSwitchThresholds(data):
    undef = "<enter threshold>"

    LOG.info("updateBSTSwitchThresholds: enter")
    args = ["bv-bstctl.py", "cfg-thresholds"]

    if data["include_ingress_port_service_pool_um_share_threshold"] != undef:
        args.append("ingress-port-service-pool:{}:{}:{}".format(\
            data["include_ingress_port_service_pool_port"], \
            data["include_ingress_port_service_pool_service_pool"], \
            data["include_ingress_port_service_pool_um_share_threshold"]))

    if data["include_egress_cpu_queue_cpu_threshold"] != undef:
        args.append("egress-cpu-queue:{}:{}".format(\
            data["include_egress_cpu_queue_cpu_queue"], \
            data["include_egress_cpu_queue_cpu_threshold"]))

    if data["include_device_threshold"] != undef:
        args.append("device:{}".format(data["include_device_threshold"]))

    if data["include_egress_port_service_pool_mc_share_threshold"] != undef and\
       data["include_egress_port_service_pool_uc_share_threshold"] != undef and\
       data["include_egress_port_service_pool_um_share_threshold"] != undef and\
       data["include_egress_port_service_pool_mc_share_queue_entries_threshold"] != undef:
        args.append("egress-port-service-pool:{}:{}:{}:{}:{}:{}".format(\
            data["include_egress_port_service_pool_port"], \
            data["include_egress_port_service_pool_service_pool"], \
            data["include_egress_port_service_pool_uc_share_threshold"], \
            data["include_egress_port_service_pool_um_share_threshold"], \
            data["include_egress_port_service_pool_mc_share_threshold"], \
            data["include_egress_port_service_pool_mc_share_queue_entries_threshold"]))

    if data["include_ingress_service_pool_um_share_threshold"] != undef:
        args.append("ingress-service-pool:{}:{}".format(\
            data["include_ingress_service_pool_service_pool"], \
            data["include_ingress_service_pool_um_share_threshold"]))

    if data["include_egress_uc_queue_uc_threshold"] != undef:
        args.append("egress-uc-queue:{}:{}".format(\
            data["include_egress_uc_queue_uc_queue"], \
            data["include_egress_uc_queue_uc_threshold"]))

    if data["include_egress_service_pool_mc_share_threshold"] != undef and \
       data["include_egress_service_pool_um_share_threshold"] != undef and \
       data["include_egress_service_pool_mc_share_queue_entries_threshold"] != undef:
        args.append("egress-service-pool:{}:{}:{}:{}".format(\
            data["include_egress_service_pool_service_pool"], \
            data["include_egress_service_pool_um_share_threshold"], \
            data["include_egress_service_pool_mc_share_threshold"], \
            data["include_egress_service_pool_mc_share_queue_entries_threshold"]))

    if data["include_egress_rqe_queue_rqe_threshold"] != undef:
        args.append("egress-rqe-queue:{}:{}".format(\
            data["include_egress_rqe_queue_rqe_queue"], \
            data["include_egress_rqe_queue_rqe_threshold"]))

    if data["include_egress_uc_queue_group_uc_threshold"] != undef:
        args.append("egress-uc-queue-group:{}:{}".format(\
            data["include_egress_uc_queue_group_uc_queue_group"], \
            data["include_egress_uc_queue_group_uc_threshold"]))

    if data["include_egress_mc_queue_mc_queue_entries_threshold"] != undef:
        args.append("egress-mc-queue:{}:{}".format(\
            data["include_egress_mc_queue_mc_queue"], \
            data["include_egress_mc_queue_mc_queue_entries_threshold"]))

    if data["include_ingress_port_priority_group_um_headroom_threshold"] != undef and\
       data["include_ingress_port_priority_group_um_share_threshold"] != undef:
        args.append("ingress-port-priority-group:{}:{}:{}:{}".format(\
            data["include_ingress_port_priority_group_port"], \
            data["include_ingress_port_priority_group_priority_group"], \
            data["include_ingress_port_priority_group_um_share_threshold"], \
            data["include_ingress_port_priority_group_um_headroom_threshold"]))

    switch = data["switch"].split(" ")[0].split(":")
    args.append("host:{}".format(switch[0]))
    args.append("port:{}".format(switch[1]))
    args.append("timeout:30")

    try:
        output = subprocess.Popen(args, stdout=subprocess.PIPE).communicate()[0]
        output = json.loads(output)
    except:
        LOG.info("updateBSTSwitchThresholds: unable to execute bv-bstctl {}".format(sys.exc_info()[0]))

class BSTThresholdsForm(forms.SelfHandlingForm):
    yes_no_choices = [('yes', _('Yes')),
                      ('no', _('No'))]

    switch_choices = switches.getBSTSwitchChoices()

    # the actual ranges are passed to the template as context
    # data. Here, we set the choices to min max so that the
    # middleware will validate (and pass along to handlers). 

    nochoices = [(x, x) for x in range(0, 4098)]

    switch = forms.ChoiceField(
        label=_('Select a switch'),
        choices=switch_choices,
        widget=forms.Select(attrs={
            'style': "width:250px",
            'class': 'switchable',
            'data-slug': 'switch'}),
        required=False)

    include_ingress_port_priority_group_port = forms.ChoiceField(
        label=_(''),
        choices=nochoices,
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'include_ingress_port_priority_group_port'}),
        required=False)

    include_ingress_port_priority_group_priority_group = forms.ChoiceField(
        label=_(''),
        choices=nochoices,
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'include_ingress_port_priority_group_priority_group'}),
        required=False)

    include_ingress_port_priority_group_um_share_threshold = forms.CharField(
        label=_(''),
        widget=forms.widgets.TextInput(),
        required=False)

    include_ingress_port_priority_group_um_headroom_threshold = forms.CharField(
        label=_(''),
        widget=forms.widgets.TextInput(),
        required=False)

    include_ingress_port_service_pool_port = forms.ChoiceField(
        label=_(''),
        choices=nochoices,
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'include_ingress_port_service_pool_port'}),
        required=False)

    include_ingress_port_service_pool_service_pool = forms.ChoiceField(
        label=_(''),
        choices=nochoices,
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'include_ingress_port_service_pool_service_pool'}),
        required=False)

    include_ingress_port_service_pool_um_share_threshold = forms.CharField(
        label=_(''),
        widget=forms.widgets.TextInput(),
        required=False)

    include_egress_port_service_pool_port = forms.ChoiceField(
        label=_(''),
        choices=nochoices,
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'include_egress_port_service_pool_port'}),
        required=False)

    include_egress_port_service_pool_service_pool = forms.ChoiceField(
        label=_(''),
        choices=nochoices,
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'include_egress_port_service_pool_service_pool'}),
        required=False)

    include_egress_port_service_pool_uc_share_threshold = forms.CharField(
        label=_(''),
        widget=forms.widgets.TextInput(),
        required=False)

    include_egress_port_service_pool_um_share_threshold = forms.CharField(
        label=_(''),
        widget=forms.widgets.TextInput(),
        required=False)

    include_egress_port_service_pool_mc_share_threshold = forms.CharField(
        label=_(''),
        widget=forms.widgets.TextInput(),
        required=False)

    include_egress_port_service_pool_mc_share_queue_entries_threshold = forms.CharField(
        label=_(''),
        widget=forms.widgets.TextInput(),
        required=False)

    include_egress_uc_queue_group_uc_queue_group = forms.ChoiceField(
        label=_(''),
        choices=nochoices,
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'include_egress_uc_queue_group_uc_queue_group'}),
        required=False)

    include_egress_uc_queue_group_uc_threshold = forms.CharField(
        label=_(''),
        widget=forms.widgets.TextInput(),
        required=False)

    include_egress_uc_queue_uc_queue = forms.ChoiceField(
        label=_(''),
        choices=nochoices,
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'include_egress_uc_queue_uc_queue'}),
        required=False)

    include_egress_uc_queue_uc_threshold = forms.CharField(
        label=_(''),
        widget=forms.widgets.TextInput(),
        required=False)

    include_egress_mc_queue_mc_queue = forms.ChoiceField(
        label=_(''),
        choices=nochoices,
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'include_egress_mc_queue_mc_queue'}),
        required=False)

    include_egress_mc_queue_mc_queue_entries_threshold = forms.CharField(
        label=_(''),
        widget=forms.widgets.TextInput(),
        required=False)

    include_ingress_service_pool_service_pool = forms.ChoiceField(
        label=_(''),
        choices=nochoices,
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'include_ingress_service_pool_service_pool'}),
        required=False)

    include_ingress_service_pool_um_share_threshold = forms.CharField(
        label=_(''),
        widget=forms.widgets.TextInput(),
        required=False)

    include_egress_service_pool_service_pool = forms.ChoiceField(
        label=_(''),
        choices=nochoices,
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'include_egress_service_pool_service_pool'}),
        required=False)

    include_egress_service_pool_um_share_threshold = forms.CharField(
        label=_(''),
        widget=forms.widgets.TextInput(),
        required=False)

    include_egress_service_pool_mc_share_threshold = forms.CharField(
        label=_(''),
        widget=forms.widgets.TextInput(),
        required=False)

    include_egress_service_pool_mc_share_queue_entries_threshold = forms.CharField(
        label=_(''),
        widget=forms.widgets.TextInput(),
        required=False)

    include_egress_rqe_queue_rqe_queue = forms.ChoiceField(
        label=_(''),
        choices=nochoices,
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'include_egress_rqe_queue_rqe_queue'}),
        required=False)

    include_egress_rqe_queue_rqe_threshold = forms.CharField(
        label=_(''),
        widget=forms.widgets.TextInput(),
        required=False)

    include_egress_cpu_queue_cpu_queue = forms.ChoiceField(
        label=_(''),
        choices=nochoices,
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'include_egress_cpu_queue_cpu_queue'}),
        required=False)

    include_egress_cpu_queue_cpu_threshold = forms.CharField(
        label=_(''),
        widget=forms.widgets.TextInput(),
        required=False)

    include_device_threshold = forms.CharField(
        label=_(''),
        widget=forms.widgets.TextInput(),
        required=False)

    class Meta(object):
        name = _('BST Edit Feature')

    def clean(self):
        cleaned = super(BSTThresholdsForm, self).clean()
        LOG.info('leave clean {}'.format(cleaned))

        return cleaned

    def handle(self, request, data):
        LOG.info('enter handle {}'.format(data))
        updateBSTSwitchThresholds(data) 
        LOG.info('leave handle')
        return redirect(request.build_absolute_uri())
