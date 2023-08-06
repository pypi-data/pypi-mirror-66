```
Copyright (c) 2010-2018 ViSUS L.L.C., 
Scientific Computing and Imaging Institute of the University of Utah
 
ViSUS L.L.C., 50 W. Broadway, Ste. 300, 84101-2044 Salt Lake City, UT
University of Utah, 72 S Central Campus Dr, Room 3750, 84112 Salt Lake City, UT
 
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
contributors may be used to endorse or promote products derived from
this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

For additional information about this project contact: pascucci@acm.org
For support: support@visus.net
```

# ViSUS Visualization project  

* `osx linux` build status: [![Build Status](https://travis-ci.com/sci-visus/visus.svg?token=yzpwCyVPupwSzFjgTCoA&branch=master)](https://travis-ci.com/sci-visus/visus)

* `windows` build status: [![Windows Build status](https://ci.appveyor.com/api/projects/status/32r7s2skrgm9ubva/branch/master?svg=true)](https://ci.appveyor.com/api/projects/status/32r7s2skrgm9ubva/branch/master)

Table of content:


[PIP Distribution](#pip-distribution)

[Windows compilation](#windows-compilation)

[MacOSX compilation](#macosx-compilation)

[Linux compilation](#linux-compilation)


## PIP distribution


### Windows

On a command prompt:

```
REM change this as needed
set PYTHON_EXECUTABLE=c:\Python38\python.exe

%PYTHON_EXECUTABLE% -m pip install --user --no-cache numpy opencv-python OpenVisus

REM finilize the installation 
%PYTHON_EXECUTABLE% -m OpenVisus configure 

%PYTHON_EXECUTABLE% -m OpenVisus dirname
cd \to\the\direttory\printed\by\above\command

REM test python  examples 
%PYTHON_EXECUTABLE% Samples\python\Array.py
%PYTHON_EXECUTABLE% Samples\python\Dataflow.py
%PYTHON_EXECUTABLE% Samples\python\Idx.py
%PYTHON_EXECUTABLE% Samples\python\TestViewer1.py

REM test OpenVisus viewer
.\visusviewer.bat
```

### OSX

On a terminal:

```
python -m pip install --user --no-cache numpy OpenVisus

# finilize installation 
python -m OpenVisus configure 

cd $(python -m OpenVisus dirname)

# test python  examples
python Samples/python/Array.py
python Samples/python/Dataflow.py
python Samples/python/Idx.py
python Samples/python/Viewer.py

# run OpenVisus viewer
./visusviewer.command 
```


### Linux

On a terminal:

```
python -m pip install --user --no-cache numpy OpenVisus

# finilize installation 
python -m OpenVisus configure 

cd $(python -m OpenVisus dirname)

# test python  examples
python Samples/python/Array.py
python Samples/python/Dataflow.py
python Samples/python/Idx.py
python Samples/python/Viewer.py

# run OpenVisus viewer
./visusviewer.sh
```


## Windows compilation

Install git, cmake and swig. 
The fastest way is to use `chocolatey` i.e from an Administrator Prompt:

```
@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
choco install -y -allow-empty-checksums git cmake swig 
```

Install [Python3.7] (https://www.python.org/ftp/python/3.7.0/python-3.7.0-amd64.exe)
Install [Qt5](http://download.qt.io/official_releases/online_installers/qt-unified-windows-x86-online.exe) 

If you want to use Microsoft vcpkg (faster) install [vcpkg](https://github.com/Microsoft/vcpkg):

```
cd c:\
mkdir tools
cd tools
git clone https://github.com/Microsoft/vcpkg
cd vcpkg
.\bootstrap-vcpkg.bat
set CMAKE_TOOLCHAIN_FILE=c:/tools/vcpkg/scripts/buildsystems/vcpkg.cmake
set VCPKG_TARGET_TRIPLET=x64-windows
```

To compile OpenVIsus:

```
git clone https://github.com/sci-visus/OpenVisus
cd OpenVisus

REM *** change path as needed *** 
set PYTHON_EXECUTABLE=C:\Python37\python.exe
set CMAKE_EXECUTABLE=C:\Program Files\CMake\bin\cmake.exe
set QT5_DIR=c:\Qt\5.11.2\msvc2015_64\lib\cmake\Qt5
.\CMake\build.bat
```

To test if it's working:

```
cd install
.\visus.bat
.\visusviewer.bat 
```


## MacOSX compilation

Make sure you have command line toos:

```
sudo xcode-select --install
# if command line tools do not work, type the following: sudo xcode-select --reset
```

Build the repository:

```
git clone https://github.com/sci-visus/OpenVisus
cd OpenVisus
./CMake/build.sh
```

To test if it's working:

```
cd install
./visus.command
./visusviewer.command 
```
      
## Linux compilation

Build the repository:

```
git clone https://github.com/sci-visus/OpenVisus
cd OpenVisus
./CMake/build.sh
```

To test if it's working:

```
cd install
./visus.sh
./visusviewer.sh
```

Note that on linux you can even compile using docker. An example is:


```
BUILD_DIR=$(pwd)/build/docker/manylinux PYTHON_VERSION=3.6.1 DOCKER_IMAGE=quay.io/pypa/manylinux1_x86_64 ./CMake/build_docker.sh
BUILD_DIR=$(pwd)/build/docker/trusty    PYTHON_VERSION=3.6.1 DOCKER_IMAGE=ubuntu:trusty                  ./CMake/build_docker.sh
BUILD_DIR=$(pwd)/build/docker/bionic    PYTHON_VERSION=3.6.1 DOCKER_IMAGE=ubuntu:bionic                  ./CMake/build_docker.sh
BUILD_DIR=$(pwd)/build/docker/xenial    PYTHON_VERSION=3.6.1 DOCKER_IMAGE=ubuntu:xenial                  ./CMake/build_docker.sh
BUILD_DIR=$(pwd)/build/docker/leap      PYTHON_VERSION=3.6.1 DOCKER_IMAGE=opensuse:leap                  ./CMake/build_docker.sh
```


## Commit, Continuous Integration deploy

Edit the file `conda/openvisus/meta.yaml` and increase the Tag version number (line 3)
Edit the file `CMake/setup.py` and increase the Tag version number ()

Commit, tag the current commit and push to origin:

```
TAG=...insert your tag number here...
git commit -a -m "New tag"
git tag -a $TAG -m "$TAG"
git push origin && git push origin $TAG
```
