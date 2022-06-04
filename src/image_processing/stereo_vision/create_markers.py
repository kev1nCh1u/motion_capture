import cv2
import numpy as np

fs = cv2.FileStorage("data/parameter/test.yaml", cv2.FILE_STORAGE_WRITE)


orginDistance = np.array([
                    [0., 79.41495679, 92.6760091, 60.54557344, ],
                    [79.41495679, 0., 55.3985338, 82.12350075, ],
                    [92.6760091, 55.3985338, 0., 54.1674151,],
                    [60.54557344, 82.12350075, 54.1674151, 0.],
                    ])

fs.write('realNode', 900)
fs.write('strNode', 'test text')
fs.write('orginDistance', orginDistance)

fs.release()