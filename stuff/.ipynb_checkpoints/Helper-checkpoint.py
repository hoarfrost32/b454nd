import cv2
import numpy as np
from PrePro import PrePro
from GetTail import GetTail

# Assuming that the following classes are available or need to be defined
# Edge, FlowchartShape, Point, Rectangle, Rhombus, Graph, ProgressBar

class Helper:
    @staticmethod
    def BuildArrows(r, center, tails):
        edges = []
        for i in range(r):
            e = Edge(Point(tails[i][0], tails[i][1]), Point(center[i][0], center[i][1]))
            edges.append(e)
        return edges

    @staticmethod
    def BuildRectangles(r, anchors, center):
        rect = []
        for i in range(r):
            width = anchors[i][0]
            height = anchors[i][1]
            shape = Rectangle(Point(center[i][0], center[i][1]), width, height)
            rect.append(shape)
        return rect

    @staticmethod
    def BuildDiamonds(r, anchors, center):
        diamonds = []
        for i in range(r):
            width = anchors[i][0]
            height = anchors[i][1]
            shape = Rhombus(Point(center[i][0], center[i][1]), width, height)
            diamonds.append(shape)
        return diamonds

    @staticmethod
    def getGraph(img, progressBar=None):
        Helper.setProgressBarRatio(progressBar, 0)

        height, width = img.shape[:2]

        Helper.setProgressBarRatio(progressBar, 0.2)
        pre = PrePro.prepro(img)
        Helper.setProgressBarRatio(progressBar, 0.5)

        # Extract processed images
        matRectangle = pre[0]
        matDiamond = pre[1]
        matArrow = pre[2]

        print("Height", height)
        print("Width", width)

        # Connected components analysis
        num_labels_rect, labels_rect, stats_rect, centroids_rect = cv2.connectedComponentsWithStats(matRectangle)
        Helper.setProgressBarRatio(progressBar, 0.6)

        num_labels_diamond, labels_diamond, stats_diamond, centroids_diamond = cv2.connectedComponentsWithStats(matDiamond)
        Helper.setProgressBarRatio(progressBar, 0.6)

        num_labels_arrow, labels_arrow, stats_arrow, centroids_arrow = cv2.connectedComponentsWithStats(matArrow)
        Helper.setProgressBarRatio(progressBar, 0.7)

        print("Regions (Rectangles):", num_labels_rect)
        print("Regions (Diamonds):", num_labels_diamond)
        print("Regions (Arrows):", num_labels_arrow)

        r_rect = num_labels_rect - 1
        r_diamond = num_labels_diamond - 1
        r_arrow = num_labels_arrow - 1

        # Find centers
        center_rect = centroids_rect[1:].astype(int)
        center_diamond = centroids_diamond[1:].astype(int)
        center_arrow = centroids_arrow[1:].astype(int)
        Helper.setProgressBarRatio(progressBar, 0.8)

        # Anchors for rectangles and diamonds
        anchors_rect = stats_rect[1:, [2, 3]]  # Width and height
        anchors_diamond = stats_diamond[1:, [2, 3]]
        Helper.setProgressBarRatio(progressBar, 0.9)

        # Tails and heads for arrows
        tails = []
        heads = []
        for i in range(r_arrow):
            x = stats_arrow[i+1, cv2.CC_STAT_LEFT]
            y = stats_arrow[i+1, cv2.CC_STAT_TOP]
            w = stats_arrow[i+1, cv2.CC_STAT_WIDTH]
            h = stats_arrow[i+1, cv2.CC_STAT_HEIGHT]
            center_x, center_y = center_arrow[i]

            box_X = x + 0.5 * w
            box_Y = y + 0.5 * h
            if center_x < box_X:
                if center_y < box_Y:
                    head = [x, y]
                    tail = [x + w, y + h]
                else:
                    head = [x, y + h]
                    tail = [x + w, y]
            else:
                if center_y < box_Y:
                    head = [x + w, y]
                    tail = [x, y + h]
                else:
                    head = [x + w, y + h]
                    tail = [x, y]
            heads.append(head)
            tails.append(tail)
        tails = np.array(tails)
        heads = np.array(heads)

        Helper.setProgressBarRatio(progressBar, 0.9)

        # Build shapes and edges
        rect_shapes = Helper.BuildRectangles(r_rect, anchors_rect, center_rect)
        diamond_shapes = Helper.BuildDiamonds(r_diamond, anchors_diamond, center_diamond)
        shapes = rect_shapes + diamond_shapes

        edges = Helper.BuildArrows(r_arrow, heads, tails)

        # Build graph
        graph = Graph(shapes, edges)
        Helper.setProgressBarRatio(progressBar, 1.0)
        return graph

    @staticmethod
    def setProgressBarRatio(progressBar, ratio):
        if progressBar is None:
            return
        progressBar.setRatio(ratio)
