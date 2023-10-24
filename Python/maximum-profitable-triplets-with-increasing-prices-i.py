# Time:  O(nlogn)
# Space: O(n)

from sortedcontainers import SortedList


# prefix sum, sorted list, binary search, mono stack
class Solution(object):
    def maxProfit(self, prices, profits):
        """
        :type prices: List[int]
        :type profits: List[int]
        :rtype: int
        """
        left = [float("-inf")]*len(prices)
        sl = SortedList()
        for i in xrange(len(prices)):
            j = sl.bisect_left((prices[i], -1))
            if j-1 >= 0:
                left[i] = sl[j-1][1]
            if j < len(sl) and sl[j][0] == prices[i]:
                if not (sl[j][1] < profits[i]):
                    continue
                del sl[j]
            elif not (j-1 < 0 or sl[j-1][1] < profits[i]):
                continue
            sl.add((prices[i], profits[i]))
            while j+1 < len(sl) and sl[j+1][1] <= sl[j][1]:
                del sl[j+1]
        result = float("-inf")
        sl = SortedList()
        for i in reversed(xrange(len(prices))):
            j = sl.bisect_left((-prices[i], -1))
            if j-1 >= 0:
                result = max(result, left[i]+profits[i]+sl[j-1][1])
            if j < len(sl) and -sl[j][0] == prices[i]:
                if not (sl[j][1] < profits[i]):
                    continue
                del sl[j]
            elif not (j-1 < 0 or sl[j-1][1] < profits[i]):
                continue
            sl.add((-prices[i], profits[i]))
            while j+1 < len(sl) and sl[j+1][1] <= sl[j][1]:
                del sl[j+1]
        return result if result != float("-inf") else -1


# Time:  O(nlogn)
# Space: O(n)
from sortedcontainers import SortedList


# prefix sum, sorted list, binary search, mono stack
class Solution2(object):
    def maxProfit(self, prices, profits):
        """
        :type prices: List[int]
        :type profits: List[int]
        :rtype: int
        """
        left = [float("-inf")]*len(prices)
        sl = SortedList()
        for i in xrange(len(prices)):
            j = sl.bisect_left((prices[i], -1))
            if j-1 >= 0:
                left[i] = sl[j-1][1]
            if j < len(sl) and sl[j][0] == prices[i]:
                if not (sl[j][1] < profits[i]):
                    continue
                del sl[j]
            elif not (j-1 < 0 or sl[j-1][1] < profits[i]):
                continue
            sl.add((prices[i], profits[i]))
            while j+1 < len(sl) and sl[j+1][1] <= sl[j][1]:
                del sl[j+1]
        right = [float("-inf")]*len(prices)
        sl = SortedList()
        for i in reversed(xrange(len(prices))):
            j = sl.bisect_left((-prices[i], -1))
            if j-1 >= 0:
                right[i] = sl[j-1][1]
            if j < len(sl) and -sl[j][0] == prices[i]:
                if not (sl[j][1] < profits[i]):
                    continue
                del sl[j]
            elif not (j-1 < 0 or sl[j-1][1] < profits[i]):
                continue
            sl.add((-prices[i], profits[i]))
            while j+1 < len(sl) and sl[j+1][1] <= sl[j][1]:
                del sl[j+1]
        result = max(left[i]+profits[i]+right[i] for i in xrange(len(profits)))
        return result if result != float("-inf") else -1
