import os
import sys
import shutil
import tarfile
import textwrap
import urllib.request
import subprocess
from zipfile import ZipFile

from phylofisher import help_formatter


def bash(cmd):
    subprocess.run(cmd, shell=True)


def is_in_path(cmd):
    """
    Checks to see if command provided is in PATH already. If it is return True, if not returns False
    """
    if shutil.which(cmd) is None:
        in_path = False
    else:
        in_path = True

    return in_path


def download(url):
    fname = url.split('/')[-1]
    urllib.request.urlretrieve(url, f'{fisher_dir}/{fname}')

    return fname


def extract(fname):
    if fname.endswith("tar.gz"):
        tar = tarfile.open(fname, "r:gz")
        tar.extractall()
        tar.close()
        os.remove(fname)
    elif fname.endswith("tar"):
        tar = tarfile.open(fname, "r:")
        tar.extractall()
        tar.close()
        os.remove(fname)
    elif fname.endswith("zip"):
        zipped = ZipFile(fname, 'r')
        zipped.extractall()
        zipped.close()
        os.remove(fname)


def get_trimal():
    if is_in_path('trimal') is False:
        url = 'http://trimal.cgenomics.org/_media/trimal.v1.2rev59.tar.gz'
        extract(download(url))
        os.chdir(f'{fisher_dir}/trimAl/source/')
        bash('make')
        os.chdir(fisher_dir)
        # Symlink executables to user bin
        src = f'{fisher_dir}/trimAl/source/trimal'
        des = f'{user_bin}/trimal'
        os.symlink(src, des)
        src = f'{fisher_dir}/trimAl/source/readal'
        des = f'{user_bin}/readal'
        os.symlink(src, des)


def get_raxml():
    if is_in_path('raxmlHPC-PTHREADS-AVX2') is False:
        # Download and extract RAxML
        url = 'https://github.com/stamatak/standard-RAxML/archive/master.zip'
        extract(download(url))
        os.chdir(f'{fisher_dir}/standard-RAxML-master/')
        bash('make -f Makefile.AVX.PTHREADS.gcc')
        # Symlink executables to user bin
        src = f'{fisher_dir}/standard-RAxML-master/raxmlHPC-PTHREADS-AVX'
        des = f'{user_bin}/raxmlHPC-PTHREADS-AVX2'
        os.symlink(src, des)

        os.chdir(fisher_dir)


def get_hmmer():
    if is_in_path('hmmsearch') is False:
        # Download and extract hmmer
        url = 'http://eddylab.org/software/hmmer/hmmer.tar.gz'
        extract(download(url))

        os.chdir(f'{fisher_dir}/hmmer-3.3/')
        bash('./configure --prefix=$HOME && make install')


def get_diamond():
    if is_in_path('diamond') is False:
        # Download and extract Diamond
        url = 'http://github.com/bbuchfink/diamond/releases/download/v0.9.31/diamond-linux64.tar.gz'
        extract(download(url))
        os.symlink('diamond', f'{user_bin}/diamond')


home = os.path.expanduser('~')
user_bin = f'{home}/bin'
fisher_dir = f'{home}/PhyloFisher_lib'

if os.path.isdir(user_bin) is False:
    os.mkdir(user_bin)
if os.path.isdir(fisher_dir) is False:
    os.mkdir(fisher_dir)

os.chdir(fisher_dir)
# get_trimal()
# get_raxml()
# get_hmmer()
get_diamond()

# if __name__ == '__main__':
#     description = 'Script for ortholog fishing.'
#     parser, optional, required = help_formatter.initialize_argparse(name='fisher.py',
#                                                                     desc=description,
#                                                                     usage='fisher.py [OPTIONS]')
#
#     optional.add_argument('-t', '--threads', type=int, metavar='N',
#                           help=textwrap.dedent("""\
#                             Number of threads, where N is an integer.
#                             Default: 1
#                             """))
#     optional.add_argument('-n', '--max_hits', type=int, metavar='N',
#                           help=textwrap.dedent("""\
#                             Max number of hits to check, where N is an interger.
#                             Default: 5
#                             """))
#     optional.add_argument('--keep_tmp', action='store_true',
#                           help=textwrap.dedent("""\
#                             Keep temporary files
#                             """))
#     optional.add_argument('--add', metavar='<inputfile>',
#                           help=textwrap.dedent("""\
#                             Input file (different from original one in config.ini) only with new organisms.
#                             """))
#     args = help_formatter.get_args(parser, optional, required, pre_suf=False, inp_dir=False)
#
