#
# Copyright 2018 Markus Peröbner
#
'''Tools for reading, writing and manipulating datasets.

Writing a dataset:
    with perkeep.datasets.FileSystemDatasetWriter('some/ds', [
        {
            "id": "tread_left_velocity",
            "type": "float",
        },
    ]) as ds:
        for e in some_input:
            ds.append([
                e.value,
            ])

Appending a random value to a written dataset:
    ds = perkeep.datasets.RandomSampleDatasetWriter(ds)

Reading a dataset:
    ds = perkeep.datasets.build_from_resource_identifier('pk:attr:"per:type":dataset')
'''
from .common import UnionDatasetReader, ShuffleDatasetReader, split, RandomSampleDatasetWriter
from .fs import FileSystemDatasetReader, FileSystemDatasetWriter
from .pk import PerkeepDatasetReader, PerkeepDatasetWriter
from .uri import build_from_resource_identifier
