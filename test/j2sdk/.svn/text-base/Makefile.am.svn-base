include $(top_srcdir)/Makefile.xt
# include $(top_srcdir)/test/Makefile.parse-unit

# create J2SDK testsuites
j2sdk-src : src.zip
	rm -rf j2sdk-src
	mkdir j2sdk-src
	unzip src.zip -d j2sdk-src

j2sdk.list : j2sdk-src
	find j2sdk-src -name '*.java' | sort > $@

# j2sdk.atestsuite : j2sdk.list $(prefix)/bin/files2parse-unit-testsuite
# 	$(prefix)/bin/files2parse-unit-testsuite -i $< -o $@

j2sdkcheck : ppcheck

# $(J2SDK_TESTSUITES:.testsuite=.runtestsuite)

# targets
# J2SDK_TESTSUITES = j2sdk.testsuite
# PARSE_UNIT_PTABLE = $(sdfdatadir)/Java.tbl
# %.jasfix : %.java $(prefix)/share/sdf/java-front/Java.tbl
# 	sglr -2lv -p $(prefix)/share/sdf/java-front/Java.tbl -i $< -o $@

PARSEJAVA=XTC_REPOSITORY="$(BUILD_REPOSITORY)" $(XTC)/bin/xtc call parse-java
PPJAVA=XTC_REPOSITORY="$(BUILD_REPOSITORY)" $(XTC)/bin/xtc call pp-java

# pretty-print tests
ppcheck : j2sdk.list
	FILES="`cat j2sdk.list`" && \
	for file in $$FILES; do \
	  if   test "$${file}" = "j2sdk-src/com/sun/org/apache/xalan/internal/xsltc/compiler/FunctionCall.java" \
            || test "$${file}" = "j2sdk-src/com/sun/org/apache/xml/internal/utils/StringComparable.java" \
            || test "$${file}" = "j2sdk-src/java/util/jar/Attributes.java" \
            || test "$${file}" = "j2sdk-src/javax/sql/rowset/spi/SyncFactory.java" \
            || test "$${file}" = "j2sdk-src/javax/swing/text/html/parser/ContentModelState" \
          ; then \
            $(MAKE) "$${file%.java}.jtree" "$${file%.java}.ppjtree" || exit 1; \
          else \
            $(MAKE) "$${file%.java}.jtree" "$${file%.java}.ppjtree" "$${file%.java}.ppdiff" || exit 1; \
          fi \
	done

%.ppdiff : %.jtree %.ppjtree
	if diff $*.jtree $*.ppjtree > /dev/null ; then \
	  touch $@; \
	else \
	  $(ATERM_FRONT)/bin/pp-aterm -i $*.jtree -o $*.jtree ; \
	  $(ATERM_FRONT)/bin/pp-aterm -i $*.ppjtree -o $*.ppjtree ; \
	  diff $*.jtree $*.ppjtree > $@ ; \
	fi

%.ppjtree : %.jtree
	$(PPJAVA) -i $< | $(PARSEJAVA) -1.5 -o $@

%.jtree : %.java
	$(PARSEJAVA) -1.5 -i $< -o $@

clean-local:
	find . -name "*.jtree" | xargs -r rm
	find . -name "*.ppjtree" | xargs -r rm
	find . -name "*.ppdiff" | xargs -r rm
