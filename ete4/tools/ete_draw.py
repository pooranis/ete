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

from .common import log, POSNAMES, node_matcher, src_tree_iterator
from .. import PhyloTree
from ..smartview import TreeStyle

from selenium import webdriver
from selenium.common import exceptions 
from selenium.webdriver.common.action_chains import ActionChains

import time
import csv
import subprocess
import requests
import os

url = "http://127.0.0.1:5000/"

DESC = "Launches an instance of the ETE smartview tree explorer server."
TOOLSPATH = os.path.realpath(os.path.split(os.path.realpath(__file__))[0])
DRIVERPATH = os.path.join(TOOLSPATH, "external_lib/geckodriver")
CURRENTPATH = os.getcwd()

def populate_args(explore_args_p):
    explore_args_p.add_argument("--face", action="append",
                             help="adds a face to the selected nodes. In example --face 'value:@dist, pos:b-top, color:red, size:10, if:@dist>0.9' ")
    explore_args_p.add_argument("--metadata", action="append",
                             help="add the annotations metadata as tsv file")
    explore_args_p.add_argument("--alignment", action="append",
                             help="add the alignment as fasta file")
    explore_args_p.add_argument("--outdir", action="append",
                             help="output annotated tree nw file")
    explore_args_p.add_argument("--image", action="append",
                             help="Render tree image instead of showing it. A filename should be provided. PDF, SVG and PNG file extensions are supported (i.e. - tree.svg)")
    return


# def start_flask():
#     subprocess.Popen(['nohup', 'ete4', 'explore', '-t', '/home/deng/Projects/ete4/hackathon/metadata_annotation/trees/phylotree.nw'],
#                 #  stdout=open('/dev/null', 'w'),
#                 #  stderr=open('logfile.log', 'a'),
#                 #  preexec_fn=os.setpgrp
#                  )
#     return 

def end_flask():
    requests.get('http://127.0.0.1:5000/shutdown')

def browser_driver(url, executable_path=DRIVERPATH, outdir=CURRENTPATH):
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.dir", outdir)

    browser_driver = webdriver.Firefox(
            executable_path=DRIVERPATH,  # 这里必须要是绝对路径
            # windows是.exe文件 xxx/xxx/geckodriver.exe, xxx/xxx/firefox.exe
            # linux直接是xxx/xxx/geckodriver, xxx/xxx/firefox
            #firefox_binary=r"/home/deng/FireFox/firefox",
            options=options)
    try:
        #url = r'https://www.google.com/
        browser_driver.get(url)
        #print ('当前爬取的网页url为:{0}'.format(browser_driver.current_url)) 
        # print(browser_driver.find_element_by_id('div_tree').get_attribute('innerHTML'))
        time.sleep(0.5)
        actions = ActionChains(browser_driver)
        actions.send_keys('d')
        actions.perform()
        print("downloaded")

    finally:
        time.sleep(0.5)
        browser_driver.quit()

def main(args):
    tfile = next(src_tree_iterator(args))
    
    command_list = ['nohup', 'ete4', 'explore', '-t', tfile]

    if args.metadata:
        metadata = args.metadata[0]
        command_list.append('--metadata')
        command_list.append(metadata)

    if args.alignment:
        alignment = args.alignment[0]
        command_list.append('--alignment')
        command_list.append(alignment)



    subprocess.Popen(command_list,
                #  stdout=open('/dev/null', 'w'),
                #  stderr=open('logfile.log', 'a'),
                #  preexec_fn=os.setpgrp
                 )

    if args.outdir:
        outdir = args.outdir[0]
    else:
        outdir = CURRENTPATH
        
    browser_driver(url, outdir=outdir)
    time.sleep(1)
    end_flask()
    return

def run(args):
    main(args)
    # VISUALIZATION
    # Basic tree style
    # ts = TreeStyle()
    # ts.show_leaf_name = True
    # try:
    #     tfile = next(src_tree_iterator(args))
    # except StopIteration:
    #     run_smartview()
    # else:
    #     t = PhyloTree(tfile, format=args.src_newick_format)
        
    #     if args.metadata:
    #         metadata = args.metadata[0]
    #         add_annotations(t, metadata)
    #         t.annotate_ncbi_taxa(taxid_attr='taxid')
    #     if args.alignment:
    #         fastafile = args.alignment[0]
    #         fasta_dict = parse_fasta(fastafile)
    #         for leaf in t.iter_leaves():
    #             leaf.add_prop("seq", fasta_dict.get(leaf.name))
    #         t.explore(tree_name=tfile, layouts=[seq_layouts.LayoutAlignment()])
        
    #     elif args.outfile:
    #         filename = args.outfile[0]
    #         t.write(outfile=filename, properties=[])
    #     else:
    #         t.explore(tree_name=tfile)
        
    


 
        
