from django import template
import os
import json

register = template.Library()

@register.simple_tag
def vcap_application():
    if "VCAP_APPLICATION" in os.environ:
        VCAP_APPLICATION = json.loads(os.environ['VCAP_APPLICATION'])
        print(VCAP_APPLICATION['instance_index'])
        return VCAP_APPLICATION
    return None
