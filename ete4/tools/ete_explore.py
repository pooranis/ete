# #START_LICENSE###########################################################
#
#
# This file is part of the Environment for Tree Exploration program
# (ETE).  http://etetoolkit.org
#
# ETE is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ETE is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
# License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ETE.  If not, see <http://www.gnu.org/licenses/>.
#
#
#                     ABOUT THE ETE PACKAGE
#                     =====================
#
# ETE is distributed under the GPL copyleft license (2008-2015).
#
# If you make use of ETE in published work, please cite:
#
# Jaime Huerta-Cepas, Joaquin Dopazo and Toni Gabaldon.
# ETE: a python Environment for Tree Exploration. Jaime BMC
# Bioinformatics 2010,:24doi:10.1186/1471-2105-11-24
#
# Note that extra references to the specific methods implemented in
# the toolkit may be available in the documentation.
#
# More info at http://etetoolkit.org. Contact: huerta@embl.de
#
#
# #END_LICENSE#############################################################
from __future__ import absolute_import
from __future__ import print_function

import random
import re
import colorsys
from collections import defaultdict

from .common import log, POSNAMES, node_matcher, src_tree_iterator
# from .. import (Tree, PhyloTree, TextFace, RectFace, faces, TreeStyle, CircleFace, AttrFace,
#                 add_face_to_node, random_color)
from .. import PhyloTree
from ..smartview import TreeStyle
from ..smartview.gui.server import run_smartview
from ..smartview.renderer.layouts import (
                                            context_layouts,
                                            evol_events_layouts,
                                            ncbi_taxonomy_layouts,
                                            phylocloud_egg5_layouts,
                                            seq_layouts,
                                        )

import csv

DESC = "Launches an instance of the ETE smartview tree explorer server."

def populate_args(explore_args_p):
    explore_args_p.add_argument("--face", action="append",
                             help="adds a face to the selected nodes. In example --face 'value:@dist, pos:b-top, color:red, size:10, if:@dist>0.9' ")
    explore_args_p.add_argument("--metadata", action="append",
                             help="add the annotations metadata as tsv file")
    explore_args_p.add_argument("--alignment", action="append",
                             help="add the alignment as fasta file")
    explore_args_p.add_argument("--outfile", action="append",
                             help="output annotated tree nw file")
    # explore_args_p.add_argument("--image", action="append",
    #                          help="Render tree image instead of showing it. A filename should be provided. PDF, SVG and PNG file extensions are supported (i.e. - tree.svg)")
    return

def parse_metadata(metadata):
    metatable = []
    tsv_file = open(metadata)
    read_tsv = csv.DictReader(tsv_file, delimiter="\t")

    for row in read_tsv:
        metatable.append(row)
    tsv_file.close()

    return metatable, read_tsv.fieldnames

def parse_fasta(fastafile):
    fasta_dict = {}
    with open(fastafile,'r') as f:
        head = ''
        seq = ''
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if seq != '':
                    fasta_dict[head] = seq
                    seq = ''
                    head = line[1:]
                else:
                    head = line[1:]
            else:
                seq += line
    fasta_dict[head] = seq

    return fasta_dict

def add_annotations(t, metadata):
    # add props to leaf
    annotations, columns = parse_metadata(metadata)

    #['#query', 'seed_ortholog', 'evalue', 'score', 'eggNOG_OGs', 'max_annot_lvl', 'COG_category', 'Description', \
    # 'Preferred_name', 'GOs', 'EC', 'KEGG_ko', 'KEGG_Pathway', 'KEGG_Module', 'KEGG_Reaction', 'KEGG_rclass', \
    # 'BRITE', 'KEGG_TC', 'CAZy', 'BiGG_Reaction', 'PFAMs']
    for annotation in annotations:
        gene_name = next(iter(annotation.items()))[1] #gene name must be on first column
        try:
            target_node = t.search_nodes(name=gene_name)[0]
            for _ in range(1, len(columns)):
                if columns[_] == 'seed_ortholog': # only for emapper annotations
                    taxid, gene = annotation[columns[_]].split('.', 1)
                    target_node.add_prop('taxid', taxid)
                    target_node.add_prop('gene', gene)
                target_node.add_prop(columns[_], annotation[columns[_]])
        except:
            pass


def run(args):
    
    # VISUALIZATION
    # Basic tree style
    ts = TreeStyle()
    ts.show_leaf_name = True
    
    try:
        tfile = next(src_tree_iterator(args))
    except StopIteration:
        run_smartview()
    else:
        t = PhyloTree(tfile, format=args.src_newick_format)
        
        if args.metadata:
            metadata = args.metadata[0]
            add_annotations(t, metadata)
            t.annotate_ncbi_taxa(taxid_attr='taxid')
        if args.alignment:
            fastafile = args.alignment[0]
            fasta_dict = parse_fasta(fastafile)
            for leaf in t.iter_leaves():
                leaf.add_prop("seq", fasta_dict.get(leaf.name))
            t.explore(tree_name=tfile, layouts=[seq_layouts.LayoutAlignment()])
        
        elif args.outfile:
            filename = args.outfile[0]
            t.write(outfile=filename, properties=[])
        else:
            t.explore(tree_name=tfile)
        


 
        
