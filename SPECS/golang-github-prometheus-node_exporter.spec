# If any of the following macros should be set otherwise,
# you can wrap any of them with the following conditions:
# - %%if 0%%{centos} == 7
# - %%if 0%%{?rhel} == 7
# - %%if 0%%{?fedora} == 23
# Or just test for particular distribution:
# - %%if 0%%{centos}
# - %%if 0%%{?rhel}
# - %%if 0%%{?fedora}
#
# Be aware, on centos, both %%rhel and %%centos are set. If you want to test
# rhel specific macros, you can use %%if 0%%{?rhel} && 0%%{?centos} == 0 condition.
# (Don't forget to replace double percentage symbol with single one in order to apply a condition)

%global provider        github
%global provider_tld    com
%global project         prometheus
%global repo            node_exporter
# https://github.com/prometheus/node_exporter
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}

Name:           golang-%{provider}-%{project}-%{repo}
Version:        %{getenv:NODE_EXPORTER_VERSION}
Release:        1%{?dist}
Summary:        Exporter for machine metrics
License:        ASL 2.0
URL:            https://%{provider_prefix}
Source0:        node_exporter
Source1:        sysconfig.node_exporter
Source2:        node_exporter.service
Source3:        node_exporter_textfile_wrapper.sh
Source4:        textfile_collectors_README

Provides:       node_exporter = %{version}-%{release}


%description
%{summary}

%install
install -d -p   %{buildroot}%{_sbindir} \
                %{buildroot}%{_defaultdocdir}/node_exporter \
                %{buildroot}%{_sysconfdir}/sysconfig \
                %{buildroot}%{_sysconfdir}/prometheus/node_exporter/text_collectors

%if 0%{?rhel} != 6
install -d -p   %{buildroot}%{_unitdir}
%endif

install -p -m 0644 %{_sourcedir}/textfile_collectors_README %{buildroot}%{_sysconfdir}/prometheus/node_exporter/text_collectors/README
install -p -m 0644 %{_sourcedir}/sysconfig.node_exporter %{buildroot}%{_sysconfdir}/sysconfig/node_exporter
%if 0%{?rhel} != 6
install -p -m 0644 %{_sourcedir}/node_exporter.service %{buildroot}%{_unitdir}/node_exporter.service
%endif
install -p -m 0755 %{_sourcedir}/node_exporter_textfile_wrapper.sh %{buildroot}%{_sbindir}/node_exporter_textfile_wrapper
install -p -m 0755 %{_sourcedir}/node_exporter %{buildroot}%{_sbindir}/node_exporter

%files
%if 0%{?rhel} != 6
%{_unitdir}/node_exporter.service
%endif
%config(noreplace) %{_sysconfdir}/sysconfig/node_exporter
%config %{_sysconfdir}/prometheus/node_exporter/text_collectors/README
%{_sbindir}/*

%pre
getent group node_exporter > /dev/null || groupadd -r node_exporter
getent passwd node_exporter > /dev/null || \
    useradd -rg node_exporter -d /var/lib/node_exporter -s /sbin/nologin \
            -c "Prometheus node exporter" node_exporter
mkdir -p /var/lib/node_exporter/textfile_collector
chgrp node_exporter /var/lib/node_exporter/textfile_collector
chmod 771 /var/lib/node_exporter/textfile_collector

%post
%if 0%{?rhel} != 6
%systemd_post node_exporter.service
%endif

%preun
%if 0%{?rhel} != 6
%systemd_preun node_exporter.service
%endif

%postun
%if 0%{?rhel} != 6
%systemd_postun node_exporter.service
%endif

%changelog
* Tue Apr 20 2021 Kristian Berg <kristian.berg@tietoevry.com> 1.1.2-1
- Rewrote spec to use externally built binary (kristian.berg@tietoevry.com)

* Wed Jun 17 2020 Tobias Florek <tob@butter.sh> 1.0.1-1
- bump version to v1.0.1 (tob@butter.sh)

* Fri May 29 2020 Tobias Florek <tob@butter.sh> 1.0.0-1
- bump version to v1.0.0 (tob@butter.sh)

* Thu Jun 13 2019 Tobias Florek <tob@butter.sh> 0.18.1-6
- add missing argument to systemd_postun for f31+ (tob@butter.sh)

* Thu Jun 13 2019 Tobias Florek <tob@butter.sh> 0.18.1-5
- buildrequire git (tob@butter.sh)

* Thu Jun 13 2019 Tobias Florek <tob@butter.sh> 0.18.1-4
- really don't try to patch obsolete patch (tob@butter.sh)

* Thu Jun 13 2019 Tobias Florek <tob@butter.sh> 0.18.1-3
- remove obsolete build fix (tob@butter.sh)

* Thu Jun 13 2019 Tobias Florek <tob@butter.sh> 0.18.1-2
- bump version to v0.18.1 (tob@butter.sh)

* Wed Jan 23 2019 Tobias Florek <tob@butter.sh> 0.17.0-9
- only apply patch for fedora and rhel > 7 (tob@butter.sh)
- also include patch file (tob@butter.sh)
- use upstream go.sum patch to fix checksum errors (tob@butter.sh)
- Revert "add -mod=vendor to go build flags" (tob@butter.sh)
- Revert "clean go modcache to work around checksum errors" (tob@butter.sh)

* Wed Jan 23 2019 Tobias Florek <tob@butter.sh> 0.17.0-8
- clean go modcache to work around checksum errors (tob@butter.sh)
- add -mod=vendor to go build flags (tob@butter.sh)

* Tue Jan 22 2019 Tobias Florek <tob@butter.sh> 0.17.0-7
- hopefully fix setting version (tob@butter.sh)
- Make text collector folder writable for the group
  (mohsen0@users.noreply.github.com)
- Revert "use go-toolkit-7 scl on rhel7" (tob@butter.sh)
- use go-toolkit-7 scl on rhel7 (tob@butter.sh)
- use rhel macro instead of centos to allow rhel builds (tob@butter.sh)
- also reset release no when bumping version (tob@butter.sh)
- fix documentation re tito (tob@butter.sh)
- add script to help in making new releases (tob@butter.sh)

* Tue Dec 04 2018 Tobias Florek <tob@butter.sh> 0.17.0-6
- bump version to v0.17.0 (tob@butter.sh)

* Sun Aug 05 2018 Tobias Florek <tob@butter.sh> 0.16.0-5
- Configure systemd to restart node_exporter.service (evan@eklitzke.org)

* Mon May 21 2018 Tobias Florek <tob@butter.sh> 0.16.0-4
- don't require systemd on centos6 (tob@butter.sh)

* Mon May 21 2018 Tobias Florek <tob@butter.sh> 0.16.0-3
- fix wrong tag

* Mon May 21 2018 Tobias Florek <tob@butter.sh>
- tag fix wrong tag

* Wed May 16 2018 Tobias Florek <tob@butter.sh> 0.16.0-1
- bump to 0.16.0 (tob@butter.sh)

* Mon Jan 08 2018 Tobias Florek <tob@butter.sh> 0.15.2-13
- textfile_wrapper: set permissions for generated files (tob@butter.sh)

* Mon Jan 08 2018 Tobias Florek <tob@butter.sh> 0.15.2-12
- also include README in the rpm (tob@butter.sh)

* Mon Jan 08 2018 Tobias Florek <tob@butter.sh> 0.15.2-11
- fix directory name typo (tob@butter.sh)

* Sun Jan 07 2018 Tobias Florek <tob@butter.sh> 0.15.2-10
- fix missing source (tob@butter.sh)

* Sun Jan 07 2018 Tobias Florek <tob@butter.sh> 0.15.2-9
- add textfile script wrapper (tob@butter.sh)

* Sun Jan 07 2018 Tobias Florek <tob@butter.sh> 0.15.2-8
- fix default sysconfig option (tob@butter.sh)

* Sat Jan 06 2018 Tobias Florek <tob@butter.sh> 0.15.2-7
- fix version strings also on el7 (tob@butter.sh)

* Fri Jan 05 2018 Tobias Florek <tob@butter.sh> 0.15.2-6
- fix missing version string in binary (tob@butter.sh)

* Thu Jan 04 2018 Tobias Florek <tob@butter.sh> 0.15.2-5
- resubmit

* Thu Jan 04 2018 Tobias Florek <tob@butter.sh> 0.15.2-4
- fix tarball (tob@butter.sh)

* Thu Jan 04 2018 Tobias Florek <tob@butter.sh> - 0.15.2-3
- fix tarball

* Thu Jan 04 2018 Tobias Florek <tob@butter.sh> 0.15.2-2
- bump to v0.15.2 (tob@butter.sh)
- add license file (tob@butter.sh)

* Thu Jan 04 2018 Tobias Florek <tob@butter.sh> - 0.15.2-1
- new version

* Thu Mar 23 2017 Tobias Florek <tob@butter.sh> 0.14.0-5
- fix typo in textfile dir (tob@butter.sh)

* Wed Mar 22 2017 Tobias Florek <tob@butter.sh> 0.14.0-4
- rename textfile dir according to upstream preference (tob@butter.sh)

* Wed Mar 22 2017 Tobias Florek <tob@butter.sh> 0.14.0-3
- really fix sysconfig and systemd file (tob@butter.sh)

* Wed Mar 22 2017 Tobias Florek <tob@butter.sh> 0.14.0-2
- fix installing sysconfig file and systemd unit (tob@butter.sh)

* Tue Mar 21 2017 Tobias Florek <tob@butter.sh> 0.14.0-1
- Upgrade to stable 0.14.0

* Thu Mar 09 2017 Tobias Florek <tob@butter.sh> 0.14.0_rc2-6
- add textfile directory (tob@butter.sh)
- move node_exporter to sbin (tob@butter.sh)

* Thu Mar 09 2017 Tobias Florek <tob@butter.sh> 0.14.0_rc2-5
- install systemd unit, really create user (tob@butter.sh)

* Thu Mar 09 2017 Tobias Florek <tob@butter.sh> 0.14.0_rc2-4
- let the main package provide node_exporter (tob@butter.sh)

* Thu Mar 09 2017 Tobias Florek <tob@butter.sh> 0.14.0_rc2-3
- provide node_exporter package (tob@butter.sh)

* Wed Mar 08 2017 Tobias Florek <tob@butter.sh> 0.14.0_rc2-2
- define gobuild macro when not defined (tob@butter.sh)

* Wed Mar 08 2017 Tobias Florek <tob@butter.sh> 0.14.0_rc2-1
- bump version (tob@butter.sh)

* Wed Mar 08 2017 Tobias Florek <tob@butter.sh> 0.14.0_rc1-8
- don't use git annex (tob@butter.sh)

* Wed Mar 08 2017 Tobias Florek <tob@butter.sh> 0.14.0_rc1-7
- actually build (tob@butter.sh)

* Wed Mar 08 2017 Tobias Florek <tob@butter.sh> 0.14.0_rc1-6
- install text_collector_examples (tob@butter.sh)
- don't run tests on build (tob@butter.sh)

* Wed Mar 08 2017 Tobias Florek <tob@butter.sh> 0.14.0_rc1-5
- build with bundled deps (tob@butter.sh)

* Wed Mar 08 2017 Tobias Florek <tob@butter.sh> 0.14.0_rc1-4
- add node_exporter source (tob@butter.sh)
- delete git-annex pointer (tob@butter.sh)
- add source file (tob@butter.sh)

* Wed Mar 08 2017 Tobias Florek <tob@butter.sh> 0.14.0_rc1-3
- use git annex to download source (tob@butter.sh)

* Wed Mar 08 2017 Tobias Florek <tob@butter.sh> 0.14.0_rc1-2
- new package built with tito

