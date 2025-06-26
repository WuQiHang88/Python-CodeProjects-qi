# 题目4：给定一个整数数组 nums，找到一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。
# 示例：
# 输入：nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
# 输出：6
# 解释：连续子数组 [4, -1, 2, 1] 的和为 6，是最大和

def maxSubArray(nums):
    max_current = max_global = nums[0]   #首先，创立两个变量，一个是当前最大值，max_current，一个是总的最大值，max_global,进行赋值，取nums这个数组的第一个数字赋值上
    for i in range(1,len(nums)):  #然后，从数组里，第二个数字开始遍历整个数组
        max_current = max(nums[i], max_current + nums[i])  #重新赋值给max_current,通过比较当前遍历到的数字，与当前最大的数字+当前遍历到的数字做对比，取二者大的那个
        if max_current > max_global:    #如果当前最大值，大于总的最大值，说明总的最大值需要更新了，此时，把总的最大值替换为当前最大值
            max_global = max_current
    return max_global        #最后，返回总的最大值

print(maxSubArray( [-2,1,-3,4,-1,2,1,-5,9]))



##运行逻辑如下：（以当前数组[-2,1,-3,4,-1,2,1,-5,9]为例）
## 1） max_current = max_global = -2 (数组中的第一个数字)
## 2） max_current = max(1 , -2+1) = 1, max_current(1) > max_global(-2), max_global = max_current = 1
## 3） max_current = max(-3 , 1+(-3) ) = -2 ,max_global = 1
## 4） max_current = max(4, -2+4) = 4, max_current(4) > max_global(1) , max_global = max_current = 4
##........
##最后，max_global = 6,返回最后的结果，如此，便能得到连续的最大的子数组