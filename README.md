Note
====

This repo supports versions of BroadView up to, but not including, version
3 of the agent protocol. For all later versions of BroadView, please visit
https://github.com/Broadcom-Switch/broadview-ui.

Overview
========

broadview-ui is a horizon dashboard for configuring BroadView agents.

broadview-ui currently supports BroadView BST. Support for other BroadView
components may be added as functionality is added to broadview-lib
(https://github.com/openstack/broadview-lib) and to broadview-collector
(https://github.com/openstack/broadview-collector).

Screenshot
==========

[BST Thresholds Editor](doc/images/thresholds-editor.png)

Devstack
========

Devstack support for installing broadview-ui is provided by the 
broadview-collector project. Devstack is the supported way in which this 
project is installed. 

If you are not using broadview-collector, follow the instructions outlined 
below.

Installation Prerequisites
==========================

broadview-ui itself does not have a dependency on broadview-collector,
but it does have a dependency on a component that is itself a dependency
of broadview-collector: broadview-lib. So you will need to install 
broadview-lib on your host. To do so:

* git clone https://github.com/openstack/broadview-lib.git
* cd broadview-lib
* sudo python setup.py install
* sudo cp broadview_lib/tools/bv-bstctl.py /usr/local/bin
* sudo chmod 755 /usr/local/bin/bv-bstctl.py

Further details are available in the README.md file at 
https://github.com/openstack/broadview-lib/README.md

Installation
============

After you have broadview-lib installed, follow these steps:

* git clone https://github.com/openstack/broadview-ui.git
* cp _50_broadview.py /opt/stack/horizon/openstack_dashboard/enabled/
* cp -r broadview /opt/stack/horizon/openstack_dashboard/dashboards

Configuration
=============

Broadview-ui depends on a configuration file that supplies a list of 
BroadView-enabled switches in your cluster. This configuration file is
located /etc, and is called broadviewswitches.conf. 

An example /etc/broadviewswitches.conf is located in the broadview/config 
directory of this repository. 

The config file must contain a [topology] section, and the [topology]
section must contain a setting named "bst_switches". 

The bst_switches setting is a list of dictionaries, each which contain the
following key-value pairs:

* ip: the IPV4 address of the BroadView agent
* port: the port upon which the agent is listening
* description: a short text description of the switch

Known Issues
============

* The layout of the panels needs some UI improvement
* There is no way to view the current settings of thresholds in the
thresholds panel UI. For this, you can use broadview-lib's bv-bstctl 
get-thresholds command from the commandline.
* Loading the thresholds panel is slow, particularly if multiple switches
are configured. This is due to a design choice in the underlying protocol
to the switch to obtain range values for things like ports, service pools,
and so on. We hope to address this in a future release.
* The BST clear stats and clear threshold commands are not supported.

License
=======

(C) Copyright Broadcom Corporation 2016

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.

You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

