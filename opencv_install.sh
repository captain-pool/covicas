sudo apt-get update && sudo apt-get upgrade
sudo apt-get install build-essential cmake pkg-config
sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev
sudo apt-get install libgtk2.0-dev libgtk-3-dev
sudo apt-get install libatlas-base-dev gfortran
sudo apt-get install python2.7-dev python3-dev python3-pip
cd $HOME
if [[ ! -f opencv.zip ]]
then
  wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.3.0.zip
  unzip opencv.zip
fi
if [[ ! -f opencv_contrib.zip ]]
then
  wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.3.0.zip
  unzip opencv_contrib.zip
fi
cd $OLDPWD
pip3 install -r requirements.txt
cd $HOME/opencv-3.3.0/
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.3.0/modules \
    -D BUILD_EXAMPLES=ON ..
sudo sed -i -e "s/CONF_SWAPSIZE=100/CONF_SWAPSIZE=1024/g" /etc/dphys-swapfile
sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start
make -j$(nproc)
sudo make install
sudo ldconfig
