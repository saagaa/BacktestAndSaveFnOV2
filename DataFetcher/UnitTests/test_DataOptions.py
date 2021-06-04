from unittest import TestCase
from DataFetcher.DataAggregator.DataOptions import *

class TestDataOptions(TestCase):
    def test_get_options_list(self):
        print( DataOptions.GetOptionsList())
