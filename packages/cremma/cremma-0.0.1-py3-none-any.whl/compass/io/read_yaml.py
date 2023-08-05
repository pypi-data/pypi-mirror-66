import yaml
from compass.core.report_frame import Report

def read_yaml(filepath):
    ''' Reads yaml to return a report'''

    txt = open(filepath, "r"). read()
    specs = yaml.load(txt, Loader=yaml.CLoader)

    rp = Report(specs)

    return rp

