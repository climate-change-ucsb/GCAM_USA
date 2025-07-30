GCAM Install guideline for Princeton Cluster

Preparing for Della Cluster:

Install Princeton VPN (Be connected before using Princeton Cluster) 

https://princeton.service-now.com/service?id=kb_article&sys_id=6023

Link to login Della Cluster:

https://mydella.princeton.edu/

1. Load the necessary modules

Please make sure that you have loaded this module before compiling. 

module load gcc-toolset/13 or 14

module load intel/2024.0.2

module load cmake/3.18.2

module load java/11

module load intel-tbb/2021.11

module list (To check the module is loaded successfully)

may need to check with, e.g., module avail gcc-toolset

2. Download GCAM:

Code Example with path in cluster: 

cd ~/hk6264/work

mkdir GCAM

cd GCAM

wget https://github.com/JGCRI/gcam-core/archive/refs/tags/gcam-v8.2.zip

unzip gcam-v8.2.zip

echo $CC



2. Build Boost 

Code Example with path in cluster: 

cd ~/hk6264/work/GCAM
mkdir build
mkdir libs
cd build
wget https://archives.boost.io/release/1.78.0/source/boost_1_78_0.tar.bz2
tar --bzip2 -xf ./boost_1_78_0.tar.bz2
mv boost_1_78_0 ../libs/boost-lib
cd ../libs/boost-lib
./bootstrap.sh --with-libraries=system,filesystem --prefix=~/work/GCAM/libs/boost-lib/stage/lib
./b2 stage

3. Build Eigen 

Code Example with path in cluster: 

cd ~/hk6264/work/GCAM/build
wget https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.tar.gz
tar -zxf eigen-master.tar.gz
mv eigen-master ../libs/eigen

4. Build Hector (2.5.0)

Code Example with path in cluster: 

cd ~/hk6264/work/GCAM/gcam-core-gcam-v6.0/cvs/objects/climate/source
wget https://github.com/JGCRI/hector/archive/refs/tags/v2.5.0.zip
unzip v2.5.0.zip or unzip rcmip-tier1.zip
rename hector2.5.0 to hector:
mv hector-rcmip-tier1 hector
#mv hector-rcmip-tier1/* .
#rm -rf hector-rcmip-tier1
suggestions: try v3.2.0.zip

4b. Build TBB

Code Example with path in cluster: 

cd ~/hk6262/work/GCAM/libs
wget https://github.com/uxlfoundation/oneTBB/archive/refs/tags/v2022.0.0.tar.gz 
tar -zxf oneTBB-2022.0.0.tar.gz
mv oneTBB-2022.0.0 tbb


5. Download Java and openjdk

Code Example with path in cluster: 

cd ~/hk6264/work/GCAM/libs
wget https://github.com/JGCRI/modelinterface/releases/download/v5.1/jars.zip
unzip jars.zip

Code Example with path in cluster: 

cd ~/hk6264/work/GCAM/libs
wget https://download.java.net/java/GA/jdk22.0.1/c7ec1332f7bb44aeba2eb341ae18aca4/8/GPL/openjdk-22.0.1_linux-x64_bin.tar.gz
tar -zxf openjdk-22.0.1_linux-x64_bin.tar.gz


6. Compiling

Code Example with path in cluster: 
cd ~/hk6264/work_1/GCAM
cd ~/hk6264/work/GCAM
vi .bashrc

export CXX="g++" 
export GCAM_HOME=${HOME}/hk6264/work/GCAM
export GCAMLIB_HOME=${GCAM_HOME}/libs 
export BOOST_INCLUDE=${GCAMLIB_HOME}/boost-lib
export BOOST_LIB=${GCAMLIB_HOME}/boost-lib/stage/lib/
export JAVA_INCLUDE=${GCAMLIB_HOME}/jdk-22.0.1/include
export JAVA_LIB=${GCAMLIB_HOME}/jdk-22.0.1/lib/server
export JARS_LIB=${GCAMLIB_HOME}/jars/*
export EIGEN_INCLUDE=${GCAMLIB_HOME}/eigen
export TBB_INCLUDE=${HOME}/libs/tbb/include
export TBB_LIB=${HOME}/libs/tbb/lib
export USE_GCAM_PARALLEL=0
export PATH=$HOME/xerces-c/bin:$PATH
export LD_LIBRARY_PATH=$HOME/xerces-c/lib:$LD_LIBRARY_PATH
export CXXFLAGS="-I home/hk6264 /work/GCAM /xercesc/include"
source .bashrc


7. Build GCAM

cd ~/hk6264/work/GCAM/gcam-core-gcam-v6.0/cvs/objects/build/linux
make clean
make gcam -j 8

Common error:
Error:
In file included from manage_state_variables.cpp:44:
../../../util/base/include/manage_state_variables.hpp:114:5: error: 'uint64_t' does not name a type
  114 |     uint64_t mNumCollected;

Solution: 
cd gcam-core-gcam-v6.0/cvs/objects/util/base/include
vi manage_state_variables : 
add #include <stdint.h> at line 50.


May need: make xml. or copy xml (the same GCAM version) to input/gcamdata/
See https://docs.google.com/document/d/1sJJgvWVmH2558JtqxEy9CilCv62hOQ2tgPmrPUcDWQU/edit?usp=sharing
for the last part

8. Run model

#!/bin/bash
#SBATCH --job-name=gcam_run           # Job name
#SBATCH --nodes=1                    # Number of nodes
#SBATCH --ntasks=1                   # Number of tasks
#SBATCH --cpus-per-task=1            # Number of CPU cores per task
#SBATCH --mem=16G                     # Memory per node
#SBATCH --time=02:00:00              # Time limit (HH:MM:SS)
#SBATCH --output=gcam_output.log     # Standard output log
#SBATCH --error=gcam_error.log       # Standard error log

# Load necessary modules
module purge
module load gcc-toolset/13
module load boost/1.85.0
module load java/11


# Set environment variables
export GCAM_HOME=~/hk6264/work/GCAM/gcam-core-gcam-v6.0
export EIGEN_INCLUDE=$GCAM_HOME/libs/eigen
export BOOST_LIB=$GCAM_HOME/libs/boost-lib/stage/lib
export LD_LIBRARY_PATH=/home/ee0338/GCAM/libs/boost-lib/stage/lib/:$LD_LIBRARY_PATH

# Navigate to the executable directory
cd $GCAM_HOME/exe

# Run GCAM with the specified configuration file and output directory
./gcam.exe -C configuration_ref.xml 

And 

Write “sbatch gcam_job.slurm” in the command to run GCAM.
