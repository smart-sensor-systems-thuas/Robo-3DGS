# Robo-3DGS
3D Gaussian Splatting utilizing known camera poses through robotic control and localization.

Instead of using Structure from Motion (SfM) to estimate camera poses, which introduces inaccuracies to 3D reconstruction, camera positions and orientations known a priori could be used to elliminate this source of uncertainty.
Besides estimation of camera poses, SfM is also used to generate a sparse point cloud.
This sparse point cloud serves as starting point for the 3DGS procedure; each point in the sparse point cloud gets attributed a 3D Gaussian.

Another benefit of using known camera positions is that the scale and orientation of the reconstruction agree with the ground-truth. 
Since in general SfM has no calibration object, only relative camera poses can be obtained. 
That is, the 3D reconstruction will have an arbitrary scale and orientation.
This requires the use of post-processing to correct for scale/orientation.
However, with known camera poses this post-processing becomes redundant. 

## File Structure 

```
experiments/exp-id/
  input/
      04d.jpg
  config/
      cameras.txt
      images.txt
      points3D.txt
```

- `input` raw jpg images. 
- `config` camera meta data:
    - `cameras.txt` camera intrinsics of the used cameras 
    - `images.txt` image with correpsonding camera pose and used camera
    - `points3D.txt` starting point cloud

Typically you would use only one camera, however setups with multiple different cameras are supported through `cameras.txt`.

```
#   CAMERA_ID, MODEL, WIDTH, HEIGHT, PARAMS[]
1 SIMPLE_PINHOLE 1080 1080 600 540 540
```

The `images.txt` contain for every image the pose and camera/file ids in the following structure:

```
#   IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME
10 0.707733 0.593858 -0.245984 0.293153 -0.636396 -0.874299 0.800376 1 0010.jpg
```

In here `Q_` denotes a Quarternion component, and `T_` denotes a translation.

The `points.txt` can be left empty. For more information on the camera-meta data check the
[COLMAP documentation](https://colmap.github.io/format.html). 

## Run

```

```