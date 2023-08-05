echo "Installing CUDA 10.1 and CuDNN"
rm -rf /usr/local/cuda-10.1 /usr/local/cuda
# # install CUDA 10.1 in the same container
wget -q http://developer.download.nvidia.com/compute/cuda/10.1/Prod/local_installers/cuda_10.1.243_418.87.00_linux.run
chmod +x cuda_10.1.243_418.87.00_linux.run
./cuda_10.1.243_418.87.00_linux.run    --extract=/tmp/cuda
rm -f cuda_10.1.243_418.87.00_linux.run
mv /tmp/cuda/cuda-toolkit /usr/local/cuda-10.1
rm -rf /tmp/cuda
rm -f /usr/local/cuda && ln -s /usr/local/cuda-10.1 /usr/local/cuda
