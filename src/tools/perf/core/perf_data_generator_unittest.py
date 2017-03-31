# Copyright 2017 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
import unittest

from core import perf_data_generator
from core.perf_data_generator import BenchmarkMetadata


class PerfDataGeneratorTest(unittest.TestCase):

  def testVerifyAllTestsInBenchmarkCsvPassesWithCorrectInput(self):
    tests = {
        'AAAAA1 AUTOGENERATED': {},
        'Android Nexus5 Perf (2)': {
            'scripts': [
                {'name': 'benchmark_name_1'},
                {'name': 'benchmark_name_2'}
            ]
        },
        'Linux Perf': {
            'isolated_scripts': [
                {'name': 'benchmark_name_2.reference'},
                {'name': 'benchmark_name_3'}
            ]
        }
    }
    benchmarks = {
        'benchmark_name_1': BenchmarkMetadata(None, None),
        'benchmark_name_2': BenchmarkMetadata(None, None),
        'benchmark_name_3': BenchmarkMetadata(None, None)
    }

    perf_data_generator.verify_all_tests_in_benchmark_csv(tests, benchmarks)


  def testVerifyAllTestsInBenchmarkCsvCatchesMismatchedTests(self):
    tests = {
        'Android Nexus5 Perf (2)': {
            'scripts': [
                {'name': 'benchmark_name_1'},
                {'name': 'benchmark_name_2'}
            ]
        }
    }
    benchmarks = {
        'benchmark_name_2': BenchmarkMetadata(None, None),
        'benchmark_name_3': BenchmarkMetadata(None, None),
    }

    with self.assertRaises(AssertionError) as context:
      perf_data_generator.verify_all_tests_in_benchmark_csv(tests, benchmarks)
    exception = context.exception.message
    self.assertTrue('Add benchmark_name_1' in exception)
    self.assertTrue('Remove benchmark_name_3' in exception)


  def testVerifyAllTestsInBenchmarkCsvFindsFakeTest(self):
    tests = {'Random fake test': {}}
    benchmarks = {
        'benchmark_name_1': BenchmarkMetadata(None, None)
    }

    with self.assertRaises(AssertionError) as context:
      perf_data_generator.verify_all_tests_in_benchmark_csv(tests, benchmarks)
    self.assertTrue('Unknown test' in context.exception.message)