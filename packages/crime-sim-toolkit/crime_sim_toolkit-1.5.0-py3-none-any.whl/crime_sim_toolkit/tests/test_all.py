import os
import json
import unittest
from unittest.mock import patch
import numpy as np
import pandas as pd
import folium
from crime_sim_toolkit import vis_utils
import crime_sim_toolkit.initialiser as Initialiser
import crime_sim_toolkit.poisson_sim as Poisson_sim
import pkg_resources

# specified for directory passing test
test_dir = os.path.dirname(os.path.abspath(__file__))

# Could be any dot-separated package/module name or a "Requirement"
resource_package = 'crime_sim_toolkit'

class Test(unittest.TestCase):

    def setUp(self):

        self.init = Initialiser.Initialiser(LA_names=['Kirklees','Calderdale','Leeds','Bradford','Wakefield'])

        self.init_data = self.init.initialise_data(directory=None)

    @classmethod
    def setUpClass(cls):
        super(Test, cls).setUpClass()

        cls.poisson = Poisson_sim.Poisson_sim(LA_names=['Kirklees','Calderdale','Leeds','Bradford','Wakefield'],
                                              directory=None,
                                              timeframe='Week')

        cls.poisson_day = Poisson_sim.Poisson_sim(LA_names=['Kirklees','Calderdale','Leeds','Bradford','Wakefield'],
                                                  directory=None,
                                                  timeframe='Day')

    def test_new_data_load(self):
        """
        Test new data load function

        """

        # pass it the directory to test data
        self.path_good = os.path.abspath(os.path.join(test_dir,'testing_data/test_policedata'))

        self.path_bad = os.path.abspath(os.path.join(test_dir,'testing_data/test_policedata/bad'))

        self.test = self.init.initialise_data(directory=self.path_good)

        self.assertTrue(isinstance(self.init.report_frame, pd.DataFrame))

        # test that on passing bad path system exits
        with self.assertRaises(SystemExit) as cm:

            self.init.initialise_data(directory=self.path_bad)

        self.assertEqual(cm.exception.code, 0)

    def test_match_LSOA_to_LA(self):
        """
        test for a given LSOA code this will return the local area code
        """

        self.to_match = pd.read_csv(pkg_resources.resource_filename(resource_package, 'tests/testing_data/match_LSOA_test.csv'))

        self.assertEqual(vis_utils.match_LSOA_to_LA(self.to_match['LSOA_cd'][0]),self.to_match['LA_cd'][0])

        self.assertEqual(vis_utils.match_LSOA_to_LA(self.to_match['LSOA_cd'][1]),self.to_match['LA_cd'][1])

        self.assertEqual(vis_utils.match_LSOA_to_LA(self.to_match['LSOA_cd'][2]),self.to_match['LA_cd'][2])

    def test_get_Geojson_link(self):
        """
        test that link retrieved is correct
        """

        self.target = 'https://raw.githubusercontent.com/martinjc/UK-GeoJSON/master/json/statistical/eng/lsoa_by_lad/E08000036.json'

        self.assertEqual(vis_utils.get_LA_GeoJson('E08000036'), self.target)

    def test_get_Geojson(self):
        """
        Test to confirm that get_GeoJson function works
        dictionary match between 2 files
        """

        self.data = vis_utils.get_GeoJson(['E09000020'])

        with open(pkg_resources.resource_filename(resource_package, 'tests/testing_data/test_1.json')) as datafile , open(pkg_resources.resource_filename(resource_package, 'tests/testing_data/test_2.json')) as falsefile:

            self.matchTrue = json.loads(datafile.read())

            self.matchFalse = json.loads(os.path.join(falsefile.read()))

            self.assertEqual(self.data, self.matchTrue)

            self.assertNotEqual(self.data, self.matchFalse)

    @patch('builtins.input', return_value='test')
    def test_map_Geojson(self, input):
        """
        Test to check we can take a dataframe and build a folium map
        """

        self.data = pd.read_csv(pkg_resources.resource_filename(resource_package, 'tests/testing_data/data_to_map.csv'), index_col=False)

        self.test = vis_utils.get_choropleth(data=self.data, inline=False)

        self.assertTrue(isinstance(self.test, folium.Map))


    def test_oob(self):
        """
        Test for checking out-of-bag sampling works as desired
        """


        self.data = pd.read_csv(pkg_resources.resource_filename(resource_package, 'tests/testing_data/test_oobsplit.csv'))

        self.output = self.poisson.out_of_bag_prep(self.data)

        self.assertTrue(isinstance(self.output, pd.DataFrame))

        self.assertEqual(self.output.datetime.dt.year.max(), 2018)

    def test_oob_split(self):
        """
        Test function for splitting data based on oob data
        """

        self.oobdata = pd.read_csv(pkg_resources.resource_filename(resource_package, 'tests/testing_data/test_oobdata.csv'))

        self.data = pd.read_csv(pkg_resources.resource_filename(resource_package, 'tests/testing_data/test_oobsplit.csv'))

        self.train_output = self.poisson.oob_train_split(full_data=self.data, test_data=self.oobdata)

        self.assertTrue(isinstance(self.train_output, pd.DataFrame))

        self.assertEqual(2017, self.train_output.datetime.max().year)

        self.assertEqual(2016, self.train_output.datetime.min().year)

        self.assertFalse(2018 in self.train_output.datetime.dt.year.unique().tolist())

    def test_sampler(self):
        """
        Test for checking the output of the poisson sampler is as expected
        """

        self.oobdata = pd.read_csv(pkg_resources.resource_filename(resource_package, 'tests/testing_data/test_oobdata.csv'))

        self.traindata = pd.read_csv(pkg_resources.resource_filename(resource_package, 'tests/testing_data/test_traindata.csv'))

        self.poi_data = self.poisson.SimplePoission(train_data = self.traindata, test_data = self.oobdata, method = 'simple')

        self.assertTrue(isinstance(self.poi_data, pd.DataFrame))

        self.assertEqual(self.poi_data.columns.tolist(), ['Week','datetime','Crime_type','Counts','LSOA_code'])

        self.assertEqual(self.poi_data.Week.unique().tolist(), [26,27,28,29,30,31])

        self.assertEqual(self.poi_data.datetime.apply(lambda x: x.split('-')[0]).unique().tolist(),
                         self.oobdata.datetime.apply(lambda x: x.split('-')[0]).unique().tolist())

    def test_sampler_day_func_simp(self):
        """
        Test for checking the output of the poisson sampler is as expected
        when sampling using days
        """

        self.oobdata = pd.read_csv(pkg_resources.resource_filename(resource_package, 'tests/testing_data/test_oobDay_data.csv'))

        self.traindata = pd.read_csv(pkg_resources.resource_filename(resource_package, 'tests/testing_data/test_trainDay_data.csv'))

        self.poi_data = self.poisson_day.SimplePoission(train_data = self.traindata, test_data = self.oobdata, method = 'simple')

        self.assertTrue(isinstance(self.poi_data, pd.DataFrame))

        self.assertEqual(self.poi_data.columns.tolist(), ['datetime','Crime_type','Counts','LSOA_code'])

        self.assertEqual(len(self.poi_data.datetime.dt.day.unique()), 31)

    def test_sampler_day_func_zero(self):
        """
        Test for checking the output of the poisson sampler is as expected
        when sampling using days
        """

        self.oobdata = pd.read_csv(pkg_resources.resource_filename(resource_package, 'tests/testing_data/test_oobDay_data.csv'))

        self.traindata = pd.read_csv(pkg_resources.resource_filename(resource_package, 'tests/testing_data/test_trainDay_data.csv'))

        self.poi_data = self.poisson_day.SimplePoission(train_data = self.traindata, test_data = self.oobdata, method = 'zero')

        self.assertTrue(isinstance(self.poi_data, pd.DataFrame))

        self.assertEqual(self.poi_data.columns.tolist(), ['datetime','Crime_type','Counts','LSOA_code'])

        self.assertEqual(len(self.poi_data.datetime.dt.day.unique()), 31)

    def test_sampler_day(self):
        """
        Test for checking the output of the poisson sampler is as expected
        when sampling using days
        """

        self.oobdata = pd.read_csv(pkg_resources.resource_filename(resource_package, 'tests/testing_data/test_oobDay_data.csv'))

        self.traindata = pd.read_csv(pkg_resources.resource_filename(resource_package, 'tests/testing_data/test_trainDay_data.csv'))

        self.poi_data = self.poisson_day.SimplePoission(train_data = self.traindata, test_data = self.oobdata, method = 'mixed')

        self.assertTrue(isinstance(self.poi_data, pd.DataFrame))

        self.assertEqual(self.poi_data.columns.tolist(), ['datetime','Crime_type','Counts','LSOA_code'])

        self.assertEqual(len(self.poi_data.datetime.dt.day.unique()), 31)

    @patch('matplotlib.pyplot.show')
    def test_sampler_error(self, mock_show):
        """
        Testing for the error reporting function for sampler
        """
        # TODO: the double call of SimplePoission here is very labourious and may not be necessary
        # this errors on calculating rmse Input contains NaN, infinity or a value too large for dtype('float64')

        self.oobdata = pd.read_csv(pkg_resources.resource_filename(resource_package, 'tests/testing_data/test_oobdata.csv'))

        self.traindata = pd.read_csv(pkg_resources.resource_filename(resource_package, 'tests/testing_data/test_traindata.csv'))

        self.poi_data = self.poisson.SimplePoission(train_data = self.traindata, test_data = self.oobdata, method = 'simple')

        self.plot = self.poisson.error_Reporting(test_data = self.oobdata, simulated_data = self.poi_data)

        self.assertTrue(isinstance(self.plot, pd.DataFrame))

        self.assertEqual(self.plot.columns.tolist(), ['Week','Pred_counts','Actual','Difference'])

    @patch('matplotlib.pyplot.show')
    def test_sampler_errorDay(self, mock_show):
        """
        Testing for the error reporting function for sampler
        """
        # TODO: the double call of SimplePoission here is very labourious and may not be necessary
        # this errors on calculating rmse Input contains NaN, infinity or a value too large for dtype('float64')

        self.oobdata = pd.read_csv(pkg_resources.resource_filename(resource_package, 'tests/testing_data/test_oobDay_data.csv'))

        self.traindata = pd.read_csv(pkg_resources.resource_filename(resource_package, 'tests/testing_data/test_trainDay_data.csv'))

        self.poi_data = self.poisson_day.SimplePoission(train_data = self.traindata, test_data = self.oobdata, method = 'simple')

        self.plot = self.poisson.error_Reporting(test_data = self.oobdata, simulated_data = self.poi_data)

        self.assertTrue(isinstance(self.plot, pd.DataFrame))

        self.assertEqual(self.plot.columns.tolist(), ['datetime','Pred_counts','Actual','Difference'])

    def test_sampler_week_agg(self):
        """
        Test for checking the output of the poisson sampler is as expected
        """

        self.oobdata = pd.read_csv(pkg_resources.resource_filename(resource_package, 'tests/testing_data/test_aggoobdata.csv'),
                                   parse_dates=['datetime'])

        self.traindata = pd.read_csv(pkg_resources.resource_filename(resource_package, 'tests/testing_data/test_aggtraindata.csv'))

        self.poi_data = self.poisson.SimplePoission(train_data = self.traindata, test_data = self.oobdata, method = 'simple')

        self.assertTrue(isinstance(self.poi_data, pd.DataFrame))

        self.assertEqual(self.poi_data.columns.tolist(), ['Week','datetime','Crime_type','Counts','LSOA_code'])

        self.assertEqual(self.poi_data.Week.unique().tolist(), [26,27,28,29,30,31])

        self.assertEqual(pd.to_datetime(self.poi_data.datetime).dt.year.unique().tolist(), self.oobdata.datetime.dt.year.unique().tolist())

        self.assertEqual(self.poi_data.shape[0], 14 * 6)

    def test_moving_window_week(self):

        self.week = 4

        self.test1 = Poisson_sim.Poisson_sim.moving_window_week(self.week, window=1)

        self.test2 = Poisson_sim.Poisson_sim.moving_window_week(self.week, window=0)

        self.test3 = Poisson_sim.Poisson_sim.moving_window_week(self.week, window=2)

        self.assertEqual(self.test1, [4, 3, 5])

        self.assertEqual(self.test2, [4])

        self.assertEqual(self.test3, [4, 3, 5, 2, 6])

    def test_moving_window_datetime(self):

        self.week = pd.to_datetime("2017-01-01")

        self.test1 = [x.strftime("%Y-%m-%d") for x in Poisson_sim.Poisson_sim.moving_window_datetime(self.week, window=1)]

        self.test2 = [x.strftime("%Y-%m-%d") for x in Poisson_sim.Poisson_sim.moving_window_datetime(self.week, window=0)]

        self.test3 = [x.strftime("%Y-%m-%d") for x in Poisson_sim.Poisson_sim.moving_window_datetime(self.week, window=2)]

        self.assertEqual(self.test1, ["2017-01-01",
                                      "2017-01-02",
                                      "2016-12-31"])

        self.assertEqual(self.test2, ["2017-01-01"])

        self.assertEqual(self.test3, ["2017-01-01",
                                      "2017-01-02",
                                      "2016-12-31",
                                      "2017-01-03",
                                      "2016-12-30"]
                                      )


if __name__ == "__main__":
    unittest.main(verbosity=2)
