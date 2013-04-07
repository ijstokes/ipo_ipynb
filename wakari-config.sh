export BLPAPI_ROOT=~/opt/blpapi
export LD_LIBRARY_PATH=$BLPAPI_ROOT/lib

# INSTALL INSTRUCTIONS
# --------------------
#
# To install Bloomberg and get it working, the following are necessary:
#
# 1. CFLAGS and LIBRARY_PATH for build only
#     export CFLAGS=-I$BLPAPI_ROOT/include
#     export LIBRARY_PATH=$BLPAPI_ROOT/lib
#
# 2. From here: http://www.openbloomberg.com/open-api/
#       - C++ SDK: http://cdn.gotraffic.net/open/blpapi_cpp_3.6.3.1-linux.tar.gz
#       - Python interface: http://cdn.gotraffic.net/open/blpapi_python-3.5.2.1.tar.gz
#
# 3. Put C++ SDK in $BLAPI_ROOT
#
# 4. Make sure Anaconda is default python, CFLAGS, and LIBRARY_PATH are set as above
#    then execute the following from the Bloomberg Python Interface directory:
#       python setup.py install
#
# 5. Need to use root perms on the container to set the hostname to something that is
#    world resolvable, so if 'hostname' returns 'prod-vz-16' then you need to execute:
#       mylaptop   $ ssh prod-vz-16.aws.continuum.io
#       prod-vz-16 $ sudo su -
#       prod-vz-16 # vzctl enter 501 # or whatever container your Wakari session is
#       prod-vz-16 # hostname prod-vz-16.aws.continuum.io
#
# 6. From your Wakari account, the Bloomberg Python API should now be installed in
#    Anaconda, and can be used if BLPAPI_ROOT and LD_LIBRARY_PATH are set as above
