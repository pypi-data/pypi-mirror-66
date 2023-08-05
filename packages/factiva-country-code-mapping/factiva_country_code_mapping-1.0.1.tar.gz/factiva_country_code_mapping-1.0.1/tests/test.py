from factiva_country_code_mapping import CountryCodeMapping
from factiva_country_code_mapping import CountryDictionary
from factiva_country_code_mapping import CountryList

import time
import timeit
import unittest

class TestFactivaCountryCodeMappingClass(unittest.TestCase):

    def setUp(self):

        self.country_list = CountryList()
        self.country_list.create_country_list()

        self.country_dictionary = CountryDictionary()
        self.country_dictionary.create_country_name_dict()
        self.country_dictionary.create_djii_rc_dict()
        self.country_dictionary.create_iso_alpha_2_dict()

        self.fcp_test = CountryCodeMapping()
        self.factiva_country_map = CountryCodeMapping()

    
    def test_read_write_file(self):
        """For this function we are actually reading from a static file,
        to actually check if write functions are working correctly, 
        please check the '/factiva_country_code_mapping/process/' 
        directory for a file by the name of 'test_iso_alpha_2.csv'.
        """

        start = time.time_ns()

        self.factiva_country_map.read_file(\
            'tests/process/input/test_iso_alpha_2.csv')

        self.factiva_country_map.write_csv_file('out_iso_alpha_2',\
            self.factiva_country_map.iso_alpha_2_list)

        print(f'test_read_write_file runtime = \
            {time.time_ns() - start} nanoseconds')

        self.fcp_test.read_file(\
            'tests/process/output/out_iso_alpha_2.csv')

        self.assertEqual(self.factiva_country_map.iso_alpha_2_list,\
            self.fcp_test.iso_alpha_2_list,\
            'error reading and/or writing to a file')


    def test_list_search(self):

        self.factiva_country_map.read_file(\
            'tests/process/input/test_iso_alpha_2.csv')

        start = time.time_ns()

        for iso_alpha_2 in self.factiva_country_map.iso_alpha_2_list:
            self.factiva_country_map.country_name_list.append(\
                self.country_list.get_country_name(\
                iso_alpha_2))

        print(f'test_list_search runtime = \
            {time.time_ns() - start} nanoseconds')

        self.fcp_test.read_file(\
            'tests/process/input/test_country_name.csv')

        self.assertEqual(self.factiva_country_map.country_name_list,\
            self.fcp_test.country_name_list,\
            'error mapping country name')


    def test_dictionary_search(self):

        self.factiva_country_map.read_file(\
            'tests/process/input/test_country_name.csv')

        start = time.time_ns()

        for country_name in self.factiva_country_map.country_name_list:
            self.factiva_country_map.djii_rc_list.append(\
                self.country_dictionary.get_djii_rc(\
                country_name))

        print(f'test_dictionary_search runtime = \
            {time.time_ns() - start} nanoseconds')

        self.fcp_test.read_file(\
            'tests/process/input/test_djii_rc.csv')

        self.assertEqual(self.factiva_country_map.djii_rc_list,\
            self.fcp_test.djii_rc_list,\
            'error mapping DJII region code')


if __name__ == '__main__':

    unittest.main()