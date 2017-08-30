# class state:
#
#     def __init__(self, list):
#         self.dic = dict()
#         for i in list:
#             self.dic[i] = 1
#
#     def __eq__(self, other):
#         for i in self.dic:
#             if i not in other.dic:
#                 return False
#             if self.dic[i] != other.dic[i]:
#                 return False
#         return True
#
# s = state([1, 2, 3])
# t = state([3, 2, 1])
# p = state([2, 1])
# l = {t:1, p:2}
# print(s in l)

# l = [1]
# l.append((1,2,3))
# print(l)

# for i in range(3):
#     print(i)
#     for j in range(3):
#         print(-j)
#         if 1 == 1:
#             continue

c = {1:'1', 2:'2', 3:'3'}
d = {1:'1', 2:'2', 3:'3'}
print(c == d)