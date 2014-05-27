%define files_for_build fastHadd.cc run_fastHadd_tests.sh test_fastHaddMerge.py fastParallelHadd.py

Name:           fasthadd
Version:        2.1
Release:        2%{?dist}
Summary:        A program to add ProtocolBuffer-formatted ROOT files in a quick way
License:        GPLv2+
Group:          Applications/System
Source0:        https://github.com/rovere/cmssw/archive/%{name}%{version}.tar.gz
URL:            https://github.com/cms-sw/cmssw
%if 0%{?el5}
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
%endif
BuildRequires:  pkgconfig
BuildRequires:  root = 5.34.14, root-physics = 5.34.14, root-graf3d = 5.34.14, root-tree-player = 5.34.14, root-python = 5.34.14
BuildRequires:  protobuf-devel >= 2.4.1, protobuf-compiler >= 2.4.1
Requires:       root = 5.34.14, root-tree-player = 5.34.14, root-python = 5.34.14, protobuf >= 2.4.1

%description
A program to add ProtocolBuffer-formatted ROOT files in a quick way

%prep
%setup -q -n cmssw-%{name}%{version}


%build
mkdir %{name}
cd %{name}
for f in %{files_for_build}; do cp %{_builddir}/cmssw-%{name}%{version}/DQMServices/Components/test/${f} .; done
sed -i -e s#DQMServices/Core/src/ROOTFilePB.pb.h#ROOTFilePB.pb.h# fastHadd.cc
cp %{_builddir}/cmssw-%{name}%{version}/DQMServices/Core/src/ROOTFilePB.proto .
protoc -I ./ --cpp_out=./ ROOTFilePB.proto
g++ -O2 -o fastHadd ROOTFilePB.pb.cc fastHadd.cc `pkg-config --libs protobuf` `root-config --cflags --libs`


#make %{?_smp_mflags}


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}/
cp -p %{name}/fastHadd %{buildroot}%{_bindir}/
cp -p %{name}/fastParallelHadd.py %{buildroot}%{_bindir}/

%check
mkdir -p test
pushd test
cp ../%{name}/fastHadd .
for f in %{files_for_build}; do cp %{_builddir}/cmssw-%{name}%{version}/DQMServices/Components/test/${f} .; done
export PATH=./:${PATH}
echo $PATH
. ./run_fastHadd_tests.sh
if [ $? -ne 0 ]; then
  exit $?
fi
popd
rm -fr test

%if 0%{?el5}
%clean
rm -rf %{buildroot}
%endif


%files
%defattr(-,root,root,-)
%doc
%{_bindir}/fastHadd
%{_bindir}/fastParallelHadd.py*

%changelog
* Sat Feb 22 2014 Salvatore Di Guida <salvatore.di.guida[at]cern.ch> - 2.1-2
- Align to a fixed ROOT version.
- Ported to el6.
- Use GitHub Releases.

* Fri Nov 15 2013 Marco Rovere <marco.rovere[at]cern.ch> - 2.1-1
- Add fastParallelHadd.py to the list of files to be deployed.
- Bumped to version 2.1 and add checks while building RPMs.
