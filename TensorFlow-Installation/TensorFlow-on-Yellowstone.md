# Trial 1: Failed!!!!

- ```mkdir -p /glade/p/work/abanihi/ys/installs/local/src/```
- move into this directory
- Copy content from cheyenne bazel source code into yellowstone directory

```cp -r /glade/p/work/abanihi/cy/installs/local/src/bazel-0.5.2-dist.zip .```

- ```unzip bazel-0.5.2-dist.zip```

- ```cd bazel```

- ```./compile.sh```


- ```git clone git@github.com:tensorflow/tensorflow.git```
- ```cd tensorflow```
- ```nano +165 configure```
- Change ```bazel version > bazel.version``` to ```../bazel/output/bazel version > bazel.version```
- ```mkdir -p /glade/p/work/abanihi/ys/local/tensorflow-gpu/1.2.1/lib/python2.7/site-packages```
- Add this directory to python path
- ```export PYTHONPATH=$/glade/p/work/abanihi/ys/installs/local/tensorflow-gpu/1.2.1/lib/python2.7/site-packages:$PYTHONPATH```
- Create a temp environment installation variable
- ```export TEMP_INSTALL=/glade/p/work/abanihi/ys/local/tensorflow-gpu/1.2.1```

```
abanihi@yslogin3: /glade/p/work/abanihi/ys/installs/local/src/tensorflow $ ./configure 
You have bazel 0.5.2- installed.
Please specify the location of python. [Default is /glade/apps/opt/python/2.7.7/gnu-westmere/4.8.2/bin/python]: 
Found possible Python library paths:
  /glade/apps/opt/numexpr/2.6.0/intel-autodispatch/16.0.2/lib/python2.7/site-packages
  /glade/apps/opt/numpy/1.11.0/intel-autodispatch/16.0.0/lib/python2.7/site-packages
  /glade/apps/opt/Pillow/3.2.0/gnu-westmere/4.8.2/lib/python2.7/site-packages
  /glade/apps/opt/biggus/0.13.0/lib/python2.7/site-packages
  /glade/apps/opt/scikit-learn/0.17.1/gnu/4.8.2/lib/python2.7/site-packages
  /glade/apps/opt/scipy/0.17.1/intel-autodispatch/16.0.0/lib/python2.7/site-packages
  /glade/apps/opt/tornado/4.4.3/gnu/4.8.2/lib/python2.7/site-packages
  /glade/apps/opt/pandas/0.18.1/gnu/4.8.2/lib/python2.7/site-packages
  /glade/apps/opt/jupyter/5.0.0/gnu/4.8.2/lib/python2.7/site-packages
  /glade/apps/opt/bottleneck/1.1.0/gnu/4.8.2/lib/python2.7/site-packages
  /glade/apps/opt/python/2.7.7/gnu-westmere/4.8.2/lib/python2.7/site-packages
  /glade/apps/opt/pyzmq/16.0.2/gnu/4.8.2/lib/python2.7/site-packages
  /glade/p/work/abanihi/ys/installs/local/tensorflow-gpu/1.2.1/lib/python2.7/site-packages/
Please input the desired Python library path to use.  Default is [/glade/apps/opt/numexpr/2.6.0/intel-autodispatch/16.0.2/lib/python2.7/site-packages]
/glade/p/work/abanihi/ys/local/tensorflow-gpu/1.2.1/lib/python2.7/site-packages
Do you wish to build TensorFlow with MKL support? [y/N] N
No MKL support will be enabled for TensorFlow
Please specify optimization flags to use during compilation when bazel option "--config=opt" is specified [Default is -mcpu=native]: --config=opt
Do you wish to use jemalloc as the malloc implementation? [Y/n] Y
jemalloc enabled
Do you wish to build TensorFlow with Google Cloud Platform support? [y/N] N
No Google Cloud Platform support will be enabled for TensorFlow
Do you wish to build TensorFlow with Hadoop File System support? [y/N] N
No Hadoop File System support will be enabled for TensorFlow
Do you wish to build TensorFlow with the XLA just-in-time compiler (experimental)? [y/N] N
No XLA JIT support will be enabled for TensorFlow
Do you wish to build TensorFlow with VERBS support? [y/N] N
No VERBS support will be enabled for TensorFlow
Do you wish to build TensorFlow with OpenCL support? [y/N] N
No OpenCL support will be enabled for TensorFlow
Do you wish to build TensorFlow with CUDA support? [y/N] y
CUDA support will be enabled for TensorFlow
Do you want to use clang as CUDA compiler? [y/N] N
nvcc will be used as CUDA compiler
Please specify the CUDA SDK version you want to use, e.g. 7.0. [Leave empty to default to CUDA 8.0]: 
Please specify the location where CUDA  toolkit is installed. Refer to README.md for more details. [Default is /usr/local/cuda]: /ncar/opt/cuda/8.0.61
Please specify which gcc should be used by nvcc as the host compiler. [Default is /glade/apps/opt/modulefiles/ys/cmpwrappers/gcc]: 
Please specify the cuDNN version you want to use. [Leave empty to default to cuDNN 6.0]:         
Please specify the location where cuDNN  library is installed. Refer to README.md for more details. [Default is /ncar/opt/cuda/8.0.61]: /glade/u/apps/contrib/cudnn/6.0 
Please specify a list of comma-separated Cuda compute capabilities you want to build with.
You can find the compute capability of your device at: https://developer.nvidia.com/cuda-gpus.
Please note that each additional compute capability significantly increases your build time and binary size.
[Default is: "3.5,5.2"]: 3.5
Do you wish to build TensorFlow with MPI support? [y/N] N
MPI support will not be enabled for TensorFlow
Configuration finished
```

```sh
abanihi@yslogin3: /glade/p/work/abanihi/ys/installs/local/src/tensorflow $ ../bazel/output/bazel build -c opt --config=cuda //tensorflow/tools/pip_package:build_pip_package
INFO: Loading package: @boringssl//
```


**Causes:**
- Compiled everything with gnu/6.0.1: Tensorflow doesn't support gnu version 5+.
- Abused the login nodes by compiling tensorflow and bazel on the login node.



# Trial 2


- Log into yellowstone
- module load gnu/5.0.1
- qsub caldera
- ```cd /glade/p/work/abanihi/ys/installs/local/src/bazel```
- ```/.compile```
-  Got ```Build successful! Binary is here: /glade/p/work/abanihi/ys/installs/local/src/bazel/output/bazel```
- ```cd /glade/p/work/abanihi/ys/installs/local/src/tensorflow```
- ```nano +165 configure```
- Change ```bazel version > bazel.version``` to ```../bazel/output/bazel version > bazel.version```
- ```./configure```

```sh
bash-4.1$ ./configure 
Extracting Bazel installation...
.
You have bazel 0.5.2- installed.
Please specify the location of python. [Default is /glade/apps/opt/python/2.7.7/gnu-westmere/4.8.2/bin/python]: 
Found possible Python library paths:
  /glade/p/work/abanihi/ys/installs/local/tensorflow-gpu/1.2.1/lib/python2.7/site-packages
  /glade/apps/opt/numexpr/2.6.0/intel-autodispatch/16.0.2/lib/python2.7/site-packages
  /glade/apps/opt/numpy/1.11.0/intel-autodispatch/16.0.0/lib/python2.7/site-packages
  /glade/apps/opt/Pillow/3.2.0/gnu-westmere/4.8.2/lib/python2.7/site-packages
  /glade/apps/opt/biggus/0.13.0/lib/python2.7/site-packages
  /glade/apps/opt/scikit-learn/0.17.1/gnu/4.8.2/lib/python2.7/site-packages
  /glade/apps/opt/scipy/0.17.1/intel-autodispatch/16.0.0/lib/python2.7/site-packages
  /glade/apps/opt/tornado/4.4.3/gnu/4.8.2/lib/python2.7/site-packages
  /glade/apps/opt/pandas/0.18.1/gnu/4.8.2/lib/python2.7/site-packages
  /glade/apps/opt/jupyter/5.0.0/gnu/4.8.2/lib/python2.7/site-packages
  /glade/apps/opt/bottleneck/1.1.0/gnu/4.8.2/lib/python2.7/site-packages
  /glade/apps/opt/python/2.7.7/gnu-westmere/4.8.2/lib/python2.7/site-packages
  /glade/apps/opt/pyzmq/16.0.2/gnu/4.8.2/lib/python2.7/site-packages
Please input the desired Python library path to use.  Default is [/glade/p/work/abanihi/ys/installs/local/tensorflow-gpu/1.2.1/lib/python2.7/site-packages]

Using python library path: /glade/p/work/abanihi/ys/installs/local/tensorflow-gpu/1.2.1/lib/python2.7/site-packages
Do you wish to build TensorFlow with MKL support? [y/N] N
No MKL support will be enabled for TensorFlow
Please specify optimization flags to use during compilation when bazel option "--config=opt" is specified [Default is -mcpu=native]: --config=opt
Do you wish to use jemalloc as the malloc implementation? [Y/n] Y
jemalloc enabled
Do you wish to build TensorFlow with Google Cloud Platform support? [y/N] N
No Google Cloud Platform support will be enabled for TensorFlow
Do you wish to build TensorFlow with Hadoop File System support? [y/N] N
No Hadoop File System support will be enabled for TensorFlow
Do you wish to build TensorFlow with the XLA just-in-time compiler (experimental)? [y/N] N
No XLA JIT support will be enabled for TensorFlow
Do you wish to build TensorFlow with VERBS support? [y/N] N
No VERBS support will be enabled for TensorFlow
Do you wish to build TensorFlow with OpenCL support? [y/N] N
No OpenCL support will be enabled for TensorFlow
Do you wish to build TensorFlow with CUDA support? [y/N] y
CUDA support will be enabled for TensorFlow
Do you want to use clang as CUDA compiler? [y/N] N
nvcc will be used as CUDA compiler
Please specify the CUDA SDK version you want to use, e.g. 7.0. [Leave empty to default to CUDA 8.0]: 
Please specify the location where CUDA  toolkit is installed. Refer to README.md for more details. [Default is /usr/local/cuda]: /ncar/opt/cuda/8.0.61
Please specify which gcc should be used by nvcc as the host compiler. [Default is /glade/apps/opt/modulefiles/ys/cmpwrappers/gcc]: 
Please specify the cuDNN version you want to use. [Leave empty to default to cuDNN 6.0]: 
Please specify the location where cuDNN  library is installed. Refer to README.md for more details. [Default is /ncar/opt/cuda/8.0.61]: /glade/u/apps/contrib/cudnn/6.0
Please specify a list of comma-separated Cuda compute capabilities you want to build with.
You can find the compute capability of your device at: https://developer.nvidia.com/cuda-gpus.
Please note that each additional compute capability significantly increases your build time and binary size.
[Default is: "3.5,5.2"]: 3.5
Do you wish to build TensorFlow with MPI support? [y/N] N
MPI support will not be enabled for TensorFlow
Configuration finished
bash-4.1$ 
```

- ```../bazel/output/bazel build -c opt --config=cuda --verbose_failures 
//tensorflow/tools/pip_package:build_pip_package```




Some Common Errors

```sh
ERROR: /glade/u/home/abanihi/.cache/bazel/_bazel_abanihi/49a6c47494a00a8cfd813563c1763438/external/nccl_archive/BUILD:33:1: undeclared inclusion(s) in rule '@nccl_archive//:nccl':
this rule is missing dependency declarations for the following files included by 'external/nccl_archive/src/libwrap.cu.cc':
  '/glade/u/apps/opt/gnu/4.8.2/include/c++/4.8.2/new'
  '/glade/u/apps/opt/gnu/4.8.2/include/c++/4.8.2/exception'
  '/glade/u/apps/opt/gnu/4.8.2/include/c++/4.8.2/bits/atomic_lockfree_defines.h'
  '/glade/u/apps/opt/gnu/4.8.2/include/c++/4.8.2/bits/exception_ptr.h'
  '/glade/u/apps/opt/gnu/4.8.2/include/c++/4.8.2/bits/exception_defines.h'
  '/glade/u/apps/opt/gnu/4.8.2/include/c++/4.8.2/bits/nested_exception.h'
  '/glade/u/apps/opt/gnu/4.8.2/include/c++/4.8.2/cmath'
  '/glade/u/apps/opt/gnu/4.8.2/include/c++/4.8.2/bits/cpp_type_traits.h'
  '/glade/u/apps/opt/gnu/4.8.2/include/c++/4.8.2/ext/type_traits.h'
  '/glade/u/apps/opt/gnu/4.8.2/include/c++/4.8.2/cstdlib'
  '/glade/u/apps/opt/gnu/4.8.2/include/c++/4.8.2/cstdio'.
Target //tensorflow/tools/pip_package:build_pip_package failed to build
```

- [tensorflow build fails with “missing dependency” error](https://stackoverflow.com/questions/35256110/tensorflow-build-fails-with-missing-dependency-error)



------------



# Environment:
- OS:
- GCC: locally installed 4.8.2
- Bazel:
- Tensorflow:
- CUDA:
- CUDNN:



