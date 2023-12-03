import numpy as np
import cv2

p1 = [1400, 200]
p2 = [1400, 1400]
p3 = [2300, 200]
p4 = [2300, 1400]
p5 = np.array([1850, 1400, 1])

p1_prime = [659, 510]
p2_prime = [5, 590]
p3_prime = [1102, 541]
p4_prime = [796, 1376]

p = np.float32([p1, p2, p3, p4])
p_prime = np.float32([p1_prime, p2_prime, p3_prime, p4_prime])

matrix = cv2.getPerspectiveTransform(p, p_prime)

print(matrix)
result = np.matmul(matrix, [1850, 1400, 1])
result = result / result[2]
print(result)

# def recover_homogenous_affine_transformation(p, p_prime):
#     '''
#     Find the unique homogeneous affine transformation that
#     maps a set of 3 points to another set of 3 points in 3D
#     space:
#
#         p_prime == np.dot(p, R) + t
#
#     where `R` is an unknown rotation matrix, `t` is an unknown
#     translation vector, and `p` and `p_prime` are the original
#     and transformed set of points stored as row vectors:
#
#         p       = np.array((p1,       p2,       p3))
#         p_prime = np.array((p1_prime, p2_prime, p3_prime))
#
#     The result of this function is an augmented 4-by-4
#     matrix `A` that represents this affine transformation:
#
#         np.column_stack((p_prime, (1, 1, 1))) == \
#             np.dot(np.column_stack((p, (1, 1, 1))), A)
#
#     Source: https://math.stackexchange.com/a/222170 (robjohn)
#     '''
#
#     # construct intermediate matrix
#     Q       = p[1:]       - p[0]
#     Q_prime = p_prime[1:] - p_prime[0]
#
#     # calculate rotation matrix
#     R = np.dot(np.linalg.inv(np.row_stack((Q, np.cross(*Q)))),
#                np.row_stack((Q_prime, np.cross(*Q_prime))))
#
#     # calculate translation vector
#     t = p_prime[0] - np.dot(p[0], R)
#
#     # calculate affine transformation matrix
#     return np.column_stack((np.row_stack((R, t)),
#                             (0, 0, 0, 1)))
#
# def transform_pt(point, trans_mat):
#     a  = np.array([point[0], point[1], point[2], 1])
#     ap = np.dot(a, trans_mat)[:3]
#     return [ap[0], ap[1], ap[2]]
# # print(recover_homogenous_affine_transformation(p, p_prime))
# tr_matrix = recover_homogenous_affine_transformation(p, p_prime)
# print(transform_pt(p4, tr_matrix))