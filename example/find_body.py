import os
import sys
sys.path.append(os.getcwd())
from lib.kevin.kevincv import *

# from matplotlib import pyplot as plt

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
                        [84.0008849766173, 1.0253193717497644, 484.2133958228639],
                        [11.402377138005159, 22.452479238189188, 458.8405626214418],
                        [93.7861030447076, 55.47613355449325, 487.92861245647583],
                        # [0, 0, 0],
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

    fb = FindBody()
    fb.orginDis = orginDis
    fb.orginDisSumTable4 = orginDisSumTable4
    fb.orginDisSumTable3 = orginDisSumTable3

    start_time_1 = time.time()
    for i in range(1):

        pc = pointCount(points3d)
        # print("pointCount:\n", pc, "\n")

        pointDis = findAllDis(points3d)
        print("points distanse:\n", pointDis, "\n")
        pointDisSum = arraySum(pointDis)[0]
        print("points distanse sum:\n",pointDisSum, "\n")

        # find body in any case
        nums, pra = fb.findBodySwith(pointDisSum, pc)

        # numsSort
        numsSort = np.append(nums, np.arange(4).reshape((4, 1)), axis=1)
        numsSort = np.sort(numsSort.view('i8,i8,i8'), order=['f1'], axis=0).view(np.int64)
        print("numsSort:\n", numsSort, "\n")

        # worstPoint
        worstPoint = 0
        if(pc == 4):
            worstPoint = findWorstPoint(pra)

        # generate lost point
        if(pc == 3):
            worstPoint = numsSort[1][0]
            gp = GenPoint()
            gp.a = points3d[numsSort[1][2]]
            gp.b = points3d[numsSort[2][2]]
            gp.c = points3d[numsSort[3][2]]
            gp.dis = np.delete(orginDis[nums[0][0]], nums[0][0], None)
            lp = gp.solve_fsolve()
            print("generate lost point:\n", lp, "\n")
            points3d[numsSort[0][2]] = lp
            # points3d[numsSort[0][2]] = [93.7861030447076, 55.47613355449325, 487.92861245647583]
            print("new 3d points:\n", points3d, "\n")

            # Reliability point
            prp = percentReliabilityPoint(orginDisSumTable4[0][numsSort[1][0]], points3d, numsSort[0][2])
            print("Reliability: ", prp, "\n")

            # new numsSort
            numsSort[0][1] = numsSort[1][0] + 1
            numsSort = np.sort(numsSort.view('i8,i8,i8'), order=['f1'], axis=0).view(np.int64)
            print("new numsSort:\n", numsSort, "\n")

        # create gen axis point
        print("worstPoint", worstPoint)
        numList = [i for i in range(4) if i != worstPoint]
        gp = GenPoint()
        gp.a = points3d[numsSort[numList[0]][2]]
        gp.b = points3d[numsSort[numList[1]][2]]
        gp.c = points3d[numsSort[numList[2]][2]]
        
        # gen virtual point
        gp2d = GenPoint2d()
        gp2d.genBodyPoint()
        virtualPoint3d = np.array([gp2d.a,gp2d.b,gp2d.c,gp2d.d])
        print("virtual 3d point:\n", virtualPoint3d, "\n")

        # axisDis
        axisDis = findAxisDis(virtualPoint3d)
        print("axis dis:\n", axisDis, "\n")
        
        # find axis point
        axisPoint = np.zeros((3,3))
        axisDisSort = np.delete(axisDis, worstPoint, axis=1)
        print("axisDisSort:\n",axisDisSort, "\n")
        for i in range(3):
            gp.dis = axisDisSort[i]
            axisPoint[i] = gp.solve_fsolve()
        print("axisPoint:\n", axisPoint, "\n")

        # showPlot3d
        showPlot3d(points3d, axisPoint, numsSort[:,2], pc, numsSort[0][2])

    # time
    print("--- 1: %s seconds ---" % (time.time() - start_time_1))

###################################################################################
# if main
###################################################################################
if __name__ == '__main__':
    import time
    start_time = time.time()
    main()
    print("--- total %s seconds ---" % (time.time() - start_time))