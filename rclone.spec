%global debug_package %{nil}

Name: rclone
Epoch: 100
Version: 1.57.0
Release: 1%{?dist}
Summary: Rsync for cloud storage
License: MIT
URL: https://github.com/rclone/rclone/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: go >= 1.18
BuildRequires: glibc-static

%description
Rsync for cloud storage. rclone is a command line program to sync files
and directories to and from a wide variety of cloud storage providers,
providing various additional features.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
mkdir -p bin
set -ex && \
    export CGO_ENABLED=1 && \
    go build \
        -mod vendor -buildmode pie -v \
        -ldflags "-s -w" \
        -o ./bin/rclone .

%install
install -Dpm755 -d %{buildroot}%{_bindir}
install -Dpm755 -d %{buildroot}%{_prefix}/share/bash-completion/completions
install -Dpm755 -t %{buildroot}%{_bindir}/ bin/rclone
install -Dpm755 -t %{buildroot}%{_bindir}/ bin/rclonefs
./bin/rclone genautocomplete bash %{buildroot}%{_prefix}/share/bash-completion/completions/rclone

%files
%license COPYING
%{_bindir}/*
%{_prefix}/share/bash-completion/completions/*

%changelog
