# sesp_radseq
## Get software
### Get STACKS (on CentOS machine and rsync over to SuperMikeII)
    cd ~/bin/
    wget http://catchenlab.life.illinois.edu/stacks/source/stacks-1.44.tar.gz
    tar xzf stacks-1.44.tar.gz
    rm stacks-1.44.tar.gz
    cd stacks-1.44/
    # Need a C++11 compiler for STACKS
    # http://hiltmon.com/blog/2015/08/09/c-plus-plus-11-on-centos-6-dot-6/ #
    # Install a C++11 Compiler
    # We need to get the repo files for DevTools2, 
    # a Red Hat package that contains a supported C++11 compiler.
    # As root, run the following command to retrieve
    # the repo file: 
    su
    wget http://people.centos.org/tru/devtools-2/devtools-2.repo -O /etc/yum.repos.d/devtools-2.repo
    #
    # Then install the compiler and support tools:
    yum install devtoolset-2-gcc devtoolset-2-binutils devtoolset-2-gcc-c++
    #
    # Before you can compile C++11 code with the DevTools2 compiler, you need to enable it in a new shell:
    scl enable devtoolset-2 bash
    ./configure --prefix=/home/jelber2/bin/stacks-1.44
    make
### Get EMBOSS
    cd ~/bin/
    wget ftp://emboss.open-bio.org/pub/EMBOSS/EMBOSS-6.6.0.tar.gz
    tar xzf EMBOSS-6.6.0.tar.gz
    rm EMBOSS-6.6.0.tar.gz
    cd EMBOSS-6.6.0
    ./configure --without-x
    make
### BWA
    
## Analysis of 3RAD data
### BCL2FASTQ
    
### Demultiplex the PLATES (i7 barcode)
    
