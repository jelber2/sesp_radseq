#sesp_radseq
========
## Get gene names, # genes, # exons for pigmentome of zebra finch and white-throated sparrow
### Get newest bedtools
    cd ~/bin/
    wget https://github.com/arq5x/bedtools2/releases/download/v2.26.0/bedtools-2.26.0.tar.gz
    tar -xzf bedtools-2.26.0.tar.gz
    mv bedtools2 bedtools-2.26.0
    cd bedtools-2.26.0
    make
### Zebra Finch pigmentome stats (after following rGO2TR, see rGO2TR_zebra_finch.R script)
    cd ~/Dropbox/LSU/Dissertation/Manuscripts/sesp_radseq/zebra_finch/
    ~/bin/bedtools-2.26.0/bin/bedtools intersect \
    -a zebra.finch.103.genome.gff3.gz \
    -b zebra.finch.pigmentome.bed \
    > zebra.finch.pigmentome.gff
    # count number of exons
    awk 'BEGIN{OFS="\t";} $3=="exon" {print $1,$2,$3,$4,$5,$6,$7,$8,$9}' \
    zebra.finch.pigmentome.gff > zebra.finch.pigmentome.exons.gff
    # how many exons are there
    wc -l zebra.finch.pigmentome.exons.gff
    # 1114
    # count number of unqiue genes
    awk 'BEGIN{OFS="\t";} $3=="gene" {print $1,$2,$3,$4,$5,$6,$7,$8,$9}' \
    zebra.finch.pigmentome.gff > zebra.finch.pigmentome.genes.gff
    perl -pe "s/\S+=GeneID:(\d+).+/\1/g" zebra.finch.pigmentome.genes.gff | \
    cut -f 9 | sort | uniq > zebra.finch.pigmentome.genes.unique.txt
    # how many unique genes
    wc -l zebra.finch.pigmentome.genes.unique.txt
    # 71
    # r code for gene descriptions
    install.packages("devtools")
    install.packages("rvest")
    install.packages("XML")
    source("http://bioconductor.org/biocLite.R")
    biocLite("GenomicRanges")
    biocLite("GOstats")
    biocLite("GO.db")
    devtools::install_github("jelber2/rGO2TR")
    library("rvest")
    library("XML")
    library("rGO2TR")
    library("RCurl")
    sessionInfo()
    #R version 3.3.2 (2016-10-31)
    #Platform: x86_64-w64-mingw32/x64 (64-bit)
    #Running under: Windows >= 8 x64 (build 9200)
    #
    #locale:
    #[1] LC_COLLATE=English_United States.1252  LC_CTYPE=English_United States.1252   
    #[3] LC_MONETARY=English_United States.1252 LC_NUMERIC=C                          
    #[5] LC_TIME=English_United States.1252    
    #
    #attached base packages:
    #[1] stats     graphics  grDevices utils     datasets  methods   base     
    #
    #other attached packages:
    #[1] RCurl_1.95-4.8 bitops_1.0-6   rGO2TR_1.0.4   XML_3.98-1.4   rvest_0.3.2    xml2_1.0.0    
    #
    #loaded via a namespace (and not attached):
    #[1] httr_1.2.1   magrittr_1.5 R6_2.2.0     tools_3.3.2  Rcpp_0.12.7     setwd("C:/Users/jelber2/Dropbox/LSU/Dissertation/Manuscripts/sesp_radseq/zebra_finch/")
    input <- read.table("zebra.finch.pigmentome.genes.unique.txt")
    Sys.setenv(email="jelber2@lsu.edu")
    output <- rGO2TR::efetch2(id = input$V1,
                              "gene",
                              "gb",
                              "xml")
    output2 <- strsplit(output, "\n")
    output3 <- output2[[1]][grepl("<Gene-ref_desc>.+</Gene-ref_desc>",
                            output2[[1]],
                            perl=TRUE)]
    output4 <- sub("\\s+<Gene-ref_desc>(.+)</Gene-ref_desc>",
                   "\\1",
                   output3,
                   perl=TRUE)
    writeLines(output4, "zebra.finch.pigmentome.genes.unique.desc.txt")
### White-throated sparrow pigmentome(after following rGO2TR, see rGO2TR_white_throated_sparrow.R script)
    cd ~/Dropbox/LSU/Dissertation/Manuscripts/sesp_radseq/white_throated_sparrow/
    ~/bin/bedtools-2.26.0/bin/bedtools intersect \
    -a sparrow.genome.gff3.gz \
    -b sparrow.pigmentome.bed \
    > sparrow.pigmentome.gff
    # count number of exons
    awk 'BEGIN{OFS="\t";} $3=="exon" {print $1,$2,$3,$4,$5,$6,$7,$8,$9}' \
    sparrow.pigmentome.gff > sparrow.pigmentome.exons.gff
    # how many exons are there
    wc -l sparrow.pigmentome.exons.gff
    # 1633
    # count number of unqiue genes
    awk 'BEGIN{OFS="\t";} $3=="gene" {print $1,$2,$3,$4,$5,$6,$7,$8,$9}' \
    sparrow.pigmentome.gff > sparrow.pigmentome.genes.gff
    perl -pe "s/\S+=GeneID:(\d+).+/\1/g" sparrow.pigmentome.genes.gff | \
    cut -f 9 | sort | uniq > sparrow.pigmentome.genes.unique.txt
    # how many unique genes
    wc -l sparrow.pigmentome.genes.unique.txt
    # 67
    # r code for gene descriptions
    setwd("C:/Users/jelber2/Dropbox/LSU/Dissertation/Manuscripts/sesp_radseq/white_throated_sparrow/")
    input <- read.table("sparrow.pigmentome.genes.unique.txt")
    Sys.setenv(email="jelber2@lsu.edu")
    output <- rGO2TR::efetch2(id = input$V1,
                              "gene",
                              "gb",
                              "xml")
    output2 <- strsplit(output, "\n")
    output3 <- output2[[1]][grepl("<Gene-ref_desc>.+</Gene-ref_desc>",
                            output2[[1]],
                            perl=TRUE)]
    output4 <- sub("\\s+<Gene-ref_desc>(.+)</Gene-ref_desc>",
                   "\\1",
                   output3,
                   perl=TRUE)
    writeLines(output4, "sparrow.pigmentome.genes.unique.desc.txt")
### White-throated sparrow pigmentome version 2
    #Compared white-throated sparrow pigmentome and zebra finch pigmentome
    #Ended up "missing" some pigment mRNA identified in the zebra finch but
    #but not white-throated sparrow (WTSP)
#### Reran rGO2TR with WTSP
    #added following mRNA to retained.mRNA.list 
    missing.pigment.mRNAs.based.on.zebra.finch.pigmentome <- c("XM_005490308.2",
          "XM_014269348.1","XM_014264578.1","XM_014274929.1",
          "XM_014267885.1","XM_014265378.1","XM_005486403.2","XM_005487847.2",
          "XM_014273782.1","XM_014270825.1","XM_014274776.1")
    retained.mRNA.list <- c(retained.mRNA.list, missing.pigment.mRNAs.based.on.zebra.finch.pigmentome)
    # Result is sparrow.pigmentome.ver2.bed, which is ~ 257kbp
#### Calculate number of genes and exons
    ~/bin/bedtools-2.22.1/bin/bedtools intersect \
    -a sparrow.genome.gff3.gz \
    -b sparrow.pigmentome.ver2.bed \
    > sparrow.pigmentome.ver2.gff
    # count number of exons
    awk 'BEGIN{OFS="\t";} $3=="exon" {print $1,$2,$3,$4,$5,$6,$7,$8,$9}' \
    sparrow.pigmentome.ver2.gff > sparrow.pigmentome.ver2.exons.gff
    # how many exons are there
    wc -l sparrow.pigmentome.ver2.exons.gff
    # 1874
    # count number of unqiue genes
    awk 'BEGIN{OFS="\t";} $3=="gene" {print $1,$2,$3,$4,$5,$6,$7,$8,$9}' \
    sparrow.pigmentome.ver2.gff > sparrow.pigmentome.ver2.genes.gff
    perl -pe "s/\S+=GeneID:(\d+).+/\1/g" sparrow.pigmentome.ver2.genes.gff | \
    cut -f 9 | sort | uniq > sparrow.pigmentome.ver2.genes.unique.txt
    # how many unique genes
    wc -l sparrow.pigmentome.ver2.genes.unique.txt
    # 80
## Install ARC (Assembly by Reduced Complexity)
### Install ARC
    cd ~/bin/
    wget https://github.com/ibest/ARC/tarball/master
    tar zxf master
    cd ~/bin/ibest-ARC-3831cb8
    python setup.py install
### Download BOWTIE 2
    cd ~/bin/
    wget http://downloads.sourceforge.net/project/bowtie-bio/bowtie2/2.2.9/bowtie2-2.2.9-linux-x86_64.zip?r=https%3A%2F%2Fsourceforge.net%2Fprojects%2Fbowtie-bio%2Ffiles%2Fbowtie2%2F2.2.9%2F&ts=1480614131&use_mirror=pilotfiber
    mv bowtie2-2.2.9-linux-x86_64.zip\?r\=https\:%2F%2Fsourceforge.net%2Fprojects%2Fbowtie-bio%2Ffiles%2Fbowtie2%2F2.2.9%2F bowtie2-2.2.9.zip
    unzip bowtie2-2.2.9.zip
    # add bowtie2 to path
    nano ~/.bash_profile
    # add the following line:
    PATH=$PATH:/home/jelber2/bin/bowtie2-2.2.9
    # exit and save with ctrl+X then Y
    # resource bash_profile
    source ~/.bash_profile
### Download SPAdes
    cd ~/bin/
    wget http://spades.bioinf.spbau.ru/release3.9.0/SPAdes-3.9.0-Linux.tar.gz
    tar xzf SPAdes-3.9.0-Linux.tar.gz
    mv SPAdes-3.9.0-Linux.tar.gz SPAdes-3.9.0-Linux/.
    # add SPAdes to path
    nano ~/.bash_profile
    # add the following line:
    PATH=$PATH:/home/jelber2/bin/SPAdes-3.9.0-Linux/bin
    # exit and save with ctrl+X then Y
    # resource bash_profile
    source ~/.bash_profile

