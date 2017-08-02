# sesp_radseq
## Get software
### Get STACKS (on CentOS machine and rsync over to SuperMikeII)
    cd ~/bin/
    wget http://catchenlab.life.illinois.edu/stacks/source/stacks-1.44.tar.gz
    tar xzf stacks-1.44.tar.gz
    rm stacks-1.44.tar.gz
    cd stacks-1.44/
    # add +gcc-4.7.2 to ~/.soft file then resoft
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
    cd ~/bin/
    wget https://github.com/lh3/bwa/releases/download/v0.7.15/bwa-0.7.15.tar.bz2
    tar xjz bwa-0.7.15.tar.bz2
    rm bwa-0.7.15.tar.bz2
    cd bwa-0.7.15
    make
### BCL2FASTQ2
    cd ~/bin/
    wget https://support.illumina.com/content/dam/illumina-support/documents/downloads/software/bcl2fastq/bcl2fastq2-v2-18-0-12-tar.zip
    unzip bcl2fastq2-v2-18-0-12-tar.zip
    rm bcl2fastq2-v2-18-0-12-tar.zip
    tar xzf bcl2fastq2-v2.18.0.12.tar.gz
    rm bcl2fastq2-v2.18.0.12.tar.gz
    cd bcl2fastq
    # add +cmake-2.8.9-gcc-4.4.6 and +gcc-4.7.2 to ~/.soft file then resoft
    mkdir bin
    cd bin/
    chmod ugo+x ../src/configure
    chmod ugo+x ../src/cmake/bootstrap/installCmake.sh
    ../src/configure --prefix=/home/jelber2/bin/bcl2fastq/bin
    make
    make install
## Analysis of 3RAD data
    mkdir -p /work/jelber2/radseq/
### BCL2FASTQ
    
### Demultiplex the PLATES (i7 barcode)
### Demultiplex the Samples (internal barcodes)
### Remove PCR duplicates with clone_filter
### Reference approach to RAD locus analysis
#### Get reference genome
    cd /work/jelber2/radseq/
    wget ftp://ftp.ncbi.nlm.nih.gov/genomes/Zonotrichia_albicollis/CHR_Un/44394_ref_Zonotrichia_albicollis-1.0.1_chrUn.fa.gz
#### Make BWA index
    ~/bin/bwa-0.7.15/bwa index -a bwtsw \
    -p 44394_ref_Zonotrichia_albicollis-1.0.1_chrUn \
    44394_ref_Zonotrichia_albicollis-1.0.1_chrUn.fa.gz
    # implemented in 000-make-bwa-index.sh on SuperMikeII
    # qsub ~/scripts/sesp_radseq/000-make-bwa-index.sh
#### Map deduped reads to reference genome with BWA
#### Use pstacks to extract stacks from reference
#### Use cstacks to make a catalog of consensus loci
#### Use sstacks to compare an individuals' stacks to catalog
#### Use populations to get FASTA and VCF files
### De novo assembly approach to RAD locus analysis
#### Use cstacks to make a catalog of consensus loci
#### Use sstacks to compare an individuals' stacks to catalog
#### Use populations to get FASTA and VCF files
