AC_PREREQ([2.58])
AC_INIT([java-front],[0.9.1],[users@strategoxt.org])
AC_CONFIG_AUX_DIR([config])
AM_INIT_AUTOMAKE([1.7.2 -Wall -Wno-portability])

# comment to make this a stable release
XT_PRE_RELEASE

m4_pattern_forbid([^(AB|XT)_])
m4_pattern_forbid([^PKG_CHECK_MODULES$])

test "x$prefix" = xNONE && prefix=$ac_default_prefix

XT_SETUP
XT_USE_BOOTSTRAP_XT_PACKAGES

AC_PROG_CC
AC_PROG_INSTALL
AC_PROG_LN_S
AC_PROG_LIBTOOL

AC_CONFIG_SUBDIRS([syntax])
AC_CONFIG_FILES([
  java-front.spec
  java-front.pc
  Makefile
  news-archive/Makefile
    
  syntax-embedding/Makefile
  lib/Makefile
  tools/Makefile
  
  test/Makefile
  test/syn/Makefile
  test/syn/Java/Makefile
  test/syn/StrategoJava/Makefile
  test/gnu-classpath/Makefile
  test/gnu-classpath/v1.5/Makefile
  test/j2sdk/Makefile
  test/pp/Makefile
])
AC_OUTPUT
