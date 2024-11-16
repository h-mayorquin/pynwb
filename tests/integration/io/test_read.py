from pathlib import Path
import tempfile

from pynwb import read_nwb
from pynwb.testing.mock.file import mock_NWBFile
from pynwb.testing import TestCase

import unittest
try:
    from hdmf_zarr import NWBZarrIO  # noqa f401
    HAVE_NWBZarrIO = True 
except ImportError:
    HAVE_NWBZarrIO = False


class TestReadNWBMethod(TestCase):
    """
    Test that H5DataIO functions correctly on round trip with the HDF5IO backend
    """
    def setUp(self):
        self.nwbfile = mock_NWBFile()


    def test_read_nwb_hdf5(self):
        from pynwb import NWBHDF5IO
        
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "test.nwb"
            with NWBHDF5IO(path, 'w') as io:
                io.write(self.nwbfile)
            
            read_nwbfile = read_nwb(path=path)
            self.assertContainerEqual(read_nwbfile, self.nwbfile)
            read_nwbfile.get_read_io().close()
            
    @unittest.skipIf(not HAVE_NWBZarrIO, "NWBZarrIO library not available")
    def test_read_zarr(self):
        # from pynwb import NWBZarrIO
        from hdmf_zarr import NWBZarrIO

        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "test.nwb"
            with NWBZarrIO(path, 'w') as io:
                io.write(self.nwbfile)
            
            read_nwbfile = read_nwb(path=path)
            self.assertContainerEqual(read_nwbfile, self.nwbfile)
            read_nwbfile.get_read_io().close()