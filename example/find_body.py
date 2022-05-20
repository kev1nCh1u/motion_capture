import os
import sys
sys.path.append(os.getcwd())
from lib.kevin.kevincv import *

###################################################################################
# main
###################################################################################
def main():
    print("find body...\n")

    origin  = np.array([
                        [14.414906327500171, 22.34505201771049, 449.62576160776894],
                        [86.50438840372979, 0.6729383451448048, 474.92717314288876],
                        [96.13160683183148, 55.10663416683474, 478.5723029681971],
                        [47.43867422337718, 71.66474800800661, 461.57418427997044],
                        ])

    orginDis  = np.array([
                        [0.,    79.,    93.,    61.],
                        [79.,   0.,     57.,    82.],
                        [93.,   57.,    0.,     54.],
                        [61.,   82.,    54.,    0.],      
                        ])

    points3d  = np.array([
                        [44.408427247312176, 71.80456867683641, 471.56922565559825],
                        [0, 0, 0],
                        [11.402377138005159, 22.452479238189188, 458.8405626214418],
                        [84.0008849766173, 1.0253193717497644, 484.2133958228639],
                        # [93.7861030447076, 55.47613355449325, 487.92861245647583],
                        # [0, 0, 0],
                        # [0, 0, 0],
                        # [0, 0, 0],
                        ])

    orginDis = findAllDis(origin)
    print("origin distanse:\n", orginDis, "\n")
    orginDisSumTable4 = arraySum(orginDis)
    print("orginDisSumTable4:\n",orginDisSumTable4, "\n")
    orginDisSumTable3 = arraySumPart3(orginDis)
    print("orginDisSumTable3:\n",orginDisSumTable3, "\n")

    FB = FindBody()
    FB.orginDis = orginDis
    FB.orginDisSumTable4 = orginDisSumTable4
    FB.orginDisSumTable3 = orginDisSumTable3

    for i in range(60):
        start_time_1 = time.time()

        pc = pointCount(points3d)
        # print("pointCount:\n", pc, "\n")

        basePoint = 3 - 1

        pointDis = findAllDis(points3d)
        # print("points distanse:\n", pointDis, "\n")
        pointDisSum = arraySum(pointDis)[0]
        print("points distanse sum:\n",pointDisSum, "\n")
        
        # # findBody_num
        # nums = findBody_num(pointDis, pointDisSum, orginDis, orginDisSumTable4, basePoint)
        # print("points nums:", nums, "\n")

        # # findBody_np
        # nums = findBody_np(pointDis, orginDis, basePoint)
        # print("points nums:", nums, "\n")

        # # findBody_sum
        # nums = findBody_sum(pointDisSum, orginDisSumTable3)
        # print("points nums:\n", nums, "\n")

        # # Reliability
        # pra = percentReliabilityArray(orginDisSumTable3, pointDisSum, nums)
        # print("percentReliabilityArray", pra, "\n")

        # find body in any case
        nums = FB.findBodySwith(pointDisSum, pc)

        # generate lost point
        SP = SolvePoint()
        numsSort = np.append(nums, np.arange(4).reshape((4, 1)), axis=1)
        numsSort = np.sort(numsSort.view('i8,i8,i8'), order=['f1'], axis=0).view(np.int64)
        SP.a = points3d[numsSort[1][2]]
        SP.b = points3d[numsSort[2][2]]
        SP.c = points3d[numsSort[3][2]]
        SP.dis = np.delete(orginDis[nums[0][0]], nums[0][0], None)
        lp = SP.solve_fsolve()
        print("generate lost point:\n", lp, "\n")
        points3d[nums[0][0]-1] = lp
        print("new 3d points:\n", points3d, "\n")

        # Reliability
        observed = np.sum(findPointDis(points3d, nums[0][0]-1))
        pra = 100 - percentError(orginDisSumTable4[0][nums[0][0]-1], observed)
        print("Reliability: ", pra, "\n")

        # time
        print("--- 1: %s seconds ---" % (time.time() - start_time_1))

        break

###################################################################################
# if main
###################################################################################
if __name__ == '__main__':
    import time
    start_time = time.time()
    main()
    print("--- total %s seconds ---" % (time.time() - start_time))