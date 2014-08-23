Name:           example
Version:        1.0 
Release:        1%{?dist}
Summary:        Just a file 

Group:          Misc 
License:        GPLv3 
URL:            http://example.com
Source0:        example-1.0.tar.gz

#BuildRequires:  
#Requires:       

%description
This is just my description

#%prep
#%setup -q


#%build
#%configure
#make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
#make install DESTDIR=$RPM_BUILD_ROOT
install -d -m 0755 $RPM_BUILD_ROOT/opt/example-1.0
# Make sure that the 'source' material is available in this line '/root/example-1.0/example-file.txt'
install -m 0644 /root/example-1.0/example-file.txt $RPM_BUILD_ROOT/opt/example-1.0/example-file.txt


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc
/opt/example-1.0/
/opt/example-1.0/example-file.txt


%changelog
