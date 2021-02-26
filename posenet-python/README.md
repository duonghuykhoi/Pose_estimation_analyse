## PoseNet Python

This repository contains a pure Python implementation (multi-pose only) of the Google TensorFlow.js Posenet model. For a (slightly faster) PyTorch implementation that followed from this, see (https://github.com/rwightman/posenet-pytorch)

I first adapted the JS code more or less verbatim and found the performance was low so made some vectorized numpy/scipy version of a few key functions (named `_fast`).

Further optimization is possible
* The base MobileNet models have a throughput of 200-300 fps on a GTX 1080 Ti (or better)
* The multi-pose post processing code brings this rate down significantly. With a fast CPU and a GTX 1080+:
  * A literal translation of the JS post processing code dropped performance to approx 30fps
  * My 'fast' post processing results in 90-110fps
* A Cython or pure C++ port would be even better...  

### Install

A suitable Python 3.x environment with a recent version of Tensorflow is required.

Development and testing was done with Conda Python 3.6.8 and Tensorflow 1.12.0 on Linux.

Windows 10 with the latest (as of 2019-01-19) 64-bit Python 3.7 Anaconda installer was also tested.

If you want to use the webcam demo, a pip version of opencv (`pip install opencv-python`) is required instead of the conda version. Anaconda's default opencv does not include ffpmeg/VideoCapture support. Also, you may have to force install version 3.4.x as 4.x has a broken drawKeypoints binding.

A conda environment setup as below should suffice: 
```
conda install tensorflow-gpu scipy pyyaml python=3.6
pip install opencv-python==3.4.5.20

```

### Usage

There are three demo apps in the root that utilize the PoseNet model. They are very basic and could definitely be improved.

The first time these apps are run (or the library is used) model weights will be downloaded from the TensorFlow.js version and converted on the fly.

For all demos, the model can be specified with the '--model` argument by using its ordinal id (0-3) or integer depth multiplier (50, 75, 100, 101). The default is the 101 model.

#### get_images.py 

Get_images runs inference on an input video and outputs those images cutting into frame.

`!python get_images.py --video_dir ./video/A.mp4 --output_dir ./imagesA`

#### image_demo.py 

Image demo runs inference on an input folder of images and outputs those images with the keypoints and skeleton overlayed, coords-point csv and jsonfile.

`!python image_demo.py --model 101 --image_dir ./images --output_dir ./output --outputcsv_dir ./outputcsv --outputjson_dir ./outputjson --name Squat_Video`

#### Squat folder: __main__.py 

__main__ runs inference on an input jsonfile and outputs number of Squat

`!python ./Squat/__main__.py --input_json_path ./outputjson/Squat_VideoA.json`

### Credits

The original model, weights, code, etc. was created by Google and can be found at https://github.com/tensorflow/tfjs-models/tree/master/posenet

This original image_demo.py was created by Ross Wightman and can be found at https://github.com/rwightman/posenet-python . I modified it a little bit

