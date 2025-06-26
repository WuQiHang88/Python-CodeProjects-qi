# 题目5：将两个升序链表合并为一个新的升序链表并返回。新链表是通过拼接给定的两个链表的所有节点组成的。
# 示例：
# 输入：l1 = [1, 2, 4], l2 = [1, 3, 4]
# 输出：[1, 1, 2, 3, 4, 4]

class ListNode: #定义链表的节点类，是构建链表的基础
    def __init__(self, val=0, next=None):
        self.val = val   #self指向下面新创建的实例dummy，self.val被赋值为0（ListNode（0））
        self.next = next  #self.next默认为None（未指定下一个节点）
        #例如：node = ListNode(5)   创建值为 5 的孤立节点
              # node.val → 5
              # node.next → None

def mergeTwoLists(l1, l2):
    dummy = ListNode(0)  #首先，创立一个虚拟头节点，值为0，（实际不存储任何值，用于简化边界处理（边界条件即处理链表时，可能出现的特殊情况，例如空指针异常，逻辑错误等，加入虚拟头节点，就可以不用对这些条件进行判断））
                         #常见的边界条件：链表为空，链表只有一个节点，操作涉及头节点或尾节点（如删除头节点，尾部插入节点）。如果不处理边界条件，可能会导致访问空指针
                         #dummy（哑节点，虚拟的节点头）→ 1（真正的节点头） → 3 → 5
    current = dummy  #当前指针初始指向哑节点

    while l1 and l2:   #当l1和l2不为空时循环
        if l1.val <= l2.val:  #如果l1节点小于或等于l2节点
            current.next = l1  #将l1节点接入新链表
            l1 = l1.next  #然后l1指针往后移
        else:
            current.next = l2  #或者，将l2节点接入新链表
            l2 = l2.next  #然后l2指针往后移
        current = current.next   #执行完判操作后，就是新链表的当前指针往后移

    current.next = l1 if l1 else l2  #即当循环结束了，就表示至少有一个链表已经遍历完了（l1或l2为空）然后就把剩余的部分，连接到新链表的末尾
    return dummy.next   #返回哑节点的下一个节点，即新链表的头节点


def list_to_linkedlist(lst):  #构建将列表转换为链表的结构
    dummy = ListNode(0)  # 创建哑节点作为临时头节点（调用前面构建的方法）
    current = dummy   #当前指针转向哑节点
    for val in lst:  #遍历列表
        current.next = ListNode(val)  # 创建新节点并连接并连接到当前节点的下一个位置，并用lst的数字进行赋值
        current = current.next        # 移动指针到新添加的节点
    return dummy.next  # 返回真正的头节点（哑节点的下一个节点）
##核心逻辑：对于列表中的每个值val，创建一个新的ListNode节点，然后将新节点连接到current的next位置（即链表的末尾），最后，将current移到新节点
#（以 lst = [1, 3, 5] 为例）：
# 初始状态：dummy → 0，current 指向 dummy。
# 第一次循环（val=1）：
# current.next = ListNode(1) → dummy → 0 → 1。
# current = current.next → current 指向 1。
# 第二次循环（val=3）：
# current.next = ListNode(3) → dummy → 0 → 1 → 3。
# current 指向 3。
# 第三次循环（val=5）：
# current.next = ListNode(5) → dummy → 0 → 1 → 3 → 5。
# current 指向 5。


def linkedlist_to_list(head):  #核心功能：将链表表转换为列表，然后返回
    result = []   #存储结果的列表
    current = head  #当前指针指向链表的头节点
    while current:  #当current不为None时，继续循环，即链表未遍历完
        result.append(current.val)  #取出current节点的val值，再添加到result列表中
        current = current.next    ##将current指向下一个链表节点
    return result
# （以链表 1→3→5 为例）：
# 初始状态：current 指向头节点 1，result = []。
# 第一次循环：
# result.append(1) → result = [1]。
# current = current.next → current 指向 3。
# 第二次循环：
# result.append(3) → result = [1, 3]。
# current 指向 5。
# 第三次循环：
# result.append(5) → result = [1, 3, 5]。
# current = current.next → current 为 None，循环结束。


# 使用示例：
t1 = list_to_linkedlist([1, 3, 5])  # 创建链表 1 → 3 → 5
t2 = list_to_linkedlist([2, 4, 6])  # 创建链表 2 → 4 → 6

merged_head = mergeTwoLists(t1, t2)
print("合并后的链表为：", linkedlist_to_list(merged_head))

##整体运行逻辑如下：
##1. 首先，构造创建虚拟头节点，即哑节点的方法
##2. 用双指针分别遍历两个升序的链表，并重新排序
##3. 构造把列表变为链表的方法
##4. 重新把链表变为列表，再打印出来
