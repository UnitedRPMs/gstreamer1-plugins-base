%global         majorminor      1.0

#global gitrel     140
#global gitcommit  c52adc8fcccf691754ab762e667fffb5465c3354
#global shortcommit %(c=%{gitcommit}; echo ${c:0:5})

Name:           gstreamer1-plugins-base
Version:        1.11.91
Release:        2%{?gitcommit:.git%{shortcommit}}%{?dist}
Summary:        GStreamer streaming media framework base plugins

License:        LGPLv2+
URL:            http://gstreamer.freedesktop.org/
%if 0%{?gitrel}
# git clone git://anongit.freedesktop.org/gstreamer/gst-plugins-base
# cd gst-plugins-base; git reset --hard %{gitcommit}; ./autogen.sh; make; make distcheck
Source0:        gst-plugins-base-%{version}.tar.xz
%else
Source0:        http://gstreamer.freedesktop.org/src/gst-plugins-base/gst-plugins-base-%{version}.tar.xz
%endif

BuildRequires:  gstreamer1-devel >= %{version}
BuildRequires:  gobject-introspection-devel >= 1.31.1
BuildRequires:  iso-codes-devel

BuildRequires:  alsa-lib-devel
BuildRequires:  cdparanoia-devel
BuildRequires:  libogg-devel >= 1.0
BuildRequires:  libtheora-devel >= 1.1
BuildRequires:  libvisual-devel
BuildRequires:  libvorbis-devel >= 1.0
BuildRequires:  libXv-devel
BuildRequires:  orc-devel >= 0.4.18
BuildRequires:  pango-devel
BuildRequires:  pkgconfig

BuildRequires:  chrpath

# documentation
BuildRequires:  gtk-doc >= 1.3

Requires:       iso-codes


%description
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plug-ins.

This package contains a set of well-maintained base plug-ins.


%package tools
Summary:        Tools for GStreamer streaming media framework base plugins
Requires:       %{name} = %{version}-%{release}


%description tools
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plug-ins.

This package contains the command-line tools for the base plugins.
These include:

* gst-discoverer


%package devel
Summary:        GStreamer Base Plugins Development files
Requires:       %{name} = %{version}-%{release}


%description devel
The %{name}-devel package contains libraries and header files
for developing applications that use %{name}.


%package devel-docs
Summary:        Developer documentation for GStreamer Base plugins library
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch


%description devel-docs
This %{name}-devel-docs package contains developer documentation
for the GStreamer Base Plugins library.


%prep
%setup -q -n gst-plugins-base-%{version}


%build
%configure \
  --with-package-name='Fedora GStreamer-plugins-base package' \
  --with-package-origin='http://download.fedoraproject.org' \
  --enable-experimental \
  --enable-gtk-doc \
  --enable-silent-rules \
  --enable-orc

  # https://bugzilla.gnome.org/show_bug.cgi?id=655517
  sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0/g' libtool

make %{?_smp_mflags} V=0

sed -e 's/^SUBDIRS_EXT =.*/SUBDIRS_EXT =/' -i Makefile

%install
make install DESTDIR=$RPM_BUILD_ROOT


  make -C %{_builddir}/gst-plugins-base-%{version}/gst-libs DESTDIR=%{buildroot} install
  make -C %{_builddir}/gst-plugins-base-%{version}/ext DESTDIR=%{buildroot} install

# Register as an AppStream component to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/gstreamer-base.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2013 Richard Hughes <richard@hughsie.com> -->
<component type="codec">
  <id>gstreamer-base</id>
  <metadata_license>CC0-1.0</metadata_license>
  <name>GStreamer Multimedia Codecs - Base</name>
  <summary>Multimedia playback for Ogg, Theora and Vorbis</summary>
  <description>
    <p>
      This addon includes system codecs that are essential for the running system.
    </p>
    <p>
      A codec decodes audio and video for for playback or editing and is also
      used for transmission or storage.
      Different codecs are used in video-conferencing, streaming media and
      video editing applications.
    </p>
  </description>
  <compulsory_for_desktop>GNOME</compulsory_for_desktop>
  <url type="homepage">http://gstreamer.freedesktop.org/</url>
  <url type="bugtracker">https://bugzilla.gnome.org/enter_bug.cgi?product=GStreamer</url>
  <url type="donation">http://www.gnome.org/friends/</url>
  <url type="help">http://gstreamer.freedesktop.org/documentation/</url>
  <update_contact><!-- upstream-contact_at_email.com --></update_contact>
</component>
EOF

%find_lang gst-plugins-base-%{majorminor}

# Clean out files that should not be part of the rpm.
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'



%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files -f gst-plugins-base-%{majorminor}.lang
%license COPYING
%doc AUTHORS README REQUIREMENTS
%{_datadir}/appdata/*.appdata.xml
%{_libdir}/libgstallocators-%{majorminor}.so.*
%{_libdir}/libgstaudio-%{majorminor}.so.*
%{_libdir}/libgstfft-%{majorminor}.so.*
%{_libdir}/libgstriff-%{majorminor}.so.*
%{_libdir}/libgsttag-%{majorminor}.so.*
%{_libdir}/libgstrtp-%{majorminor}.so.*
%{_libdir}/libgstvideo-%{majorminor}.so.*
%{_libdir}/libgstpbutils-%{majorminor}.so.*
%{_libdir}/libgstrtsp-%{majorminor}.so.*
%{_libdir}/libgstsdp-%{majorminor}.so.*
%{_libdir}/libgstapp-%{majorminor}.so.*

# gobject-introspection files
%{_libdir}/girepository-1.0/GstAllocators-%{majorminor}.typelib
%{_libdir}/girepository-1.0/GstApp-%{majorminor}.typelib
%{_libdir}/girepository-1.0/GstAudio-%{majorminor}.typelib
%{_libdir}/girepository-1.0/GstFft-%{majorminor}.typelib
%{_libdir}/girepository-1.0/GstPbutils-%{majorminor}.typelib
%{_libdir}/girepository-1.0/GstRtp-%{majorminor}.typelib
%{_libdir}/girepository-1.0/GstRtsp-%{majorminor}.typelib
%{_libdir}/girepository-1.0/GstSdp-%{majorminor}.typelib
%{_libdir}/girepository-1.0/GstTag-%{majorminor}.typelib
%{_libdir}/girepository-1.0/GstVideo-%{majorminor}.typelib

# base plugins without external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstadder.so
%{_libdir}/gstreamer-%{majorminor}/libgstapp.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudioconvert.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudiorate.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudioresample.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudiotestsrc.so
# {_libdir}/gstreamer-%{majorminor}/libgstencodebin.so
%{_libdir}/gstreamer-%{majorminor}/libgstgio.so
%{_libdir}/gstreamer-%{majorminor}/libgstplayback.so
%{_libdir}/gstreamer-%{majorminor}/libgstsubparse.so
%{_libdir}/gstreamer-%{majorminor}/libgsttcp.so
%{_libdir}/gstreamer-%{majorminor}/libgsttypefindfunctions.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideoconvert.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideorate.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideoscale.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideotestsrc.so
%{_libdir}/gstreamer-%{majorminor}/libgstvolume.so
%{_libdir}/gstreamer-%{majorminor}/libgstpbtypes.so
%{_libdir}/gstreamer-%{majorminor}/libgstencoding.so
%{_libdir}/gstreamer-%{majorminor}/libgstrawparse.so

# base plugins with dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstalsa.so
%{_libdir}/gstreamer-%{majorminor}/libgstcdparanoia.so
%{_libdir}/gstreamer-%{majorminor}/libgstlibvisual.so
%{_libdir}/gstreamer-%{majorminor}/libgstogg.so
%{_libdir}/gstreamer-%{majorminor}/libgstpango.so
%{_libdir}/gstreamer-%{majorminor}/libgsttheora.so
%{_libdir}/gstreamer-%{majorminor}/libgstvorbis.so
%{_libdir}/gstreamer-%{majorminor}/libgstximagesink.so
%{_libdir}/gstreamer-%{majorminor}/libgstxvimagesink.so


%files tools
%{_bindir}/gst-discoverer-%{majorminor}
%{_bindir}/gst-play-%{majorminor}
%{_bindir}/gst-device-monitor-%{majorminor}
%{_mandir}/man1/gst-discoverer-*.gz
%{_mandir}/man1/gst-play-*.gz
%{_mandir}/man1/gst-device-monitor-*.gz


%files devel
%dir %{_includedir}/gstreamer-%{majorminor}/gst/allocators
%{_includedir}/gstreamer-%{majorminor}/gst/allocators/allocators.h
%{_includedir}/gstreamer-%{majorminor}/gst/allocators/gstdmabuf.h
%{_includedir}/gstreamer-%{majorminor}/gst/allocators/gstfdmemory.h
%dir %{_includedir}/gstreamer-%{majorminor}/gst/app
%{_includedir}/gstreamer-%{majorminor}/gst/app/app.h
%{_includedir}/gstreamer-%{majorminor}/gst/app/gstappsink.h
%{_includedir}/gstreamer-%{majorminor}/gst/app/gstappsrc.h
%{_includedir}/gstreamer-%{majorminor}/gst/app/app-enumtypes.h
%dir %{_includedir}/gstreamer-%{majorminor}/gst/audio
%{_includedir}/gstreamer-%{majorminor}/gst/audio/audio-channels.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/audio-format.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/audio-info.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/audio-enumtypes.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/audio.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstaudiobasesink.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstaudiobasesrc.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstaudiocdsrc.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstaudioclock.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstaudiodecoder.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstaudioencoder.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstaudiofilter.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstaudioiec61937.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstaudiometa.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstaudioringbuffer.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstaudiosink.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstaudiosrc.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/streamvolume.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/audio-resampler.h
%dir %{_includedir}/gstreamer-%{majorminor}/gst/fft
%{_includedir}/gstreamer-%{majorminor}/gst/fft/fft.h
%{_includedir}/gstreamer-%{majorminor}/gst/fft/gstfft.h
%{_includedir}/gstreamer-%{majorminor}/gst/fft/gstfftf32.h
%{_includedir}/gstreamer-%{majorminor}/gst/fft/gstfftf64.h
%{_includedir}/gstreamer-%{majorminor}/gst/fft/gstffts16.h
%{_includedir}/gstreamer-%{majorminor}/gst/fft/gstffts32.h
%dir %{_includedir}/gstreamer-%{majorminor}/gst/pbutils
%{_includedir}/gstreamer-%{majorminor}/gst/pbutils/codec-utils.h
%{_includedir}/gstreamer-%{majorminor}/gst/pbutils/descriptions.h
%{_includedir}/gstreamer-%{majorminor}/gst/pbutils/encoding-profile.h
%{_includedir}/gstreamer-%{majorminor}/gst/pbutils/encoding-target.h
%{_includedir}/gstreamer-%{majorminor}/gst/pbutils/gstdiscoverer.h
%{_includedir}/gstreamer-%{majorminor}/gst/pbutils/gstpluginsbaseversion.h
%{_includedir}/gstreamer-%{majorminor}/gst/pbutils/install-plugins.h
%{_includedir}/gstreamer-%{majorminor}/gst/pbutils/missing-plugins.h
%{_includedir}/gstreamer-%{majorminor}/gst/pbutils/pbutils-enumtypes.h
%{_includedir}/gstreamer-%{majorminor}/gst/pbutils/pbutils.h
%dir %{_includedir}/gstreamer-%{majorminor}/gst/riff
%{_includedir}/gstreamer-%{majorminor}/gst/riff/riff.h
%{_includedir}/gstreamer-%{majorminor}/gst/riff/riff-ids.h
%{_includedir}/gstreamer-%{majorminor}/gst/riff/riff-media.h
%{_includedir}/gstreamer-%{majorminor}/gst/riff/riff-read.h
%dir %{_includedir}/gstreamer-%{majorminor}/gst/rtp
%{_includedir}/gstreamer-%{majorminor}/gst/rtp/gstrtcpbuffer.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtp/gstrtpbaseaudiopayload.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtp/gstrtpbasedepayload.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtp/gstrtpbasepayload.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtp/gstrtpbuffer.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtp/gstrtpdefs.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtp/gstrtp-enumtypes.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtp/gstrtphdrext.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtp/gstrtppayloads.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtp/rtp.h
%dir %{_includedir}/gstreamer-%{majorminor}/gst/rtsp
%{_includedir}/gstreamer-%{majorminor}/gst/rtsp/gstrtsp.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtsp/gstrtsp-enumtypes.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtsp/gstrtspconnection.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtsp/gstrtspdefs.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtsp/gstrtspextension.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtsp/gstrtspmessage.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtsp/gstrtsprange.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtsp/gstrtsptransport.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtsp/gstrtspurl.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtsp/rtsp.h
%dir %{_includedir}/gstreamer-%{majorminor}/gst/sdp
%{_includedir}/gstreamer-%{majorminor}/gst/sdp/gstsdp.h
%{_includedir}/gstreamer-%{majorminor}/gst/sdp/gstsdpmessage.h
%{_includedir}/gstreamer-%{majorminor}/gst/sdp/gstmikey.h
%{_includedir}/gstreamer-%{majorminor}/gst/sdp/sdp.h
%dir %{_includedir}/gstreamer-%{majorminor}/gst/tag
%{_includedir}/gstreamer-%{majorminor}/gst/tag/gsttagdemux.h
%{_includedir}/gstreamer-%{majorminor}/gst/tag/gsttagmux.h
%{_includedir}/gstreamer-%{majorminor}/gst/tag/tag.h
%{_includedir}/gstreamer-%{majorminor}/gst/tag/xmpwriter.h
%{_includedir}/gstreamer-%{majorminor}/gst/tag/tag-enumtypes.h
%dir %{_includedir}/gstreamer-%{majorminor}/gst/video
%{_includedir}/gstreamer-%{majorminor}/gst/video/colorbalance.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/colorbalancechannel.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/gstvideodecoder.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/gstvideoencoder.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/gstvideofilter.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/gstvideometa.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/gstvideopool.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/gstvideosink.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/gstvideoutils.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/navigation.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video-blend.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video-overlay-composition.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video-chroma.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video-color.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video-converter.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video-dither.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video-enumtypes.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video-event.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video-format.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video-frame.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video-info.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video-multiview.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video-resampler.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video-scaler.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video-tile.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/videoorientation.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/videooverlay.h

%{_includedir}/gstreamer-%{majorminor}/gst/video/gstvideotimecode.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/videodirection.h

%{_includedir}/gstreamer-%{majorminor}/gst/audio/audio-channel-mixer.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/audio-converter.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/audio-quantize.h
%{_includedir}/gstreamer-%{majorminor}/gst/pbutils/gstaudiovisualizer.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/gstvideoaffinetransformationmeta.h

%{_libdir}/libgstallocators-%{majorminor}.so
%{_libdir}/libgstaudio-%{majorminor}.so
%{_libdir}/libgstriff-%{majorminor}.so
%{_libdir}/libgstrtp-%{majorminor}.so
%{_libdir}/libgsttag-%{majorminor}.so
%{_libdir}/libgstvideo-%{majorminor}.so
%{_libdir}/libgstpbutils-%{majorminor}.so
%{_libdir}/libgstrtsp-%{majorminor}.so
%{_libdir}/libgstsdp-%{majorminor}.so
%{_libdir}/libgstfft-%{majorminor}.so
%{_libdir}/libgstapp-%{majorminor}.so

%dir %{_datadir}/gst-plugins-base/%{majorminor}/
%{_datadir}/gst-plugins-base/%{majorminor}/license-translations.dict

%{_datadir}/gir-1.0/GstAllocators-%{majorminor}.gir
%{_datadir}/gir-1.0/GstApp-%{majorminor}.gir
%{_datadir}/gir-1.0/GstAudio-%{majorminor}.gir
%{_datadir}/gir-1.0/GstFft-%{majorminor}.gir
%{_datadir}/gir-1.0/GstPbutils-%{majorminor}.gir
%{_datadir}/gir-1.0/GstRtp-%{majorminor}.gir
%{_datadir}/gir-1.0/GstRtsp-%{majorminor}.gir
%{_datadir}/gir-1.0/GstSdp-%{majorminor}.gir
%{_datadir}/gir-1.0/GstTag-%{majorminor}.gir
%{_datadir}/gir-1.0/GstVideo-%{majorminor}.gir

# pkg-config files
%{_libdir}/pkgconfig/*.pc


%files devel-docs
%doc %{_datadir}/gtk-doc/html/gst-plugins-base-libs-%{majorminor}
%doc %{_datadir}/gtk-doc/html/gst-plugins-base-plugins-%{majorminor}


%changelog

* Sat Apr 29 2017 David Vásquez <davidva AT tutanota DOT com> 1.11.91-2
- Updated to 1.11.91-2

* Thu Apr 20 2017 David Vásquez <davidva AT tutanota DOT com> 1.11.90-2
- Updated to 1.11.90-2

* Fri Feb 24 2017 David Vásquez <davidjeremias82 AT gmail DOT com> 1.11.2-1
- Updated to 1.11.2

* Fri Jan 27 2017 David Vásquez <davidjeremias82 AT gmail DOT com> 1.11.1-1
- Updated to 1.11.1

* Sat Oct 15 2016 David Vásquez <davidjeremias82 AT gmail DOT com> 1.9.90-1
- Updated to 1.9.90

* Thu Oct 06 2016 David Vásquez <davidjeremias82 AT gmail DOT com> 1.9.2-1
- Updated to 1.9.2

* Fri Jul 08 2016 David Vásquez <davidjeremias82 AT gmail DOT com> 1.9.1-1
- Updated to 1.9.1

* Thu Jun 23 2016 David Vásquez <davidjeremias82 AT gmail DOT com> 1.8.2-1
- Updated to 1.8.2

* Wed Apr 20 2016 David Vásquez <davidjeremias82 AT gmail DOT com> 1.8.1-1
- Updated to 1.8.1

* Wed Jan 20 2016 Wim Taymans <wtaymans@redhat.com> - 1.6.3-1
- Update to 1.6.3

* Tue Dec 15 2015 Wim Taymans <wtaymans@redhat.com> - 1.6.2-1
- Update to 1.6.2

* Mon Nov 2 2015 Wim Taymans <wtaymans@redhat.com> - 1.6.1-1
- Update to 1.6.1

* Sat Sep 26 2015 Kalev Lember <klember@redhat.com> - 1.6.0-1
- Update to 1.6.0
- Use license macro for COPYING

* Mon Sep 21 2015 Wim Taymans <wtaymans@redhat.com> - 1.5.91-1
- Update to 1.5.91

* Fri Sep 18 2015 Richard Hughes <rhughes@redhat.com> - 1.5.90-2
- Add optional data to AppStream metadata.

* Wed Aug 19 2015 Wim Taymans <wtaymans@redhat.com> - 1.5.90-1
- Update to 1.5.90

* Thu Jun 25 2015 Wim Taymans <wtaymans@redhat.com> - 1.5.2-1
- Update to 1.5.2
- Don't produce gir and typlib for GstRiff
- Add multiview headers

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 5 2015 Wim Taymans <wtaymans@redhat.com> - 1.5.1-1
- Update to 1.5.1
- add missing headers

* Wed Mar 25 2015 Richard Hughes <rhughes@redhat.com> - 1.4.5-3
- Register as an AppStream component.

* Sat Feb 21 2015 Kalev Lember <kalevlember@gmail.com> - 1.4.5-2
- Backport new missing plugins API

* Wed Jan 28 2015 Bastien Nocera <bnocera@redhat.com> 1.4.5-1
- Update to 1.4.5

* Fri Nov 14 2014 Kalev Lember <kalevlember@gmail.com> - 1.4.4-1
- Update to 1.4.4

* Mon Sep 22 2014 Wim Taymans <wtaymans@redhat.com> - 1.4.2-1
- Update to 1.4.2.

* Fri Aug 29 2014 Wim Taymans <wtaymans@redhat.com> - 1.4.1-1
- Update to 1.4.1.

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 1.4.0-2
- Rebuilt for gobject-introspection 1.41.4

* Tue Jul 22 2014 Wim Taymans <wtaymans@redhat.com> - 1.4.0-1
- Update to 1.4.0.

* Fri Jul 11 2014 Wim Taymans <wtaymans@redhat.com> - 1.3.91-1
- Update to 1.3.91.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Wim Taymans <wtaymans@redhat.com> - 1.2.4-2
- Improve conditional SSE and SSE2 compilation

* Sun Apr 20 2014 Brian Pepple <bpepple@fedoraproject.org> - 1.2.4-1
- Update to 1.2.4.

* Mon Feb 10 2014 Brian Pepple <bpepple@fedoraproject.org> - 1.2.3-1
- Update to 1.2.3.
- Drop patch to fix build on aarch64. Fixed upstream.

* Mon Jan 13 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.2-2
- Add upstream patch to fix build on aarch64

* Fri Dec 27 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.2.2-1
- Update to 1.2.2.

* Wed Dec 04 2013 Nils Philippsen <nils@redhat.com> - 1.2.1-2
- rebuild for new libvisual

* Mon Nov 11 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1.
- Drop patch to fix potential deadlock on startup. Fixed upstream.

* Thu Oct 03 2013 Bastien Nocera <bnocera@redhat.com> 1.2.0-2
- Fix potential deadlock on startup when playing audio files

* Tue Sep 24 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0.

* Thu Sep 19 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.1.90-1
- Update to 1.1.90.
- Bump minimum version of orc needed.

* Wed Aug 28 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.1.4-1
- Update to 1.1.4.

* Mon Jul 29 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.1.3-1
- Update to 1.1.3.

* Fri Jul 12 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.1.2-1
- Update to 1.1.2.
- Drop contrast/brightness video playback patch. Fixed upstream.

* Wed May 29 2013 Daniel Drake <dsd@laptop.org> - 1.0.7-2
- Upstream patch to fix contrast/brightness in video playback

* Fri Apr 26 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.0.7-1
- Update to 1.0.7.

* Wed Apr  3 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.0.6-2
- Drop gst-visualise mention from description. (#947658)

* Fri Mar 22 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.0.6-1
- Update to 1.0.6.
- Drop BR on PyXML.
- Drop alsa delay patch. Fixed upstream.

* Thu Jan 24 2013 Daniel Drake <dsd@laptop.org> - 1.0.5-3
- Add upstream fix for excessive alsasink CPU usage

* Fri Jan 18 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.0.5-2
- Add patch to fix missing mp3 codec discovery. (#680809, #896018)

* Tue Jan  8 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.0.5-1
- Update to 1.0.5.

* Wed Dec 19 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.4-1
- Update to 1.0.4

* Wed Nov 21 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3

* Thu Oct 25 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2.

* Sun Oct  7 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1

* Mon Oct  1 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.0-2
- Enable verbose build

* Mon Sep 24 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.0-1
- Update to 1.0.0.

* Wed Sep 19 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.99-1
- Update to 0.11.99

* Fri Sep 14 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.94-1
- Update to 0.11.94.

* Tue Aug 14 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.93-1
- Update to 0.11.93.
- Package gst-visualise.

* Tue Aug  7 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.92-2
- Remove rpath.

* Tue Jul 17 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.92-1
- Initial Fedora spec file.
