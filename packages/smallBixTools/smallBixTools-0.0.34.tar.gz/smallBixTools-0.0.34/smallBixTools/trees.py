import tempfile
from shutil import copyfile
import subprocess
import os
import sys
import argparse
import random
from ete3 import Tree, TreeStyle, NodeStyle, faces, AttrFace, CircleFace
import smallBixTools as st
from haplotype_aligned_file import haplo_with_freq_aligned_file
from math import log

def layout(node):
    """

    :param node:
    :return:
    """
    if node.is_leaf():
        # Add node name to laef nodes
        N = AttrFace("name", fsize=14, fgcolor="black")
        faces.add_face_to_node(N, node, 0)
    if "weight" in node.features:
        # Creates a sphere face whose size is proportional to node's
        # feature "weight"
        C = CircleFace(radius=node.weight, color="RoyalBlue", style="sphere")
        # Let's make the sphere transparent
        C.opacity = 0.3
        # And place as a float face over the tree
        faces.add_face_to_node(C, node, 0, position="float")


def get_nonhaplo_tree(infile, leaf_colours_dict):
    """

    :param infile:
    :param leaf_colours_dict:
    :return:
    """
    t = Tree(infile)
    for n in t.traverse():
        if n.name != '':
            nstyle = NodeStyle()
            nstyle["fgcolor"] = leaf_colours_dict[n.name]
            n.set_style(nstyle)
    ts = TreeStyle()
    # Set our custom layout function
    ts.layout_fn = layout

    # Draw a tree
    ts.mode = "r"

    # We will add node names manually
    ts.show_leaf_name = False
    # Show branch data
    ts.show_branch_length = True
    ts.show_branch_support = True

    return t, ts


def get_haplo_tree(infile, leaf_colours_dict, apply_log):
    """

    :param infile:
    :param leaf_colours_dict:
    :param apply_log:
    :return:
    """
    t = Tree(infile)
    for n in t.traverse():
        if n.name != '':
            this_freq = float(n.name.split("_")[-1])
            nstyle = NodeStyle()
            nstyle["fgcolor"] = leaf_colours_dict[n.name]
            if apply_log:
                node_size = 10 * log(1000 * this_freq)
            else:
                node_size = 100*this_freq
            nstyle["size"] = node_size
            n.set_style(nstyle)
    ts = TreeStyle()
    # Set our custom layout function
    ts.layout_fn = layout

    # Draw a tree
    ts.mode = "r"

    # We will add node names manually
    ts.show_leaf_name = False
    # Show branch data
    ts.show_branch_length = True
    ts.show_branch_support = True

    return t, ts


def confirm_newick_has_frequencies(inNewick):
    """
    Takes a filepath to a file containing a newick format tree with frequency information in the tip labels.
    This function confirms that this is readable, and appears to have frequency information in the tip labels.
    The arg can be None - in which case a False is returned.
    :param inNewick: filepath to a file containing a newick format tree with frequency information in the tip labels
                     indicated as the last field split on underscores.
    :return: True or False (Python bool).
    """
    print("Confirming that the supplied newick format file has frequencies on in its leaves.\nWork in progress")

    return False


def confirm_not_zero_file_size(fn):
    """
    Checks if the file is zero sized on disc. Returns True if it is, False otherwise.
    :param fn: The filename (full path required) to check.
    :return: True if file is non-zero sized. False if file doesn't exist, or is zero sized.
    """
    if os.path.exists(fn):
        print("file exists")
        if os.path.getsize(fn) > 0:
            print("file is larger than zero")
            return True
        else:
            print("file is zero sized")
            return False
    else:
        print("file does not exist")
        return False


def convert_vsearch_size_to_freq(fastafn):
    """
    Takes a fasta file which has been clustered with vsearch, and has sequence ids like:
    H50306877_1100_011WPI_GAG_2_NN_AAACACCTAG_41_NGS_treatment_NGS;size=416
    specifically with the trailing ";size=X"
    And converts this to a frequency
    :param fastafn:
    :return: Returns True is successful, returns False if something went wrong.
    """
    dct = st.fasta_to_dct(fastafn)
    print("Dct has {} keys.".format(len(dct)))
    total = 0
    try:
        for seqid in dct.keys():
            size_info = seqid.split(";")[1]
            size_strng = size_info.split("=")[1]
            size_int = int(size_strng)
            total += size_int
        new_dct = {}
        for seqid, seq in dct.items():
            size_info = seqid.split(";")[1]
            size_strng = size_info.split("=")[1]
            size_int = int(size_strng)
            new_seqid = seqid.split(";")[0] + "_" + str(round((size_int/total), 4))
            new_dct[new_seqid] = seq
        st.dct_to_fasta(new_dct, fastafn)
    except Exception as e:
        print(e)
        return False
    return True


def cluster_with_vsearch(infasta, prcnt_id):
    """
    Runs usearch on the given fasta file.
    Writes results to the same directory as the input - with "_clustID{}" appended to the filename.

    :param infasta: infile to cluster
    :param prcnt_id: percent id to cluster at
    :return: the output clustered filename if successful. None if something broke
    """

    defult_tmp_dir = tempfile._get_default_tempdir()
    temp_name = next(tempfile._get_candidate_names())
    tmpfn = os.path.join(defult_tmp_dir, temp_name)
    copyfile(infasta, tmpfn)
    if prcnt_id > 1:
        print("Cluster threshold must be between 0 and 1.")
        sys.exit()

    base_path = os.path.split(infasta)[0]
    filenamenoext = os.path.splitext(os.path.split(infasta)[1])[0]
    outfn = os.path.join(base_path, filenamenoext+"_clust_{}.fasta".format(prcnt_id))

    cmd = 'sed -i "s/-//g" {}'.format(tmpfn)
    try:
        print("Going to call cmd:\n"+cmd)
        subprocess.call(cmd, shell=True)
        if not confirm_not_zero_file_size(tmpfn):
            raise OSError
    except Exception as e:
        print(e)
        print("Something went wrong while trying to cluster with vsearch [1]")
        return None

    cmd = "vsearch --sizeout --cluster_size {} --id {} --centroids {}".format(tmpfn, prcnt_id, outfn)
    try:
        print("Going to call cmd:\n"+cmd)
        subprocess.call(cmd, shell=True)
        if not confirm_not_zero_file_size(outfn):
            raise OSError
        os.remove(tmpfn)
    except Exception as e:
        print(e)
        print("Something went wrong while trying to cluster with vsearch [2]")
        return None
    #convert_vsearch_size_to_freq(outfn)
    return outfn


def align_with_mafft(file_to_align):
    """
    Runs mafft on the given fasta format file. Returns the filename produced.
    :param clustered_fn: file to align.
    :return: filename of aligned file - if its created. None if something fails.
    """
    base_path = os.path.split(file_to_align)[0]
    filenamenoext = os.path.splitext(os.path.split(file_to_align)[1])[0]
    outfn = os.path.join(base_path, filenamenoext+"_aligned.fasta")

    cmd = "mafft {} > {}".format(file_to_align, outfn)
    try:
        print("Going to call cmd:\n" + cmd)
        subprocess.call(cmd, shell=True)
    except Exception as e:
        print(e)
        print("Something went wrong while running mafft to make an alignment")
        return None
    return outfn


def estimate_tree(alignment_fn):
    """
    Estimates a tree using fasttree
    :param alignment_fn: The aligned fasta format file to estimate a tree from.
    :return: The estimated tree filename if its created. Else False
    """
    base_path = os.path.split(alignment_fn)[0]
    filenamenoext = os.path.splitext(os.path.split(alignment_fn)[1])[0]
    outfn = os.path.join(base_path, filenamenoext+"_TREE.nwk")

    cmd = "fasttree -nt -gtr < {} > {}".format(alignment_fn, outfn)
    try:
        print("Going to call cmd:\n" + cmd)
        subprocess.call(cmd, shell=True)
    except Exception as e:
        print(e)
        print("Something went wrong calling fasttree.")
        return False
    return outfn


def collect_into_tmp(into_this_fn, from_fn):
    """

    :param into_this_fn:
    :param from_fn:
    :return:
    """
    with open(into_this_fn, "a") as fw:
        with open(from_fn, "r") as fh:
            file_content = fh.read()
        fw.write(file_content)
    return True


def populate_colour_dct(fasta_fn, leaf_dict, colours_list, colour_index):
    """
    reads the fasta file, adding to leaf_dict for each fasta seqid, the colour from colours_list, based on the index
    specified as colour_index
    :param clustered_fn: fasta to get seqids from
    :param leaf_dict: the dictionary to populate with seqids : colour
    :param colours_list: the lookup list of colours
    :param colour_index: the index to use to get a colour from the colours_list
    :return: no return. It populates the dictionary.
    """
    dct = st.fasta_to_dct(fasta_fn)
    for seqid in list(dct.keys()):
        leaf_dict[seqid] = colours_list[colour_index % len(colours_list)]


def apply_threshold(threshold, in_fn, out_fn):
    """

    :param threshold:
    :param in_fn:
    :param out_fn:
    :return:
    """
    dct = st.fasta_to_dct(in_fn)
    out_dct = {}
    print("input alignment has {} seqs.".format(len(dct)))
    for seqid, seq in dct.items():
        this_seqid_freq = float(seqid.split("_")[-1])
        if this_seqid_freq > threshold:
            out_dct[seqid] = seq
    st.dct_to_fasta(out_dct, out_fn)
    print("after applying threshold filter, output alignemnt has {} seqs".format(len(out_dct)))


def apply_topX(topX, in_fn, out_fn):
    """

    :param topX:
    :param in_fn:
    :param out_fn:
    :return:
    """
    dct = st.fasta_to_dct(in_fn)
    out_dct = {}
    print("Applying topX thresholding to input file: {}, with {} sequences.".format(in_fn, len(dct)))

    list_of_freqs = []
    list_of_seqids = []
    for seqid, seq in dct.items():
        this_seqid_freq = float(seqid.split("_")[-1])
        list_of_freqs.append(this_seqid_freq)
        list_of_seqids.append(seqid)
    sorted_seqid_list = [x for _, x in sorted(zip(list_of_freqs, list_of_seqids), reverse=True)]
    top_x_seqids = sorted_seqid_list[:topX]
    for kept_seqid in top_x_seqids:
        out_dct[kept_seqid] = dct[kept_seqid]
    st.dct_to_fasta(out_dct, out_fn)
    print("After applying threshold filter, output alignment has {} sequences".format(len(out_dct)))


def main(inFastas, inNewick, is_aliged, clusterThreshold, draw_haplo, exclude_threshold, apply_log, topX):
    print("Making a tree from the fasta files: {}".format(inFastas))
    print("A newick tree has {}been provided.".format("" if inNewick else "not "))
    print("Input fasta file is {}aligned".format("" if is_aliged else "not "))
    print("Input fasta file must {}be clustered first.".format("" if clusterThreshold else "not "))
    print("A bubble haplotype tree is {} to be drawn.".format("" if draw_haplo else "not "))
    print("Any taxa with a frequency below {} will not be drawn.".format(exclude_threshold))
    print("We will scale the bubble sizes with a log scale.")
    print("We are {}going to include the top X variants.".format("" if topX else "not "))

    colours_list = ["red", "blue"] #, "green", "orange"]
    colour_index = 0
    leaf_colours = {} # a dictionary which will hold leaf names and their colour assignments.

    basePath = os.path.split(inFastas[0].name)[0]
    firstFileNameNoExt = os.path.splitext(os.path.split(inFastas[0].name)[1])[0]
    defaultTmpDir = tempfile._get_default_tempdir()
    must_apply_thresholding = True

    # We are either going to cluster, or haplotype - never both. Both reduce total sequences, and give frequency info
    if clusterThreshold:
        # we have to cluster, at the given threshold. For now, use vsearch
        tmpFnToCollectInto = os.path.join(basePath, "all_clustered_{}.fasta".format(clusterThreshold))
        if os.path.exists(tmpFnToCollectInto):
            os.remove(tmpFnToCollectInto)
        for fn in inFastas:
            filenamenoext = os.path.splitext(os.path.split(fn.name)[1])[0]
            clustered_fn = cluster_with_vsearch(fn.name, clusterThreshold)
            convert_vsearch_size_to_freq(clustered_fn)
            topX_fn = os.path.join(basePath, filenamenoext + "_topX.fasta")
            if topX:
                apply_topX(topX, clustered_fn, topX_fn)
            else:
                topX_fn = clustered_fn
            collect_into_tmp(tmpFnToCollectInto, topX_fn)
            populate_colour_dct(clustered_fn, leaf_colours, colours_list, colour_index)
            colour_index += 1
        filename_to_align = tmpFnToCollectInto

    # The user wants to draw a haplotyped tree. So, we have to perform haplotyping to get the frequencies.
    elif draw_haplo:
        tmpFnToCollectInto = os.path.join(basePath, "all_haplotyped.fasta")
        if os.path.exists(tmpFnToCollectInto):
            os.remove(tmpFnToCollectInto)
        for fn in inFastas:
            filenamenoext = os.path.splitext(os.path.split(fn.name)[1])[0]
            haploFastaFN = os.path.join(basePath, filenamenoext + "_haploWithFreq.fasta")
            haplo_with_freq_aligned_file(infile=fn.name, outfile=haploFastaFN, dp=4)
            topX_fn = os.path.join(basePath, filenamenoext + "_topX.fasta")
            if topX:
                apply_topX(topX, haploFastaFN, topX_fn)
            else:
                topX_fn = haploFastaFN
            collect_into_tmp(tmpFnToCollectInto, topX_fn)
            populate_colour_dct(topX_fn, leaf_colours, colours_list, colour_index)
            colour_index += 1
        filename_to_align = tmpFnToCollectInto

    else:
        # no clustering, no haplotyping - just collect all the files into one.
        tmpFnToCollectInto = os.path.join(basePath, "all_collected.fasta")
        for fn in inFastas:
            collect_into_tmp(tmpFnToCollectInto, fn.name)
            populate_colour_dct(fn.name, leaf_colours, colours_list, colour_index)
            colour_index += 1
        filename_to_align = tmpFnToCollectInto

        # Do we want to exclude taxa below a given frequency? Here, no - because there is no clustering or haplotying
        # So we might not know a frequency... User wants to show everything on the tree.
        must_apply_thresholding = False

    # Apply threshold filter if required.
    input_to_alignment = os.path.join(basePath, "inputToAlignment.fasta")
    if must_apply_thresholding:
        apply_threshold(exclude_threshold, filename_to_align, input_to_alignment)
    else:
        copyfile(filename_to_align, input_to_alignment)

    # Align - because clustering breaks alignment. Use mafft for now.
    if not is_aligned:
        print("Going to call align_with_mafft on clustered or haplotyped file: {}".format(input_to_alignment))
        aligned_fn = align_with_mafft(input_to_alignment)
    else:
        if clusterThreshold:
            print("Clustering was done, and you have specified that the file was aligned. Need to realign post "
                  "clustering")
            aligned_fn = align_with_mafft(input_to_alignment)
        else:
            print("No clustering was done. Possibly haplotyping was done. No alignment required. Just "
                  "collected all the sequences "
                  "from all the specified files for tree drawing.")
            aligned_fn = input_to_alignment


    # then estimate a tree, because any tree supplied will be for a fasta which then gets clustered.
    # TODO Need to fix this - we must be able to specify a tree file, and use it. This will always re-estimate a tree.
    newick_tree_fn = estimate_tree(aligned_fn)

    # then draw a tree.
    if draw_haplo or clusterThreshold:
        t, ts = get_haplo_tree(newick_tree_fn, leaf_colours, apply_log)
    else:
        t, ts = get_nonhaplo_tree(newick_tree_fn, leaf_colours)

    out_tree_fn = os.path.join(basePath, "bubble_tree.png")
    t.render(out_tree_fn, w=1000, dpi=600, tree_style=ts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Tree estimation and drawing methods. Can be called from cmd line '
                                                 'to estimate and plot a tree from a fasta file. Can supply own tree in'
                                                 ' newick format. Multiple fasta files can be provided. One after the '
                                                 'other. If multiple are provided, each will have its own frequency'
                                                 ' within just that file calculated - then all files joined together to'
                                                 ' make one tree, and bubbles coloured per input fasta file.')
    parser.add_argument('inFastas', type=argparse.FileType('r'), nargs='+', help='multiple fasta files can be specified')
    parser.add_argument('-it', '--inNewick', type=str, required=False,
                        help='If supplied, attempt to use the supplied tree in Newick format, rather than estimating '
                             'one using fasttree. NOTE: The tip labels must contain frequency data to draw frequency'
                             'trees.')
    parser.add_argument('-hap', '--haplo', action='store_const', const=True,
                        help='Specify this flag if you want to draw bubble frequency trees. If this is '
                             'not specified, non-bubble trees will be drawn.', required=False)
    parser.add_argument('-a', '--aligned', action='store_const', const=True,
                        help='Is the fasta aligned? Include this flag is the alignment is already aligned and '
                             'haplotyping will be done. If clustering is to be done, alignment will be required.'
                             'It is assumed that alignment will be done.', required=False)
    parser.add_argument('-ct', '--clusterThreshold', type=float, default=None,
                        help='Specify a value between 0 and 1.0 to cluster with vsearch first. This will also cause '
                             'alignment to procede, and a new tree to be estimated.', required=False)
    parser.add_argument('-lg', '--scale_with_log', action='store_const', const=True, default=False, required=False,
                        help='If there are very low frequency terminal nodes being plotted, we can apply a '
                             'log scaling to the node sizes - this will make the small nodes appear larger, and the '
                             'larger ones appear less large.')

    arg_group_et_topX = parser.add_mutually_exclusive_group()
    arg_group_et_topX.add_argument('-top', '--include_top_x', type=int, required=False,
                        help='If you want to only include the top X frequency variants from each input file, specify '
                             'that number here. This same number will be applied to all input fasta files.')
    arg_group_et_topX.add_argument('-et', '--exclude_threshold', type=float, required=False, default=0.0,
                        help='A threshold, below which, variants wont be included when drawing the tree. specified '
                             'as a decimal between 0.0 and 1.0. ')

    args = parser.parse_args()
    infiles = args.inFastas
    inNewick = args.inNewick
    is_aligned = args.aligned
    clusterThresh = args.clusterThreshold
    draw_haplo = args.haplo
    exclude_thresh = args.exclude_threshold
    scale_with_log = args.scale_with_log
    topX = args.include_top_x

    if draw_haplo:
        if clusterThresh:
            print("Cannot specify to do both clustering and haplotyping. Choose only one.\n     Now exiting")
            sys.exit()

    if is_aligned:
        if clusterThresh:
            r = input("Clustering will remove alignment. Alignment will be remade with mafft.\nHit Enter to confirm "
                      "this")

    confirm_newick_has_frequencies(inNewick)

    main(infiles, inNewick, is_aligned, clusterThresh, draw_haplo, exclude_thresh, scale_with_log, topX)
