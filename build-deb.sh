#!/bin/bash

set -e
set -x

source versions

DISTRO="$1"
ARCH="$2"
DISTRO_NAME="${DISTRO%%-*}"
DISTRO_VERSION="${DISTRO#*-}"

mkdir -p output

deps_flags=""
if [ -f distros/$DISTRO_NAME/needs-deps-override.$DISTRO_NAME-$DISTRO_VERSION ]
then
	deps_flags="-d"
fi

docker buildx build \
	--platform linux/$ARCH \
	-t builder-$DISTRO_NAME-$DISTRO_VERSION-$ARCH \
	-f distros/$DISTRO_NAME/Dockerfile.$DISTRO_NAME-$DISTRO_VERSION \
	--load \
	.

docker run \
	-i \
	--platform linux/$ARCH \
	-v $PWD/xrdp:/src/xrdp \
	-v $PWD/distros/$DISTRO_NAME/xrdp:/src-debian/xrdp \
	-v $PWD/output:/output \
	builder-$DISTRO_NAME-$DISTRO_VERSION-$ARCH \
	bash -c "
		set -x &&
		mkdir /build &&
		cp -r /src/xrdp /build/xrdp-$xrdp_version &&
		cp -r /src-debian/xrdp/* /build/xrdp-$xrdp_version/ &&
		cd /build &&
		cd xrdp-$xrdp_version &&
		./bootstrap &&
		tar -czf ../xrdp_$xrdp_version.orig.tar.gz -C .. xrdp-$xrdp_version &&
		dpkg-buildpackage -us -uc $deps_flags &&
		cd .. &&
		for x in *.*deb;
		do
			cp \"\$x\" \"/output/\$(echo \"\$x\" | sed -r \"s/(\\.d?deb)/.$DISTRO_NAME-$DISTRO_VERSION\\1/\")\" || exit 1
		done
	"

docker run \
	-i \
	--platform linux/$ARCH \
	-v $PWD/xorgxrdp:/src/xorgxrdp \
	-v $PWD/distros/$DISTRO_NAME/xorgxrdp:/src-debian/xorgxrdp \
	-v $PWD/output:/output \
	builder-$DISTRO_NAME-$DISTRO_VERSION-$ARCH \
	bash -c "
		set -x &&
		dpkg -i /output/xrdp*_\$(dpkg --print-architecture).$DISTRO_NAME-$DISTRO_VERSION.deb ;
		DEBIAN_FRONTEND=noninteractive apt-get -f install -y &&
		mkdir /build &&
		cp -r /src/xorgxrdp /build/xorgxrdp-$xorgxrdp_version &&
		cp -r /src-debian/xorgxrdp/* /build/xorgxrdp-$xorgxrdp_version/ &&
		cd /build &&
		cd xorgxrdp-$xorgxrdp_version &&
		./bootstrap &&
		tar -czf ../xorgxrdp_$xorgxrdp_version.orig.tar.gz -C .. xorgxrdp-$xorgxrdp_version &&
		dpkg-buildpackage -us -uc &&
		cd .. &&
		for x in *.*deb;
		do
			cp \"\$x\" \"/output/\$(echo \"\$x\" | sed -r \"s/(\\.d?deb)/.$DISTRO_NAME-$DISTRO_VERSION\\1/\")\" || exit 1
		done
	"
