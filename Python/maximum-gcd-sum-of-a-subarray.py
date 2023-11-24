# Time:  O(nlogr), r = max(nums)
# Space: O(logr)

# number theory, dp, prefix sum
class Solution(object):
    def maxGcdSum(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        def gcd(a, b):
            while b:
                a, b = b, a%b
            return a

        result = prev = 0
        prefix = {0:0}
        dp = []
        for right, x in enumerate(nums):
            dp.append((right, x))
            new_dp = []
            for left, g in dp:  # Time:  O(logr)
                ng = gcd(g, x)  # Total Time: O(nlogr)
                if not new_dp or new_dp[-1][1] != ng:
                    new_dp.append((left, ng))  # left and ng are both non-decreasing
            dp = new_dp
            prefix = {right:prefix[right] for right, _ in dp}
            prefix[right+1] = prev + x
            prev = prefix[right+1]
            for left, g in dp:
                if right-left+1 < k:
                    break
                result = max(result, (prefix[right+1]-prefix[left])*g)
        return result


# Time:  O(nlogr), r = max(nums)
# Space: O(n)
# number theory, dp, prefix sum
class Solution2(object):
    def maxGcdSum(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        def gcd(a, b):
            while b:
                a, b = b, a%b
            return a

        prefix = [0]*(len(nums)+1)
        for i, x in enumerate(nums):
            prefix[i+1] = prefix[i]+x
        result = 0
        dp = []
        for right, x in enumerate(nums):
            dp.append((right, x))
            new_dp = []
            for left, g in dp:  # Time:  O(logr)
                ng = gcd(g, x)  # Total Time: O(nlogr)
                if not new_dp or new_dp[-1][1] != ng:
                    new_dp.append((left, ng))  # left and ng are both non-decreasing
            dp = new_dp
            for left, g in dp:
                if right-left+1 < k:
                    break
                result = max(result, (prefix[right+1]-prefix[left])*g)
        return result


# Time:  O(nlogr * logn), r = max(nums)
# Space: O(nlogn)
# number theory, binary search, rmq, sparse table, prefix sum
class Solution3_TLE(object):
    def maxGcdSum(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        def gcd(a, b):
            while b:
                a, b = b, a%b
            return a

        def binary_search_right(left, right, check):
            while left <= right:
                mid = left + (right-left)//2
                if not check(mid):
                    right = mid-1
                else:
                    left = mid+1
            return right

        def log2_floor(x):  # assumed x >= 1
           return x.bit_length()-1

        # RMQ - Sparse Table
        # Template: https://github.com/kamyu104/GoogleCodeJam-Farewell-Rounds/blob/main/Round%20D/genetic_sequences2.py3
        class SparseTable(object):
            def __init__(self, arr):  # Time: O(nlogn), Space: O(nlogn)
                n = len(arr)
                k = log2_floor(n)
                self.st = [[0]*n for _ in xrange(k+1)]
                self.st[0] = arr[:]
                for i in xrange(1, k+1):
                    for j in xrange((n-(1<<i))+1):
                        self.st[i][j] = gcd(self.st[i-1][j], self.st[i-1][j+(1<<(i-1))])

            def query(self, L, R):
                i = log2_floor(R-L+1)
                return gcd(self.st[i][L], self.st[i][R-(1<<i)+1])  # Time: O(logr)
        
        prefix = [0]*(len(nums)+1)
        for i, x in enumerate(nums):
            prefix[i+1] = prefix[i]+x
        result = 0
        rmq = SparseTable(nums)
        for left, x in enumerate(nums):
            right = left
            while right != len(nums):  # O(logr) times
                g = rmq.query(left, right)
                right = binary_search_right(right, len(nums)-1, lambda x: rmq.query(left, x) >= g)  # Time: O(logn)
                if right-left+1 >= k:
                    result = max(result, (prefix[right+1]-prefix[left])*g)
                right += 1
        return result
        
