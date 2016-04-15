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

def updateBSTSwitchFeature(data):

    args = ["bv-bstctl.py", "cfg-feature"]
    if "stat_in_percentage" in data and data["stat_in_percentage" ] == "yes":
        args.append("stat_in_percentage")
    if  "send_snapshot_on_trigger" in data and data["send_snapshot_on_trigger"] == "yes":
        args.append("send_snapshot_on_trigger")
    if "enable" in data and data["enable"] == "yes":
        args.append("enable")
    if "stat_units_in_cells" in data and data["stat_units_in_cells"] == "yes":
        args.append("stat_units_in_cells")
    if "async_full_reports" in data and data["async_full_reports"] == "yes":
        args.append("async_full_reports")
    if "send_async_reports" in data and data["send_async_reports"] == "yes":
        args.append("send_async_reports")

    if "trigger_rate_limit" in data and len(data["trigger_rate_limit"]):
        args.append("trigger_rate_limit:{}".format(data["trigger_rate_limit"]))
    if "trigger_rate_limit_interval" in data and len(data["trigger_rate_limit_interval"]):
        args.append("trigger_rate_limit_interval:{}".format(data["trigger_rate_limit_interval"]))
    if "collection_interval" in data and len(data["collection_interval"]):
        args.append("collection_interval:{}".format(data["collection_interval"]))
    switch = data["switch"].split(" ")[0].split(":")
    args.append("host:{}".format(switch[0]))
    args.append("port:{}".format(switch[1]))
    args.append("timeout:30")

    try:
        output = subprocess.Popen(args, stdout=subprocess.PIPE).communicate()[0]
        output = json.loads(output)
    except:
        LOG.info("updateBSTSwitchFeature: unable to execute bv-bstctl {}".format(sys.exc_info()[0]))


class BSTFeatureForm(forms.SelfHandlingForm):
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

    enable = forms.ChoiceField(
        label=_('Enable BST Feature'),
        choices=yes_no_choices,
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'enable'}),
        required=True)

    send_async_reports = forms.ChoiceField(
        label=_('Send Async Reports'),
        choices=yes_no_choices,
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'send_async_reports'}),
        required=True)

    stat_in_percentage = forms.ChoiceField(
        label=_('Report Percentages'),
        choices=yes_no_choices,
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'stat_in_percentage'}),
        required=True)

    stat_units_in_cells = forms.ChoiceField(
        label=_('Report as cells'),
        choices=yes_no_choices,
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'stat_units_in_cells'}),
        required=True)

    send_snapshot_on_trigger = forms.ChoiceField(
        label=_('Send Snapshot on Trigger'),
        choices=yes_no_choices,
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'send_snapshot_on_trigger'}),
        required=True)

    async_full_reports = forms.ChoiceField(
        label=_('Async Full Reports'),
        choices=yes_no_choices,
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'async_full_reports'}),
        required=True)

    collection_interval = forms.CharField(
        label=_('Collection Interval'),
        widget=forms.widgets.TextInput(attrs={
            'class': 'switched',
            'data-switch-on': 'scriptsource',
            'data-scriptsource-raw': _('Script Data')}),
        required=False)

    trigger_rate_limit = forms.CharField(
        label=_('Trigger Rate Limit'),
        widget=forms.widgets.TextInput(attrs={
            'class': 'switched',
            'data-switch-on': 'scriptsource',
            'data-scriptsource-raw': _('Script Data')}),
        required=False)

    trigger_rate_limit_interval = forms.CharField(
        label=_('Trigger Rate Limit Interval'),
        widget=forms.widgets.TextInput(attrs={
            'class': 'switched',
            'data-switch-on': 'scriptsource',
            'data-scriptsource-raw': _('Script Data')}),
        required=False)

    class Meta(object):
        name = _('BST Edit Feature')

    def clean(self):
        cleaned = super(BSTFeatureForm, self).clean()

        return cleaned

    def handle(self, request, data):
        updateBSTSwitchFeature(data) 
        return redirect(request.build_absolute_uri())
