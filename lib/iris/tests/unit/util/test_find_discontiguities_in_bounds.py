# (C) British Crown Copyright 2018, Met Office
#
# This file is part of Iris.
#
# Iris is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Iris is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Iris.  If not, see <http://www.gnu.org/licenses/>.
"""Unit tests for handling and plotting of 2-dimensional coordinates"""

from __future__ import (absolute_import, division, print_function)
from six.moves import (filter, input, map, range, zip)  # noqa

# Import iris.tests first so that some things can be initialised before
# importing anything else.
import iris.tests as tests

import numpy as np

from iris.util import find_discontiguities_in_bounds
from iris.tests.stock import simple_3d
from iris.tests.stock import sample_2d_latlons
from iris.tests.stock import make_bounds_discontiguous_at_point


def full2d_global():
    return sample_2d_latlons(transformed=True)


@tests.skip_data
class Test(tests.IrisTest):
    def setUp(self):
        # Set up a 2d lat-lon cube with 2d coordinates that have been
        # transformed so they are not in a regular lat-lon grid.
        # Then generate a discontiguity at a single lat-lon point.
        self.latlon_2d_cube = full2d_global()
        make_bounds_discontiguous_at_point(self.latlon_2d_cube, 3, 3)
        self.longitude_coord = self.latlon_2d_cube.coord('longitude')

    def test_find_discontiguities(self):
        # Check that the mask we generate when making the discontiguity
        # matches that generated by find_discontiguities_in_bounds
        cube = self.latlon_2d_cube
        coord = self.longitude_coord
        expected = cube.data.mask

        returned = find_discontiguities_in_bounds(coord)
        self.assertTrue(np.all(expected == returned))

    def test_find_discontiguities_1d_coord(self):
        # Check that an error is raised when we try and use
        # find_discontiguities_in_bounds on 1D coordinates:
        cube = simple_3d()
        coord = cube.coord('longitude')

        expected_err = 'Discontiguity searches are currently only ' \
                       'supported for 2-dimensional coordinates'
        with self.assertRaises(NotImplementedError):
            real_err = find_discontiguities_in_bounds(coord)
            self.assertEqual(expected_err, real_err)

    def test_find_discontiguities_with_tol(self):
        coord = self.longitude_coord
        # Choose a very large tolerance which will result in fine
        # discontiguities being disregarded
        atol = 100

        # Construct an array the size of the points array filled with 'False'
        # to represent a mask showing no discontiguities
        empty_mask = np.zeros(self.longitude_coord.points.shape,
                              dtype=bool)
        expected = empty_mask
        returned = find_discontiguities_in_bounds(coord, abs_tol=atol)
        self.assertTrue(np.all(expected == returned))


if __name__ == '__main__':
    tests.main()