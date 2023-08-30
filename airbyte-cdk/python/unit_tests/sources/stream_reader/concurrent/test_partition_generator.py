#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
#

from queue import Queue
from unittest.mock import Mock

import pytest
from airbyte_cdk.models import SyncMode
from airbyte_cdk.sources.stream_reader.concurrent.partition_generator import PartitionGenerator
from airbyte_cdk.sources.stream_reader.concurrent.stream_partition import StreamPartition


@pytest.mark.parametrize(
    "partitions", [pytest.param([], id="test_no_partitions"), pytest.param([{"partition": 1}, {"partition": 2}], id="test_two_partitions")]
)
def test_partition_generator(partitions):
    queue = Queue()
    partition_generator = PartitionGenerator(queue, "A")

    stream = Mock()
    stream.generate_partitions.return_value = iter(partitions)

    sync_mode = SyncMode.full_refresh
    cursor_field = ["A_NESTED", "CURSOR_FIELD"]

    assert queue.empty()

    actual_partitions = list(partition_generator.generate_partitions_for_stream(stream, sync_mode, cursor_field))

    expected_partitions = [StreamPartition(stream, p, cursor_field) for p in partitions]
    assert actual_partitions == expected_partitions

    partitions_from_queue = []
    while queue.qsize() > 0:
        partitions_from_queue.append(queue.get())

    assert partitions_from_queue == expected_partitions