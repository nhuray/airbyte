#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
#


import sys

from airbyte_cdk.entrypoint import launch

from .source import SourceSpacexApi


def run():
    source = SourceSpacexApi()
    launch(source, sys.argv[1:])
