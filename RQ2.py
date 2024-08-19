from rdflib import Graph, URIRef, Literal, Namespace, BNode
from rdflib.namespace import RDF, XSD, RDFS, OWL
import pandas as pd
import string
import uuid
import numpy as np


from DataLoaderSaver import DataLoaderSaver
from DataAnalyzer import DataAnalyzer
from URREFHelper import URREFHelper

""" Load datasets """
ncsc_data = DataLoaderSaver().load_dataset("NCSC", "engineered")
apt_data = DataLoaderSaver().load_dataset("APT", "processed")
ncsc_classification_data = DataLoaderSaver().load_dataset("NCSC", "classification")

""" Explode NCSC datasets so each CVE-ID is its own instance """
ncsc_data = URREFHelper().explode_columns(ncsc_data, ['CVE-ID'])
ncsc_classification_data = URREFHelper().explode_columns(ncsc_classification_data, ['CVE-ID'])

""" Explode NCSC dataset so each product, os and version is its own instance """
ncsc_data = URREFHelper().explode_columns(ncsc_data, ['Platformen', 'Toepassingen', 'Versies'])

""" Select only necessary columns and merge NCSC and APT datasets"""
ncsc = ncsc_data[["CVE-ID", "Toepassingen", "Versies", "Platformen"]]
apt = apt_data[["CVE-ID", "product", "version", "os"]]
# ncsc = ncsc_data[["CVE-ID", "Toepassingen"]]
# apt = apt_data[["CVE-ID", "product"]]
merged = pd.merge(ncsc, apt, on='CVE-ID')

# merged = merged.head(10000)

# print(len(merged))
merged.dropna(subset=["Toepassingen", "Versies", "Platformen"], how="all", inplace=True)
# print(len(merged))

# product_ncsc = merged['Toepassingen'].dropna().unique()
# product_apt = merged['product'].dropna().unique()
# unique_products = np.unique(np.concatenate((product_ncsc, product_apt)))
# print(unique_products)

# product_ncsc = merged['Versies'].dropna().unique()
# product_apt = merged['version'].dropna().unique()
# unique_versions = np.unique(np.concatenate((product_ncsc, product_apt)))
# print(unique_versions)

# product_ncsc = merged['Platformen'].dropna().unique()
# product_apt = merged['os'].dropna().unique()
# unique_versions = np.unique(np.concatenate((product_ncsc, product_apt)))
# print(unique_versions)

# for i in unique_versions:
#     print(i)

# print((merged['Versies'] == merged['version']).sum())
print((merged['Platformen'] == merged['os']).sum())

product_mapping = {
    '2007 Office System SP1/SP2': 'Microsoft Office',
    'Adobe Acrobat': 'Adobe Acrobat',
    'Adobe Acrobat 9 <9.5.5': 'Adobe Acrobat',
    'Adobe Acrobat Reader': 'Adobe Acrobat Reader',
    'Adobe Acrobat X <10.1.7': 'Adobe Acrobat',
    'Adobe Acrobat XI <11.0.03': 'Adobe Acrobat',
    'Adobe Flash CS3': 'Adobe Flash',
    'Adobe Flash CS4': 'Adobe Flash',
    'Adobe Flash Player': 'Adobe Flash Player',
    'Adobe Flash Player Desktop Runtime': 'Adobe Flash Player',
    'Adobe Flash Player for Google Chrome': 'Adobe Flash Player',
    'Adobe Flash Player for Linux': 'Adobe Flash Player',
    'Adobe Flash Player for Microsoft Edge and Internet Explorer 11': 'Adobe Flash Player',
    'Adobe Integrated Runtime (AIR)': 'Adobe AIR',
    'Adobe Integrated Runtime (AIR) SDK': 'Adobe AIR',
    'Adobe Acrobat Reader': 'Adobe Acrobat Reader',
    'Adobe Acrobat Reader 9 <9.5.5': 'Adobe Acrobat Reader',
    'Adobe Acrobat Reader X <10.1.7': 'Adobe Acrobat Reader',
    'Adobe Acrobat Reader XI <11.0.03': 'Adobe Acrobat Reader',
    'Apple Java 1.6 for Mac OS X': 'Apple Java',
    'Apple Java 1.6 voor Mac OS X': 'Apple Java',
    'Apple MacBook Pro, iPad, iPhone': 'Apple',
    'Apple Safari': 'Apple',
    'Apple iPad': 'Apple',
    'Apple iPhone': 'Apple',
    'Apple iPod Touch': 'Apple',
    'Atlassian Confluence': 'Atlassian Confluence',
    'Attachmate Reflection': 'Attachmate Reflection',
    'BEA Systems JRockit': 'BEA Systems JRockit',
    'Diverse IBM-producten (zie "Mogelijke oplossingen")': 'IBM',
    'Edge': 'Microsoft Edge',
    'Google Chrome': 'Google Chrome',
    'IBM Java': 'IBM Java',
    'IBM WebSphere Application Server': 'IBM WebSphere',
    'IBM WebSphere MQ': 'IBM WebSphere',
    'IBM Websphere Message Broker': 'IBM WebSphere',
    'Internet Explorer': 'Microsoft Internet Explorer',
    'Macromedia Flash': 'Macromedia Flash',
    'Microsoft .NET': 'Microsoft .NET',
    'Microsoft Biztalk Server': 'Microsoft Biztalk Server',
    'Microsoft Commerce Server': 'Microsoft Commerce Server',
    'Microsoft Edge': 'Microsoft Edge',
    'Microsoft Excel Viewer': 'Microsoft Excel Viewer',
    'Microsoft Internet Explorer': 'Microsoft Internet Explorer',
    'Microsoft Lync': 'Microsoft Lync',
    'Microsoft Lync 2010': 'Microsoft Lync',
    'Microsoft Lync 2013 SP1': 'Microsoft Lync',
    'Microsoft Office': 'Microsoft Office',
    'Microsoft Office 2003': 'Microsoft Office',
    'Microsoft Office 2003, 2007, 2010, 2013': 'Microsoft Office',
    'Microsoft Office 2007 Basic': 'Microsoft Office',
    'Microsoft Office 2007 SP3': 'Microsoft Office',
    'Microsoft Office 2007, 2010 en 2013': 'Microsoft Office',
    'Microsoft Office 2010 SP2': 'Microsoft Office',
    'Microsoft Office Converter Pack': 'Microsoft Office',
    'Microsoft Office Mac 2011 en 2016': 'Microsoft Office',
    'Microsoft Office Web Apps Server 2013': 'Microsoft Office',
    'Microsoft Office Word Viewer': 'Microsoft Office Word Viewer',
    'Microsoft Office for Mac': 'Microsoft Office for Mac',
    'Microsoft Office for Mac 2011': 'Microsoft Office for Mac',
    'Microsoft Office for Mac 2016': 'Microsoft Office for Mac',
    'Microsoft Outlook': 'Microsoft Outlook',
    'Microsoft PowerPoint Viewer': 'Microsoft PowerPoint Viewer',
    'Microsoft PowerShell': 'Microsoft PowerShell',
    'Microsoft SQL Server 2005': 'Microsoft SQL Server',
    'Microsoft SQLServer': 'Microsoft SQL Server',
    'Microsoft Sharepoint': 'Microsoft Sharepoint',
    'Microsoft Sharepoint Server 2010, 2013': 'Microsoft Sharepoint',
    'Microsoft Sharepoint Server 2013': 'Microsoft Sharepoint',
    'Microsoft Silverlight': 'Microsoft Silverlight',
    'Microsoft Silverlight 5': 'Microsoft Silverlight',
    'Microsoft Visio Viewer': 'Microsoft Visio Viewer',
    'Microsoft Visual Basic': 'Microsoft Visual Basic',
    'Microsoft Visual Fox Pro': 'Microsoft Visual Fox Pro',
    'Microsoft Windows': 'Microsoft Windows',
    'Microsoft Word': 'Microsoft Word',
    'Microsoft Word Viewer': 'Microsoft Word',
    'Microsoft Works': 'Microsoft Office',
    'Microsoft XML Core Services': 'Microsoft Office',
    'Mozilla Firefox': 'Mozilla',
    'Office 2003 SP3': 'Microsoft Office',
    'Office 2004 for Mac': 'Microsoft Office',
    'Office 2008 for Mac': 'Microsoft Office',
    'Office Compatibility Pack for Word Excel and PowerPoint 2007 File Formats SP1/SP2': 'Microsoft Office',
    'Office Excel Viewer 2003 SP3': 'Microsoft Office',
    'Office Excel Viewer SP1/SP2': 'Microsoft Office',
    'Office XP SP3': 'Microsoft Office',
    'Open XML File Converter for Mac': 'Microsoft Office',
    'Oracle Java': 'Oracle Java',
    'Oracle Java SE': 'Oracle Java',
    'Oracle OpenJDK': 'Oracle Java',
    'RARLAB WinRAR': 'RARLAB',
    'RIM Blackberry': 'RIM',
    'RIM Blackberry 7270': 'RIM',
    'RIM Blackberry Device Software': 'RIM',
    'Skype': 'Skype',
    'Skype for Business 2016': 'Skype',
    'Sun JDK': 'Oracle Java',
    'Sun JRE': 'Oracle Java',
    'Sun Java Update': 'Oracle Java',
    'Windows': 'Microsoft Windows',
    'Windows OLE': 'Microsoft Windows',
    'acrobat': 'Adobe Acrobat',
    'acrobat_reader': 'Adobe Acrobat Reader',
    'adobe_air': 'Adobe AIR',
    'air': 'Adobe AIR',
    'air_sdk': 'Adobe AIR',
    'biztalk_server': 'Microsoft Biztalk Server',
    'commerce_server': 'Microsoft Commerce Server',
    'confluence': 'Atlassian Confluence',
    'enterprise_linux_desktop': 'Linux',
    'enterprise_linux_desktop_supplementary': 'Linux',
    'enterprise_linux_server': 'Linux',
    'enterprise_linux_server_supplementary': 'Linux',
    'enterprise_linux_workstation': 'Linux',
    'enterprise_linux_workstation_supplementary': 'Linux',
    'excel': 'Microsoft Excel Viewer',
    'excel_viewer': 'Microsoft Excel Viewer',
    'flash_player': 'Adobe Flash Player',
    'flash_player_desktop_runtime': 'Adobe Flash Player',
    'flash_player_for_linux': 'Adobe Flash Player',
    'ie': 'Microsoft Internet Explorer',
    'internet_explorer': 'Microsoft Internet Explorer',
    'iphone_os': 'Apple',
    'jdk': 'Oracle Java',
    'jre': 'Oracle Java',
    'jscript': 'Microsoft Internet Explorer',
    'office': 'Microsoft Office',
    'office_compatibility_pack': 'Microsoft Office',
    'office_web_apps': 'Microsoft Office',
    'office_web_apps_server': 'Microsoft Office',
    'office_web_components': 'Microsoft Office',
    'open_xml_file_format_converter': 'Microsoft Office',
    'opensuse': 'Linux',
    'powerpoint': 'Microsoft PowerPoint Viewer',
    'server_message_block': 'Microsoft Windows',
    'sharepoint_enterprise_server': 'Microsoft SharePoint',
    'sharepoint_foundation': 'Microsoft SharePoint',
    'sharepoint_server': 'Microsoft SharePoint',
    'silverlight': 'Microsoft Silverlight',
    'sql_server': 'Microsoft SQL Server',
    'suse_linux_enterprise_desktop': 'Linux',
    'vbscript': 'Microsoft Internet Explorer',
    'visual_basic': 'Microsoft Visual Studio',
    'visual_foxpro': 'Microsoft Visual Studio',
    'windows_10': 'Microsoft Windows',
    'windows_2003_server': 'Microsoft Windows',
    'windows_7': 'Microsoft Windows',
    'windows_8': 'Microsoft Windows',
    'windows_8.1': 'Microsoft Windows',
    'windows_nt': 'Microsoft Windows',
    'windows_rt': 'Microsoft Windows',
    'windows_rt_8.1': 'Microsoft Windows',
    'windows_server_2003': 'Microsoft Windows',
    'windows_server_2008': 'Microsoft Windows',
    'windows_server_2012': 'Microsoft Windows',
    'windows_server_2016': 'Microsoft Windows',
    'windows_server_2019': 'Microsoft Windows',
    'windows_vista': 'Microsoft Windows',
    'windows_xp': 'Microsoft Windows',
    'winrar': 'RARLAB',
    'word': 'Microsoft Word',
    'word_viewer': 'Microsoft Word',
    'xml_core_services': 'Microsoft Office'
}

os_mapping = {
    'Android': 'Android',
    'Apple': 'Apple',
    'Apple Mac': 'Apple Mac',
    'Apple Mac OS': 'Apple Mac',
    'Apple Mac OS X': 'Apple Mac',
    'Apple Mac OS X Server': 'Apple Mac',
    'Apple iOS': 'Apple iOS',
    'Apple iOS < 10.0.1': 'Apple iOS',
    'BSD': 'BSD',
    'BlackBerry 10 OS': 'BlackBerry',
    'Canonical Ubuntu Linux': 'Ubuntu',
    'CentOS': 'Linux',
    'Debian': 'Linux',
    'Debian GNU/Linux': 'Linux',
    'Debian Linux': 'Linux',
    'Fedora': 'Linux',
    'Fedoraproject Fedora': 'Linux',
    'FreeBSD': 'FreeBSD',
    'FreeBSD FreeBSD': 'FreeBSD',
    'Google Android Operating System': 'Android',
    'Google Chrome OS': 'Chrome OS',
    'HP HP-UX family of operating systems': 'HP-UX',
    'HP-UX': 'HP-UX',
    'IBM AIX': 'IBM AIX',
    'IBM z/OS': 'IBM z/OS',
    'Linux': 'Linux',
    'Linux Linux': 'Linux',
    'Mac OS X': 'Apple Mac',
    'Mac OSX': 'Apple Mac',
    'Microsoft Windows': 'Windows',
    'Microsoft Windows (alle versies behalve x64- en Itanium-gebaseerde versies)': 'Windows',
    'Microsoft Windows 10': 'Windows 10',
    'Microsoft Windows 7': 'Windows 7',
    'Microsoft Windows 8': 'Windows 8',
    'Microsoft Windows 8 RT': 'Windows 8',
    'Microsoft Windows 8.1': 'Windows 8.1',
    'Microsoft Windows Server': 'Windows Server',
    'Microsoft Windows Server 2003': 'Windows Server 2003',
    'Microsoft Windows Server 2003 Service Pack 2': 'Windows Server 2003',
    'Microsoft Windows Server 2003 with SP2 for Itanium-based Systems': 'Windows Server 2003',
    'Microsoft Windows Server 2003 x64 Edition Service Pack 2': 'Windows Server 2003',
    'Microsoft Windows Server 2008': 'Windows Server 2008',
    'Microsoft Windows Server 2012': 'Windows Server 2012',
    'Microsoft Windows Server 2016': 'Windows Server 2016',
    'Microsoft Windows Vista': 'Windows Vista',
    'Microsoft Windows XP': 'Windows XP',
    'Microsoft Windows XP Professional x64 Edition Service Pack 2': 'Windows XP',
    'Microsoft Windows XP Service Pack 2': 'Windows XP',
    'Microsoft Windows XP Service Pack 3': 'Windows XP',
    'Novell Opensuse': 'Linux',
    'Novell SUSE Linux Enterprise Desktop 11 Service Pack 1': 'Linux',
    'Novell SUSE linux': 'Linux',
    'Novell SuSE Linux': 'Linux',
    'Novell Suse linux': 'Linux',
    'Novell suse linux': 'Linux',
    'OS X': 'Apple Mac',
    'OpenSUSE': 'Linux',
    'OpenSUSE Linux': 'Linux',
    'OpenSUSE OpenSUSE': 'Linux',
    'OpenSuSE': 'Linux',
    'OpenVMS': 'OpenVMS',
    'Oracle Solaris': 'Solaris',
    'Red Hat Linux': 'Red Hat',
    'RedHat Enterprise Linux': 'Red Hat',
    'RedHat Linux': 'Red Hat',
    'RedHat Red Hat Desktop': 'Red Hat',
    'RedHat Red Hat Enterprise Linux': 'Red Hat',
    'RedHat Red Hat Fedora': 'Red Hat',
    'RedHat Red Hat Linux': 'Red Hat',
    'SUSE': 'SUSE',
    'SUSE Linux': 'SUSE',
    'SUSE Linux Enterprise': 'SUSE',
    'SUSE Linux Enterprise Desktop': 'SUSE',
    'SUSE OpenSuSE': 'SUSE',
    'SuSE': 'SUSE',
    'SuSE Linux': 'SUSE',
    'SuSE Linux Enterprise Desktop': 'SUSE',
    'SuSE OpenSuSE': 'SUSE',
    'Sun Solaris': 'Solaris',
    'UNIX': 'UNIX',
    'Ubuntu': 'Ubuntu',
    'Ubuntu Desktop': 'Ubuntu',
    'Ubuntu Server': 'Ubuntu',
    'Windows': 'Windows',
    'analysis_services': 'Windows',
    'android': 'Android',
    'chrome_os': 'Chrome OS',
    'express_advanced_services': 'Windows',
    'internet_explorer': 'Windows',
    'iphone_os': 'Apple iOS',
    'itanium': 'Windows',
    'linux_kernel': 'Linux',
    'mac': 'Apple Mac',
    'mac_os': 'Apple Mac',
    'mac_os_x': 'Apple Mac',
    'office': 'Windows',
    'pro': 'Windows',
    'runtime_extended_files': 'Windows',
    'solaris': 'Solaris',
    'windows': 'Windows',
    'windows_10': 'Windows 10',
    'windows_2003_server': 'Windows Server 2003',
    'windows_7': 'Windows 7',
    'windows_8.1': 'Windows 8.1',
    'windows_rt_8.1': 'Windows 8.1',
    'windows_server': 'Windows Server',
    'windows_server_2003': 'Windows Server 2003',
    'windows_server_2008': 'Windows Server 2008',
    'windows_server_2012': 'Windows Server 2012',
    'windows_server_2016': 'Windows Server 2016',
    'windows_server_2019': 'Windows Server 2019',
    'windows_vista': 'Windows Vista',
    'windows_xp': 'Windows XP',
    'x32': 'Windows',
    'x64': 'Windows',
    'x86': 'Windows'
    }

# for key, value in product_mapping.items():
#     merged['product'] = merged['product'].replace(key, value)
#     merged['Toepassingen'] = merged['Toepassingen'].replace(key, value)

for key, value in os_mapping.items():
    merged['os'] = merged['os'].replace(key, value)
    merged['Platformen'] = merged['Platformen'].replace(key, value)

# print(merged.head(10))

# print((merged['product'] == merged['Toepassingen']).sum())
print((merged['os'] == merged['Platformen']).sum())
    

print(hello)

# # One-hot encode the columns
# toepassingen_dummies = pd.get_dummies(merged['Toepassingen'].str.strip()).add_prefix('NCSC_Toepassingen_')
# versies_dummies = pd.get_dummies(merged['Versies'].str.strip()).add_prefix('NCSC_Versies_')
# platformen_dummies = pd.get_dummies(merged['Platformen'].str.strip()).add_prefix('NCSC_Platformen_')
# product_dummies = pd.get_dummies(merged['product']).add_prefix('APT_product_')
# version_dummies = pd.get_dummies(merged['version']).add_prefix('APT_version_')
# os_dummies = pd.get_dummies(merged['os']).add_prefix('APT_os_')

# # Concatenate the one-hot encoded columns with the original dataset
# merged_onehot = pd.concat([merged, toepassingen_dummies, versies_dummies, platformen_dummies, product_dummies, version_dummies, os_dummies], axis=1)

# # Drop the original columns
# merged_onehot.drop(['Toepassingen', 'Versies', 'Platformen', 'product', 'version', 'os'], axis=1, inplace=True)

# print(merged_onehot.head(10))


print(hello)

""" Load the URREF ontology """
g = Graph()
g.parse("URREF.owl", format="xml")
print("Graph loaded successfully!")

""" Create URREF Namespace and bind this + other namespaces to the graph """
TI = Namespace("http://example.org/urref/")
# URREF= Namespace("http://eturwg.c4i.gmu.edu/files/ontologies/URREF.owl#")
g.bind("ti", TI)
g.bind("rdfs", RDFS)
g.bind("owl", OWL)

""" Create new threat intelligence classes, including hierarcy, and add them to the graph """
URREFHelper().create_classes(g, ["ThreatIntelligence", "Vulnerability", "Product", "Version", "OS"])
URREFHelper().assign_labels(g,["ThreatIntelligence"], ["Threat Intelligence"])
URREFHelper().add_subclasses_to_thing(g, [TI.ThreatIntelligence])
URREFHelper().add_subclasses_to_ti(g, [TI.Vulnerability])
URREFHelper().add_subclasses_to_vulnerability(g, [TI.Product, TI.Version, TI.OS])

# merged = merged.head(1000) # for testing

""" Populate ontology with all instances of the merged dataset in batches """
batch_size = 1000
num_batches = (len(merged) + batch_size - 1) // batch_size

for i in range(num_batches):
    start = i * batch_size
    end = (i + 1) * batch_size
    batch = merged.iloc[start:end]

    for index, row in batch.iterrows():
        CVE_ID = row['CVE-ID']
        TOEPASSING = row['Toepassingen']
        PRODUCT = row["product"]
        VERSIE = row["Versies"]
        VERSION = row["version"]
        PLATFORM = row["Platformen"]
        OS = row["os"]

        vulnerability_uri = URIRef(f"http://example.org/urref/vulnerability/{CVE_ID}")
        g.add((vulnerability_uri, RDF.type, TI.Vulnerability))
        g.add((vulnerability_uri, TI.hasCVEID, Literal(row['CVE-ID'], datatype=XSD.string)))

        """ Product """
        toepassing_uri = URIRef(f"http://example.org/urref/product/{uuid.uuid4()}")
        g.add((toepassing_uri, RDF.type, TI.Product))
        g.add((toepassing_uri, TI.hasProductName, Literal(TOEPASSING, datatype=XSD.string)))
        g.add((toepassing_uri, TI.fromDataset, Literal("NCSC", datatype=XSD.string)))
        g.add((vulnerability_uri, URIRef("http://example.org/urref/affectsProduct"), toepassing_uri))

        product_uri = URIRef(f"http://example.org/urref/product/{uuid.uuid4()}")
        g.add((product_uri, RDF.type, TI.Product))
        g.add((product_uri, TI.hasProductName, Literal(PRODUCT, datatype=XSD.string)))
        g.add((product_uri, TI.fromDataset, Literal("APT", datatype=XSD.string)))
        g.add((vulnerability_uri, URIRef("http://example.org/urref/affectsProduct"), product_uri))

        """ Version """
        versie_uri = URIRef(f"http://example.org/urref/version/{uuid.uuid4()}")
        g.add((versie_uri, RDF.type, TI.Version))
        g.add((versie_uri, TI.hasVersionName, Literal(VERSIE, datatype=XSD.string)))
        g.add((versie_uri, TI.fromDataset, Literal("NCSC", datatype=XSD.string)))
        g.add((product_uri, URIRef("http://example.org/urref/affectsVersion"), versie_uri))

        version_uri = URIRef(f"http://example.org/urref/version/{uuid.uuid4()}")
        g.add((version_uri, RDF.type, TI.Version))
        g.add((version_uri, TI.hasVersionName, Literal(VERSION, datatype=XSD.string)))
        g.add((version_uri, TI.fromDataset, Literal("APT", datatype=XSD.string)))
        g.add((product_uri, URIRef("http://example.org/urref/affectsVersion"), version_uri))

        """ OS """
        os_uri = URIRef(f"http://example.org/urref/os/{uuid.uuid4()}")
        g.add((os_uri, RDF.type, TI.OS))
        g.add((os_uri, TI.hasOSlabel, Literal(PLATFORM, datatype=XSD.string)))
        g.add((os_uri, TI.fromDataset, Literal("NCSC", datatype=XSD.string)))
        g.add((version_uri, URIRef("http://example.org/urref/runsOn"), os_uri))

        os_uri = URIRef(f"http://example.org/urref/os/{uuid.uuid4()}")
        g.add((os_uri, RDF.type, TI.OS))
        g.add((os_uri, TI.hasOSlabel, Literal(OS, datatype=XSD.string)))
        g.add((os_uri, TI.fromDataset, Literal("APT", datatype=XSD.string)))
        g.add((version_uri, URIRef("http://example.org/urref/runsOn"), os_uri)) 

        # print(row, "added from total rows:", len(merged))

    # Commit the batch to the graph
    g.commit()

    print(f"Batch {i+1} of {num_batches} committed.")

# Serialize and save the graph
g.serialize(destination="output_urref.owl", format="xml")
print("Graph serialized and saved successfully!")
