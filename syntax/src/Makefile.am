include $(top_srcdir)/MakefileData.xt
include $(wildcard *.dep)

nobase_pkgdata_DATA = $(MODS) $(GENMODS)
pkgdata_DATA        = $(TBLS_DEFS)

EXTRA_DIST = $(MODS) $(GENMODS) $(TBLS_DEFS) 
CLEANFILES =         $(GENMODS) $(TBLS_DEFS) $(wildcard *.dep)

PGEN_FLAGS  = -m $*
SDFINCLUDES = -I $(srcdir)

TBLS_DEFS = \
  Java-15.def \
  Java-15.tbl \
  JavaCompilationUnit-15.def \
  JavaCompilationUnit-15.tbl \
  JavaMix.def

MIX     = languages/java-15/JavaMix.sdf
GENMODS = $(MIX)

MODS = \
  Java-15.sdf \
  JavaCompilationUnit-15.sdf \
  $(wildcard languages/java/*.sdf) \
  $(wildcard languages/java-15/*.sdf) \
  $(wildcard languages/java-15/lexical/*.sdf) \
  $(wildcard languages/java-15/lexical/literals/*.sdf) \
  $(wildcard languages/java-15/names/*.sdf) \
  $(wildcard languages/java-15/types/*.sdf) \
  $(wildcard languages/java-15/packages/*.sdf) \
  $(wildcard languages/java-15/classes/*.sdf) \
  $(wildcard languages/java-15/interfaces/*.sdf) \
  $(wildcard languages/java-15/arrays/*.sdf) \
  $(wildcard languages/java-15/statements/*.sdf) \
  $(wildcard languages/java-15/expressions/*.sdf)

$(MIX): Java-15.def
	$(GENSDFMIX) -i $< --main languages/java-15/Main --name languages/java-15/JavaMix -o $@

JavaMix.def : $(MIX) Java-15.def
	$(PACKSDF) -i languages/java/JavaMix.sdf -o $@ -Idef Java-15.def -I .
