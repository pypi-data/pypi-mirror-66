# Copyright 2019 WHG (International) Limited. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import argparse
import json
from pprint import pprint

from ccvs_scanning_api_client.command import analysis


def main():
    parser = argparse.ArgumentParser(
        description='Find vulnabilities in docker images.')

    parser.add_argument(
        '--imagetag',
        help='docker image: docker-registry.exemple.com/image:tag',
        dest='image_tag',
        required=True)

    image_tag = parser.parse_args().image_tag
    analysis_result = analysis.analysis(image_tag)
    results = analysis.resume(analysis_result)
    pprint(json.dumps(results))  # noqa


if __name__ == '__main__':
    main()
