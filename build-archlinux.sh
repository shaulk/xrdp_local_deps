#!/bin/bash

set -e
set -x

source versions

ARCH="$1"

mkdir -p output

docker buildx build \
	--platform linux/$ARCH \
	-t builder-archlinux-$ARCH \
	-f distros/archlinux/Dockerfile \
	--load \
	.

docker run \
	-i \
	--platform linux/$ARCH \
	-v $PWD/xrdp:/src/xrdp \
	-v $PWD/distros/archlinux/xrdp:/src-archlinux/xrdp \
	-v $PWD/output:/output \
	builder-archlinux-$ARCH \
	bash -c "
		set -x &&
		mkdir /build &&
		cp -r /src-archlinux/xrdp /build/ &&
		cp -r /src/xrdp /build/xrdp/xrdp-dmabuf-$xrdp_version &&
		useradd -m builder &&
		chown -R builder /build &&
		tar -czf /build/xrdp/xrdp.tar.gz -C /build/xrdp xrdp-dmabuf-$xrdp_version &&
		su - builder -c \"cd /build/xrdp && makepkg\" &&
		for x in /build/xrdp/*.pkg.tar.*;
		do
			cp \"\$x\" \"/output/\$(basename \"\$x\" | sed -r \"s/(\\.pkg\\..*)$/.archlinux\\1/\")\" || exit 1
		done
	"

docker run \
	-i \
	--platform linux/$ARCH \
	-v $PWD/xorgxrdp:/src/xorgxrdp \
	-v $PWD/distros/archlinux/xorgxrdp:/src-archlinux/xorgxrdp \
	-v $PWD/output:/output \
	builder-archlinux-$ARCH \
	bash -c "
		set -x &&
		pacman -U --noconfirm /output/xrdp-dmabuf-${xrdp_version}-*-\$(pacman-conf Architecture).archlinux.pkg.*;
		mkdir /build &&
		cp -r /src-archlinux/xorgxrdp /build/ &&
		cp -r /src/xorgxrdp /build/xorgxrdp/xorgxrdp-dmabuf-$xorgxrdp_version &&
		useradd -m builder &&
		chown -R builder /build &&
		tar -czf /build/xorgxrdp/xorgxrdp.tar.gz -C /build/xorgxrdp xorgxrdp-dmabuf-$xorgxrdp_version &&
		su - builder -c \"
			cd /build/xorgxrdp &&
			makepkg
		\" &&
		for x in /build/xorgxrdp/*.pkg.tar.*;
		do
			cp \"\$x\" \"/output/\$(basename \"\$x\" | sed -r \"s/(\\.pkg\\..*)$/.archlinux\\1/\")\" || exit 1
		done
	"
