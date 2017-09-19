%global scl_name_base eclipse
%global scl_name_version 46
%global scl rh-%{scl_name_base}%{scl_name_version}

# Do not produce empty debuginfo package
%global debug_package %{nil}

%scl_package %scl

Summary: Package that installs %scl
Name: %scl_name
Version: 1
Release: 15%{?dist}
License: GPLv2+

Source0: README
Source1: LICENSE
Source2: macros.xmvn

BuildRequires: scl-utils-build >= 20120927-11
BuildRequires: help2man

Requires: %{name}-base = %{version}-%{release}
Requires: %{scl_prefix}eclipse-cdt
Requires: %{scl_prefix}eclipse-cdt-docker
Requires: %{scl_prefix}eclipse-cdt-llvm
Requires: %{scl_prefix}eclipse-cdt-parsers
Requires: %{scl_prefix}eclipse-cdt-qt
Requires: %{scl_prefix}eclipse-changelog
Requires: %{scl_prefix}eclipse-dltk
Requires: %{scl_prefix}eclipse-dltk-mylyn
Requires: %{scl_prefix}eclipse-dltk-rse
Requires: %{scl_prefix}eclipse-dltk-ruby
Requires: %{scl_prefix}eclipse-dltk-sh
Requires: %{scl_prefix}eclipse-dltk-tcl
Requires: %{scl_prefix}eclipse-gcov
Requires: %{scl_prefix}eclipse-gprof
Requires: %{scl_prefix}eclipse-launchbar
Requires: %{scl_prefix}eclipse-linuxtools
Requires: %{scl_prefix}eclipse-linuxtools-javadocs
Requires: %{scl_prefix}eclipse-linuxtools-libhover
Requires: %{scl_prefix}eclipse-manpage
Requires: %{scl_prefix}eclipse-mylyn-context-cdt
Requires: %{scl_prefix}eclipse-oprofile
Requires: %{scl_prefix}eclipse-perf
Requires: %{scl_prefix}eclipse-ptp
Requires: %{scl_prefix}eclipse-ptp-gem
Requires: %{scl_prefix}eclipse-ptp-rm-contrib
Requires: %{scl_prefix}eclipse-ptp-sci
Requires: %{scl_prefix}eclipse-ptp-sdm
Requires: %{scl_prefix}eclipse-pydev
Requires: %{scl_prefix}eclipse-pydev-mylyn
Requires: %{scl_prefix}eclipse-remote
Requires: %{scl_prefix}eclipse-rpm-editor
Requires: %{scl_prefix}eclipse-rse
Requires: %{scl_prefix}eclipse-rse-server
Requires: %{scl_prefix}eclipse-systemtap
Requires: %{scl_prefix}eclipse-valgrind

%description
This is the main package for %scl Software Collection.
Installs all Eclipse packages available in this SCL.

%package base
Summary: Package that installs a minimal %scl
Requires: %{name}-runtime = %{version}-%{release}
Requires: %{scl_prefix}eclipse-abrt
Requires: %{scl_prefix}eclipse-cdt-native
Requires: %{scl_prefix}eclipse-ecf-core
Requires: %{scl_prefix}eclipse-ecf-runtime
Requires: %{scl_prefix}eclipse-egit
Requires: %{scl_prefix}eclipse-egit-mylyn
Requires: %{scl_prefix}eclipse-emf-core
Requires: %{scl_prefix}eclipse-emf-runtime
Requires: %{scl_prefix}eclipse-epp-logging
Requires: %{scl_prefix}eclipse-equinox-osgi
Requires: %{scl_prefix}eclipse-filesystem
Requires: %{scl_prefix}eclipse-gef
Requires: %{scl_prefix}eclipse-jdt
Requires: %{scl_prefix}eclipse-jgit
Requires: %{scl_prefix}eclipse-linuxtools-docker
Requires: %{scl_prefix}eclipse-linuxtools-vagrant
Requires: %{scl_prefix}eclipse-m2e-core
Requires: %{scl_prefix}eclipse-mpc
Requires: %{scl_prefix}eclipse-mylyn
Requires: %{scl_prefix}eclipse-mylyn-builds
Requires: %{scl_prefix}eclipse-mylyn-builds-hudson
Requires: %{scl_prefix}eclipse-mylyn-context-java
Requires: %{scl_prefix}eclipse-mylyn-context-pde
Requires: %{scl_prefix}eclipse-mylyn-docs-epub
Requires: %{scl_prefix}eclipse-mylyn-docs-wikitext
Requires: %{scl_prefix}eclipse-mylyn-tasks-bugzilla
Requires: %{scl_prefix}eclipse-mylyn-tasks-trac
Requires: %{scl_prefix}eclipse-mylyn-tasks-web
Requires: %{scl_prefix}eclipse-mylyn-versions
Requires: %{scl_prefix}eclipse-mylyn-versions-cvs
Requires: %{scl_prefix}eclipse-mylyn-versions-git
Requires: %{scl_prefix}eclipse-p2-discovery
Requires: %{scl_prefix}eclipse-pde
Requires: %{scl_prefix}eclipse-platform
Requires: %{scl_prefix}eclipse-swt
Requires: %{scl_prefix}eclipse-testng
Requires: %{scl_prefix}eclipse-tm-terminal
Requires: %{scl_prefix}eclipse-tm-terminal-connectors
Requires: %{scl_prefix}eclipse-usage
Requires: %{scl_prefix}eclipse-webtools-common
Requires: %{scl_prefix}eclipse-webtools-javaee
Requires: %{scl_prefix}eclipse-webtools-jsf
Requires: %{scl_prefix}eclipse-webtools-servertools
Requires: %{scl_prefix}eclipse-webtools-sourceediting
Requires: %{scl_prefix}eclipse-xsd

%description base
This is the base package for %scl Software Collection.
Installs the set of Eclipse packages that are shared between this SCL and
Red Hat Devstudio.

%package runtime
Summary: Runtime scripts for the %scl Software Collection
Requires: scl-utils >= 20120927-11
Requires: rh-java-common-runtime
# Eclipse requires Java 8 to run and build
Requires: java-1.8.0-openjdk-devel

%description runtime
Package shipping essential scripts to work with the %scl Software
Collection.

%package build
Summary: Build configuration for the %scl Software Collection
Requires: scl-utils-build >= 20120927-11
Requires: %{name}-scldevel = %{version}-%{release}

%description build
Package shipping essential configuration macros to build the %scl
Software Collection itself.

%package scldevel
Summary: Development files for the %scl Software Collection
Requires: %{name}-runtime = %{version}-%{release}
Requires: rh-maven33-scldevel

%description scldevel
Package shipping development files, especially useful for development of
packages depending on the %scl Software Collection.

%prep
%setup -c -T

# Prepare documentation
cat > README << EOF
%{expand:%(cat %{SOURCE0})}
EOF
cp %{SOURCE1} .

# Macro overrides
cp %{SOURCE2} macros.xmvn.x.%{scl}

%build
# Enable collection script
# ========================
cat <<EOF >enable
#!/bin/bash

# We have a run-time dependency on java-common, enable it first
. scl_source enable rh-java-common

# The IDE has optional deps on other collections, so enable them if present
if test -e /opt/rh/devtoolset-6/enable ; then
  . scl_source enable devtoolset-6
fi
if test -e /opt/rh/python27/enable ; then
  . scl_source enable python27
fi
if test -e /opt/rh/python33/enable ; then
  . scl_source enable python33
fi
if test -e /opt/rh/rh-python34/enable ; then
  . scl_source enable rh-python34
fi
if test -e /opt/rh/rh-python35/enable ; then
  . scl_source enable rh-python35
fi

# General environment variables
export PATH=%{_bindir}:%{_prefix}/lib/jvm/java/bin\${PATH:+:\${PATH}}
export MANPATH=%{_mandir}:\${MANPATH}

# Needed by Java Packages Tools to locate java.conf
export JAVACONFDIRS="%{_sysconfdir}/java:\${JAVACONFDIRS:-/etc/java}"

# Required by XMvn to locate its configuration files
export XDG_CONFIG_DIRS="%{_sysconfdir}/xdg:\${XDG_CONFIG_DIRS:-/etc/xdg}"
export XDG_DATA_DIRS="%{_datadir}:\${XDG_DATA_DIRS:-/usr/local/share:/usr/share}"

# Some perl Ext::MakeMaker versions install things under /usr/lib/perl5
# even though the system otherwise would go to /usr/lib64/perl5.
export PERL5LIB=%{_scl_root}/%{perl_vendorarch}:%{_scl_root}/usr/lib/perl5:%{_scl_root}/%{perl_vendorlib}\${PERL5LIB:+:\${PERL5LIB}}
# bz847911 workaround:
# we need to evaluate rpm's installed run-time % { _libdir }, not rpmbuild time
# or else /etc/ld.so.conf.d files?
rpmlibdir=\$(rpm --eval "%%{_libdir}")
# bz1017604: On 64-bit hosts, we should include also the 32-bit library path.
if [ "\$rpmlibdir" != "\${rpmlibdir/lib64/}" ]; then
  rpmlibdir32=":%{_scl_root}\${rpmlibdir/lib64/lib}"
fi
export LD_LIBRARY_PATH=%{_scl_root}\$rpmlibdir\$rpmlibdir32\${LD_LIBRARY_PATH:+:\${LD_LIBRARY_PATH}}
EOF

# Java configuration
# ==================
cat <<EOF >java.conf
JAVA_LIBDIR=%{_prefix}/share/java
JNI_LIBDIR=%{_prefix}/lib/java
JVM_ROOT=%{_prefix}/lib/jvm
EOF

# Javapackages config
# ===================
cat <<EOF >javapackages-config.json
{
    "maven.req": {
	"always_generate": [
	    "%{scl}-runtime"
	],
	"java_requires": {
	    "package_name": "java",
	    "always_generate": true,
	    "skip": false
	},
	"java_devel_requires": {
	    "package_name": "java-devel",
	    "always_generate": false,
	    "skip": false
	}
    },
    "javadoc.req": {
	"always_generate": [
	    "%{scl}-runtime"
	]
    }
}
EOF

# Ivy configuration
# =================
cat <<EOF >ivysettings.xml
<!-- Ivy configuration file for %{scl} software collection
     Artifact resolution order is:
      1. %{scl} collection
      2. rh-java-common collection
      3. rh-maven33 collection
-->
<ivysettings>
  <settings defaultResolver="default"/>
  <resolvers>
    <filesystem name="%{scl}-public">
      <ivy pattern="\${ivy.conf.dir}/lib/[module]/apache-ivy-[revision].xml" />
      <artifact pattern="%{_datadir}/java/\[artifact].[ext]" />
    </filesystem>
    <filesystem name="rh-java-common-public">
      <ivy pattern="\${ivy.conf.dir}/lib/[module]/apache-ivy-[revision].xml" />
      <artifact pattern="/opt/rh/rh-java-common/root/%{_root_datadir}/java/\[artifact].[ext]" />
    </filesystem>
    <filesystem name="rh-maven33-public">
      <ivy pattern="\${ivy.conf.dir}/lib/[module]/apache-ivy-[revision].xml" />
      <artifact pattern="/opt/rh/rh-maven33/root/%{_root_datadir}/java/\[artifact].[ext]" />
    </filesystem>
    <filesystem name="public">
      <ivy pattern="\${ivy.conf.dir}/lib/[module]/apache-ivy-[revision].xml" />
      <artifact pattern="%{_root_datadir}/java/\[artifact].[ext]" />
    </filesystem>
    <chain name="main" dual="true">
      <resolver ref="%{scl}-public"/>
      <resolver ref="rh-java-common-public"/>
      <resolver ref="rh-maven33-public"/>
      <resolver ref="public"/>
    </chain>
  </resolvers>
  <include url="\${ivy.default.settings.dir}/ivysettings-local.xml"/>
  <include url="\${ivy.default.settings.dir}/ivysettings-default-chain.xml"/>
</ivysettings>
EOF

# XMvn configuration
# ==================
cat <<EOF >configuration.xml
<?xml version="1.0" encoding="US-ASCII"?>
<!-- XMvn configuration file for %{scl} software collection
     Artifact resolution order is:
      1. %{scl} collection
      2. rh-java-common collection
      3. rh-maven33 collection
-->
<configuration xmlns="http://fedorahosted.org/xmvn/CONFIG/2.0.0">
  <resolverSettings>
    <metadataRepositories>
      <repository>/opt/rh/%{scl}/root/usr/share/maven-metadata</repository>
      <repository>/opt/rh/rh-java-common/root/usr/share/maven-metadata</repository>
      <repository>/opt/rh/rh-maven33/root/usr/share/maven-metadata</repository>
    </metadataRepositories>
    <prefixes>
      <prefix>/opt/rh/%{scl}/root</prefix>
      <prefix>/opt/rh/rh-java-common/root</prefix>
      <prefix>/opt/rh/rh-maven33/root</prefix>
    </prefixes>
  </resolverSettings>
  <installerSettings>
    <metadataDir>opt/rh/%{scl}/root/usr/share/maven-metadata</metadataDir>
  </installerSettings>
  <repositories>
    <repository>
      <id>resolve-%{scl}</id>
      <type>compound</type>
      <properties>
        <prefix>/opt/rh/%{scl}/root</prefix>
        <namespace>%{scl}</namespace>
      </properties>
      <configuration>
        <repositories>
          <repository>base-resolve</repository>
        </repositories>
      </configuration>
    </repository>
    <repository>
      <id>resolve-rh-java-common</id>
      <type>compound</type>
      <properties>
        <prefix>/opt/rh/rh-java-common/root</prefix>
        <namespace>rh-java-common</namespace>
      </properties>
      <configuration>
        <repositories>
          <repository>base-resolve</repository>
        </repositories>
      </configuration>
    </repository>
    <repository>
      <id>resolve-rh-maven33</id>
      <type>compound</type>
      <properties>
        <prefix>/opt/rh/rh-maven33/root</prefix>
        <namespace>rh-maven33</namespace>
      </properties>
      <configuration>
        <repositories>
          <repository>base-resolve</repository>
        </repositories>
      </configuration>
    </repository>
    <repository>
      <id>resolve-local</id>
      <type>maven</type>
      <properties>
        <root>.m2</root>
      </properties>
    </repository>
    <repository>
      <id>resolve</id>
      <type>compound</type>
      <configuration>
        <repositories>
	  <!-- Put resolvers in order you want to use them, from
	       highest to lowest preference. (resolve-local is
	       resolver that resolves from local Maven repository in
	       .xm2 in current directory.) -->
          <repository>resolve-local</repository>
          <repository>resolve-%{scl}</repository>
          <repository>resolve-rh-java-common</repository>
          <repository>resolve-rh-maven33</repository>
        </repositories>
      </configuration>
    </repository>
    <repository>
      <id>install</id>
      <type>compound</type>
      <properties>
        <prefix>opt/rh/%{scl}/root</prefix>
        <namespace>%{scl}</namespace>
      </properties>
      <configuration>
        <repositories>
          <repository>base-install</repository>
        </repositories>
      </configuration>
    </repository>
  </repositories>
</configuration>
EOF

# SCL devel macros
# ================
cat <<EOF >macros.%{scl}-scldevel
%%scl_%{scl_name_base} %{scl}
%%scl_prefix_%{scl_name_base} %{scl_prefix}
EOF

# Additional SCL build macros
# ===========================
cat <<EOF >macros.%{scl}-config
%%app_name_prefix Red Hat Eclipse 4.6
%%app_exec_prefix scl enable %{scl_name}
EOF

# Generate a helper script that will be used by help2man
cat <<EOF >h2m_helper
#!/bin/bash
[ "\$1" == "--version" ] && echo "%{scl_name} %{version} Software Collection" || cat README
EOF
chmod a+x h2m_helper

# Generate the man page
help2man -N --section 7 ./h2m_helper -o %{scl_name}.7

%install
(%{scl_install})

# Install scl scripts
install -d -m 755 %{buildroot}%{_scl_scripts}
install -p -m 755 enable %{buildroot}%{_scl_scripts}/

# Install man page
install -d -m 755 %{buildroot}%{_mandir}/man7
install -p -m 644 %{scl_name}.7 %{buildroot}%{_mandir}/man7/

# Install rpm macros
install -d -m 755 %{buildroot}%{_root_sysconfdir}/rpm
install -p -m 644 macros.%{scl}-scldevel %{buildroot}%{_root_sysconfdir}/rpm/
install -p -m 644 macros.xmvn.x.%{scl} %{buildroot}%{_root_sysconfdir}/rpm/

# Install java, ivy and xmvn config
install -d -m 755 %{buildroot}%{_sysconfdir}/java
install -d -m 755 %{buildroot}%{_sysconfdir}/java/security
install -d -m 755 %{buildroot}%{_sysconfdir}/java/security/security.d
install -p -m 644 java.conf %{buildroot}%{_sysconfdir}/java/
install -p -m 644 javapackages-config.json %{buildroot}%{_sysconfdir}/java/
install -d -m 755 %{buildroot}%{_sysconfdir}/ivy
install -p -m 644 ivysettings.xml %{buildroot}%{_sysconfdir}/ivy/
install -d -m 755 %{buildroot}%{_sysconfdir}/xdg/xmvn
install -p -m 644 configuration.xml %{buildroot}%{_sysconfdir}/xdg/xmvn/

# Other directories that should be owned by the runtime
install -d -m 755 %{buildroot}%{_datadir}/appdata
# Otherwise unowned java directories (native java bits are always in /usr/lib even on 64bit arches)
install -d -m 755 %{buildroot}%{_prefix}/share/java
install -d -m 755 %{buildroot}%{_prefix}/share/javadoc
install -d -m 755 %{buildroot}%{_prefix}/lib/java
install -d -m 755 %{buildroot}%{_prefix}/lib/jvm
# Otherwise unowned maven directories
install -d -m 755 %{buildroot}%{_datadir}/maven-metadata
install -d -m 755 %{buildroot}%{_datadir}/maven-poms
# Otherwise unowned perl directories
install -d -m 755 %{buildroot}%{_libdir}/perl5
install -d -m 755 %{buildroot}%{_libdir}/perl5/vendor_perl
install -d -m 755 %{buildroot}%{_libdir}/perl5/vendor_perl/auto

# Symlink to JVM in base operating system
ln -s -T %{_root_prefix}/lib/jvm/java-1.8.0 %{buildroot}%{_prefix}/lib/jvm/java
ln -s -T %{_root_prefix}/share/javadoc/java %{buildroot}%{_prefix}/share/javadoc/java

# Additional SCL build macros
cat macros.%{scl}-config >> %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl}-config

# Usage marker
install -d -m 755 %{buildroot}%{_libdir}/eclipse/.pkgs
echo "%{version}-%{release}" > %{buildroot}%{_libdir}/eclipse/.pkgs/RHSCL

# Be more explicit about the content of libdir in the files list
cat <<EOF | sed -e 's|\(.*%{_libdir}$\)|%%dir \1|' > filelist-scl
%scl_files
%%attr(555,root,root) %{_libdir}/games
%%attr(555,root,root) %{_libdir}/perl5
%%attr(555,root,root) %{_libdir}/pm-utils
%%attr(555,root,root) %{_libdir}/sse2
%%attr(555,root,root) %{_libdir}/tls
%%attr(555,root,root) %{_libdir}/X11
EOF

%files
# Metapackage only, empty file list except for usage marker
%{_libdir}/eclipse/.pkgs

%files base
# Metapackage only, empty file list

%files runtime -f filelist-scl -f filelist
%doc README LICENSE
%{_sysconfdir}/ivy
%{_sysconfdir}/java
%dir %{_datadir}/appdata
%dir %{_prefix}/share/java
%dir %{_prefix}/share/javadoc
%dir %{_prefix}/lib/java
%dir %{_prefix}/lib/jvm
%dir %{_datadir}/maven-metadata
%dir %{_datadir}/maven-poms
%{_prefix}/lib/jvm/java
%{_prefix}/share/javadoc/java

%files build
%{_root_sysconfdir}/rpm/macros.%{scl}-config
%{_root_sysconfdir}/rpm/macros.xmvn.x.%{scl}

%files scldevel
%{_root_sysconfdir}/rpm/macros.%{scl}-scldevel

%changelog
* Sun Apr 02 2017 Mat Booth <mat.booth@redhat.com> - 1-15
- Include Eclipse version number in desktop app shortcut names

* Fri Jan 20 2017 Mat Booth <mat.booth@redhat.com> - 1-14
- Add deps on m2e and testng to base package

* Tue Oct 25 2016 Mat Booth <mat.booth@redhat.com> - 1-13
- Add dep on usage plugin and install marker file

* Fri Oct 21 2016 Mat Booth <mat.booth@redhat.com> - 1-12
- Move deps from main package to base to satisfy requirements for devstudio

* Fri Aug 12 2016 Mat Booth <mat.booth@redhat.com> - 1-11
- Adjust requirements for new tm-terminal package

* Wed Aug 03 2016 Mat Booth <mat.booth@redhat.com> - 1-10
- Add requires on webtools packages

* Tue Aug 02 2016 Mat Booth <mat.booth@redhat.com> - 1-9
- Add more requires to base package

* Mon Aug 01 2016 Mat Booth <mat.booth@redhat.com> - 1-8
- Add macros to configure application names for the collection

* Mon Aug 01 2016 Mat Booth <mat.booth@redhat.com> - 1-7
- Split installation between main metapackage and "base" metapackage,
  rhbz#1361195
- Enable DTS 6, if installed

* Fri Jul 22 2016 Mat Booth <mat.booth@redhat.com> - 1-6
- Improve RPM macros to deal with native jars

* Fri Jul 22 2016 Mat Booth <mat.booth@redhat.com> - 1-5
- Ensure JVM symlinks are always for Java 8 by default

* Thu Jul 21 2016 Mat Booth <mat.booth@redhat.com> - 1-4
- Add symlinks to base OS version of JVM for use during package builds

* Thu Jul 21 2016 Mat Booth <mat.booth@redhat.com> - 1-3
- Ensure Java 8 is available

* Wed Jul 20 2016 Mat Booth <mat.booth@redhat.com> - 1-2
- Install xmvn macro overrides

* Tue Jul 19 2016 Mat Booth <mat.booth@redhat.com> - 1-1
- Commit initial package.

