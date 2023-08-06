#!/usr/bin/env python

from jinja2 import Template
import os

diagnostic_endpoints = [
    {"name": "API", "endpoint": "/heartbeat"},
    {"name": "Upstream - IProperty MY",
     "endpoint": "tcp://ca1i1tqbwmeff73.cyl26brsmuwz.ap-southeast-1.rds.amazonaws.com:3306"},
    {"name": "Downstream - Some API", "endpoint": "tcp://auroradb.cust-tools.prod.sg.rea-asia.local:3307"},
    {"name": "Database", "endpoint": "tcp://ca1i1tqbwmeff73.cyl26brsmuwz.ap-southeast-1.rds.amazonaws.com:3306"}
]


def get_status(endpoints):
    status = "All Systems Are Operational"
    for endpoint in endpoints:
        endpoint_status = endpoint["status"]
        if endpoint_status == "Not Operational":
            status = "Not All Systems Are Operational"
            break
    return status


def render_html(diagnostic_components):
    status = get_status(diagnostic_endpoints)
    length = len(diagnostic_endpoints)
    current_path = os.path.dirname(os.path.realpath(__file__))
    with open(f"{current_path}/templates/diagnostics.html", 'r') as template_html:
        template = Template(template_html.read())
        return template.render(len=length, diagnostic_components=diagnostic_components, status=status)


if __name__ == "__main__":
    current_path = os.path.dirname(os.path.realpath(__file__))
    with open(f"{current_path}/templates/diagnostics_generated.html", 'w') as generated_html:
        generated_html.write(render_html(diagnostic_endpoints))
