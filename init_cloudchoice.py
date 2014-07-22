from django.core.exceptions import ObjectDoesNotExist
from cloudchoice.models import *
from addressbook.models import *

def init_components():
    component_names = ("CPU", "Ram", "Storage", "Network(Inbound)",
                       "Network(Outbound)", "IP Address"
    )

    for component_name in component_names:
        try:
            cn = ComponentName(name = component_name)
            cn.save()
        except:
            print "ComponentName %s exists, ignore." % component_name

def init_units():
    unit_names = ("Month", "Day", "GB", "Hour", "Unit")

    for unit_name in unit_names:
        try:
            u = Unit(unit = unit_name)
            u.save()
        except:
            print "Unit %s exists, ignore." % unit_name


def init_os():
    os_names = ("Ubuntu 10.04 Server LTS",
                "Ubuntu 12.04 Server LTS",
                "CentOS 5.8",
                "CentOS 6.3",
                "Debian 6.0.6",
                "Microsoft Windows Server 2008 R2 with SP1 (Standard, Enterprise & Datacenter Editions)",
                "Microsoft Windows Server 2012 (Standard, Enterprise & Datacenter Editions)",
                "Microsoft SQL Server 2012 (Web, Standard and Enterprise Editions)",
                "Microsoft Office 2013 (Standard and Professional Plus Editions)",
                "Oracle Linux 5 Update 8",
                "Oracle Linux 6 Update 3",
                "Oracle Solaris 11 Update 1",
                "Vyatta Network OS Community & Subscription Edition 6.5",
                "VMware - CentOS 5.6",
                "VMWare - CentOS 6 64bit",
                "VMWare - Ubuntu 10.04 64bit",
                "VMWare - Ubuntu 12.04 LTS 64bit",
                "Managed cPanel/Litespeed (max 200 sites)",
                "Managed cPanel/Litespeed (max 10 sites)  ",
                "Windows Server 2008 Enterprise (64-bit)",
                "Windows Server 2008 Enterprise R2 (64-bit) ",
                "Windows Server 2003 R2 Standard (32-bit)",
                "Windows Server 2012 Datacenter",
                "Managed MS SQL Server 2008",
                "Windows/Linux",
                "CentOS",
                "Fedora",
                "Red Hat",
                "Debian",
    )

    for os_name in os_names:
        try:
            os = OS(name = os_name)
            os.save()
        except:
            print "OS %s exists, ignore." % os_name

def init_cloudmodels():
    for model in ("IaaS", "PaaS", "SaaS"):
        try:
            cloudmodel = CloudModel(model=model);
            cloudmodel.save();
        except:
            print "Model %s exists, ignore." % model

def init_services():
    for service in ("Virtual Server", "Email"):
        try:
            s = Service(service = service)
            s.save()
        except:
            print "Service %s exists, ignore." % service
            
def init_vendor(vendor_name, phone, url):

    try:
        contact = Contact.objects.filter(first_name='Vendor', last_name="Vendor", organization=vendor_name)[0]
    except:
        contact = Contact(first_name='Vendor', last_name="Vendor", organization=vendor_name, url=url)
        contact.save()

    contact = Contact.objects.filter(first_name='Vendor', last_name="Vendor", organization=vendor_name)[0]

    phonenumber = PhoneNumber(
        contact = contact,
        phone = phone,
        type = 'Work')

    website = Website(
        contact = contact,
        website = url,
        type = "Work")

    phonenumber.save()
    website.save()

    try:
        vendor = Vendor(
            name = vendor_name,
            contact = contact,
            website = Website.objects.filter(contact = contact, website = url)[0],
            phonenumber = PhoneNumber.objects.filter(contact = contact, phone = phone)[0],
        )
    except ObjectDoesNotExist:
        print "Website %s or PhoneNumber %s doesn't exist." % (website, phone)

    try:
        vendor.save()
    except:
        print "Vendor %s exists, ignore." % vendor_name

init_components()
init_os()
init_cloudmodels()
init_services()
init_units()

### CloudCentral     
init_vendor('CloudCentral', "1300144007", 'www.cloudcentral.com.au')
init_vendor('BitCloud', "1300 932 248", 'www.bitcloud.com.au')
init_vendor('Crazydomains', "1300210210", 'www.crazydomains.com.au')
        
#product = Product(
#    vendor = Vendor.objects.filter(name='CloudCentral')[0]
#)

vendor = Vendor.objects.get(name='CloudCentral')
cloudmodel = CloudModel.objects.get(model="Iaas")
service = Service.objects.get(service="Virtual Server")
product = Product(
    vendor = vendor,
    cloudmodel = cloudmodel,
    service = service,
    product_name = "Compute"
)

try:
    product.save()
except:
    print "%s product %s exists, ignore" % (vendor.name, product.product_name)
