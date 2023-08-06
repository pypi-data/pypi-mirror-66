
# DeepARG
A deep learning based approach to predict Antibiotic Resistance Genes (ARGs) from metagenomes. It provides two models,deepARG-SS and deepARG-LS.

## Web Service
We have released a web service to process raw sequences (paired end) using deepARG. You will get absolute and relative abundances of each submitted sample. You can find the website at http://bench.cs.vt.edu/deeparg

## Docker (recommended!)
DeepARG can be executed using a docker. It is higly recommended to use this setup because there is not need to make any additional configuration.

### Installation
Make sure Docker is installed and running. To install docker please see: https://www.docker.com/community-edition

### Usage:
To start using the docker deepARG image, first you need to setup the $DEEPARG_DATA global variable. Please point to this variable the path where your raw reads are placed. Then, run the following commands:

        DEEPARG_DATA=$PWD
        docker run --rm -it -v $DEEPARG_DATA:/data/  gaarangoa/deeparg:latest python /deeparg/deepARG.py -h

Note that the command -v $DEEPARG_DATA:/data/ transfers the content of $DEEPARG_DATA to the internal /data/ directory. The input/output files need to be referrenced by using the relative /data/ directory. For instance, FASTA reads would be placed under /data/*.fasta. The global $DEEPARG_DATA variable requires to point to the FULL PATH of your raw data. Othercase, it will not work.

### Example:
In this example, we will classify a set of ORFs from a set of assembled contigs. The fasta file contains gene sequences (nucleotides).
#### Download test fasta file:

    mkdir test
    cd test
    wget https://bitbucket.org/gusphdproj/deeparg-ss/raw/1c29d3594960a5f1b23898ad76164dc6393b818a/test/ORFs.fa
#### Setup relative directory and run deepARG

    DEEPARG_DATA=$PWD/
    docker run --rm -it -v $DEEPARG_DATA:/data/  gaarangoa/deeparg:latest \
        python /deeparg/deepARG.py \
        --align \
        --genes \
        --input /data/ORFs.fa \
        --output /data/ORFs \
        --type nucl

#### DeepARG output
DeepARG generates two files: *.ARG that contains the sequences with a probability >= --prob (0.8 default) and *.potential.ARG with sequences containing a probability < --prob (0.8 default). The *.potential.ARG file can still contain ARG-like sequences, howevere, it is necessary inspect its sequences.

The output format for both files consists of the following fields:

    * ARG_NAME
    * QUERY_START
    * QUERY_END
    * QUERY_ID
    * PREDICTED_ARG_CLASS
    * BEST_HIT_FROM_DATABASE
    * PREDICTION_PROBABILITY
    * ALIGNMENT_BESTHIT_IDENTITY (%)
    * ALIGNMENT_BESTHIT_LENGTH
    * ALIGNMENT_BESTHIT_BITSCORE
    * ALIGNMENT_BESTHIT_EVALUE
    * COUNTS

# Alternative Installation

<!-- docker run --rm -it -v $PWD:/src/ python:2.7 /bin/bash -->

If you cannot use docker, you can install it in your local (unix) machine, or you can create a virtual environment.
## Dependencies
DeepARG requires the next python modules (all can be installed via pip):

    1 Nolearn (0.6)
    2 lasagne (0.1) deep learning library.
    3 Sklearn (0.19.1) machine learning routines.
    4 Theano (0.8.2) for fast computation. For GPU usage (see theano documentation)
    5 tqdm for progress bar visualization
    6 diamond version 0.9.24

## Instalation
Clone this git repository:
    git clone https://bitbucket.org/gusphdproj/deeparg-ss

## Configuration

    Go to the directory where the program was saved and open the file options.py

    Replace path = '/home/gustavo1/tmp/deeparg-ss/'; with the current directory (deepARG path).

For instance, deepARG was cloned at /home/user/deeparg-ss/
The options.py file should looks like

    path = '/home/user/deeparg-ss/';

Finally allow diamond to be executed:

Go to ./bin under deeparg-ss and run:

    chmod +x diamond (only for LINUX)

If you are installing deepARG in a MacOs machine, please take a look at the DIAMOND instructions. Then, copy and paste the executable to the bin directory under deepARG https://github.com/bbuchfink/diamond

## Installation using virtualenv

(optional) if not pip is installed in yor machine:

    1. wget https://bootstrap.pypa.io/get-pip.py
    2. python get-pip.py

Create a virutal environment

    1. virtualenv env
    2. source env/bin/activate

Install packages required to run deepARG

    1. pip install -r https://raw.githubusercontent.com/dnouri/nolearn/0.6.0/requirements.txt
    2. pip install nolearn
    3. pip install tqdm

Deactivate the virtual environment:

    1. deactivate

To re-activate the virtual environment:

    source env/bin/activate

installation was tested under gcc v5.2.0 and pytnon v2.7.10

## Known instalation issues
In most of the cases, the instalation of nolearn is straightforward. However, in some cases incompatibilities with BLAS libraries can cause more than one headache. So, make sure you have the lasagne=0.2, scikit-learn=0.17 and the corresponding BLAS where numpy and scipy run without problem.
visit for details:
https://github.com/dnouri/nolearn/tree/0.6.0/requirements.txt


## Usage

Type: python deepARG.py -h

    DeepARG:
        https://bitbucket.org/gusphdproj/deeparg-ss

        A deep learning based approach for predicting Antibiotic Resistance Genes and annotation.
        You can use --predict if you already have a blast-like tabular output (outfmt6) from any
        other program (blast, userarch, vsearch, diamond, etc.). Here you can use the --reads options
        that will predict NGS reads or --genes that will take longer gene-like sequences (NOT ASSEMBLED CONTIGS).
        If you use the --align flag, the system will first perform blast over the input you provide
        (genes or reads) and continue with the predict stage. There are additional parameter such as idenity (60% default)
        or prediction probability to retrieve the most significant predictions (default --prob 0.8).

    USAGE:  python deepARG.py --predict --reads --input /Volumes/data/dev/deepARG/test/test.tsv --output /Volumes/data/dev/deepARG/test/test.out
            python deepARG.py --align --genes --type prot --input /Volumes/data/dev/deepARG/test/test.fasta --output /Volumes/data/dev/deepARG/test/test.out

    General options:
        --type          (nucl/prot) Molecule type of input data
        --iden          (50% default) minimum percentaje of identity to consider
        --prob          (0.8 default) Significance of the prediction, default 0.8
        --evalue        (1e-10 default) evalue of alignments (default 1e-10)
        --coverage      (0.8 default) minimum coverage of the alignment (alignment_length/reference_gene_length)
        --reads         short sequences version
        --genes         long sequences version
        --v1            Use this flag to activate deepARG version v1 [default: v2]

    Optional:
        --nk            (1000 default) maximum number of alignments reported for each query (diamond alignment)


    PREDICT ARG-like sequences using blast output file as input:
        deepARG --predict --input <inputfile> --output <outputfile>
            --input         blast tab delimited file.
            --output        output of annotated reads.

    ALIGN sequences to DEEP_ARGDB and PREDICT ARGs using fasta files as input:
        deepARG --align  --input <inputfile> --output <outputfile>
            --input         fasta file containing reads.
            --output        blast tab delimited alignment file.


### Usage examples:

Go to the deeparg-ss directory and run any of the following commands:

Input is a FASTA file:

    1) Annotate gene-like sequences when the input is a nucleotide FASTA file:
        python deepARG.py --align --type nucl --genes --input /path/file.fasta --out /path/to/out/file.out

    2) Annotate gene-like sequences when the input is an amino acid FASTA file:
        python deepARG.py --align --type prot --genes --input /path/file.fasta --out /path/to/out/file.out

    3) Annotate short sequence reads when the input is a nucleotide FASTA file:
        python deepARG.py --align --type nucl --reads --input /path/file.fasta --out /path/to/out/file.out

    3) Annotate short sequence reads when the input is a protein FASTA file (unusual case):
        python deepARG.py --align --type prot --reads --input /path/file.fasta --out /path/to/out/file.out

Input is a tabular BLAST-like file:

    4) Annotate gene-like sequences when the input is a nucleotide BLAST alignment file:
        python deepARG.py --predict --type nucl --genes --input /path/file.fasta --out /path/to/out/file.out

    5) Annotate gene-like sequences when the input is an amino acid BLAST alignment file:
        python deepARG.py --predict --type prot --genes --input /path/file.fasta --out /path/to/out/file.out

    6) Annotate short sequence reads when the input is a nucleotide BLAST alignment file:
        python deepARG.py --predict --type nucl --reads --input /path/file.fasta --out /path/to/out/file.out

    7) Annotate short sequence reads when the input is a protein BLAST alignment file (unusual case):
        python deepARG.py --predict --type prot --reads --input /path/file.fasta --out /path/to/out/file.out

# Train the DeepARG models
This section contains the instructions to re-train the deepARGs models. Useful if you want to try your own database and use the deep learning architecture provided in this repository.

### Input database format
Please make sure the database is an amino acid fasta file and the header is properly set to:

    >GENE_ID|FEATURES|DATABASE|ARG_TYPE|ARG_SUBTYPE

Where:

    * GENE_ID: unique identifier of the protein sequence
    * FEATURES: keyword [all genes contain this keyword]
    * DATABASE: Name of the database where the gene is coming from
    * ARG_TYPE: Class of antibiotic where the gene is coming from
    * ARG_SUBTYPE: Specific gene name (HUGO nomenclature)

For example:

    >B9J113|FEATURES|UNIPROT|beta_lactam|bla
    MKHKNQATHKEFSQLEKKFDARLGLYAIDTGTNQTIAYRPNERFAFASTYKALAAGVLLQ
    QNSTKKLDE
    >YP_001119417|FEATURES|ARDB|multidrug|AmrB
    MARFFDDGRMTDVQLGEYASANVVQALRRVDGVGRVQFWGAE

If you plan to train a different database (e.g., Metal Resistance Database). Fit the database metadata to the provided format.

Then, store the fasta file into the ./database/ directory as ./database/features.fasta

### Build the database index

First make sure ./bin/diamond has executable permission, if not, just type:

    chmod +x ./bin/diamond

DeepARG uses the bitscore as the similarity metric. Therefore, you need to index the database to the Diamond aligner format by typing:

    ./bin/diamond makedb --in ./database/features.fasta --db ./database/features

This step will create the file ./database/features.dmnd

### DeepARG-SS model
These are the steps required to train the deepARG-SS model:

#### Generate short sequence reads from database
To train the deepARG-SS model you need to build a dataset of reads. The generate_short_reads.py script build a fasta file of short reads (31 aa as default).

    python ./train/generate_short_reads.py ./database/features.fasta ./database/train_reads.fasta train_reads 31

For this step make sure you have installed the Bio Python module (http://biopython.org/). For categories that have less than 50 sequences, genes are oversampled. This step is useful to make the training set. If you are planing to test performance prediction, oversample should NOT be done for testing sequences. In that case, please use the script under ./train/generate_short_reads_no_oversample.py (same parameters)


#### Get similiarities (bit scores) between the reads and the reference database
This step is required to build the similarity matrix

    ./bin/diamond blastp --db ./database/features.dmnd --query ./database/train_reads.fasta --id 30 --evalue 1e-10 --sensitive -k 10000 -a ./database/train_reads
    ./bin/diamond view -a ./database/train_reads.daa -o ./database/train_reads.tsv

#### Train the DeepARG-SS model
This step will train the deep learning models using the aigned file from diamond.

    python ./argdb/train_arc.py

This process will take few hours depending of the available computing. It is recommended to train the deep learning models using the system's GPU. One alternative that will reduce the training time is to decrease the -k parameter in diamond and increase the --id value. However, this would affect the performance.

### DeepARG-LS model
These are the steps required to train the deepARG-LS model (long sequences):

#### Get similiarities (bit scores) between the reads and the reference database
This step is required to build the similarity matrix, but, fist need to format the fasta file for the genes.

    python ./train/generate_train_genes.py ./database/features.fasta ./database/train_genes.fasta train
    ./bin/diamond blastp --db ./database/features --query ./database/train_genes.fasta --id 30 --evalue 1e-10 --sensitive -k 10000 -a ./database/train_genes
    ./bin/diamond view -a ./database/train_genes.daa -o ./database/train_genes.tsv

#### Train the DeepARG-LS model
This step will train the deep learning models using the aigned file from diamond.

    python ./argdb/train_arc_genes.py


## License
deepARG is under the MIT licence. However, please take a look at te comercial restrictions of the databases used during the mining process (CARD, ARDB, and UniProt).

## About
If you use deepARG in published research, please cite:

Arango-Argoty GA, Garner E, Pruden A, Heath LS, Vikesland P, Zhang L. DeepARG: A deep learning approach for predicting antibiotic resistance genes from metagenomic data. Microbiome20186:23
https://doi.org/10.1186/s40168-018-0401-z.

## Database
Details about the database mining can be found at http://bench.cs.vt.edu/ftp/deeparg/scripts/ instructions are placed in the python notebook called main.ipynb

## Contact
If need any asistance please contact: gustavo1@vt.edu
