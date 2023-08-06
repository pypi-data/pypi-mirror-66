import glob
from pathlib import Path
from typing import Optional, List, Callable, Any

from tqdm.auto import tqdm

from shmr.misc import get_filepath_template, get_func_by_name
from shmr.partition import Partition
from shmr.partition_writer import PartitionWriter


class ListPartition:

    def __init__(self, infile: str, deser_fn: Callable[[bytes], Any], ser_fn: Callable[[Any], bytes], skip_nrows: int):
        partitions = []
        for file_path in sorted(glob.glob(infile)):
            partitions.append(Partition(file_path, deser_fn, ser_fn, skip_nrows))

        if len(partitions) == 0:
            raise ValueError(f"No partition matches the pattern: {infile}")
        self.partitions: List[Partition] = partitions
        self.ser_fn = ser_fn
        self.size = self._size()

    def _size(self) -> Optional[int]:
        size = 0
        for part in self.partitions:
            if part.n_records is None:
                return None
            size += part.n_records
        return size

    def coalesce(self, outfile: str, records_per_partition: Optional[int] = None,
                 num_partitions: Optional[int] = None, verbose: bool = True):
        """The current partitions are coalesce into `num_partitions` partitions. If `num_partitions` is not specified, it will be figure out automatically
        from `records_per_partition`.
        
        Args:
            outfile (str): path template of output partitions
            records_per_partition (Optional[int], optional): number of records per partition. Defaults to None.
            num_partitions (Optional[int], optional): number of partitions. Defaults to None.
            verbose (bool, optional): log execution progress. Defaults to True.
        
        Raises:
            ValueError: if the output directory does not exist
        """
        outfile = get_filepath_template(outfile)
        if not Path(outfile).parent.exists():
            raise ValueError(f"Output directory does not exist: {Path(outfile).parent}")

        if records_per_partition is None:
            assert num_partitions is not None
            # TODO: cal the records_per_partition based on num_partitions

        part_counter = 0
        start = 0

        writer = None
        try:
            writer = PartitionWriter(outfile % part_counter).open()
            for inpart in self.partitions:
                with inpart._open() as f:
                    for i, line in (tqdm(enumerate(f), initial=start, total=self.size) if verbose else enumerate(f)):
                        if (i + 1) % records_per_partition == 0:
                            writer.close()
                            part_counter += 1
                            writer = PartitionWriter(outfile % part_counter).open()
                        writer.write(line)
        finally:
            if writer is not None:
                writer.close()

    def concat(self, outfile: str, verbose: bool = True):
        """Concatenate partitions to one file

        Args:
            outfile (str): path to output partition
            verbose (bool): log execution progress. Defaults to True

        Returns:
            ValueError: if the output directory does not exist
        """
        with PartitionWriter(outfile) as g:
            start = 0
            for inpart in self.partitions:
                with inpart._open() as f:
                    for line in (tqdm(f, initial=start, total=self.size) if verbose else f):
                        g.write(line)

    def reduce(self, fn: str, outfile: str, init_val: Any = None, verbose: bool = True):
        """Reduce

        Args:
            fn (str): [description]
            outfile (str): [description]
            init_val (Any): [description]
            verbose (bool, optional): [description]. Defaults to True.
        """
        fn = get_func_by_name(fn)
        if init_val is not None:
            accum = init_val
        else:
            accum = None

        with PartitionWriter(outfile) as g:
            for inpart in self.partitions:
                with inpart._open() as f:
                    total = inpart.n_records
                    if accum is None:
                        try:
                            record = inpart.deser_fn(next(f))
                            accum = fn(record)
                            if total is not None:
                                total -= 1
                        except StopIteration:
                            pass

                    for line in tqdm(f, total=total) if verbose else f:
                        record = inpart.deser_fn(line)
                        accum = fn(record, accum)

            g.write(self.ser_fn(accum))
            g.write_new_line()
