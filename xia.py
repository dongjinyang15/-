import numpy as npy

A = npy.arange(13, 1, -1).reshape(3, 4)

print(A)

print(npy.split(A, 4, axis=1))
# 按列分割,需等分
print(npy.array_split(A, 3, axis=1))
# 按列分割,不需等分
print(npy.vsplit(A, 3))
# 按行分割，学等分
print(npy.hsplit(A, 2))
# 按列分割，需等分

b = A[0]
# 关联复制
c = A[0].copy()
# deep copy 不会关联
A[0][0] = 15
print(b)
print(c)