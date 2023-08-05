FROM nvidia/cuda:10.2-devel-centos6

RUN yum update -y
RUN yum install -y wget curl perl util-linux xz bzip2 git patch which perl
RUN yum install -y yum-utils centos-release-scl
RUN yum-config-manager --enable rhel-server-rhscl-7-rpms
RUN yum install -y devtoolset-7-gcc devtoolset-7-gcc-c++ devtoolset-7-gcc-gfortran devtoolset-7-binutils
ENV PATH=/opt/rh/devtoolset-7/root/usr/bin:$PATH
ENV LD_LIBRARY_PATH=/opt/rh/devtoolset-7/root/usr/lib64:/opt/rh/devtoolset-7/root/usr/lib:$LD_LIBRARY_PATH

COPY ./build_scripts /build_scripts

RUN bash build_scripts/build.sh && rm -r build_scripts

ENV SSL_CERT_FILE=/opt/_internal/certs.pem

ENV AUDITWHEEL_PLAT=manylinux2010_x86_64

RUN yum remove -y cmake cmake3
RUN /opt/python/cp36-cp36m/bin/pip install cmake

RUN ln -s /opt/python/cp36-cp36m/bin/cmake /usr/bin/cmake

