"""Utility functions for ReSDK.

The MIT License (MIT)
Copyright (c) 2017 Charles Y. Lin, Domen Blenkuš, Barbara Jenko, Rachel Hirsch
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import getpass
import os

from pexpect import pxssh
from six.moves import input

SSH_HOSTNAME = 'mhgcp-h00.grid.bcm.edu'
DATA_FOLDER_PATH = '/storage/genialis/bcm.genialis.com/data/'


def create_links(resource, genome_name, links, path='resdk_results'):
    """Create links to files on `taco` server.

    :param resource: Single resource or list of resources which will be
        linked
    :type resource: `~resdk.resources.sample.Sample` or
        `~resdk.resources.collection.Collection`
    :param str genome_name: name of the genome used in links' names
    :param list links: list with links descriptions in format described
        below
    :param str path: path to directory on taco where links will be
        created. If path is relative, it is relative to user's home
        directory (Default: resdk_results)

    `links` list should be in following form::

        [
            {'type': 'data:alignment:bam:bowtie2:', 'field': 'bam', 'subfolder': 'bams'},
            {'type': 'data:alignment:bam:bowtie2:', 'field': 'bai', 'subfolder': 'bams'},
            {'type': 'data:chipseq:macs14:', 'field': 'peaks_bed', 'subfolder': 'macs'},
            {'type': 'data:chipseq:macs14:', 'field': 'peaks_xls', 'subfolder': 'macs'},
            {'type': 'data:chipseq:rose2:', 'field': 'all_enhancers', 'subfolder': 'roses'},
        ]

    """
    # This must be a dict, so the reference doesn't breake even if it
    # is assigned in sub-function.
    ssh = {'connection': None}

    def _create_local_link(src, dest):
        dest_dir = os.path.dirname(dest)
        if not os.path.isdir(dest_dir):
            os.makedirs(dest_dir)

        if os.path.isfile(dest):
            os.remove(dest)

        os.symlink(src, dest)

    def _create_ssh_link(src, dest):
        if ssh['connection'] is None:
            print('Credentials for connection to {}:'.format(SSH_HOSTNAME))
            username = input('username: ')
            password = getpass.getpass('password: ')

            ssh['connection'] = pxssh.pxssh()
            ssh['connection'].login(SSH_HOSTNAME, username, password)

        dest_dir = os.path.dirname(dest)

        ssh['connection'].sendline('mkdir -p "{}"'.format(dest_dir))
        ssh['connection'].sendline('ln -sf "{}" "{}"'.format(src, dest))

    if not isinstance(resource, list):
        resource = [resource]

    print('Linking results...')
    for link in links:
        for single_resource in resource:
            for data in single_resource.data.filter(status='OK', type=link['type']):
                for file_name in data.files(field_name=link['field']):
                    file_path = os.path.join(DATA_FOLDER_PATH, str(data.id), file_name)

                    link_name = '{:05}_{}_{}_{}'.format(
                        data.id,
                        data.sample.slug if data.sample else data.slug,
                        link['field'],
                        genome_name,
                    )
                    if '.' in file_name:
                        link_extension = file_name.split('.', 1)[1]
                        link_name = '{}.{}'.format(link_name, link_extension)

                    link_path = os.path.join(path, link['subfolder'], link_name)

                    if os.path.isfile(file_path):
                        _create_local_link(file_path, link_path)
                    else:
                        _create_ssh_link(file_path, link_path)

    if ssh['connection'] is not None:
        ssh['connection'].logout()


def link_project(resource, genome_name, path, output_table=''):
    links = [
                {'type': 'data:alignment:bam:bowtie2:', 'field': 'bam', 'subfolder': 'bams'},
                {'type': 'data:alignment:bam:bowtie2:', 'field': 'bai', 'subfolder': 'bams'},
                {'type': 'data:alignment:bam:hisat2:', 'field': 'bam', 'subfolder': 'bams'},
                {'type': 'data:alignment:bam:hisat2:', 'field': 'bai', 'subfolder': 'bams'},
                {'type': 'data:chipseq:macs14:','field':'peaks_bed','subfolder': 'macs14'},
                {'type': 'data:chipseq:rose2:','field':'ALL','subfolder': 'rose2'},
                {'type': 'data:cufflinks:cuffquant:','field':'ALL','subfolder': 'cufflinks/cuffquant'},
                {'type': 'data:expressionset:cuffnorm:','field':'ALL','subfolder': 'cufflinks/cuffnorm'},
            ]

    # This must be a dict, so the reference doesn't breake even if it
    # is assigned in sub-function.
    ssh = {'connection': None}
    def _create_local_link(src, dest):
        dest_dir = os.path.dirname(dest)
        if not os.path.isdir(dest_dir):
            os.makedirs(dest_dir)
        if os.path.isfile(dest):
            os.remove(dest)
        os.symlink(src, dest)
    def _create_ssh_link(src, dest):
        if ssh['connection'] is None:
            print('Credentials for connection to {}:'.format(SSH_HOSTNAME))
            username = input('username: ')
            password = getpass.getpass('password: ')
            ssh['connection'] = pxssh.pxssh()
            ssh['connection'].login(SSH_HOSTNAME, username, password)
        dest_dir = os.path.dirname(dest)
        ssh['connection'].sendline('mkdir -p "{}"'.format(dest_dir))
        ssh['connection'].sendline('ln -sf "{}" "{}"'.format(src, dest))

    data_table = [['FILE_PATH','UNIQUE_ID','GENOME','NAME','BACKGROUND','ENRICHED_REGION','ENRICHED_MACS','COLOR','RAW']]

    print('Linking results...')
    for link in links:
        for data in resource.data.filter(status='OK', type=link['type']):

            if link['field'] == 'ALL':
                files_filter = {}
            else:
                files_filter = {'field_name': link['field']}

            for file_name in data.files(**files_filter):

                if link['field'] == 'bam':
                    bam_path = os.path.join(path, 'bams/')
                    unique_ID = str(data.id)
                    genome = str(genome_name).upper()
                    name = str(data.sample.name).upper()
                    bg = data.sample.get_background(fail_silently=True)
                    if bg is not None:
                        background = str(data.sample.get_background(fail_silently=True).slug).upper()
                    else:
                        background = 'NONE'
                    enriched_region = 'NONE'
                    color = '0,0,0'
                    macs = data.sample.data.filter(type = 'data:chipseq:macs14')
                    if len(macs):
                        enriched_macs ='{:05}_{}'.format(
                           data.id,
                           macs[0].output['peaks_bed']['file']
                        )

                    else:
                        enriched_macs = 'NONE'

                    new_line = [
                       bam_path, 
                       unique_ID, 
                       genome, 
                       name, 
                       background,
                       enriched_region, 
                       enriched_macs, 
                       color,
                        '',
                    ]
                    
                    data_table.append(new_line)

                file_path = os.path.join(DATA_FOLDER_PATH, str(data.id), file_name)                         
                link_name = '{:05}_{}'.format(
                    data.id,
                    file_name,
                )
                link_path = os.path.join(path, link['subfolder'], link_name)
                if os.path.isfile(file_path):
                    _create_local_link(file_path, link_path)
                else:
                    _create_ssh_link(file_path, link_path)


    sep = '\t'
    if output_table == '':
        output_table = 'data_table.txt'


    fh_out = open(output_table, 'w')
    if len(sep) == 0:
        for i in data_table:
            fh_out.write(str(i) + '\n')
    else:
        for line in data_table:
            fh_out.write(sep.join([str(x) for x in line]) + '\n')

    fh_out.close()


    if ssh['connection'] is not None:
        ssh['connection'].logout()
