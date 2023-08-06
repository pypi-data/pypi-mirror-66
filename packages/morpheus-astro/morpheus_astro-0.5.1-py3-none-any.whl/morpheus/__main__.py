# MIT License
# Copyright 2019 Ryan Hausen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# ==============================================================================
"""Morpheus -- a package for making pixel level morphological classifications."""
import os
import sys
import argparse

from morpheus.classifier import Classifier


def _valid_file(value):
    if os.path.isfile(value) and value.endswith((".fits", ".FITS")):
        return value

    raise ValueError("File needs to be a fits file, ending with .fits or .FITS")


def _valid_dir(value):
    if os.path.isdir(value):
        return value

    raise ValueError("Value needs to be a directory.")


def _gpus(value):
    gpus = [int(v) for v in value.split(",")]

    gpu_err = "--gpus option requires more than one GPU ID. If you are trying "
    gpu_err += "to select a single gpu to use the CUDA_VISIBLE_DEVICES "
    gpu_err += "environment variable. For more information: "
    gpu_err += "https://devblogs.nvidia.com/cuda-pro-tip-control-gpu-visibility-cuda_visible_devices/"

    if len(gpus) < 2:
        raise ValueError(gpu_err)

    return gpus


def _parse_args(argv):
    """A place to set the arugments used in main."""
    parser = argparse.ArgumentParser(description=__doc__)

    # required arguments
    help_str = "The {} band FITS file location"
    parser.add_argument("h", type=_valid_file, help=help_str.format("H"))
    parser.add_argument("j", type=_valid_file, help=help_str.format("J"))
    parser.add_argument("v", type=_valid_file, help=help_str.format("V"))
    parser.add_argument("z", type=_valid_file, help=help_str.format("Z"))

    # optional arguments

    # action
    action_desc = "An additional optional flag to include additional information "
    action_desc += "to the morphological classifications. `catalog` saves a "
    action_desc += "morpholgical catalog as catalog.txt. `segmap` saves a "
    action_desc += "segmentation map as segmap.fits. `colorize` saves a colorized "
    action_desc += "version of the classification as colorized.png. "
    action_desc += "`all` saves catalog, segmap, and colorize."

    parser.add_argument(
        "--action",
        choices=["catalog", "segmap", "colorize", "all"],
        default="None",
        help=action_desc,
    )

    # parallel gpu
    gpus_desc = "Optional flag for classifying an image in parallel with multiple "
    gpus_desc += "GPUs. Should be comma seperated ints like: 1,3 or 0,1,2 no spaces."
    gpus_desc += "DO NOT use this flag for a single GPU classification. "
    gpus_desc += "Use the CUDA_VISIBLE_DEVICES enironment variable to select a "
    gpus_desc += "GPU for morpheus to use."

    parser.add_argument("--gpus", type=_gpus, help=gpus_desc)

    # parallel cpu
    parser.add_argument(
        "--cpus",
        type=int,
        help="Optional flag for classifying an image in parrallel with multiple cpus",
    )

    out_dir_desc = "The directory to save the output in."
    parser.add_argument(
        "--out_dir", type=_valid_dir, default=os.getcwd(), help=out_dir_desc
    )

    batch_size_desc = "The batch size for Moprheus to use when classifying the image."
    parser.add_argument("--batch_size", type=int, default=1000, help=batch_size_desc)

    # evaluate args
    args = parser.parse_args(argv)

    print(args.cpus, args.gpus)
    if args.cpus and args.gpus:
        raise ValueError("Both --cpus and --gpus were indicated. Choose only one.")

    return args


def main():
    args = _parse_args(sys.argv[1:])

    if args.action == "None":
        Classifier.classify(
            h=args.h,
            j=args.j,
            v=args.v,
            z=args.z,
            batch_size=args.batch_size,
            out_dir=args.out_dir,
            gpus=args.gpus,
            cpus=args.cpus,
        )
    elif args.action == "catalog":
        classified = Classifier.classify(
            h=args.h,
            j=args.j,
            v=args.v,
            z=args.z,
            batch_size=args.batch_size,
            out_dir=args.out_dir,
            gpus=args.gpus,
            cpus=args.cpus,
        )

        segmap = Classifier.segmap_from_classified(
            classified, args.h, out_dir=args.out_dir
        )

        Classifier.catalog_from_classified(
            classified,
            args.h,
            segmap,
            out_file=os.path.join(args.out_dir, "colorized.png"),
        )
    elif args.action == "segmap":
        classified = Classifier.classify(
            h=args.h,
            j=args.j,
            v=args.v,
            z=args.z,
            batch_size=args.batch_size,
            out_dir=args.out_dir,
            gpus=args.gpus,
            cpus=args.cpus,
        )

        Classifier.segmap_from_classified(classified, args.h, out_dir=args.out_dir)
    elif args.action == "colorize":
        classified = Classifier.classify(
            h=args.h,
            j=args.j,
            v=args.v,
            z=args.z,
            batch_size=args.batch_size,
            out_dir=args.out_dir,
            gpus=args.gpus,
            cpus=args.cpus,
        )

        Classifier.colorize_classified(classified, out_dir=args.out_dir)
    elif args.action == "all":
        classified = Classifier.classify(
            h=args.h,
            j=args.j,
            v=args.v,
            z=args.z,
            batch_size=args.batch_size,
            out_dir=args.out_dir,
            gpus=args.gpus,
            cpus=args.cpus,
        )

        segmap = Classifier.segmap_from_classified(
            classified, args.h, out_dir=args.out_dir
        )

        Classifier.catalog_from_classified(
            classified,
            args.h,
            segmap,
            out_file=os.path.join(args.out_dir, "colorized.png"),
        )

        Classifier.colorize_classified(classified, out_dir=args.out_dir)


if __name__ == "__main__":
    main()
