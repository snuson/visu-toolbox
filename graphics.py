from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt


class Scatter(QWidget):
    def __init__(self, x, y, grid, lines, points, axis,
                 xlab, ylab, title, legends, ngridx, ngridy):
        super().__init__()

        self.legends = legends
        self.title = title
        self.xlab = xlab
        self.ylab = ylab
        self.grid = grid
        self.lines = lines
        self.points = points
        self.axis = axis

        # the data
        self.x = x
        self.y = y

        self.dataLength_x = len(x)
        self.dataLength_y = len(y)

        # flatten data list to find global max, min
        self.scl_x = max([item for sub in x for item in sub])
        self.scl_y = max([item for sub in y for item in sub])
        self.min_x = min([item for sub in x for item in sub])
        self.min_y = min([item for sub in y for item in sub])

        self.gap_x = self.scl_x - self.min_x
        self.gap_y = self.scl_y - self.min_y

        self.mrg_b = 40
        self.mrg_s = 13
        self.ngridx = ngridx
        self.ngridy = ngridy

        # scaling tmp calculations
        self.xgs = (self.scl_x - self.min_x) / (self.ngridx + 1)
        self.ygs = (self.scl_y - self.min_y) / (self.ngridy + 1)

        # Colors to use for multiple lines
        self.colors = [Qt.red, Qt.darkGreen, Qt.blue, Qt.darkMagenta]

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle(self.title)
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)

        # Check keyword arguments for customization
        if self.axis:
            self.drawAxis(qp)
        if self.grid:
            self.drawGrid(qp)
        if self.points:
            self.drawPoints(qp)
        if self.lines:
            self.drawLines(qp)
        if self.legends is not None:
            self.drawLegends(qp)

        qp.end()

    def drawAxis(self, qp):
        pen = QPen(Qt.darkGray)
        pen.setWidth(2)
        qp.setPen(pen)

        w = self.size().width()
        h = self.size().height()

        if h <= 1 or w <= 1:
            return

        # Y axis    start x     start y     end x       end y
        qp.drawLine(self.mrg_b, self.mrg_s, self.mrg_b, h - self.mrg_b)

        # X axis
        qp.drawLine(self.mrg_b, h - self.mrg_b, w - self.mrg_s, h - self.mrg_b)

        # Draw labels
        qp.drawText(w/2, h - 1, self.xlab)
        qp.rotate(-90)
        qp.drawText(-h/2, 10, self.ylab)
        qp.rotate(90)

    def drawGrid(self, qp):
        pen = QPen(Qt.lightGray, 1, Qt.DashLine)
        qp.setPen(pen)
        w = self.size().width()
        h = self.size().height()

        # Draw vertical grid lines
        offset_x = (w - self.mrg_s - self.mrg_b) / (self.ngridx + 1)
        osx = offset_x
        for i in range(self.ngridx):
            qp.drawLine(self.mrg_b + osx, self.mrg_s, self.mrg_b + osx, h - self.mrg_b)
            gridlabel = self.min_x + (i + 1) * self.xgs
            qp.drawText(self.mrg_b + osx - 6, h - self.mrg_b + self.mrg_s, '{:.1f}'.format(gridlabel))
            osx += offset_x

        # Draw horizontal grid lines
        offset_y = (h - self.mrg_b - self.mrg_s) / (self.ngridy + 1)
        osy = offset_y
        for i in range(self.ngridy):
            qp.drawLine(self.mrg_b, h - self.mrg_b - osy, w - self.mrg_s, h - self.mrg_b - osy)
            gridlabel = self.min_y + (i + 1) * self.ygs
            qp.drawText(self.mrg_b - 2 * self.mrg_s, h - self.mrg_b - osy + 4, '{:.1f}'.format(gridlabel))
            osy += offset_y

    def drawPoints(self, qp):
        pen = QPen()
        pen.setWidth(4)
        w = self.size().width()
        h = self.size().height()

        if h <= 1 or w <= 1:
            return

        for x in range(len(self.x)):

            pen.setColor(self.colors[x])
            qp.setPen(pen)
            for i, j in zip(self.x[x], self.y[x]):
                x_draw = self.mrg_b + ((w-self.mrg_s-self.mrg_b)/self.gap_x)*(i - self.min_x)
                y_draw = h - self.mrg_b - ((h-self.mrg_s-self.mrg_b)/self.gap_y)*(j - self.min_y)

                qp.drawPoint(x_draw, y_draw)

    # connect adjacent points
    def drawLines(self, qp):
        pen = QPen()
        pen.setWidth(1)

        w = self.size().width()
        h = self.size().height()

        for x in range(len(self.x)):
            pen.setColor(self.colors[x])
            qp.setPen(pen)
            x_head, *x_tail = self.x[x]
            y_head, *y_tail = self.y[x]
            for i, j in zip(x_tail, y_tail):
                x_scale = ((w - self.mrg_s - self.mrg_b) / self.gap_x)
                y_scale = ((h - self.mrg_s - self.mrg_b) / self.gap_y)

                x_start = self.mrg_b + x_scale * (x_head - self.min_x)
                y_start = h - self.mrg_b - y_scale * (y_head - self.min_y)

                x_end = self.mrg_b + x_scale * (i - self.min_x)
                y_end = h - self.mrg_b - y_scale * (j - self.min_y)

                x_head = i
                y_head = j

                qp.drawLine(x_start, y_start, x_end, y_end)

    # label different colors used
    def drawLegends(self, qp):
        pen = QPen()
        pen.setWidth(10)

        w = self.size().width()
        h = self.size().height()

        for x in range(len(self.x)):
            pen.setColor(self.colors[x])
            qp.setPen(pen)

            qp.drawPoint(w - 2*self.mrg_b, h/4 + x*self.mrg_s)
            qp.drawText(w - 2*self.mrg_b + 11, h/4 + x*self.mrg_s + 2, self.legends[x])


class Bar(QWidget):
    def __init__(self, x, y, grid,
                 axis, xlab, ylab, title, ngridy):
        super().__init__()
        self.title = title
        self.xlab = xlab
        self.ylab = ylab
        self.grid = grid
        self.axis = axis
        self.x = x
        self.y = [float(i) for i in y]
        self.dataLen_x = len(x)
        self.dataLen_y = len(y)
        self.scl_y = max(self.y)
        self.min_y = min(self.y)
        self.mrg_b = 40
        self.mrg_s = 13
        self.ngridy = ngridy
        self.ygs = self.scl_y / (self.ngridy + 1)

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle(self.title)
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)

        # grid and axis are optional
        if self.grid:
            self.drawGrid(qp)
        self.drawBars(qp)
        if self.axis:
            self.drawAxis(qp)

        qp.end()

    def drawAxis(self, qp):
        pen = QPen(Qt.darkGray)
        pen.setWidth(2)
        qp.setPen(pen)

        w = self.size().width()
        h = self.size().height()

        # Axis
        qp.drawLine(self.mrg_b, self.mrg_s, self.mrg_b, h - self.mrg_b)
        qp.drawLine(self.mrg_b, h - self.mrg_b, w - self.mrg_s, h - self.mrg_b)

        # Draw labels
        qp.drawText(w/2, h - 1, self.xlab)
        # draw y label vertically
        qp.rotate(-90)
        qp.drawText(-h/2, 10, self.ylab)
        qp.rotate(90)

    # only horizontal gridlines for histogram
    def drawGrid(self, qp):
        pen = QPen(Qt.lightGray, 1, Qt.DashLine)
        qp.setPen(pen)
        w = self.size().width()
        h = self.size().height()

        # Draw horizontal grid lines
        offset_y = (h - self.mrg_b - self.mrg_s) / (self.ngridy + 1)
        osy = offset_y
        for i in range(self.ngridy):
            qp.drawLine(self.mrg_b, h - self.mrg_b - osy, w - self.mrg_s, h - self.mrg_b - osy)
            gridlabel = (i + 1) * self.ygs
            qp.drawText(self.mrg_b - 2 * self.mrg_s, h - self.mrg_b - osy + 4, '{:.1f}'.format(gridlabel))
            osy += offset_y

    # histogram core functionality
    def drawBars(self, qp):
        pen = QPen()
        pen.setWidth(1)
        pen.setBrush(Qt.darkGray)
        qp.setPen(pen)
        w = self.size().width()
        h = self.size().height()
        i = 1
        for cat, y in zip(self.x, self.y):
            plotw = w - self.mrg_b - self.mrg_s
            ploth = h - self.mrg_b - self.mrg_s
            barw = (plotw / self.dataLen_x) / 2
            xstr = self.mrg_b + (plotw/(self.dataLen_x + 1))*i - barw/2
            barh = ploth*(y/self.scl_y)
            ystr = self.mrg_s + ploth - barh
            qp.setBrush(Qt.Dense4Pattern)
            qp.drawRect(xstr, ystr, barw, barh)
            qp.drawText(self.mrg_b + (plotw/(self.dataLen_x + 1))*i - 4, h - 2*self.mrg_s, cat)
            i += 1


class Pie(QWidget):
    def __init__(self, x, y, title):
        super().__init__()

        self.title = title
        self.x = x
        self.y = [float(i) for i in y]
        self.dataLen_x = len(x)
        self.dataLen_y = len(y)
        self.colors = [Qt.darkCyan, Qt.darkGreen, Qt.darkMagenta,
                       Qt.blue, Qt.darkRed, Qt.darkGray]

        # pre calculations for pie sizes
        self.sum = sum(self.y)
        self.portions = [x/self.sum for x in self.y]

        self.initUI()

    def initUI(self):
        self.setGeometry(400, 400, 400, 400)
        self.setWindowTitle(self.title)
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)

        self.drawPie(qp)
        self.drawLegend(qp)

        qp.end()

    def drawPie(self, qp):
        pen = QPen(Qt.lightGray)
        pen.setWidth(1)
        qp.setPen(pen)

        # Margin for edges
        mrg = 40
        w = self.size().width() - 2*mrg
        h = self.size().height() - 2*mrg
        start = 0
        for i in range(len(self.portions)):
            qp.setBrush(self.colors[i])
            qp.drawPie(mrg, mrg, w, h, start, 360 * self.portions[i] * 16)
            start += 360 * self.portions[i] * 16

    def drawLegend(self, qp):
        pen = QPen()
        offset = 10
        for i in range(len(self.portions)):
            pen.setColor(self.colors[i])
            pen.setWidth(10)
            qp.setPen(pen)
            qp.drawPoint(self.width() - 60, offset)
            qp.drawText(self.width() - 52, offset + 3, self.x[i])
            offset += 15


