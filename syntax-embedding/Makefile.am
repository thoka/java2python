include $(top_srcdir)/Makefile.xt
include $(wildcard *.dep)

nobase_pkgdata_DATA = $(MODS) $(GENMODS)
pkgdata_DATA        = $(RTGS) $(SIGS) $(TBLS_DEFS)

EXTRA_DIST = $(MODS) $(GENMODS) $(TBLS_DEFS) $(RTGS) $(SIGS) 
CLEANFILES =         $(GENMODS) $(TBLS_DEFS) $(RTGS) $(SIGS) $(wildcard *.dep)

PGEN_FLAGS     = -m $*
SDF2RTG_FLAGS  = --main $* --ignore-missing-cons
SDFINCLUDES    = -I $(srcdir) -Idef $(MIX)

TBLS_DEFS = \
  EmbeddedJava.def \
  EmbeddedJavaMix.def \
  Stratego-Java-15.def \
  Stratego-Java-15.tbl \
  Java-EBlock.def \
  Java-EBlock.tbl \
  Stratego-Java-EBlock.def \
  Stratego-Java-EBlock.tbl \
  JavaEBlockMix.def

RTGS = Java-15.rtg Java-EBlock.rtg
SIGS = Java-15.str Java-15.rtree Java-EBlock.str Java-EBlock.rtree
MIX = $(top_srcdir)/syntax/src/JavaMix.def
EMBMIX  = languages/java/EmbeddedJavaMix.sdf
EBLOCKMIX = languages/java/eblock/JavaEBlockMix.sdf

GENMODS = $(EMBMIX) $(EBLOCKMIX)

MODS = \
  Java-EBlock.sdf \
  Stratego-Java-15.sdf \
  Stratego-Java-EBlock.sdf \
  $(wildcard languages/java/eblock/*.sdf) \
  $(wildcard languages/java/*.sdf)

if XT_BOOTSTRAP

Stratego-Java-15.def : $(EMBMIX) $(MIX)
Stratego-Java-EBlock.def : $(EMBMIX) $(MIX) $(EBLOCKMIX)

$(EMBMIX) : EmbeddedJava.def
	$(SDF_TOOLS)/bin/gen-sdf-mix -i $< --main languages/java/EmbeddedJava --name languages/java/EmbeddedJavaMix -o $@

$(EBLOCKMIX) : Java-EBlock.def
	$(SDF_TOOLS)/bin/gen-sdf-mix -i $< --main languages/java/eblock/Main --name languages/java/eblock/JavaEBlockMix -o $@

Stratego-Java-15.def : Stratego-Java-15.sdf
	$(SDF_FRONT)/bin/pack-sdf -i $< -o $@ -Idef $(STRATEGO_FRONT)/share/sdf/stratego-front/StrategoMix.def -Idef $(MIX)

Stratego-Java-EBlock.def : Stratego-Java-EBlock.sdf
	$(SDF_FRONT)/bin/pack-sdf -i $< -o $@ -Idef $(STRATEGO_FRONT)/share/sdf/stratego-front/StrategoMix.def -Idef $(MIX)

EmbeddedJava.def : languages/java/EmbeddedJava.sdf $(MIX)
	$(SDF_FRONT)/bin/pack-sdf -i $< -o $@ -Idef $(MIX)

EmbeddedJavaMix.def : $(EMBMIX) EmbeddedJava.def
	$(SDF_FRONT)/bin/pack-sdf -i $< -o $@ -Idef EmbeddedJava.def

JavaEBlockMix.def : $(EBLOCKMIX) Java-EBlock.def
	$(SDF_FRONT)/bin/pack-sdf -i $< -o $@ -Idef Java-EBlock.def

Java-15.def : $(top_srcdir)/syntax/src/Java-15.def
	cp -p $< $@
endif
