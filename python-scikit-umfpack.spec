#
# Conditional build:
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Wrapper of UMFPACK sparse direct solver to SciPy
Summary(pl.UTF-8):	Obudowanie procedur UMFPACK do rozwiązywania problemów na macierzach rzadkich dla SciPy
Name:		python-scikit-umfpack
Version:	0.3.2
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/scikit-umfpack/
Source0:	https://files.pythonhosted.org/packages/source/s/scikit-umfpack/scikit-umfpack-%{version}.tar.gz
# Source0-md5:	a92e3b8b7c864a9d5b25bf3d1a7ca39c
URL:		https://pypi.org/project/scikit-umfpack/
BuildRequires:	AMD-devel
BuildRequires:	UMFPACK-devel
BuildRequires:	blas-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	swig-python >= 2.0.4
%if %{with python2}
BuildRequires:	python-devel >= 1:2.5
BuildRequires:	python-numpy-devel
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-scipy >= 1.0.0
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-numpy-devel
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-scipy >= 1.0.0
%endif
%endif
Requires:	python-modules >= 1:2.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
scikit-umfpack provides wrapper of UMFPACK sparse direct solver to
SciPy.

%description -l pl.UTF-8
scikit-umfpack to obudowanie procedur UMFPACK do rozwiązywania
problemów na macierzach rzadkich dla SciPy.

%package -n python3-scikit-umfpack
Summary:	Wrapper of UMFPACK sparse direct solver to SciPy
Summary(pl.UTF-8):	Obudowanie procedur UMFPACK do rozwiązywania problemów na macierzach rzadkich dla SciPy
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.2

%description -n python3-scikit-umfpack
scikit-umfpack provides wrapper of UMFPACK sparse direct solver to
SciPy.

%description -n python3-scikit-umfpack -l pl.UTF-8
scikit-umfpack to obudowanie procedur UMFPACK do rozwiązywania
problemów na macierzach rzadkich dla SciPy.

%prep
%setup -q -n scikit-umfpack-%{version}

%build
export BLAS=%{_libdir}
export UMFPACK=%{_libdir}

%if %{with python2}
%py_build %{?with_tests:test}

%if %{with tests}
PYTHONPATH=$(readlink -f build-2/lib.*) \
nosetests-%{py_ver} scikits
%endif
%endif

%if %{with python3}
%py3_build %{?with_tests:test}

%if %{with tests}
PYTHONPATH=$(readlink -f build-3/lib.*) \
nosetests-%{py3_ver} scikits
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install
# ensure scikits/__init__.py is compiled
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}

%py_postclean
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/MANIFEST.in
%{__rm} -r $RPM_BUILD_ROOT%{py_sitedir}/scikits/umfpack/tests
%endif

%if %{with python3}
%py3_install
# ensure scikits/__init__.py is compiled
%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/MANIFEST.in
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/scikits/umfpack/tests
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE README.rst
%dir %{py_sitedir}/scikits
%{py_sitedir}/scikits/__init__.py[co]
%dir %{py_sitedir}/scikits/umfpack
%attr(755,root,root) %{py_sitedir}/scikits/umfpack/__umfpack.so
%{py_sitedir}/scikits/umfpack/*.py[co]
%{py_sitedir}/scikit_umfpack-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-scikit-umfpack
%defattr(644,root,root,755)
%doc LICENSE README.rst
%dir %{py3_sitedir}/scikits
%{py3_sitedir}/scikits/__init__.py
%dir %{py3_sitedir}/scikits/__pycache__
%{py3_sitedir}/scikits/__pycache__/__init__.cpython-*.py[co]
%dir %{py3_sitedir}/scikits/umfpack
%attr(755,root,root) %{py3_sitedir}/scikits/umfpack/__umfpack.cpython-*.so
%{py3_sitedir}/scikits/umfpack/*.py
%{py3_sitedir}/scikits/umfpack/__pycache__
%{py3_sitedir}/scikit_umfpack-%{version}-py*.egg-info
%endif
