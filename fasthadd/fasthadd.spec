%global commit 11e3097b139fbe062a579c0c273098ed98e36010
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%define file_to_build fastHadd.cc
%define protobuf_message_definition ROOTFilePB.proto
%define file_for_testing test_fastHaddMerge.py
%define binary_parallel fastParallelHadd.py
%define test_driver run_fastHadd_tests.sh

%define binary_file fastHadd

Name:           fasthadd
Version:        3.0
Release:        1%{?dist}
Summary:        A program to add ProtocolBuffer-formatted ROOT files in a quick way
License:        GPLv2+
Group:          Applications/System
Source0:        https://github.com/diguida/cmssw/archive/%{commit}/%{commit}.tar.gz
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
%setup -q -n cmssw-%{commit}

%build
mkdir %{name}
cd %{name}
cp %{_builddir}/cmssw-%{commit}/DQMServices/Components/bin/%{file_to_build} .
cp %{_builddir}/cmssw-%{commit}/DQMServices/Core/src/%{protobuf_message_definition} .
cp %{_builddir}/cmssw-%{commit}/DQMServices/Components/test/%{binary_parallel} .
cp %{_builddir}/cmssw-%{commit}/DQMServices/Components/test/%{file_for_testing} .
cp %{_builddir}/cmssw-%{commit}/DQMServices/Components/test/%{test_driver} .
sed -i -e s#DQMServices/Core/src/ROOTFilePB.pb.h#ROOTFilePB.pb.h# %{file_to_build}
sed -i -e s#\$\{LOCAL_TEST_DIR\}/##g %{test_driver}
protoc -I ./ --cpp_out=./ %{protobuf_message_definition}
g++ -O2 -o %{binary_file} ROOTFilePB.pb.cc %{file_to_build} `pkg-config --libs protobuf` `root-config --cflags --libs`

#make %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}/
cp -p %{name}/fastHadd %{buildroot}%{_bindir}/
cp -p %{name}/fastParallelHadd.py %{buildroot}%{_bindir}/

%check
mkdir -p test
pushd test
cp ../%{name}/%{binary_file} .
cp ../%{name}/%{binary_parallel} .
cp ../%{name}/%{file_for_testing} .
cp ../%{name}/%{test_driver} .
export PATH=./:${PATH}
echo $PATH
. ./%{test_driver}
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
