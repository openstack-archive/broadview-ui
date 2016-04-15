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

def getHostPort(val):
    try:
        val = val.split(":")
        host = val[0]
        port = val[1]
    except:
        host = None
        port = None
    return host, port

def hyphen2underscore(data):
    # django templates don't like field names with '-' (so it appears), so
    # replace them with '_' characters

    ret = []
    for x in data:
        y = {}
        for key, val in x.iteritems():
            key = key.replace("-", '_')
            y[key] = val
        ret.append(y)
    return ret

