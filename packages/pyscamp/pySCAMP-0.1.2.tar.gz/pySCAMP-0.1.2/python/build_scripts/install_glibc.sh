GLIBC_VERSION=$1

mkdir glibc_install && cd glibc_install 
wget http://ftp.gnu.org/gnu/glibc/glibc-${GLIBC_VERSION}.tar.gz
tar zxvf glibc-${GLIBC_VERSION}.tar.gz
cd glibc-${GLIBC_VERSION}
mkdir build
cd build
../configure --prefix=/opt/glibc-${GLIBC_VERSION}
make -j8
make install
export LD_LIBRARY_PATH="/opt/glibc-${GLIBC_VERSION}/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
