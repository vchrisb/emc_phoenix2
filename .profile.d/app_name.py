import os
import json

if 'VCAP_APPLICATION' in os.environ:
    VCAP_APPLICATION = json.loads(os.environ['VCAP_APPLICATION'])

    if 'application_name' in VCAP_APPLICATION:
        APPLICATION_NAME = VCAP_APPLICATION['application_name']

print(APPLICATION_NAME)
