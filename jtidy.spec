%{?_javapackages_macros:%_javapackages_macros}
%global jtidyversion r938

Name:             jtidy
Version:          1.0
Release:          0.20.20100930svn1125.1
Epoch:            2
Summary:          HTML syntax checker and pretty printer
Group:		  Development/Java
License:          zlib
URL:              http://jtidy.sourceforge.net/
# svn export -r1125 https://jtidy.svn.sourceforge.net/svnroot/jtidy/trunk/jtidy/ jtidy
# tar caf jtidy.tar.xz jtidy
Source0:          %{name}.tar.xz
Source1:          %{name}.jtidy.script
BuildArch:        noarch

BuildRequires:    java-devel >= 1:1.6.0
BuildRequires:    jpackage-utils
BuildRequires:    ant
BuildRequires:    xml-commons-apis

Requires:         java >= 1:1.6.0
Requires:         jpackage-utils
Requires:         xml-commons-apis

%description
JTidy is a Java port of HTML Tidy, a HTML syntax checker and pretty
printer.  Like its non-Java cousin, JTidy can be used as a tool for
cleaning up malformed and faulty HTML.  In addition, JTidy provides a
DOM interface to the document that is being processed, which
effectively makes you able to use JTidy as a DOM parser for real-world
HTML.

%package javadoc
Summary:          API documentation for %{name}

%description javadoc
This package contains %{summary}.

%prep
%setup -q -n %{name}

%build
ant -Dant.build.javac.source=1.4

%install
# jar
install -d -m 755 %{buildroot}%{_javadir}
install -p -m 644 target/%{name}-%{jtidyversion}.jar %{buildroot}%{_javadir}/%{name}.jar

# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -p -m 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap -a net.sf.jtidy:%{name}

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}/
cp -pr target/javadoc/* %{buildroot}%{_javadocdir}/%{name}/

# shell script
mkdir -p %{buildroot}%{_bindir}
cp -ap %{SOURCE1} %{buildroot}%{_bindir}/%{name}

# ant.d
mkdir -p %{buildroot}%{_sysconfdir}/ant.d
cat > %{buildroot}%{_sysconfdir}/ant.d/%{name} << EOF
jtidy
EOF

%files -f .mfiles
%doc LICENSE.txt
%attr(755, root, root) %{_bindir}/*
%config(noreplace) %{_sysconfdir}/ant.d/%{name}

%files javadoc
%doc LICENSE.txt
%{_javadocdir}/%{name}


%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.0-0.16.20100930svn1125
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 12 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2:1.0-0.15.20100930svn1125
- Update to current packaging guidelines

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2:1.0-0.14.20100930svn1125
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Wed Feb  6 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2:1.0-0.13.20100930svn1125
- Add missing BR and R: xml-commons-apis
- Resolves: rhbz#908421

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.0-0.12.20100930svn1125
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.0-0.11.20100930svn1125
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.0-0.10.20100930svn1125
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 6 2010 Chris Spike <chris.spike@arcor.de> 2:1.0-0.9.20100930svn1125
- Fixed Obsoletes for jtidy-scripts

* Thu Sep 30 2010 Chris Spike <chris.spike@arcor.de> 2:1.0-0.8.20100930svn1125
- Updated to latest upstream svn revision
- Installed pom.xml
- Added 'net.sf.jtidy:jtidy' to maven depmap
- Added 'jtidy:jtidy' to maven depmap

* Tue Sep 28 2010 Chris Spike <chris.spike@arcor.de> 2:1.0-0.7.r938
- Added ant javac source attribute
- Removed version from ant build requires

* Tue Sep 28 2010 Chris Spike <chris.spike@arcor.de> 2:1.0-0.6.r938
- Fixed unversioned Obsoletes
- Fixed wrapper script file permissions

* Mon Sep 27 2010 Chris Spike <chris.spike@arcor.de> 2:1.0-0.5.r938
- Dropped gcj_support
- Updated to latest upstream version
- Moved shell script to main package and obsoleted script subpackage
- Updated description
- Removed xml-commons-apis and jaxp_parser_impl from requires and build requires
- Removed xml-commons-apis from ant config file

* Tue Jan 26 2010 Deepak Bhole <dbhole@redhat.com> - 2:1.0-0.3.r7dev.1.5
- Fixed rhbz#512545 -- updated group

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.0-0.4.r7dev.1.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 20 2009 Deepak Bhole <dbhole@redhat.com> - 2:1.0-0.3.r7dev.1.4
- Add patch to set source to 1.4

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.0-0.3.r7dev.1.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:1.0-0.2.r7dev.1.3
- drop repotag
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2:1.0-0.2.r7dev.1jpp.2
- Autorebuild for GCC 4.3

* Fri Mar 16 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 2:1.0-0.1.r7dev.1jpp.2
- Remove gnu-crypto build requirement.

* Thu Feb 15 2007 Andrew Overholt <overholt@redhat.com> 2:1.0-0.1.r7dev.1jpp.1
- Don't remove JAXP APIs because we don't ship that version of
  xml-commons-apis anymore.

* Mon Feb 12 2007 Fernando Nasser <fnasser@redhat.com> 1:1.0-0.20000804r7dev.8jpp.1
- Import

* Mon Feb 12 2007 Fernando Nasser <fnasser@redhat.com> 1:1.0-0.20000804r7dev.8jpp
- Fix duplicate requires and missing build requires for xml-commons-apis

* Mon Feb 12 2007 Ralph Apel <r.apel at r-apel.de> 1:1.0-0.20000804r7dev.7jpp
- Add gcj_support option

* Thu Jun 01 2006 Fernando Nasser <fnasser@redhat.org> 1:1.0-0.20000804r7dev.6jpp
- First JPP 1.7 build

* Tue Feb 22 2005 David Walluck <david@jpackage.org> 1:1.0-0.20000804r7dev.5jpp
- add ant conf
- own non-versioned javadoc symlink
- Requires: xml-commons-apis
- use build-classpath
- macros

* Sun Aug 23 2004 Randy Watler <rwatler at finali.com> - 1:1.0-0.20000804r7dev.4jpp
- Rebuild with ant-1.6.2

* Mon May  5 2003 Ville Skyttä <ville.skytta at iki.fi> - 1:1.0-0.20000804r7dev.3jpp
- Fix non-versioned javadoc symlinking.

* Mon Apr 21 2003 Ville Skyttä <ville.skytta at iki.fi> - 1:1.0-0.20000804r7dev.2jpp
- Rebuild for JPackage 1.5.
- Fix Group tags.
- Include non-versioned javadoc symlink.
- Scripts subpackage.

* Fri Aug 30 2002 Ville Skyttä <ville.skytta at iki.fi> 1:1.0-0.20000804r7dev.1jpp
- Change version to 1.0, put revision to release, add Epoch.
- Don't use included DOM and SAX, require jaxp_parser_impl.
- Add non-versioned jar symlink.
- Add shell script.
- Vendor, Distribution tags.

* Mon Jan 21 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 20000804-0.r7dev.5jpp
- versioned dir for javadoc
- no dependencies for javadoc package
- section macro

* Mon Dec 17 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 20000804-0.r7dev.4jpp
- new versioning scheme
- jar name is now jtidy.jar
- javadoc in javadoc package

* Wed Nov 21 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 04aug2000r7-dev-3jpp
-  new jpp extension
-  compiled with xalan2

* Mon Nov 19 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 04aug2000r7-dev-2jpp
-  fixed changelog
-  fixed license

* Mon Nov 19 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 04aug2000r7-dev-1jpp
-  r7dev

* Mon Nov 19 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 04aug2000r6-1jpp
-  first release
