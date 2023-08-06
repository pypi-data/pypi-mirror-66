# -*- coding: utf-8 -*-
"""
Automated QC classifier command line interface

@author: C Heiser
"""
import os, errno, argparse
import scanpy as sc
import matplotlib.pyplot as plt

from .api import dropkick, recipe_dropkick, coef_plot, score_plot
from .qc import summary_plot


def check_dir_exists(path):
    """
    Checks if directory already exists or not and creates it if it doesn't
    """
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def main():
    parser = argparse.ArgumentParser(prog="dropkick")
    parser.add_argument(
        "counts",
        type=str,
        help="Input (cell x gene) counts matrix as .h5ad or tab delimited text file",
    )
    parser.add_argument(
        "-m",
        "--metrics",
        type=str,
        help="Heuristics for thresholding. Default ['arcsinh_n_genes_by_counts','pct_counts_ambient']",
        nargs="+",
        default=["arcsinh_n_genes_by_counts", "pct_counts_ambient"],
    )
    parser.add_argument(
        "--thresh-methods",
        type=str,
        help="Methods used for automatic thresholding on heuristics. Default ['multiotsu','otsu']",
        nargs="+",
        default=["multiotsu", "otsu"],
    )
    parser.add_argument(
        "--directions",
        type=str,
        help="Direction of thresholding for each heuristic. Default ['above','below']",
        nargs="+",
        default=["above", "below"],
    )
    parser.add_argument(
        "--n-ambient",
        type=int,
        help="Number of top genes by dropout rate to use for ambient profile. Default 10",
        default=10,
    )
    parser.add_argument(
        "--n-hvgs",
        type=int,
        help="Number of highly variable genes for training model. Default 2000",
        default=2000,
    )
    parser.add_argument(
        "--min-genes",
        type=int,
        help="Minimum number of genes detected to keep cell. Default 50",
        default=50,
    )
    parser.add_argument(
        "--seed", type=int, help="Random state for cross validation", default=18,
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        help="Output directory. Output will be placed in [output-dir]/[name]_dropkick.h5ad. Default './'",
        nargs="?",
        default=".",
    )
    parser.add_argument(
        "--alphas",
        type=float,
        help="Ratios between l1 and l2 regularization for regression model. Default [0.1]",
        nargs="*",
        default=[0.1],
    )
    parser.add_argument(
        "--n-iter",
        type=int,
        help="Maximum number of iterations for optimization. Default 1000",
        default=1000,
    )
    parser.add_argument(
        "--n-jobs",
        type=int,
        help="Maximum number of threads for cross validation. Default -1",
        default=-1,
    )
    parser.add_argument(
        "--qc",
        help="Perform analysis of ambient expression content and overall QC.",
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Verbosity of glmnet module. Default False",
        action="store_true",
    )

    args = parser.parse_args()

    # read in counts data
    print("\nReading in unfiltered counts from {}".format(args.counts), end="")
    adata = sc.read(args.counts)
    print(" - {} barcodes and {} genes".format(adata.shape[0], adata.shape[1]))

    # check that output directory exists, create it if needed.
    check_dir_exists(args.output_dir)
    # get basename of file for writing outputs
    name = os.path.splitext(os.path.basename(args.counts))[0]

    # if --qc flag, perform ambient analysis and QC
    if args.qc:
        # preprocess and calculate metrics
        adata = recipe_dropkick(
            adata,
            filter=True,
            min_genes=args.min_genes,
            n_hvgs=None,
            X_final="raw_counts",
            n_ambient=args.n_ambient,
            verbose=args.verbose,
        )
        # plot total counts distribution, gene dropout rates, and highest expressed genes
        print("Saving QC summary plot to {}/{}_qc.png".format(args.output_dir, name))
        _ = summary_plot(adata, show=False)
        plt.savefig("{}/{}_qc.png".format(args.output_dir, name))

    # otherwise, run main dropkick module
    else:
        _ = dropkick(
            adata,
            min_genes=args.min_genes,
            n_ambient=args.n_ambient,
            n_hvgs=args.n_hvgs,
            metrics=args.metrics,
            thresh_methods=args.thresh_methods,
            directions=args.directions,
            alphas=args.alphas,
            max_iter=args.n_iter,
            n_jobs=args.n_jobs,
            seed=args.seed,
            verbose=args.verbose,
        )
        # save new labels in .h5ad
        print(
            "Writing updated counts to {}/{}_dropkick.h5ad".format(
                args.output_dir, name
            )
        )
        adata.write(
            "{}/{}_dropkick.h5ad".format(args.output_dir, name), compression="gzip",
        )
        # generate plot of dropkick coefficient values and CV scores vs tested lambda_path
        print("Saving coefficient plot to {}/{}_coef.png".format(args.output_dir, name))
        _ = coef_plot(adata, show=False)
        plt.savefig("{}/{}_coef.png".format(args.output_dir, name))
        # generate plot of chosen training thresholds on heuristics
        print("Saving score plot to {}/{}_score.png".format(args.output_dir, name))
        adata = recipe_dropkick(
            adata, filter=True, min_genes=args.min_genes, n_hvgs=None, verbose=False
        )
        _ = score_plot(
            adata, ["arcsinh_n_genes_by_counts", "pct_counts_ambient"], show=False
        )
        plt.savefig("{}/{}_score.png".format(args.output_dir, name))
