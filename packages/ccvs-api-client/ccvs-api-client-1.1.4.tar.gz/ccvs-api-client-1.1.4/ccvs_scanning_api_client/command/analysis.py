# Copyright 2019 WHG (International) Limited. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import os
from time import sleep

from ccvs_scanning_api_client.api.analysis_api import AnalysisApi
from ccvs_scanning_api_client.api_client import ApiClient
from ccvs_scanning_api_client.configuration import Configuration
from ccvs_scanning_api_client.models.analysis import Analysis


config = Configuration(host=os.environ.get('CCVS_API'))


def analysis(image_name):
    analysis_api = AnalysisApi(ApiClient(config))
    analysis_obj = analysis_api.analysis_create(Analysis(image=image_name))
    x = 0
    while True:
        analysis_result = analysis_api.analysis_read(analysis_obj.id)
        print('Analysis: ', analysis_obj.id)  # noqa
        if analysis_result.result == 'pending':
            b = 'Analysing image' + '.' * x
            print(b, end='\r')  # noqa
            x += 1
            sleep(5)
        else:
            print('Image Analyzed')  # noqa
            break
    return analysis_result


def resume(analysis_result):
    link = f'{config.host}container-scanning/analysis/{analysis_result.id}'
    resume = {
        'image': analysis_result.image,
        'link': link,
        'result': analysis_result.result,
        'total_vulns': {
            'high_vulns': 0,
            'medium_vulns': 0,
            'critical_vulns': 0,
            'low_vulns': 0,
            'unknown_vulns': 0,
            'negligible_vulns': 0
        }
    }

    vulns = analysis_result.vulnerabilities
    if vulns:
        for vuln in vulns.values():
            if vuln:
                for level in vuln.items():
                    resume['total_vulns'][level[0]] += len(level[1])

    return resume
