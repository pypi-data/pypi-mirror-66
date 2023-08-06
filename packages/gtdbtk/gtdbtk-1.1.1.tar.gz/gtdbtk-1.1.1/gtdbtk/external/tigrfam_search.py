###############################################################################
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program. If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################

import logging
import multiprocessing as mp
import os
import subprocess
import sys

from gtdbtk.exceptions import GTDBTkExit
from gtdbtk.io.marker.tophit import TopHitTigrFile
from gtdbtk.tools import sha256


class TigrfamSearch(object):
    """Runs TIGRFAM HMMs over a set of genomes."""

    def __init__(self,
                 threads,
                 tigrfam_hmms,
                 protein_file_suffix,
                 tigrfam_suffix,
                 tigrfam_top_hit_suffix,
                 checksum_suffix,
                 output_dir):
        """Initialization."""
        self.logger = logging.getLogger('timestamp')
        self.threads = threads
        self.tigrfam_hmms = tigrfam_hmms
        self.protein_file_suffix = protein_file_suffix
        self.tigrfam_suffix = tigrfam_suffix
        self.tigrfam_top_hit_suffix = tigrfam_top_hit_suffix
        self.checksum_suffix = checksum_suffix
        self.output_dir = output_dir
        self.version = self._get_version()

    def _get_version(self):
        """ get HMMER version."""
        try:
            env = os.environ.copy()
            proc = subprocess.Popen(['hmmsearch', '-h'], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, env=env, encoding='utf-8')

            output, error = proc.communicate()
            for line in output.split('\n'):
                if line.startswith('# HMMER'):
                    version = line.split(';')[0].replace('# HMMER', '').strip()
                    return version
            return "(version unavailable)"
        except:
            return "(version unavailable)"

    def _topHit(self, tigrfam_file):
        """Determine top hits to TIGRFAMs.

        A gene is assigned to a single TIGRFAM
        family. This will be the top hit among
        all TIGRFAM HMMs and pass the threshold
        for the HMM.

        Parameters
        ----------
        tigrfam_file : str
            Name of file containing hits to TIGRFAM HMMs.
        """
        assembly_dir, filename = os.path.split(tigrfam_file)
        genome_id = filename.replace(self.tigrfam_suffix, '')
        tophit_file = TopHitTigrFile(self.output_dir, genome_id)

        # Populate the top-hit file.
        with open(tigrfam_file, 'r') as fh_tigrfam:
            for line in fh_tigrfam:
                if line[0] == '#':
                    continue

                line_split = line.split()
                gene_id = line_split[0]
                hmm_id = line_split[3]
                evalue = float(line_split[4])
                bitscore = float(line_split[5])
                tophit_file.add_hit(gene_id, hmm_id, evalue, bitscore)

        # Write the top-hit file to disk and calculate checksum.
        tophit_file.write()

    def _workerThread(self, queueIn, queueOut):
        """Process each data item in parallel."""
        while True:
            gene_file = queueIn.get(block=True, timeout=None)
            if gene_file is None:
                break

            assembly_dir, filename = os.path.split(gene_file)
            genome_id = filename.replace(self.protein_file_suffix, '')
            output_hit_file = os.path.join(self.output_dir, genome_id, filename.replace(self.protein_file_suffix,
                                                                                        self.tigrfam_suffix))

            hmmsearch_out = os.path.join(self.output_dir, genome_id, filename.replace(self.protein_file_suffix,
                                                                                      '_tigrfam.out'))
            cmd = 'hmmsearch -o %s --tblout %s --noali --notextw --cut_nc --cpu %d %s %s' % (hmmsearch_out,
                                                                                             output_hit_file,
                                                                                             self.cpus_per_genome,
                                                                                             self.tigrfam_hmms,
                                                                                             gene_file)
            os.system(cmd)

            # calculate checksum
            for out_file in [output_hit_file, hmmsearch_out]:
                checksum = sha256(out_file)
                with open(out_file + self.checksum_suffix, 'w') as fh:
                    fh.write(checksum)

            # identify top hit for each gene
            self._topHit(output_hit_file)

            # allow results to be processed or written to file
            queueOut.put(gene_file)

    def _writerThread(self, numDataItems, writerQueue):
        """Store or write results of worker threads in a single thread."""
        processedItems = 0
        while True:
            a = writerQueue.get(block=True, timeout=None)
            if a is None:
                break

            processedItems += 1
            statusStr = '==> Finished processing %d of %d (%.1f%%) genomes.' % (processedItems,
                                                                                numDataItems,
                                                                                float(
                                                                                    processedItems) * 100 / numDataItems)
            sys.stdout.write('\r%s' % statusStr)
            sys.stdout.flush()

        sys.stdout.write('\n')

    def run(self, gene_files):
        """Annotate genes with TIGRFAM HMMs.

        Parameters
        ----------
        gene_files : iterable
            Gene files in FASTA format to process.
        """
        if len(gene_files) == 0:
            raise GTDBTkExit('There are no genomes to process.')
        self.cpus_per_genome = max(1, self.threads / len(gene_files))

        # populate worker queue with data to process
        workerQueue = mp.Queue()
        writerQueue = mp.Queue()

        for f in gene_files:
            workerQueue.put(f)

        for _ in range(self.threads):
            workerQueue.put(None)

        try:
            workerProc = [mp.Process(target=self._workerThread, args=(
                workerQueue, writerQueue)) for _ in range(self.threads)]
            writeProc = mp.Process(target=self._writerThread, args=(
                len(gene_files), writerQueue))

            writeProc.start()

            for p in workerProc:
                p.start()

            for p in workerProc:
                p.join()

            writerQueue.put(None)
            writeProc.join()

            for proc in workerProc:
                if proc.exitcode != 0:
                    raise GTDBTkExit(
                        'An error was encountered while running hmmsearch.')

        except Exception:
            for p in workerProc:
                p.terminate()

            writeProc.terminate()
            raise
