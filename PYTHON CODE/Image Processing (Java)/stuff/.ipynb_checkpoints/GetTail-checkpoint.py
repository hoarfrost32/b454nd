import numpy as np
import math

class GetTail:
    @staticmethod
    def findTail(table, center, lengths):
        tails = []
        r = len(lengths)
        for i in range(r):
            maxDistance = -1
            tail_point = [0, 0]
            centerx = center[i][0]
            centery = center[i][1]
            for j in range(lengths[i]):
                candidatex = table[i][0][j]
                candidatey = table[i][1][j]
                distance = math.hypot(centerx - candidatex, centery - candidatey)
                if distance > maxDistance:
                    maxDistance = distance
                    tail_point = [candidatex, candidatey]
            tails.append(tail_point)
        return np.array(tails)
