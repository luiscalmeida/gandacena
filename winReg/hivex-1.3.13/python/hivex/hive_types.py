# hivex generated file
# WARNING: THIS FILE IS GENERATED FROM:
#   generator/generator.ml
# ANY CHANGES YOU MAKE TO THIS FILE WILL BE LOST.
#
# Copyright (C) 2009-2015 Red Hat Inc.
# Derived from code by Petter Nordahl-Hagen under a compatible license:
#   Copyright (c) 1997-2007 Petter Nordahl-Hagen.
# Derived from code by Markus Stephany under a compatible license:
#   Copyright (c)2000-2004, Markus Stephany.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

"""Define integer constants for hive type

The names correspond with the hive_type enum type of the C API, but without
'hive_t_' prefix.
"""

# Just a key without a value
REG_NONE = 0
# A Windows string (encoding is unknown, but often UTF16-LE)
REG_SZ = 1
# A Windows string that contains %env% (environment variable expansion)
REG_EXPAND_SZ = 2
# A blob of binary
REG_BINARY = 3
# DWORD (32 bit integer), little endian
REG_DWORD = 4
# DWORD (32 bit integer), big endian
REG_DWORD_BIG_ENDIAN = 5
# Symbolic link to another part of the registry tree
REG_LINK = 6
# Multiple Windows strings.  See http://blogs.msdn.com/oldnewthing/archive/2009/10/08/9904646.aspx
REG_MULTI_SZ = 7
# Resource list
REG_RESOURCE_LIST = 8
# Resource descriptor
REG_FULL_RESOURCE_DESCRIPTOR = 9
# Resouce requirements list
REG_RESOURCE_REQUIREMENTS_LIST = 10
# QWORD (64 bit integer), unspecified endianness but usually little endian
REG_QWORD = 11
