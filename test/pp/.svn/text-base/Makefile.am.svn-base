include $(top_srcdir)/Makefile.xt

JAVA_FILES = $(wildcard *.java)
EXTRA_DIST = $(JAVA_FILES)
CLEANFILES = $(JAVA_FILES:.java=.pp) $(JAVA_FILES:.java=.jtree)

check : $(JAVA_FILES:.java=.pp)

%.pp : %.jtree
	$(top_builddir)/tools/pp-java -i $< -o $@ 

%.jtree : %.java
	$(top_builddir)/tools/parse-java -i $< -o $@ 
