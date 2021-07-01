import unittest
from core import *


class MyTestCase(unittest.TestCase):
    def test_legend(self):
        try:
            scatterplot(src='testData/testdata.csv', title='Some Title',
                        xlab='X label(unit)', ylab='Y label(unit)',
                        legends=['viiva1', 'viiva2', 'viiva3', 'viiva4'])
        except PlotError as e:
            err = e

        self.assertNotEqual(None, err)

    def test_data_length_scatter(self):
        try:
            scatterplot([1, 2, 3], [1, 2])
        except PlotError as e:
            err = e
        self.assertNotEqual(None, err)

    def test_data_length_bar(self):
        try:
            barplot([1, 2, 3], [1, 2])
        except PlotError as e:
            err = e
        self.assertNotEqual(None, err)

    def test_data_length_bar(self):
        try:
            pieplot([1, 2, 3], [1, 2])
        except PlotError as e:
            err = e
        self.assertNotEqual(None, err)

if __name__ == '__main__':
    unittest.main()
