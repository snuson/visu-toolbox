from PyQt5.QtWidgets import QApplication
from err import *
import graphics
import sys
import csv


# Scatter plot and line chart
def scatterplot(x=None, y=None, src=None, grid=True, points=True,
                lines=True, axis=True, xlab='', ylab='', title='My Plot',
                legends=None, ngridx=4, ngridy=2):
    app = QApplication(sys.argv)

    # check if input is given directly
    if x is not None and y is not None:
        if len(x) != len(y):
            raise PlotError('X, Y not the same length')
        ex = graphics.Scatter([x], [y], grid, lines, points, axis,
                              xlab, ylab, title, legends, ngridx, ngridy)

    # otherwise take from source file
    elif src is not None:
        with open(src, newline='') as csvfile:
            reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
            data = list(reader)
            # Divide data according to specs
            xs = data[::2]
            ys = data[1::2]
            if legends is not None and len(legends) != len(xs):
                raise PlotError('Number of legends != number of datasets')
            if len(xs) != len(ys):
                raise PlotError('Uneven number of datasets')
            ex = graphics.Scatter(xs, ys, grid, lines, points, axis,
                                  xlab, ylab, title, legends, ngridx, ngridy)
    else:
        raise PlotError('No data given')

    sys.exit(app.exec_())


# standard histogram
def barplot(x=None, y=None, src=None, grid=True,
            axis=True, xlab='', ylab='', title='My Plot', ngridy=2):
    app = QApplication(sys.argv)
    # check if input is given directly
    if x is not None and y is not None:
        if len(x) != len(y):
            raise PlotError('X, Y not the same length')
        ex = graphics.Bar(x, y, grid,
                          axis, xlab, ylab, title, ngridy)

    # otherwise take from source file
    elif src is not None:
        with open(src, newline='') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            if len(data[0]) != len(data[1]):
                raise PlotError('X, Y not the same length')
            ex = graphics.Bar(data[0], data[1], grid,
                              axis, xlab, ylab, title, ngridy)
    else:
        raise PlotError('No data given')
    sys.exit(app.exec_())


# standard pie chart
def pieplot(x=None, y=None, src=None, title='My Plot'):
    app = QApplication(sys.argv)
    # check if input is given directly
    if x is not None and y is not None:
        if len(x) != len(y):
            raise PlotError('X, Y not the same length')
        ex = graphics.Pie(x, y, title)

    # otherwise take from source file
    elif src is not None:
        with open(src, newline='') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            if len(data[0]) != len(data[1]):
                raise PlotError('X, Y not the same length')
            ex = graphics.Pie(data[0], data[1], title)
    else:
        raise PlotError('No data given')
    sys.exit(app.exec_())
