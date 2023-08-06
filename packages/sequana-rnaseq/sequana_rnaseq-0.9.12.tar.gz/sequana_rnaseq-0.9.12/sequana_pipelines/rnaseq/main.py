import sys
import os
import argparse
import shutil

from sequana.pipelines_common import *
from sequana.snaketools import Module
from sequana import logger
logger.level = "INFO"

col = Colors()

NAME = "rnaseq"
m = Module(NAME)
m.is_executable()


class Options(argparse.ArgumentParser):
    def __init__(self, prog=NAME):
        usage = col.purple(
            """This script prepares the sequana pipeline rnaseq layout to
            include the Snakemake pipeline and its configuration file ready to
            use.

            In practice, it copies the config file and the pipeline into a
            directory (rnaseq) together with an executable script

            ::

                sequana_pipelines_rnaseq --input-directory PATH_TO_DATA

            You must provide a path to a genome of reference (with its GFF file).

            We save the genomes in the genome directory where lots of genomes
            can be stored. So, you also need to provide the name of a genome.

            For instance, if you work on  Saccer3, type::

                sequana_pipelines_rnaseq --input-directory --genome-directory GENOMESPATH/Saccer3

            The pipeline will search for the files Saccer3.fa and Saccer3.gff in
            the directory GENOMESPATH/Saccer3.


        """
        )
        super(Options, self).__init__(usage=usage, prog=prog, description="",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        # add a new group of options to the parser
        so = SlurmOptions()
        so.add_options(self)

        # add a snakemake group of options to the parser
        so = SnakemakeOptions(working_directory=NAME)
        so.add_options(self)

        so = InputOptions()
        so.add_options(self)

        so = GeneralOptions()
        so.add_options(self)

        pipeline_group = self.add_argument_group("pipeline_general")
        pipeline_group.add_argument("--genome-directory", dest="genome_directory",
            default=".", required=True)
        pipeline_group.add_argument("--aligner", dest="aligner", required=True,
            choices=['bowtie2', 'bowtie1', 'star', "salmon"],
            help= "a mapper in bowtie, bowtie2, star")
        pipeline_group.add_argument("--do-indexing", dest="do_indexing",
            action="store_true", help="""If bowtie/star/salmon indexing file are
                not computed, you will need to compute them by setting
                this option """)
        pipeline_group.add_argument("--force-indexing", action="store_true",
            default=False,
            help="""If indexing files exists already, but you wish to
                create them again, use this option""")
        pipeline_group.add_argument("--rRNA-feature",
            default="rRNA",
            help="""Feature name corresponding to the rRNA to be identified for QCs""")

        # cutadapt related
        so = CutadaptOptions()
        so.add_options(self)

        # fastq_screen
        pipeline_group = self.add_argument_group("section_fastq_screen")
        pipeline_group.add_argument("--do-fastq-screen", action="store_true",
            default=False,
            help="run fastq_screen ")
        pipeline_group.add_argument("--fastq-screen-conf",
            default="fastq_screen.conf", type=str,
            help="""a valid fastqc_screen.conf file. See fastq_screen
documentation for details. In a nutsheel, add a line for each genome you want to
search for in your input data. Each line is 'DATABASE name path BOWTIE2'. The
path includes the path to the genome + its prefix name.  """)

        pipeline_group = self.add_argument_group("section_feature_counts")
        pipeline_group.add_argument("--feature-counts-strandness",
            default=None, 
            help="""0 for unstranded, 1 for stranded and 2 for reversely
stranded. If you do not know, let the pipeline guess for you.""")
        pipeline_group.add_argument("--feature-counts-options",
            default="-t gene -g ID",
            help="""options for feature counts. -t should be followed by a valid
feature type, -g by a valid attribute name. Do not use -s option, use the
--feature-counts-strandness parameter instead.""")

        pipeline_group = self.add_argument_group("pipeline_others")
        pipeline_group.add_argument('--do-igvtools', action="store_true")
        pipeline_group.add_argument('--do-bam-coverage', action="store_true")
        pipeline_group.add_argument('--do-mark-duplicates', action="store_true")

        pipeline_group = self.add_argument_group("pipeline_RNAseQC")
        pipeline_group.add_argument('--do-rnaseqc', action="store_true",
            help="do RNA-seq QC using RNAseQC v2")
        pipeline_group.add_argument('--rnaseqc-gtf-file',
            help="The GTF file to be used")

        # RNADIFF
        pipeline_group = self.add_argument_group("section_rnadiff")
        pipeline_group.add_argument('--rnadiff-mode', type=str,
            required=True,
            choices=["one_factor", "GLM"],
            help="""Fix the type of analyis (one_factor or GLM)""")

def main(args=None):

    if args is None:
        args = sys.argv

    if "--version" in sys.argv:
        print_version(NAME)
        sys.exit(0)

    options = Options(NAME).parse_args(args[1:])

    manager = PipelineManager(options, NAME)

    # create the beginning of the command and the working directory
    manager.setup()

    # fill the config file with input parameters
    cfg = manager.config.config

    # --------------------------------------------------------- general
    cfg.general.genome_directory = os.path.abspath(options.genome_directory)
    cfg.general.aligner = options.aligner
    cfg.general.indexing = options.do_indexing
    cfg.general.force_indexing = options.force_indexing
    cfg.general.rRNA_feature = options.rRNA_feature

    # --------------------------------------------------------- cutadapt
    cfg.cutadapt.do = not options.skip_cutadapt
    manager.update_config(cfg, options, "cutadapt")


    # ----------------------------------------------------  others
    cfg.input_directory = os.path.abspath(options.input_directory)
    cfg.input_pattern = options.input_pattern
    cfg.input_readtag = options.input_readtag

    # ----------------------------------------------------- feature counts
    cfg.feature_counts.options = options.feature_counts_options
    cfg.feature_counts.strandness = options.feature_counts_strandness

    # ------------------------------------------------------ optional
    cfg.igvtools.do = options.do_igvtools
    cfg.coverage.do = options.do_bam_coverage
    cfg.mark_duplicates.do = options.do_mark_duplicates

    # -------------------------------------------------------- RNAseqQC
    cfg.rnaseqc2.do = options.do_rnaseqc
    cfg.rnaseqc2.gtf_file = options.rnaseqc_gtf_file

    # -------------------------------------------------------- RNAdiff
    cfg.rnadiff.mode = options.rnadiff_mode

    # ----------------------------------------------------- fastq_screen conf
    if options.do_fastq_screen:
        cfg.fastq_screen.do = True
        manager.exists(options.fastq_screen_conf)
        cfg.fastq_screen_conf = os.path.abspath(options.fastq_screen_conf)
        # copy the fastq_screen.conf input or default file
        shutil.copy(options.fastq_screen_conf, manager.workdir)
    else:
        cfg.fastq_screen.do = False
        # copy the default fastq_screen conf file
        import sequana_pipelines.rnaseq
        shutil.copy(os.path.join(sequana_pipelines.rnaseq.__path__[0] ,
            "fastq_screen.conf"), manager.workdir)


    # SANITY CHECKS
    # -------------------------------------- do we find rRNA feature in the GFF ?
    logger.info("checking your input GFF file and rRNA feature if provided")
    from sequana.gff3 import GFF3
    genome_directory = os.path.abspath(cfg["general"]["genome_directory"])
    genome_name = genome_directory.rsplit("/", 1)[1]
    prefix_name = genome_directory + "/" + genome_name
    gff_file = prefix_name + ".gff"
    gff = GFF3(gff_file)
    valid_types = gff.get_types()

    if cfg['general']["rRNA_feature"] and \
        cfg['general']["rRNA_feature"] not in valid_types:

        logger.error("rRNA feature not found in the input GFF ({})".format(gff_file) +
            " This is probably an error. Please check the GFF content and /or"
            " change the feature name with --rRNA-feature based on the content"
            " of your GFF. Valid features are: {}".format(valid_types))
        sys.exit()

    valid_types = gff.get_types()
    fc_options = cfg["feature_counts"]["options"]
    index = fc_options.split().index('-t')
    fc_type = fc_options.split()[index+1]


    logger.info("checking your input GFF file and feature counts options")
    if fc_type not in valid_types:
        logger.error("Invalid type ({}) in feature_count section of config.yaml (options {}). Valid types found in your GFF file are: {}".format(fc_type, fc_options, valid_types))

        sys.exit()


    # finalise the command and save it; copy the snakemake. update the config
    # file and save it.
    manager.teardown()

if __name__ == "__main__":
    main()
