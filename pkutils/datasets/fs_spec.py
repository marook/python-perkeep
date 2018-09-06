#
# -*- coding: utf-8 -*-
# python-perkeep-utils
# Copyright (C) 2018  Markus Peröbner
#
from . import fs
import os.path as path
import tempfile
import unittest

class FileSystemDatasetWriteReadTest(unittest.TestCase):

    def test_write_floatArray_sample(self):
        with tempfile.TemporaryDirectory() as ds_dir:
            ds_path = path.join(ds_dir, 'ds')
            probes = [
                {
                    'id': 'fa',
                    'type': 'float[]',
                },
            ]
            with fs.FileSystemDatasetWriter(ds_path, probes) as w:
                w.append([[1, 2, 3]])
            r = fs.FileSystemDatasetReader(ds_path)
            self.assertEqual(r.probes[0]['id'], 'fa')
            self.assertEqual(r.probes[0]['type'], 'float[]')
            self.assertEqual(r.sample_count, 1)
            for sample in r.samples:
                self.assertEqual(sample['fa'], [1, 2, 3])

if __name__ == '__main__':
    unittest.main()
