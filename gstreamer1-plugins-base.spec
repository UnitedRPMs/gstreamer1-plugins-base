# Force out of source build
%undefine __cmake_in_source_build

%define _legacy_common_support 1

%global         majorminor      1.0
%global         meson_conf      meson --buildtype=release --prefix=/usr --libdir=%{_libdir} --libexecdir=/usr/libexec --bindir=/usr/bin --sbindir=/usr/sbin --includedir=/usr/include --datadir=/usr/share --mandir=/usr/share/man --infodir=/usr/share/info --localedir=/usr/share/locale --sysconfdir=/etc

%global debug_package %{nil}

Name:           gstreamer1-plugins-base
Version:        1.19.3
Release:        7%{?dist}
Summary:        GStreamer streaming media framework base plugins

License:        LGPLv2+
URL:            http://gstreamer.freedesktop.org/

Source0:        http://gstreamer.freedesktop.org/src/gst-plugins-base/gst-plugins-base-%{version}.tar.xz
	
BuildRequires:  meson >= 0.48.0
BuildRequires:  gcc git chrpath cmake 
BuildRequires:  gcc-c++
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
BuildRequires:  opus-devel
BuildRequires:  gdk-pixbuf2-devel
BuildRequires:  gtk3-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libglvnd-devel
 
# for autogen.sh
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLES-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  wayland-devel
BuildRequires:  egl-wayland-devel
BuildRequires:  graphene-devel
# pkgconfig-style deps specifically searched-for by autotools/configure
BuildRequires: pkgconfig(wayland-client) >= 1.0
BuildRequires: pkgconfig(wayland-cursor) >= 1.0
BuildRequires: pkgconfig(wayland-egl) >= 9.0
BuildRequires: pkgconfig(wayland-protocols) >= 1.15
 
# New features
BuildRequires:	libvorbisidec-devel

# for autogen.sh
BuildRequires:  automake gettext-devel libtool

# documentation
%if 0%{?fedora} >= 29
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:  gtk-doc >= 1.3
%endif

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

%if 0%{?fedora} >= 29
%package devel-docs
Summary:        Developer documentation for GStreamer Base plugins library
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch


%description devel-docs
This %{name}-devel-docs package contains developer documentation
for the GStreamer Base Plugins library.
%endif

%prep
%autosetup -n gst-plugins-base-%{version}
rm -rf common && git clone git://anongit.freedesktop.org/gstreamer/common 

%build
%meson_conf _build -D package-name="UnitedRpms GStreamer-plugins-base package" -D package-origin="https://unitedrpms.github.io/" -D doc=disabled -D tests=disabled -D examples=disabled -D orc=enabled -D tremor=disabled -D introspection=enabled   \


%meson_build -C _build

%install
%meson_install -C _build 

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


# Remove rpath.
# Remove rpath.
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstximagesink.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstvideotestsrc.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstpango.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstvorbis.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstogg.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstaudiorate.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstalsa.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libgstpbutils-1.0.so.*
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstvolume.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libgstaudio-1.0.so.*
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstapp.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstencoding.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstrawparse.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstvideoscale.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstplayback.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstcdparanoia.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libgstriff-1.0.so.*
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstxvimagesink.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgsttheora.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgsttypefindfunctions.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstaudioresample.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstlibvisual.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstaudioconvert.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstvideoconvert.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstvideorate.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstaudiotestsrc.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstadder.so
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/gst-device-monitor-1.0
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/gst-discoverer-1.0
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/gst-play-1.0
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstaudiomixer.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstopengl.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstpbtypes.so

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
%{_libdir}/libgstgl-%{majorminor}.so.*

# Wayland
%{_libdir}/gstreamer-%{majorminor}/libgstcompositor.so
%{_libdir}/gstreamer-%{majorminor}/libgstoverlaycomposition.so

# Allocator
%{_libdir}/girepository-1.0/GstAllocators-1.0.typelib
%{_libdir}/girepository-1.0/GstApp-1.0.typelib
%{_libdir}/girepository-1.0/GstAudio-1.0.typelib
%{_libdir}/girepository-1.0/GstGL-1.0.typelib
%{_libdir}/girepository-1.0/GstPbutils-1.0.typelib
%{_libdir}/girepository-1.0/GstRtp-1.0.typelib
%{_libdir}/girepository-1.0/GstRtsp-1.0.typelib
%{_libdir}/girepository-1.0/GstSdp-1.0.typelib
%{_libdir}/girepository-1.0/GstTag-1.0.typelib
%{_libdir}/girepository-1.0/GstVideo-1.0.typelib
#
%{_libdir}/girepository-1.0/GstGLEGL-1.0.typelib
%{_libdir}/girepository-1.0/GstGLWayland-1.0.typelib
%{_libdir}/girepository-1.0/GstGLX11-1.0.typelib

# base plugins without external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstadder.so
%{_libdir}/gstreamer-%{majorminor}/libgstapp.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudioconvert.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudiorate.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudioresample.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudiotestsrc.so
# {_libdir}/gstreamer-{majorminor}/libgstencodebin.so
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
%{_libdir}/gstreamer-%{majorminor}/libgstaudiomixer.so

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
%{_libdir}/gstreamer-%{majorminor}/libgstopengl.so
%{_libdir}/gstreamer-%{majorminor}/libgstopus.so
#{_libdir}/gstreamer-%{majorminor}/libgstivorbisdec.so

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


%{_includedir}/gstreamer-%{majorminor}/gst/allocators/allocators-prelude.h
%{_includedir}/gstreamer-%{majorminor}/gst/app/app-prelude.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/audio-prelude.h
%{_includedir}/gstreamer-%{majorminor}/gst/fft/fft-prelude.h
%{_includedir}/gstreamer-%{majorminor}/gst/pbutils/pbutils-prelude.h
%{_includedir}/gstreamer-%{majorminor}/gst/riff/riff-prelude.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtp/rtp-prelude.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtsp/rtsp-prelude.h
%{_includedir}/gstreamer-%{majorminor}/gst/sdp/sdp-prelude.h
%{_includedir}/gstreamer-%{majorminor}/gst/tag/tag-prelude.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video-prelude.h

%{_includedir}/gstreamer-%{majorminor}/gst/allocators/gstphysmemory.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstaudioaggregator.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstaudiostreamalign.h
%{_includedir}/gstreamer-%{majorminor}/gst/gl/
%{_includedir}/GL/wglext.h

%{_includedir}/gstreamer-%{majorminor}/gst/audio/audio-buffer.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtp/gstrtpmeta.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/gstvideoaggregator.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video-anc.h

%{_includedir}/gstreamer-%{majorminor}/gst/video/video-hdr.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/gstvideocodecalphameta.h
%{_libdir}/gstreamer-1.0/include/gst/gl/gstglconfig.h

%{_libdir}/libgstgl-%{majorminor}.so
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
#{_datadir}/gir-1.0/GstFft-{majorminor}.gir
%{_datadir}/gir-1.0/GstPbutils-%{majorminor}.gir
%{_datadir}/gir-1.0/GstRtp-%{majorminor}.gir
%{_datadir}/gir-1.0/GstRtsp-%{majorminor}.gir
%{_datadir}/gir-1.0/GstSdp-%{majorminor}.gir
%{_datadir}/gir-1.0/GstTag-%{majorminor}.gir
%{_datadir}/gir-1.0/GstVideo-%{majorminor}.gir
%{_datadir}/gir-1.0/GstGL-%{majorminor}.gir
#
%{_datadir}/gir-1.0/GstGLEGL-1.0.gir
%{_datadir}/gir-1.0/GstGLWayland-1.0.gir
%{_datadir}/gir-1.0/GstGLX11-1.0.gir


# pkg-config files
%{_libdir}/pkgconfig/*.pc


%files devel-docs
%doc AUTHORS ChangeLog NEWS README RELEASE

%changelog

* Wed Nov 17 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.19.3-7
- Updated to 1.19.3

* Mon Oct 04 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.19.2-7
- Updated to 1.19.2

* Sun Jun 20 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.19.1-7
- Updated to 1.19.1

* Mon Apr 19 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.18.4-7
- Updated to 1.18.4

* Mon Jan 25 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.18.3-7
- Updated to 1.18.3

* Mon Dec 07 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.18.2-7
- Updated to 1.18.2

* Thu Oct 29 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.18.1-7
- Updated to 1.18.1

* Mon Sep 28 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.18.0-7
- Updated to 1.18.0

* Tue Aug 25 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.17.90-7
- Updated to 1.17.90

* Fri Jul 10 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.17.2-7
- Updated to 1.17.2
- Enabled libvorbisidec

* Wed Dec 04 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.16.2-7
- Updated to 1.16.2-7

* Fri Sep 27 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.16.1-7
- Updated to 1.16.1-7

* Fri Apr 19 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.16.0-7
- Updated to 1.16.0-7

* Wed Feb 27 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.15.2-7
- Updated to 1.15.2-7

* Thu Jan 17 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.15.1-7  
- Update to 1.15.1

* Wed Oct 03 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.14.4-7  
- Updated to 1.14.4-7

* Tue Sep 18 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.14.3-8  
- Automatic Mass Rebuild

* Mon Sep 17 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.14.3-7 
- Updated to 1.14.3-7

* Fri Jul 20 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.14.2-7 
- Updated to 1.14.2-7

* Mon May 21 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.14.1-7 
- Updated to 1.14.1-7

* Wed Mar 21 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.14.0-7 
- Updated to 1.14.0-7

* Fri Mar 16 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.13.91-7 
- Updated to 1.13.91-7

* Sun Mar 04 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.13.90-7  
- Updated to 1.13.90-7

* Fri Dec 08 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 1.12.4-7
- Updated to 1.12.4-7

* Mon Sep 18 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 1.12.3-7
- Updated to 1.12.3-7

* Thu Jul 20 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 1.12.2-2
- Updated to 1.12.2-2

* Sat Jun 24 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 1.12.1-2
- Updated to 1.12.1-2

* Thu May 25 2017 David Vásquez <davidva AT tutanota DOT com> 1.12.0-2
- Updated to 1.12.0-2

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
