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
### Get BWA
    cd ~/bin/
    wget https://github.com/lh3/bwa/releases/download/v0.7.15/bwa-0.7.15.tar.bz2
    tar xjz bwa-0.7.15.tar.bz2
    rm bwa-0.7.15.tar.bz2
    cd bwa-0.7.15
    make
### Get BCL2FASTQ2
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
### Rsync data to /work/jelber2/radseq/170901_NB501757_0018_AHNTVFAFXX/
    cp /work/jelber2/radseq/170901_NB501757_0018_AHNTVFAFXX/RunInfo.xml /work/jelber2/radseq/170901_NB501757_0018_AHNTVFAFXX/Data/Intensities/BaseCalls/.
### BCL2FASTQ
    cd /work/jelber2/radseq/
    python ~/scripts/sesp_radseq/00-bcl2fastq.py \
    --InDir /work/jelber2/radseq/170901_NB501757_0018_AHNTVFAFXX/Data/Intensities/BaseCalls/ \
    --OutDir /work/jelber2/radseq/fastq/ \
    --SampleSheet /work/jelber2/radseq/radcap_plate1_sample_sheet.csv
### Demultiplex the Samples (internal barcodes)
#### 1 mismatch allowed in barcode
    cd /work/jelber2/radseq/fastq/
    python ~/scripts/sesp_radseq/01b-process_radtags.py \
    --Read1 Undetermined_S0_R1_001.fastq.gz \
    --Read2 Undetermined_S0_R2_001.fastq.gz \
    --barcodes ../radcap_plate1_sesp_bacs_barcodes_samples.txt \
    --OutDir /work/jelber2/radseq/fastq/demultiplexed_1_mismatch/ \
    --logname process-radtags-plate1-samples.log
#### 3 mismatches allowed in barcode and disable radcheck
    cd /work/jelber2/radseq/fastq/
    python ~/scripts/sesp_radseq/01b-process_radtags3.py \
    --Read1 Undetermined_S0_R1_001.fastq.gz \
    --Read2 Undetermined_S0_R2_001.fastq.gz \
    --barcodes ../radcap_plate1_sesp_bacs_barcodes_samples.txt \
    --OutDir /work/jelber2/radseq/fastq/demultiplexed_3_mismatch_no_radcheck/ \
    --logname process-radtags-plate1-samples.log
### Remove PCR duplicates with clone_filter
    cd /work/jelber2/radseq/fastq/demultiplexed_3_mismatch_no_radcheck/
    python ~/scripts/sesp_radseq/01c-clone_filter.py \
    --barcodes ../../radcap_plate1_sesp_bacs_barcodes_samples.txt \
    --OutDir /work/jelber2/radseq/fastq/demultiplexed_3_mismatch_no_radcheck/deduped/
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
    cd /work/jelber2/radseq/fastq/demultiplexed_3_mismatch_no_radcheck/deduped/
    python ~/scripts/sesp_radseq/02a-bwa.py --barcodes ../../../radcap_plate1_sesp_bacs_barcodes_samples.txt
#### Use pstacks to extract stacks from reference
    cd /work/jelber2/radseq/fastq/demultiplexed_3_mismatch_no_radcheck/deduped/pstacks/
    python ~/scripts/sesp_radseq/02b-pstacks.py --barcodes ../../../../radcap_plate1_sesp_bacs_barcodes_samples.txt
#### SESP (batch 1)
##### Use cstacks to make a catalog of consensus loci for SESP
    cd /work/jelber2/radseq/fastq/demultiplexed_3_mismatch_no_radcheck/deduped/pstacks/
    python ~/scripts/sesp_radseq/04-cstacks.py --barcodes ../../../../radcap_plate1_sesp_barcodes_samples.txt --batch 1
##### Use sstacks to compare an individuals' stacks to catalog for SESP
    cd /work/jelber2/radseq/fastq/demultiplexed_3_mismatch_no_radcheck/deduped/pstacks/
    python ~/scripts/sesp_radseq/05-sstacks.py --barcodes ../../../../radcap_plate1_sesp_barcodes_samples.txt --batch 1
##### Use populations to get FASTA and VCF files for SESP
    cd /work/jelber2/radseq/fastq/demultiplexed_3_mismatch_no_radcheck/deduped/pstacks/
    python ~/scripts/sesp_radseq/06-populations.py --popmap ../../../../radcap_plate1_sesp_pop_map.txt --batch 1
#### BACS (batch 2)
##### Use cstacks to make a catalog of consensus loci for BACS
    cd /work/jelber2/radseq/fastq/demultiplexed_3_mismatch_no_radcheck/deduped/pstacks/
    python ~/scripts/sesp_radseq/04-cstacks.py --barcodes ../../../../radcap_plate1_bacs_barcodes_samples.txt --batch 2
##### Use sstacks to compare an individuals' stacks to catalog for BACS
    cd /work/jelber2/radseq/fastq/demultiplexed_3_mismatch_no_radcheck/deduped/pstacks/
    python ~/scripts/sesp_radseq/05-sstacks.py --barcodes ../../../../radcap_plate1_bacs_barcodes_samples.txt --batch 2
##### Use populations to get FASTA and VCF files for BACS
    cd /work/jelber2/radseq/fastq/demultiplexed_3_mismatch_no_radcheck/deduped/pstacks/
    python ~/scripts/sesp_radseq/06-populations.py --popmap ../../../../radcap_plate1_bacs_pop_map.txt --batch 2
#### SESP and BACS combined (batch 3)
##### Use cstacks to make a catalog of consensus loci for SESP and BACS
    cd /work/jelber2/radseq/fastq/demultiplexed_3_mismatch_no_radcheck/deduped/pstacks/
    python ~/scripts/sesp_radseq/04-cstacks.py --barcodes ../../../../radcap_plate1_sesp_bacs_barcodes_samples.txt --batch 3
##### Use sstacks to compare an individuals' stacks to catalog for SESP and BACS
    cd /work/jelber2/radseq/fastq/demultiplexed_3_mismatch_no_radcheck/deduped/pstacks/
    python ~/scripts/sesp_radseq/05-sstacks.py --barcodes ../../../../radcap_plate1_sesp_bacs_barcodes_samples.txt --batch 3
##### Use populations to get FASTA and VCF files for SESP and BACS
    cd /work/jelber2/radseq/fastq/demultiplexed_3_mismatch_no_radcheck/deduped/pstacks/
    python ~/scripts/sesp_radseq/06-populations.py --popmap ../../../../radcap_plate1_sesp_bacs_pop_map.txt --batch 3
#### batch 4
    # populations with stack depth of 3 not 6
    cd /work/jelber2/radseq/fastq/demultiplexed_3_mismatch_no_radcheck/deduped/pstacks/
    python ~/scripts/sesp_radseq/06-populations.py --popmap ../../../../radcap_plate1_sesp_bacs_pop_map.txt --batch 3
    mv batch_3.fa batch_4.fa
    mv batch_3.vcf batch_4.vcf
####Get consensus RADtag sequences
##### Get loci IDs with 1-5 SNPs only
###### Batch 1
    grep -v "##" batch_1.vcf | cut -f 3 | grep -P "\d+" | perl -pe "s/(\d+)_\d+/\1/g" | \
    sort -n | uniq -c | perl -pe "s/( )+/\t/g" | perl -pe "s/^\t//g" | \
    grep -P "[1-5]\t\d+" | cut -f 2 > batch1.loci.with.1-5.snps.txt
    # how many loci are there with 1-5 snps
    wc -l batch1.loci.with.1-5.snps.txt
    # 1425
    # export the sequences for each contig in a separate file
    mkdir batch1-fasta/
    while read i;do
    foo=">CLocus_"
    bar="_.+\n"
    foo="$foo$i$bar"
    pcregrep -M $foo batch_1.fa > ./batch1-fasta/$i.fa
    done < batch1.loci.with.1-5.snps.txt
###### Batch 2
    grep -v "##" batch_2.vcf | cut -f 3 | grep -P "\d+" | perl -pe "s/(\d+)_\d+/\1/g" | \
    sort -n | uniq -c | perl -pe "s/( )+/\t/g" | perl -pe "s/^\t//g" | \
    grep -P "[1-5]\t\d+" | cut -f 2 > batch2.loci.with.1-5.snps.txt
    # how many loci are there with 1-5 snps
    wc -l batch2.loci.with.1-5.snps.txt
    # 1425
    # export the sequences for each contig in a separate file
    mkdir batch2-fasta/
    while read i;do
    foo=">CLocus_"
    bar="_.+\n"
    foo="$foo$i$bar"
    pcregrep -M $foo batch_2.fa > ./batch2-fasta/$i.fa
    done < batch2.loci.with.1-5.snps.txt
###### Batch 3
    grep -v "##" batch_3.vcf | cut -f 3 | grep -P "\d+" | perl -pe "s/(\d+)_\d+/\1/g" | \
    sort -n | uniq -c | perl -pe "s/( )+/\t/g" | perl -pe "s/^\t//g" | \
    grep -P "[1-5]\t\d+" | cut -f 2 > batch3.loci.with.1-5.snps.txt
    # how many loci are there with 1-5 snps
    wc -l batch3.loci.with.1-5.snps.txt
    # 1425
    # export the sequences for each contig in a separate file
    mkdir batch3-fasta/
    while read i;do
    foo=">CLocus_"
    bar="_.+\n"
    foo="$foo$i$bar"
    pcregrep -M $foo batch_3.fa > ./batch3-fasta/$i.fa
    done < batch3.loci.with.1-5.snps.txt
###### Batch 4
    grep -v "##" batch_4.vcf | cut -f 3 | grep -P "\d+" | perl -pe "s/(\d+)_\d+/\1/g" | \
    sort -n | uniq -c | perl -pe "s/( )+/\t/g" | perl -pe "s/^\t//g" | \
    grep -P "[1-5]\t\d+" | cut -f 2 > batch4.loci.with.1-5.snps.txt
    # export the sequences for each contig in a separate file
    mkdir batch4-fasta/
    while read i;do
    foo=">CLocus_"
    bar="_.+\n"
    foo="$foo$i$bar"
    pcregrep -M $foo batch_4.fa > ./batch4-fasta/$i.fa
    done < batch4.loci.with.1-5.snps.txt
##### Remove loci with more than 2 alleles per individual
###### Batch 1
    cd batch1-fasta/
    for file in *.fa;do
        a=$(grep ">" $file | grep -Po "\[.+\]" | sort | uniq -c | perl -pe "s/( )+/\t/g"| cut -f 2)
        for item in $a;do
            if [ $item -gt 2 ];then
                mv $file $file.rm
            fi
        done
    done
    # how many loci have less than or equal to 2 alleles per individual
    ls *.fa | wc -l
    # 150
###### Batch 2
    cd batch2-fasta/
    for file in *.fa;do
        a=$(grep ">" $file | grep -Po "\[.+\]" | sort | uniq -c | perl -pe "s/( )+/\t/g"| cut -f 2)
        for item in $a;do
            if [ $item -gt 2 ];then
                mv $file $file.rm
            fi
        done
    done
    # how many loci have less than or equal to 2 alleles per individual
    ls *.fa | wc -l
    # 17
###### Batch 3
    cd batch3-fasta/
    for file in *.fa;do
        a=$(grep ">" $file | grep -Po "\[.+\]" | sort | uniq -c | perl -pe "s/( )+/\t/g"| cut -f 2)
        for item in $a;do
            if [ $item -gt 2 ];then
                mv $file $file.rm
            fi
        done
    done
    # how many loci have less than or equal to 2 alleles per individual
    ls *.fa | wc -l
    # 152
###### Batch 4
    cd batch4-fasta/
    for file in *.fa;do
        a=$(grep ">" $file | grep -Po "\[.+\]" | sort | uniq -c | perl -pe "s/( )+/\t/g"| cut -f 2)
        for item in $a;do
            if [ $item -gt 2 ];then
                mv $file $file.rm
            fi
        done
    done
    # how many loci have less than or equal to 2 alleles per individual
    ls *.fa | wc -l
    # 290
##### Get consensus sequence for each contig
    # cons for consensus or consambig for consensus with ambiguities
###### Batch 1
    for file in *.fa;do
    ~/bin/EMBOSS-6.6.0/emboss/cons -sequence $file -outseq $file.cons --auto --name $file.consensus
    done
    # get all sequences in one file with cat, then remove line breaks with awk, then remove 1st newline
    cat *.fa.cons > stacks.cons.fa2
    awk '/^>/ {printf("\n%s\n",$0);next; } { printf("%s",$0);}  END {printf("\n");}' stacks.cons.fa2 | tail -n +2 > stacks.cons.fa
    python ~/bin/get_fasta_lengths.py --input stacks.cons.fa
    #Reads:		150
    #Bp:		21,000
    #Avg. len:	140.0
    #STDERR len:	0.0
    #Min. len:	140
    #Max. len:	140
    #Median len:	140.0
    #Contigs > 1kb:	0
###### Batch 2
    cd batch2-fasta/
    for file in *.fa;do
    ~/bin/EMBOSS-6.6.0/emboss/cons -sequence $file -outseq $file.cons --auto --name $file.consensus
    done
    # get all sequences in one file with cat, then remove line breaks with awk, then remove 1st newline
    cat *.fa.cons > stacks.cons.fa2
    awk '/^>/ {printf("\n%s\n",$0);next; } { printf("%s",$0);}  END {printf("\n");}' stacks.cons.fa2 | tail -n +2 > stacks.cons.fa
    python ~/bin/get_fasta_lengths.py --input stacks.cons.fa
    #Reads:		17
    #Bp:		2,380
    #Avg. len:	140.0
    #STDERR len:	0.0
    #Min. len:	140
    #Max. len:	140
    #Median len:	140.0
    #Contigs > 1kb:	0
###### Batch 3
    cd batch3-fasta/
    for file in *.fa;do
    ~/bin/EMBOSS-6.6.0/emboss/cons -sequence $file -outseq $file.cons --auto --name $file.consensus
    done
    # get all sequences in one file with cat, then remove line breaks with awk, then remove 1st newline
    cat *.fa.cons > stacks.cons.fa2
    awk '/^>/ {printf("\n%s\n",$0);next; } { printf("%s",$0);}  END {printf("\n");}' stacks.cons.fa2 | tail -n +2 > stacks.cons.fa
    python ~/bin/get_fasta_lengths.py --input stacks.cons.fa
    #Reads:		152
    #Bp:		21,280
    #Avg. len:	140.0
    #STDERR len:	0.0
    #Min. len:	140
    #Max. len:	140
    #Median len:	140.0
    #Contigs > 1kb:	0
###### Batch 4
    for file in *.fa;do
    ~/bin/EMBOSS-6.6.0/emboss/cons -sequence $file -outseq $file.cons --auto --name $file.consensus
    done
    # get all sequences in one file with cat, then remove line breaks with awk, then remove 1st newline
    cat *.fa.cons > stacks.cons.fa2
    awk '/^>/ {printf("\n%s\n",$0);next; } { printf("%s",$0);}  END {printf("\n");}' stacks.cons.fa2 | tail -n +2 > stacks.cons.fa
    python ~/bin/get_fasta_lengths.py --input stacks.cons.fa
    #Reads:		290
    #Bp:		40,600
    #Avg. len:	140.0
    #STDERR len:	0.0
    #Min. len:	140
    #Max. len:	140
    #Median len:	140.0
    #Contigs > 1kb:	0
###### BLAST stacks.consensus.batch4.fa to white-throated sparrow genome
    ~/bin/ncbi-blast-2.6.0+/bin/blastn -query stacks.consensus.batch4.fa \
    -db 44394_ref_Zonotrichia_albicollis-1.0.1_chrUn.fa -outfmt 6 -out test -max_hsps 1 -max_target_seqs 1
    # 279 good hits!
### De novo assembly approach to RAD locus analysis
#### Use cstacks to make a catalog of consensus loci
#### Use sstacks to compare an individuals' stacks to catalog
#### Use populations to get FASTA and VCF files
