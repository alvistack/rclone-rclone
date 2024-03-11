# Copyright 2025 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

%global source_date_epoch_from_changelog 0

Name: rclone
Epoch: 100
Version: 1.69.0
Release: 1%{?dist}
Summary: Rsync for cloud storage
License: MIT
URL: https://github.com/rclone/rclone/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: golang-1.24
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
