include $(top_srcdir)/Makefile.xt
include $(wildcard *.dep)

SUBDIRS = . syn gnu-classpath j2sdk pp
BOOTCLEAN_SUBDIRS = $(SUBDIRS)

EXTRA_DIST = $(wildcard *.str) $(wildcard *.meta)
CLEANFILES = $(wildcard *.dep) $(wildcard *.c)

TESTS = $(check_PROGRAMS)
check_PROGRAMS = libjava-front-tests
STRCFLAGS = --main main-$*
STRINCLUDES = -I $(top_builddir)/lib
LDADD += $(top_builddir)/lib/libjava-front.la $(SSL_LIBS)
