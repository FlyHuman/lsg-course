#
# This Makefile is used to compile example code for the SURFsara LSG workshop 2016.
# Copyright (c) 2015-2016 SURFsara, all rights reserved
# This file is Open Source under the BSD 2-Clause License: http://opensource.org/licenses/BSD-2-Clause
#
# (use gnu make)

# use the gcc compiler
CC = gcc
# use C99
CFLAGS += -std=c99
# turn on as many warnings as you want (examples are strict C99)
CFLAGS += -Wall -Wextra -Werror -Wconversion -pedantic -pedantic-errors

# optimisation level: 0 for debugging, empty or 2 for production
CFLAGS += -O0

# the following programs use OpenMP:
EXECS_OMP = gridpi-mp-simple gridpi-mp-alt gridpi-mp-reduction
# all programs:
EXECS = gridpi-serial $(EXECS_OMP)

# default target
all: $(EXECS)

# OpenMP programs need an extra flag:
$(EXECS_OMP): CFLAGS += -fopenmp

clean:
	rm -f $(EXECS)

#####
# the rules below are only to create the tar file with sources

MYDIRNAME = $(notdir $(realpath .))
ifeq ($(MYDIRNAME),)
$(error cannot determine current directory in parent directory)
endif

TARFILE = gridpi-mp.tgz

$(TARFILE): README.txt Makefile *.c
	tar czf $@ -C.. $(addprefix $(MYDIRNAME)/,$^)

cleanall realclean: clean
	rm -f $(TARFILE)

# that's all folks!
