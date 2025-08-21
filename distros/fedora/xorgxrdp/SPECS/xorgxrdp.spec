Name:           xorgxrdp
Version:        0.10.4
Release:        2%{?dist}
Summary:        Implementation of xrdp backend as Xorg modules

License:        MIT
URL:            https://github.com/neutrinolabs/xorgxrdp
Source0:        https://github.com/neutrinolabs/xorgxrdp/releases/download/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  make
BuildRequires:  nasm
BuildRequires:  xorg-x11-server-devel
BuildRequires:  xorg-x11-server-Xorg
BuildRequires:  xrdp-devel >= 1:0.10.3
%if 0%{?fedora} > 0 && 0%{?fedora} <= 24
BuildRequires:  libXfont-devel
%else
BuildRequires:  libXfont2-devel
%endif

%if 0%{?fedora} >= 35 || 0%{?rhel} >= 8
BuildRequires:  mesa-libgbm-devel
BuildRequires:  libepoxy-devel
BuildRequires:  libdrm-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool

Conflicts: %{name}-glamor
%endif

Requires:       xrdp >= 1:0.10.3
Requires:       Xorg %(xserver-sdk-abi-requires videodrv 2>/dev/null)
Requires:       Xorg %(xserver-sdk-abi-requires xinput 2>/dev/null)
%if 0%{?fedora} >= 35 || 0%{?rhel} >= 8
Requires:       xorg-x11-server-Xorg
%endif

%if 0%{?fedora} >= 35 || 0%{?rhel} >= 8
%package glamor
Summary:        Implementation of xrdp backend as Xorg modules with glamor
RemovePathPostfixes: .glamor
Conflicts: %{name}

Requires:       xrdp >= 1:0.10.3
Requires:       Xorg %(xserver-sdk-abi-requires videodrv 2>/dev/null)
Requires:       Xorg %(xserver-sdk-abi-requires xinput 2>/dev/null)
Requires:       xorg-x11-server-Xorg
%endif

%description
xorgxrdp is a set of X11 modules that make Xorg act as a backend for
xrdp. Xorg with xorgxrdp is the most advanced xrdp backend with support
for screen resizing and multiple monitors.

%if 0%{?fedora} >= 35 || 0%{?rhel} >= 8
%description glamor
xorgxrdp is a set of X11 modules that make Xorg act as a backend for
xrdp. Xorg with xorgxrdp is the most advanced xrdp backend with support
for screen resizing and multiple monitors. Built with glamor support.
%endif

%prep
%autosetup -p1

%build
autoreconf -i

%if 0%{?fedora} >= 35 || 0%{?rhel} >= 8
# Build/install with glamor support first
CFLAGS="$RPM_OPT_FLAGS -I/usr/include/libdrm" \
%configure --enable-glamor
%make_build

# Preserve glamor files
%{__mv} xrdpdev/.libs/xrdpdev_drv.so xrdpdev_drv.so.glamor
%{__mv} xrdpkeyb/.libs/xrdpkeyb_drv.so xrdpkeyb_drv.so.glamor
%{__mv} xrdpmouse/.libs/xrdpmouse_drv.so xrdpmouse_drv.so.glamor
%{__mv} module/.libs/libxorgxrdp.so libxorgxrdp.so.glamor

%{__make} clean
%endif

# Regular build
%configure
%make_build

%install
%make_install

%if 0%{?fedora} >= 35 || 0%{?rhel} >= 8
# Install glamor files
%{__install} -p xrdpdev_drv.so.glamor %{buildroot}%{_libdir}/xorg/modules/drivers
%{__install} -p xrdpkeyb_drv.so.glamor %{buildroot}%{_libdir}/xorg/modules/input
%{__install} -p xrdpmouse_drv.so.glamor %{buildroot}%{_libdir}/xorg/modules/input
%{__install} -p libxorgxrdp.so.glamor %{buildroot}%{_libdir}/xorg/modules
%{__sed} '/^[[:blank:]]*Load "xorgxrdp"/i\    Load "glamoregl"' \
         %{buildroot}%{_sysconfdir}/X11/xrdp/xorg.conf > \
         %{buildroot}%{_sysconfdir}/X11/xrdp/xorg.conf.glamor
%endif

%files
%license COPYING
%doc README.md
%dir %{_sysconfdir}/X11/xrdp
%{_sysconfdir}/X11/xrdp/xorg.conf
%{_libdir}/xorg/modules/drivers/xrdpdev_drv.so
%{_libdir}/xorg/modules/input/xrdpkeyb_drv.so
%{_libdir}/xorg/modules/input/xrdpmouse_drv.so
%{_libdir}/xorg/modules/libxorgxrdp.so
%exclude %{_libdir}/xorg/modules/*.a
%exclude %{_libdir}/xorg/modules/*.la
%exclude %{_libdir}/xorg/modules/input/*.a
%exclude %{_libdir}/xorg/modules/input/*.la
%exclude %{_libdir}/xorg/modules/drivers/*.a
%exclude %{_libdir}/xorg/modules/drivers/*.la

%if 0%{?fedora} >= 35 || 0%{?rhel} >= 8
%files glamor
%license COPYING
%doc README.md
%dir %{_sysconfdir}/X11/xrdp
%{_sysconfdir}/X11/xrdp/xorg.conf.glamor
%{_libdir}/xorg/modules/drivers/xrdpdev_drv.so.glamor
%{_libdir}/xorg/modules/input/xrdpkeyb_drv.so.glamor
%{_libdir}/xorg/modules/input/xrdpmouse_drv.so.glamor
%{_libdir}/xorg/modules/libxorgxrdp.so.glamor
%exclude %{_libdir}/xorg/modules/*.a
%exclude %{_libdir}/xorg/modules/*.la
%exclude %{_libdir}/xorg/modules/input/*.a
%exclude %{_libdir}/xorg/modules/input/*.la
%exclude %{_libdir}/xorg/modules/drivers/*.a
%exclude %{_libdir}/xorg/modules/drivers/*.la
%endif

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Apr  1 2025 Bojan Smojver <bojan@rexursive.com> - 0.10.4-1
- Bump up to 0.10.4

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Dec 29 2024 Bojan Smojver <bojan@rexursive.com> - 0.10.3-5
- Change /usr/libexec/Xorg dependency to xorg-x11-server-Xorg

* Thu Dec 26 2024 Bojan Smojver <bojan@rexursive.com> - 0.10.3-2
- Add /usr/libexec/Xorg dependency

* Mon Dec 16 2024 Bojan Smojver <bojan@rexursive.com> - 0.10.3-1
- Bump up to 0.10.3

* Fri Sep 27 2024 Sérgio Basto <sergio@serjux.com> - 0.10.2-2
- Rebuild for rebase of xorg-server to versions 21.1.x

* Wed Jul 31 2024 Bojan Smojver <bojan@rexursive.com> - 0.10.2-1
- Bump up to 0.10.2

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed May 15 2024 Bojan Smojver <bojan@rexursive.com> - 0.10.1-1
- Bump up to 0.10.1

* Tue May 14 2024 Bojan Smojver <bojan@rexursive.com> - 0.10.0-4
- Rebuild against xrdp 0.10.0

* Wed Apr 03 2024 Bojan Smojver <bojan@rexursive.com> - 0.10.0-2
- Rebuild against xrdp 0.10.0-beta.2

* Tue Mar 12 2024 Bojan Smojver <bojan@rexursive.com> - 0.9.20-1
- Bump up to 0.9.20

* Mon Mar 11 2024 Bojan Smojver <bojan@rexursive.com> - 0.10.0-1
- Update to 0.10.0

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.19-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 26 2023 Bojan Smojver <bojan@rexursive.com> - 0.9.19-7
- run autoreconf before build, to avoid problems on F39

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.19-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.19-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 14 2022 Bojan Smojver <bojan@rexursive.com> - 0.9.19-5
- Insert glamoregl module into xorg.conf for glamor package
- Add missed Xorg server dependencies into glamor package

* Fri Nov  4 2022 Bojan Smojver <bojan@rexursive.com> - 0.9.19-4
- Build alternative binary with glamor enabled

* Sat Sep 10 2022 Bojan Smojver <bojan@rexursive.com> - 0.9.19-1
- Bump up to 0.9.19

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 11 2022 Bojan Smojver <bojan@rexursive.com> - 0.2.18-1
- Bump up to 0.2.18

* Mon Sep  6 2021 Bojan Smojver <bojan@rexursive.com> - 0.2.17-2
- Rebuild against xrdp 0.9.17

* Tue Aug 31 2021 Bojan Smojver <bojan@rexursive.com> - 0.2.17-1
- Bump up to 0.2.17

* Sat Aug 21 2021 Carl George <carl@george.computer> - 0.2.16-3
- Use xserver-sdk-abi-requires to require xserver ABI versions

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat May  1 2021 Bojan Smojver <bojan@rexursive.com> - 0.2.16-1
- Bump up to 0.2.16

* Wed Apr 14 2021 Bojan Smojver <bojan@rexursive.com> - 0.2.15-2
- Rebuild against xorg-x11-server 1.20.11

* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 23 2020 Bojan Smojver <bojan@rexursive.com> - 0.2.15-1
- Bump up to 0.2.15

* Thu Dec  3 2020 Bojan Smojver <bojan@rexursive.com> - 0.2.14-4
- Rebuild against xorg-x11-server 1.20.10

* Mon Oct 12 2020 Bojan Smojver <bojan@rexursive.com> - 0.2.14-3
- Rebuild against xorg-x11-server 1.20.9

* Tue Sep  1 2020 Bojan Smojver <bojan@rexursive.com> - 0.2.14-2
- Enable s390x

* Tue Sep  1 2020 Bojan Smojver <bojan@rexursive.com> - 0.2.14-1
- Bump up to 0.2.14

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.13-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Apr 16 2020 Bojan Smojver <bojan@rexursive.com> - 0.2.13-2
- Rebuild against Xorg 1.20.8

* Wed Mar 11 2020 Bojan Smojver <bojan@rexursive.com> - 0.2.13-1
- Bump up to 0.2.13

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan  4 2020 Bojan Smojver <bojan@rexursive.com> - 0.2.12-2
- Revert 228e9091af79a76819292467f17ad1ad7c6483c3 (#153) upstream
- Bug #1787612

* Wed Dec 11 2019 Bojan Smojver <bojan@rexursive.com> - 0.2.12-1
- Bump up to 0.2.12

* Tue Nov 26 2019 Bojan Smojver <bojan@rexursive.com> - 0.2.11-2
- Rebuild against Xorg 1.20.6

* Fri Aug 16 2019 Bojan Smojver <bojan@rexursive.com> - 0.2.11-1
- Bump up to 0.2.11

* Sat Aug 10 2019 Bojan Smojver <bojan@rexursive.com> - 0.2.10-4
- Add RHEL8/EPEL8 conditional.

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 24 2019 Bojan Smojver <bojan@rexursive.com> - 0.2.10-2
- Rebuild against Xorg 1.20.5

* Thu May 30 2019 Bojan Smojver <bojan@rexursive.com> - 0.2.10-1
- Bump up to 0.2.10

* Fri Mar  1 2019 Bojan Smojver <bojan@rexursive.com> - 0.2.9-3
- Rebuild against Xorg 1.20.4

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Dec 22 2018 Bojan Smojver <bojan@rexursive.com> - 0.2.9-1
- Bump up to 0.2.9

* Fri Nov  2 2018 Bojan Smojver <bojan@rexursive.com> - 0.2.8-3
- Rebuild against Xorg 1.20.3

* Thu Oct 25 2018 Bojan Smojver <bojan@rexursive.com> - 0.2.8-2
- Rebuild against Xorg 1.20.2

* Wed Sep 19 2018 Bojan Smojver <bojan@rexursive.com> - 0.2.8-1
- Bump up to 0.2.8

* Thu Sep  6 2018 Bojan Smojver <bojan@rexursive.com> - 0.2.7-3
- Rebuild against Xorg 1.20.1

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Bojan Smojver <bojan@rexursive.com> - 0.2.7-1
- Bump up to 0.2.7

* Thu May 17 2018 Bojan Smojver <bojan@rexursive.com> - 0.2.6-3
- Rebuild against Xorg 1.20.0 from F29

* Wed Apr 11 2018 Bojan Smojver <bojan@rexursive.com> - 0.2.6-2
- Rebuild against Xorg 1.19.5 from RHEL 7.5

* Sun Mar 25 2018 Bojan Smojver <bojan@rexursive.com> - 0.2.6-1
- Bump up to 0.2.6

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 15 2018 Bojan Smojver <bojan@rexursive.com> - 0.2.5-3
- Add patch for gnome-settings-daemon crash

* Fri Dec 22 2017 Bojan Smojver <bojan@rexursive.com> - 0.2.5-2
- Bump and rebuild against latest xorg-x11-server

* Sat Dec 16 2017 Bojan Smojver <bojan@rexursive.com> - 0.2.5-1
- Bump up to 0.2.5

* Fri Oct 13 2017 Bojan Smojver <bojan@rexursive.com> - 0.2.4-5
- Bump and rebuild against latest xorg-x11-server

* Sat Oct  7 2017 Bojan Smojver <bojan@rexursive.com> - 0.2.4-4
- Bump and rebuild against latest xorg-x11-server

* Sat Sep 23 2017 Bojan Smojver <bojan@rexursive.com> - 0.2.4-3
- Require xorg-x11-server-Xorg we built against

* Wed Sep 20 2017 Bojan Smojver <bojan@rexursive.com> - 0.2.4-2
- Require libXfont2-devel on RHEL7 at build time

* Wed Sep 20 2017 Bojan Smojver <bojan@rexursive.com> - 0.2.4-1
- Bump up to 0.2.4

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 20 2017 Bojan Smojver <bojan@rexursive.com> - 0.2.3-1
- Bump up to 0.2.3

* Thu Jun 22 2017 Bojan Smojver <bojan@rexursive.com> - 0.2.2-1
- Bump up to 0.2.2

* Thu Mar 30 2017 Bojan Smojver <bojan@rexursive.com> - 0.2.1-1
- Bump up to 0.2.1

* Thu Mar  9 2017 Pavel Roskin <plroskin@gmail.com> - 0.2.0-2
- Add build dependency on libXfont2-devel for f24

* Sun Mar  5 2017 Pavel Roskin <plroskin@gmail.com> - 0.2.0-1
- Package created
