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

import multiprocessing as mp
import os
import sys

from gtdbtk.exceptions import GTDBTkExit
from gtdbtk.external.pypfam.Scan.PfamScan import PfamScan
from gtdbtk.io.marker.tophit import TopHitPfamFile
from gtdbtk.tools import sha256


class PfamSearch(object):
    """Runs pfam_search.pl over a set of genomes."""

    def __init__(self,
                 threads,
                 pfam_hmm_dir,
                 protein_file_suffix,
                 pfam_suffix,
                 pfam_top_hit_suffix,
                 checksum_suffix,
                 output_dir):
        """Initialization."""

        self.threads = threads

        self.pfam_hmm_dir = pfam_hmm_dir
        self.protein_file_suffix = protein_file_suffix
        self.pfam_suffix = pfam_suffix
        self.pfam_top_hit_suffix = pfam_top_hit_suffix
        self.checksum_suffix = checksum_suffix
        self.output_dir = output_dir

    def _topHit(self, pfam_file):
        """Determine top hits to PFAMs.

        A gene may be assigned to multiple
        PFAM families from the same clan. The
        search_pfam.pl script takes care of
        most of these issues and here the results
        are simply parsed.

        Parameters
        ----------
        pfam_file : str
            Name of file containing hits to PFAM HMMs.
        """

        assembly_dir, filename = os.path.split(pfam_file)
        genome_id = filename.replace(self.pfam_suffix, '')
        tophit_file = TopHitPfamFile(self.output_dir, genome_id)

        with open(pfam_file, 'r') as fh_pfam:
            for line in fh_pfam:
                if line[0] == '#' or not line.strip():
                    continue

                line_split = line.split()
                gene_id = line_split[0]
                hmm_id = line_split[5]
                evalue = float(line_split[12])
                bitscore = float(line_split[11])
                tophit_file.add_hit(gene_id, hmm_id, evalue, bitscore)

        tophit_file.write()

    def _workerThread(self, queueIn, queueOut):
        """Process each data item in parallel."""
        try:
            while True:
                gene_file = queueIn.get(block=True, timeout=None)
                if gene_file is None:
                    break

                genome_dir, filename = os.path.split(gene_file)
                genome_id = filename.replace(self.protein_file_suffix, '')
                output_hit_file = os.path.join(self.output_dir, genome_id, filename.replace(self.protein_file_suffix,
                                                                                            self.pfam_suffix))

                pfam_scan = PfamScan(cpu=self.cpus_per_genome, fasta=gene_file, dir=self.pfam_hmm_dir)
                pfam_scan.search()
                pfam_scan.write_results(output_hit_file, None, None, None, None)

                # calculate checksum
                with open(output_hit_file + self.checksum_suffix, 'w') as fh:
                    fh.write(sha256(output_hit_file))

                # identify top hit for each gene
                self._topHit(output_hit_file)

                queueOut.put(gene_file)
        except Exception as error:
            raise error

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
                                                                                float(processedItems) * 100 / numDataItems)
            sys.stdout.write('\r%s' % statusStr)
            sys.stdout.flush()
        sys.stdout.write('\n')

    def run(self, gene_files):
        """Annotate genes with Pfam HMMs.

        Parameters
        ----------
        gene_files : iterable
            Gene files in FASTA format to process.
        """

        self.cpus_per_genome = max(1, int(self.threads / len(gene_files)))

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
                if p.exitcode != 0:
                    raise GTDBTkExit('An error was encountered while running hmmsearch.')

            writerQueue.put(None)
            writeProc.join()
        except Exception:
            for p in workerProc:
                p.terminate()

            writeProc.terminate()
            raise
