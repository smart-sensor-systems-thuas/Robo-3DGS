'''
This script runs the custom COLMAP procedure `convert.py` 
opposed to the original `gaussian-splatting/convert.py`. 
If the argument:

`python main.py -s <experiment_path> --ignore-known-poses`

is used, the original code is called and manual poses are: NOT USED.

After pre-processing with COLMAP the original 3DGS is called:
`gaussian-splatting/train.py`.

To skip the prerprocessing entirely use:

`python main.py -s <experiment_path> --sikp-preprocessing`

This script simplifies the procedure by only letting the user use the arguments:
-s (--source_path)   : for defining the experiment folder
--ignore-known-poses : for running the original code and ignoring known camera positions and orientations
--skip-preprocessing : to only perform the 3DGS splatting procedure with an already present sparse point cloud

Assuming following structure is present:

experiment/
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

experiment/
  images/
      04d.jpg
  sparse/
      0/
          cameras.bin
          images.bin
          points3D.bin
'''

import os
import subprocess
import argparse
from glob import glob
from PIL import Image
from tqdm import tqdm

def parse_args() -> argparse.Namespace :
    parser = argparse.ArgumentParser('COLMAP converter with known camera poses')
    parser.add_argument(
        '--source_path', '-s', 
        required=True, type=str,
        help='defining the experiment folder'
    )
    parser.add_argument(
        '--use_original', action='store_true',
        help='running the original code and ignoring known camera positions and orientations'
    )
    parser.add_argument(
        '--skip-preprocessing', action='store_true',
        help='only perform the 3DGS splatting procedure with an already present sparse point cloud'
    )
    return parser.parse_args()

def main() -> None :
    args = parse_args()
    # `gaussian-splatting/train.py` needs an absolute path to find the experiment
    path = os.path.abspath(args.source_path)

    if not(args.skip_preprocessing) :
        if (
            os.path.exists(os.path.join(path, 'sparse')) or
            os.path.exists(os.path.join(path, 'images')) or
            os.path.exists(os.path.join(path, 'distorted')) or
            os.path.exists(os.path.join(path, 'database.db'))
        ) : 
            print('[Robo-3DGS] clean the experiment folder to only contain: ./experiment/config/ and ./experiment/input/')
            print('[Robo-3DGS] issues might occur with overwriting the COLMAP SfM procedure')
            print('[Robo-3DGS] or only run the 3DGS: python main.py --skip-preprocessing')
            exit()

        if (args.use_original) :
            # TODO just copy the input folder to images
            images_path = os.path.join(path, 'images')
            if not(os.path.exists(images_path)) : os.mkdir(images_path)
            print('[Robo-3DGS] preparing images (rotating by 180deg) (./input/*.jpg -> ./images/*.jpg)')
            for fn in tqdm(glob(os.path.join(path, 'input/*.jpg'))) : 
                img = Image.open(fn).transpose(Image.Transpose.ROTATE_180)
                img.save(fn.replace('input', 'images'))

            print('[Robo-3DGS] ignoring manual camera poses! using the original COLMAP procedure to estimate camera poses and generate sparse point cloud')
            subprocess.run([
                'python', './gaussian_splatting/convert.py',
                '-s', path
            ])
        else :
            print('[Robo-3DGS] using manual camera poses to generate sparse point cloud via COLMAP')
            subprocess.run([
                'python', './convert.py',
                '-s', path
            ])
    print('[Robo-3DGS] starting the 3DGS procedure...')
    try:
        subprocess.run([
            'python', './gaussian-splatting/train.py',
            '-s', path,
            '-m', path,
        ], check=True)
    except subprocess.CalledProcessError : 
        print('[Robo-3DGS] 3DGS splatting procedure terminated, attempting to recover results')

    
if (__name__ == '__main__') : main()