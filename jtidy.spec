# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define gcj_support 1

Summary:        HTML syntax checker and pretty printer
Name:           jtidy
Version:        1.0
Release:        %mkrel 0.1.r7dev.1.2.9
Epoch:          2
License:        BSD-Style
URL:            http://jtidy.sourceforge.net/
Source0:        http://download.sf.net/jtidy/jtidy-04aug2000r7-dev.zip
Source1:        %{name}.jtidy.script
Patch0:         %{name}.noapis.patch
Requires:       jaxp_parser_impl
Requires:       xml-commons-jaxp-1.3-apis
Requires:       jpackage-utils
BuildRequires:  ant >= 0:1.6
BuildRequires:  java-rpmbuild >= 0:1.5
BuildRequires:  xml-commons-jaxp-1.3-apis
Group:          Development/Java
%if ! %{gcj_support}
BuildArch:      noarch
%else
BuildRequires:  java-devel
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel
%endif

%description
JTidy is a Java port of HTML Tidy, a HTML syntax checker and pretty
printer. Like its non-Java cousin, JTidy can be used as a tool for
cleaning up malformed and faulty HTML. In addition, JTidy provides a DOM
parser for real-world HTML.

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%package scripts
Summary:        Utility scripts for %{name}
Group:          Development/Java
Requires:       jpackage-utils >= 0:1.5
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description scripts
Utility scripts for %{name}.

%prep
%setup -q -n %{name}-04aug2000r7-dev
%patch0 -p0
%remove_java_binaries
# correct silly permissions
%__chmod -R go=u-w *

%build
export CLASSPATH=$(build-classpath xml-commons-jaxp-1.3-apis)
%ant -Dant.build.javac.source=1.4 jar javadoc

%install
%__rm -rf %{buildroot}

# jar
%__mkdir_p %{buildroot}%{_javadir}
%__cp -ap build/Tidy.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
# jar versioning
(cd %{buildroot}%{_javadir} && for jar in *-%{version}.jar; do \
%__ln_s ${jar} `echo $jar| %__sed "s|-%{version}||g"`; done)

# javadoc
%__mkdir_p %{buildroot}%{_javadocdir}/%{name}-%{version}
%__cp -ap doc/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && %__ln_s %{name}-%{version} %{name})

# shell script
%__mkdir_p %{buildroot}%{_bindir}
%__cp -ap %{SOURCE1} %{buildroot}%{_bindir}/%{name}

# ant.d
%__mkdir_p %{buildroot}%{_sysconfdir}/ant.d
%__cat > %{buildroot}%{_sysconfdir}/ant.d/%{name} << EOF
jtidy xml-commons-jaxp-1.3-apis
EOF

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%__rm -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}
%endif

%if %{gcj_support}
%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc LICENSE NOTES doc/devel
%{_javadir}/*
%config(noreplace) %{_sysconfdir}/ant.d/%{name}
%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/*

%files scripts
%defattr(0755,root,root,0755)
%{_bindir}/*
