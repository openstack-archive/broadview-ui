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

def updateBSTSwitchTracking(data):

    args = ["bv-bstctl.py", "cfg-tracking"]
    if "track_peak_stats" in data and data["track_peak_stats" ] == "yes":
        args.append("track_peak_stats")
    if  "track_ingress_port_priority_group" in data and data["track_ingress_port_priority_group"] == "yes":
        args.append("track_ingress_port_priority_group")
    if "track_ingress_port_service_pool" in data and data["track_ingress_port_service_pool"] == "yes":
        args.append("track_ingress_port_service_pool")
    if "track_ingress_service_pool" in data and data["track_ingress_service_pool"] == "yes":
        args.append("track_ingress_service_pool")
    if "track_egress_port_service_pool" in data and data["track_egress_port_service_pool"] == "yes":
        args.append("track_egress_port_service_pool")
    if "track_egress_service_pool" in data and data["track_egress_service_pool"] == "yes":
        args.append("track_egress_service_pool")
    if "track_egress_uc_queue" in data and data["track_egress_uc_queue"] == "yes":
        args.append("track_egress_uc_queue")
    if "track_egress_uc_queue_group" in data and data["track_egress_uc_queue_group"] == "yes":
        args.append("track_egress_uc_queue_group")
    if "track_egress_mc_queue" in data and data["track_egress_mc_queue"] == "yes":
        args.append("track_egress_mc_queue")
    if "track_egress_cpu_queue" in data and data["track_egress_cpu_queue"] == "yes":
        args.append("track_egress_cpu_queue")
    if "track_egress_rqe_queue" in data and data["track_egress_rqe_queue"] == "yes":
        args.append("track_egress_rqe_queue")
    if "track_device" in data and data["track_device"] == "yes":
        args.append("track_device")

    switch = data["switch"].split(" ")[0].split(":")
    args.append("host:{}".format(switch[0]))
    args.append("port:{}".format(switch[1]))
    args.append("timeout:30")

    try:
        output = subprocess.Popen(args, stdout=subprocess.PIPE).communicate()[0]
        output = json.loads(output)
    except:
        LOG.info("updateBSTSwitchTracking: unable to execute bv-bstctl {}".format(sys.exc_info()[0]))


class BSTTrackingForm(forms.SelfHandlingForm):
    yes_no_choices = [('yes', _('Yes')),
                      ('no', _('No'))]

    switch_choices = switches.getBSTSwitchChoices()

    switch = forms.ChoiceField(
        label=_('Select a switch to configure'),
        choices=switch_choices,
        widget=forms.Select(attrs={
            'style': "width:250px",
            'class': 'switchable',
            'data-slug': 'switch'}),
        required=True)

    track_peak_stats = forms.ChoiceField(
        label=_('Peak Stats'),
        choices=yes_no_choices,
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'track_peak_stats'}),
        required=True)

    track_ingress_port_priority_group = forms.ChoiceField(
        label=_('Ingress Port Priority Group'),
        choices=yes_no_choices,
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'track_ingress_port_priority_group'}),
        required=True)

    track_ingress_port_service_pool = forms.ChoiceField(
        label=_('Ingress Port Service Pool'),
        choices=yes_no_choices,
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'track_ingress_port_service_pool'}),
        required=True)

    track_ingress_service_pool = forms.ChoiceField(
        label=_('Ingress Service Pool'),
        choices=yes_no_choices,
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'track_ingress_service_pool'}),
        required=True)

    track_egress_port_service_pool = forms.ChoiceField(
        label=_('Egress Port Service Pool'),
        choices=yes_no_choices,
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'track_egress_port_service_pool'}),
        required=True)

    track_egress_service_pool = forms.ChoiceField(
        label=_('Egress Service Pool'),
        choices=yes_no_choices,
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'track_egress_service_pool'}),
        required=True)

    track_egress_uc_queue = forms.ChoiceField(
        label=_('Egress Uc Queue'),
        choices=yes_no_choices,
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'track_egress_uc_queue'}),
        required=True)

    track_egress_uc_queue_group = forms.ChoiceField(
        label=_('Egress Uc Queue Group'),
        choices=yes_no_choices,
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'track_egress_uc_queue_group'}),
        required=True)

    track_egress_mc_queue = forms.ChoiceField(
        label=_('Egress Mc Queue'),
        choices=yes_no_choices,
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'track_egress_mc_queue'}),
        required=True)

    track_egress_cpu_queue = forms.ChoiceField(
        label=_('Egress CPU Queue'),
        choices=yes_no_choices,
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'track_egress_cpu_queue'}),
        required=True)

    track_egress_rqe_queue = forms.ChoiceField(
        label=_('Egress RQE Queue'),
        choices=yes_no_choices,
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'track_egress_rqe_queue'}),
        required=True)

    track_device = forms.ChoiceField(
        label=_('Device'),
        choices=yes_no_choices,
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'track_device'}),
        required=True)

    class Meta(object):
        name = _('BST Configure Tracking')

    def clean(self):
        cleaned = super(BSTTrackingForm, self).clean()

        return cleaned

    def handle(self, request, data):
        updateBSTSwitchTracking(data) 
        return redirect(request.build_absolute_uri())
