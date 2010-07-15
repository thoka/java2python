include $(top_srcdir)/Makefile.xt
include $(wildcard *.dep)

bin_PROGRAMS     = java2py 
libexec_PROGRAMS = #jtree15-to-abox jtree15-parenthesize core-lift-eblocks java-concat-ids

EXTRA_DIST     = $(wildcard *.str) $(wildcard *.meta)
CLEANFILES     = $(wildcard *.dep) $(wildcard *.c)

STRCFLAGS    = --main main-$* 
STRINCLUDES  = \
  -I $(srcdir) \
  -I $(srcdir)/pp2py \
  -I $(XTC)/share/xtc \
  -I $(GPP)/share/sdf/gpp \
  -I $(GPP)/share/java-front-syntax \
  -I $(GPP)/share/java-front \
  $(STRATEGO_TOOL_DOC_STRCFLAGS)

#  -I $(top_builddir)/lib 

LDADD += $(STRATEGO_TOOL_DOC_LIBS) $(SSL_LIBS) $(GPP)/lib/libjava-front.la 
