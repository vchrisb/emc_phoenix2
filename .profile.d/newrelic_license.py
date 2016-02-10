import os
import json

if 'VCAP_SERVICES' in os.environ:
    vcap_services = json.loads(os.environ['VCAP_SERVICES'])

    if 'newrelic' in vcap_services:
        NEW_RELIC_LICENSE_KEY = vcap_services['newrelic'][0]['credentials']['licenseKey']

print(NEW_RELIC_LICENSE_KEY)
