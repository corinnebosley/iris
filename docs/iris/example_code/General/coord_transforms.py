"""
Coordinate Reference System Transforms
======================================

There are many complexities and assumptions involved in transforming coordinates
between coordinate reference systems, such as differently shaped ellipsoids.

This example shows two different outcomes of CRS transforms using different
methods.  Both are valid results, but depending on the purpose of the transform,
one must choose which is most appropriate.
"""

import cartopy.crs as ccrs
import iris
import iris.quickplot as qplt
import matplotlib.pyplot as plt


def main():

    # Load cube containing data in rotated pole CRS (RotatedGeogCS)
    fname = iris.sample_data_path('rotated_pole.nc')
    # TODO: Transform cube data into different CRS two different ways:
    # This should be one actual transform and one null transform, I think.
    # Might have to use cube projection here?:
    # http://scitools.org.uk/iris/docs/latest/whatsnew/1.0.html?highlight=transform
    cube1 = iris.load_cube(fname)
    cube2 = iris.load_cube(fname)

    # Define rotated pole globe projection for axes, with CRS of WGS84
    fig = plt.figure()
    projection = ccrs.RotatedPole(globe=ccrs.Globe(datum='WGS84',
                                                   ellipse='WGS84'))

    ax1 = fig.add_subplot(121, projection=projection)
    ax1.set_extent([351, 358, 53, 59])
    qplt.pcolor(cube1, edgecolors='black', axes=ax1)
    qplt.points(cube1)
    ax1.coastlines(resolution='10m')

    ax2 = fig.add_subplot(122, projection=projection)
    ax2.set_extent([351, 358, 53, 59])
    qplt.pcolor(cube2, edgecolors='black', axes=ax2)
    qplt.points(cube2)
    ax2.coastlines(resolution='10m')

    plt.show()


if __name__ == '__main__':
    main()
