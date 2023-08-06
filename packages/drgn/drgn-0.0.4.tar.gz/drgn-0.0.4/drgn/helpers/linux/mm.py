# Copyright 2018-2020 - Omar Sandoval
# SPDX-License-Identifier: GPL-3.0+

"""
Memory Management
-----------------

The ``drgn.helpers.linux.mm`` module provides helpers for working with the
Linux memory management (MM) subsystem. Only x86-64 support is currently
implemented.
"""

from _drgn import _linux_helper_pgtable_l5_enabled
from drgn import Object, cast


__all__ = (
    "pgtable_l5_enabled",
    "for_each_page",
    "page_to_pfn",
    "page_to_virt",
    "pfn_to_page",
    "pfn_to_virt",
    "virt_to_page",
    "virt_to_pfn",
)


def pgtable_l5_enabled(prog):
    """
    .. c:function:: bool pgtable_l5_enabled(void)

    Return whether 5-level paging is enabled.
    """
    return _linux_helper_pgtable_l5_enabled(prog)


def for_each_page(prog):
    """
    Iterate over all pages in the system.

    :return: Iterator of ``struct page *`` objects.
    """
    vmemmap = prog["vmemmap"]
    for i in range(prog["max_pfn"]):
        yield vmemmap + i


def page_to_pfn(page):
    """
    .. c:function:: unsigned long page_to_pfn(struct page *page)

    Get the page frame number (PFN) of a page.
    """
    return cast("unsigned long", page - page.prog_["vmemmap"])


def pfn_to_page(prog_or_pfn, pfn=None):
    """
    .. c:function:: struct page *pfn_to_page(unsigned long pfn)

    Get the page with the given page frame number (PFN). This can take the PFN
    as an :class:`Object`, or a :class:`Program` and the PFN as an ``int``.
    """
    if pfn is None:
        prog = prog_or_pfn.prog_
        pfn = prog_or_pfn
    else:
        prog = prog_or_pfn
    return prog["vmemmap"] + pfn


def virt_to_pfn(prog_or_addr, addr=None):
    """
    .. c:function:: unsigned long virt_to_pfn(void *addr)

    Get the page frame number (PFN) of a directly mapped virtual address. This
    can take the address as an :class:`Object`, or a :class:`Program` and the
    address as an ``int``.
    """
    if addr is None:
        prog = prog_or_addr.prog_
        addr = prog_or_addr.value_()
    else:
        prog = prog_or_addr
    return Object(prog, "unsigned long", value=(addr - prog["PAGE_OFFSET"]) >> 12)


def pfn_to_virt(prog_or_pfn, pfn=None):
    """
    .. c:function:: void *pfn_to_virt(unsigned long pfn)

    Get the directly mapped virtual address of the given page frame number
    (PFN). This can take the PFN as an :class:`Object`, or a :class:`Program`
    and the PFN as an ``int``.
    """
    if pfn is None:
        prog = prog_or_pfn.prog_
        pfn = prog_or_pfn.value_()
    else:
        prog = prog_or_pfn
    return Object(prog, "void *", value=(pfn << 12) + prog["PAGE_OFFSET"])


def page_to_virt(page):
    """
    .. c:function:: void *page_to_virt(struct page *page)

    Get the directly mapped virtual address of a page.
    """
    return pfn_to_virt(page_to_pfn(page))


def virt_to_page(prog_or_addr, addr=None):
    """
    .. c:function:: struct page *virt_to_page(void *addr)

    Get the page containing a directly mapped virtual address. This can take
    the address as an :class:`Object`, or a :class:`Program` and the address as
    an ``int``.
    """
    return pfn_to_page(virt_to_pfn(prog_or_addr, addr))
