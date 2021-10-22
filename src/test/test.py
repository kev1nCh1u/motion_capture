import argparse
parser = argparse.ArgumentParser()
parser.add_argument("camera_num", help="chose camera 0,1,2,")
args = parser.parse_args()
print(args.camera_num)