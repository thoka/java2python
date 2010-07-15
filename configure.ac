AC_PREREQ([2.58])
AC_INIT([j2py],[0.1],[thomas.kalka@googlemail.com])
AC_CONFIG_AUX_DIR([config])
AM_INIT_AUTOMAKE([1.7.2 -Wall -Wno-portability foreign])

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

#AC_CONFIG_SUBDIRS([syntax])
#  j2py.spec
#  j2py.pc

AC_CONFIG_FILES([
  Makefile
  tools/Makefile
])
AC_OUTPUT
