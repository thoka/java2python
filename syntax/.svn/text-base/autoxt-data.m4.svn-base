#                                                       -*- Autoconf -*-
# serial 3
#
# Author: Martin Bravenboer
#
# Extension of AutoXT for packages that only depend on Stratego/XT for
# bootstrapping. After bootstrapping, there is no dependency on Stratego/XT
# or the Stratego Libraries.

m4_pattern_forbid([^XT_])
m4_pattern_forbid([^PKG_CHECK_MODULES$])
m4_pattern_allow([^XT_BOOTSTRAP(_TRUE|_FALSE)?$])

# XT_DATA_PACKAGE
# ----------------------------
AC_DEFUN([XT_DATA_PACKAGE],
[
  AC_ARG_ENABLE([bootstrap],
    [AS_HELP_STRING([--enable-bootstrap], [enable a bootstrap build (requires Stratego/XT) @<:@default=no@:>@])],
    [xt_bootstrap="$enableval"])

  AC_ARG_WITH([strategoxt],
    [AS_HELP_STRING([--with-strategoxt=DIR], [use Stratego/XT at DIR @<:@find with pkg-config@:>@])],
    [STRATEGOXT=$withval])

  AC_ARG_WITH([sdf],
    [AS_HELP_STRING([--with-sdf=DIR], [use SDF Packages at DIR @<:@find with pkg-config@:>@])],
    [SDF=$withval])

  # If Stratego/XT is given, then enable bootstrap
  if test "${STRATEGOXT:+set}" = set; then
    if test "${xt_bootstrap:-set}" = set; then
      xt_bootstrap="yes"
    fi
  else
    if test "${xt_bootstrap:-set}" = set; then
      xt_bootstrap="no"
    fi
  fi

  AM_CONDITIONAL([XT_BOOTSTRAP], [test "$xt_bootstrap" = "yes"])

  AC_MSG_CHECKING([whether bootstrap build is enabled])
  if test "$xt_bootstrap" = "yes"; then
    AC_MSG_RESULT([yes])

    AC_MSG_CHECKING([whether location of Stratego/XT is explicitly set])
    if test "${STRATEGOXT:+set}" = set; then
      AC_MSG_RESULT([yes])
    else
      AC_MSG_RESULT([no])
      PKG_CHECK_MODULES([STRATEGOXT],[strategoxt])
      XT_CHECK_PACKAGE_PREFIX([STRATEGOXT],[strategoxt])
    fi

    AC_MSG_CHECKING([whether location of SDF Packages is explicitly set])
    if test "${SDF:+set}" = set; then
      AC_MSG_RESULT([yes])
    else
      AC_MSG_RESULT([no])
      PKG_CHECK_MODULES([SDF],[sdf2-bundle])
      XT_CHECK_PACKAGE_PREFIX([SDF],[sdf2-bundle])
    fi

    AC_SUBST([STRATEGOXT])
    AC_SUBST([SDF])
    AC_SUBST([SGLR], ['$(SDF)/bin/sglr'])
    AC_SUBST([SDF2TABLE], ['$(SDF)/bin/sdf2table'])
    AC_SUBST([PACKSDF], ['$(STRATEGOXT)/bin/pack-sdf'])
    AC_SUBST([GENSDFMIX], ['$(STRATEGOXT)/bin/gen-sdf-mix'])
    AC_SUBST([SDF2RTG], ['$(STRATEGOXT)/bin/sdf2rtg'])
    AC_SUBST([PARSEUNIT], ['$(STRATEGOXT)/bin/parse-unit'])
  else
    AC_MSG_RESULT([no])
  fi
])

# XT_CHECK_PACKAGE_PREFIX
# -----------------------
AC_DEFUN([XT_CHECK_PACKAGE_PREFIX],
[ AC_MSG_CHECKING([prefix of package $2])
  $1=`$PKG_CONFIG --variable=prefix "$2"`
  if test -z "$$1"; then
    AC_MSG_ERROR([package $2 does not specify its prefix in the pkg-config file.
          Report this error to the maintainer of this package.])
  else
    AC_MSG_RESULT([$$1])
  fi
])
