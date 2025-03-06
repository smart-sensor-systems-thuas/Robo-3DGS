# TODO : rotate image by 180deg from input/ -> images/

'''
Adapted from the original 3D Gaussian Splatting source code:
https://github.com/graphdeco-inria/gaussian-splatting/convert.py

Rewritten to accomodate manual camera poses.
Author: Jelle Westra (jhwestra@hhs.nl)

Assuming following structure is present:

source/
  images/
      04d.jpg
  manual/
      cameras.txt
      images.txt
      points3D.txt

Gaussian Splatting's `train.py` will expect sparse point cloud in the form
In the original `convert.py` images are also undistorted and mapper is used
However, if camera positions are extrinsics are known, triangulation can be
used to obtain a sparse point cloud.

source/
  images/
      04d.jpg
  sparse/
      0/
          cameras.bin
          images.bin
          points3D.bin
'''

import os
from argparse import ArgumentParser
import shutil

# Assuming following structure is present
# source/
#   images/
#       04d.jpg
#   manual/
#       cameras.txt
#       images.txt
#       points3D.txt

# Gaussian Splatting's `train.py` will expect sparse point cloud in the form
# In the original `convert.py` images are also undistorted and mapper is used
# However, if camera positions are extrinsics are known, triangulation can be
# used to obtain a sparse point cloud.
# source/
#   images/
#       04d.jpg
#   sparse/
#       0/
#           cameras.bin
#           images.bin
#           points3D.bin


def parse_args():
    parser = ArgumentParser('COLMAP converter with known camera positions')
    parser.add_argument('--source_path', '-s', required=True, type=str)
    parser.add_argument('--camera', default='OPENCV', type=str)
    parser.add_argument('--debug', action='store_true')
    return parser.parse_args()

def main():
    args = parse_args()

    if args.debug:
        shutil.rmtree(f'./{args.source_path}/sparse')
        os.remove(f'./{args.source_path}/database.db')
        # os.system('python cameras.py')

    os.makedirs(f'./{args.source_path}/sparse/0', exist_ok=True)

    # Feature extraction
    if os.system(
        'colmap feature_extractor'
        f' --database_path {args.source_path}/database.db' 
        f' --image_path {args.source_path}/images' 
        ' --ImageReader.camera_model SIMPLE_PINHOLE'
        ' --SiftExtraction.use_gpu 1'
    ) != 0 : exit(0)

    # Feature matching
    if os.system(
        'colmap exhaustive_matcher'
        f' --database_path {args.source_path}/database.db' 
        ' --SiftMatching.use_gpu 1'
    ) != 0 : exit(0)

    # Triangulation (instead of mapping in the regular convert since we know the camera parameters)
    if os.system(
        'colmap point_triangulator'
        f' --database_path {args.source_path}/database.db' 
        f' --image_path {args.source_path}/images' 
        f' --input_path {args.source_path}/config'
        f' --output_path {args.source_path}/sparse/0'
    ) != 0 : exit(0)

if (__name__ == '__main__') : main()