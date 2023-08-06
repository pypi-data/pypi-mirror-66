import contextlib
import ctypes
import mmap
import os
import platform
import re
import struct
import tempfile
import unittest

from drgn.helpers.linux.mm import (
    page_to_pfn,
    pfn_to_page,
    pfn_to_virt,
    pgtable_l5_enabled,
    virt_to_pfn,
)
from tests.helpers.linux import LinuxHelperTestCase, mlock


class TestMm(LinuxHelperTestCase):
    def test_page_constants(self):
        self.assertEqual(self.prog["PAGE_SIZE"], mmap.PAGESIZE)
        self.assertEqual(1 << self.prog["PAGE_SHIFT"], mmap.PAGESIZE)
        self.assertEqual(~self.prog["PAGE_MASK"] + 1, mmap.PAGESIZE)

    # Returns an mmap.mmap object for a file mapping and the pfns backing it.
    @contextlib.contextmanager
    def _pages(self):
        if not os.path.exists("/proc/self/pagemap"):
            self.skipTest("kernel does not support pagemap")

        pages = 4
        with tempfile.TemporaryFile() as f:
            f.write(os.urandom(pages * mmap.PAGESIZE))
            f.flush()
            with mmap.mmap(f.fileno(), pages * mmap.PAGESIZE) as map:
                f.close()
                address = ctypes.addressof(ctypes.c_char.from_buffer(map))
                # Make sure the pages are faulted in and stay that way.
                mlock(address, pages * mmap.PAGESIZE)

                with open("/proc/self/pagemap", "rb", buffering=0) as pagemap:
                    pagemap.seek(address // mmap.PAGESIZE * 8)
                    pfns = [
                        entry & ((1 << 54) - 1)
                        for entry in struct.unpack(f"{pages}Q", pagemap.read(pages * 8))
                    ]
                yield map, pfns

    def test_virt_to_from_pfn(self):
        with self._pages() as (map, pfns):
            for i, pfn in enumerate(pfns):
                virt = pfn_to_virt(self.prog, pfn)
                # Test that we got the correct virtual address by reading from
                # it and comparing it to the mmap.
                self.assertEqual(
                    self.prog.read(virt, mmap.PAGESIZE),
                    map[i * mmap.PAGESIZE : (i + 1) * mmap.PAGESIZE],
                )
                # Test the opposite direction.
                self.assertEqual(virt_to_pfn(virt), pfn)

    def test_pfn_to_from_page(self):
        with self._pages() as (map, pfns):
            for i, pfn in enumerate(pfns):
                page = pfn_to_page(self.prog, pfn)
                # Test that we got the correct page by looking at the index: it
                # should be page i in the file.
                self.assertEqual(page.index, i)
                # Test the opposite direction.
                self.assertEqual(page_to_pfn(page), pfn)

    @unittest.skipUnless(platform.machine() == "x86_64", "machine is not x86_64")
    def test_pgtable_l5_enabled(self):
        with open("/proc/cpuinfo", "r") as f:
            self.assertEqual(
                pgtable_l5_enabled(self.prog),
                bool(re.search(r"flags\s*:.*\bla57\b", f.read())),
            )
