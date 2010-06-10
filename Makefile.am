include $(top_srcdir)/Makefile.xt

SUBDIRS = news-archive syntax syntax-embedding lib tools test
pkgdata_DATA = java-front.m4

BOOTCLEAN_SUBDIRS = $(SUBDIRS)
DIST_SUBDIRS      = $(SUBDIRS)
EXTRA_DIST        = $(pkgdata_DATA) Makefile.xt java-front.spec java-front.spec.in java-front.pc bootstrap autoxt.m4
CLEANFILES        = XTC

XTC_IMPORT = $(STRATEGOXT)/share/strategoxt/XTC

ACLOCAL_AMFLAGS = -I .

pkgconfig_DATA = java-front.pc
