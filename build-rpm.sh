#!/bin/bash

set -e
set -x

source versions

DISTRO="$1"
ARCH="$2"
DISTRO_NAME="${DISTRO%%-*}"
DISTRO_VERSION="${DISTRO#*-}"

case $DISTRO_NAME in
	fedora) DISTRO_SHORTNAME=fc ;;
	*)
		echo "Unknown distro $DISTRO_NAME."
		exit 1
		;;
esac

mkdir -p output

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
	-v $PWD/distros/$DISTRO_NAME/xrdp:/src-rpm/xrdp \
	-v $PWD/output:/output \
	builder-$DISTRO_NAME-$DISTRO_VERSION-$ARCH \
	bash -c "
		set -x &&
		mkdir -p /build /root/rpmbuild/SOURCES &&
		cp -r /src/xrdp /build/xrdp-$xrdp_version &&
		cp -r /src-rpm/xrdp/* /root/rpmbuild/ &&
		cd /build &&
		tar -czf /root/rpmbuild/SOURCES/xrdp-$xrdp_version.tar.gz xrdp-$xrdp_version &&
		cd ~/rpmbuild/SPECS &&
		rpmbuild -bb xrdp.spec &&
		cp ~/rpmbuild/RPMS/*/*.rpm /output/
	"

docker run \
	-i \
	--platform linux/$ARCH \
	-v $PWD/xorgxrdp:/src/xorgxrdp \
	-v $PWD/distros/$DISTRO_NAME/xorgxrdp:/src-rpm/xorgxrdp \
	-v $PWD/output:/output \
	builder-$DISTRO_NAME-$DISTRO_VERSION-$ARCH \
	bash -c "
		set -x &&
		dnf install -y \
			/output/xrdp-$xrdp_version-*.$DISTRO_SHORTNAME$DISTRO_VERSION.\$(rpm --eval '%{_arch}.')rpm \
			/output/xrdp-devel-$xrdp_version-*.$DISTRO_SHORTNAME$DISTRO_VERSION.\$(rpm --eval '%{_arch}.')rpm \
			&& \
		mkdir -p /build /root/rpmbuild/SOURCES &&
		cp -r /src/xorgxrdp /build/xorgxrdp-$xorgxrdp_version &&
		cp -r /src-rpm/xorgxrdp/* /root/rpmbuild/ &&
		cd /build &&
		tar -czf /root/rpmbuild/SOURCES/xorgxrdp-$xorgxrdp_version.tar.gz xorgxrdp-$xorgxrdp_version &&
		cd ~/rpmbuild/SPECS &&
		rpmbuild -bb xorgxrdp.spec &&
		cp ~/rpmbuild/RPMS/*/*.rpm /output/
	"
