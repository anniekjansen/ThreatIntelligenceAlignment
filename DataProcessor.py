import pandas as pd
import datetime
import ast
import string
import re

class DataProcessor:

    def drop_columns(self, data, columns_to_drop):
        data = data.drop(columns=columns_to_drop)
        return data
    
    def drop_duplicates(self, data):
        data = data.drop_duplicates(ignore_index=True)
        return data
    
    def drop_missing_values(self, data):
        data = data.dropna()
        return data

    def object_to_datetime(self, data, column):
        for row in range(len(data)):
            date_string = data.loc[row, column]
            if column == 'Uitgiftedatum':
                datetime_obj = datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S%z')
            else:
                datetime_obj = datetime.datetime.strptime(date_string, '%Y-%m-%d')
        data.loc[row, column] = datetime_obj
        data[column] = pd.to_datetime(data[column], utc=True)
        return data
    
    def string_to_list(self, data, columns):
        for col in columns:
            data[col] = data[col].apply(ast.literal_eval)
        return data

    def values_to_None(self, data, columns):
        for col in columns:
            data[col] = data[col].apply(lambda x: None if x in ([], ['niet beschikbaar'], ["-"], ['-'], "*", "-") else x)
        return data
        
    def fix_cve_id(self, cve_id):
        cve_id_fixed = cve_id.translate(str.maketrans("", "", string.punctuation.replace("-", "")))
        return cve_id_fixed
     
    def valid_cve_id(self, cve_id):
        if (len(cve_id) in [13, 14] and cve_id[:3].isalpha() and cve_id[3] == "-" and all(c.isdigit() or c == "-" for c in cve_id[4:])):
            valid_cve_id = cve_id
            return valid_cve_id
        else:
            return None
        
    def replace_values_ncsc(self, x, mapping):
        if x is None:
            return x 
        result = []
        for elem in x:
            if elem in mapping:
                result.append(mapping[elem])
            else:
                result.append(elem)
        return result

    def replace_values_apt(self, x, mapping):
        if x is None:
            return x
        if x in mapping:
            return mapping[x]
        else:
            return x 

    def mapping(self, data, security_dataset):

        product_mapping = {
        'Air': 'Adobe AIR',
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
        'Adobe Acrobat XI &lt;11.0.03': 'Adobe Acrobat',
        'Adobe Acrobat X &lt;10.1.7': 'Adobe Acrobat',
        'Adobe Acrobat 9 &lt;9.5.5': 'Adobe Acrobat',
        'Adobe Reader XI &lt;11.0.03': 'Adobe Acrobat Reader',
        'Adobe Reader X &lt;10.1.7': 'Adobe Acrobat Reader',
        'Adobe Reader 9 &lt;9.5.5': 'Adobe Acrobat Reader',
        'Apple Java 1.6 for Mac OS X': 'Apple Java',
        'Apple Java 1.6 voor Mac OS X': 'Apple Java',
        'Apple MacBook Pro, iPad, iPhone': 'Apple',
        'Apple Safari': 'Apple',
        'Apple iPad': 'Apple',
        'Apple IPad': 'Apple',
        'Apple iPhone': 'Apple',
        'Apple IPhone': 'Apple',
        'Apple iPod Touch': 'Apple',
        'Apple IPod Touch': 'Apple',
        'Atlassian Confluence': 'Atlassian Confluence',
        'Attachmate Reflection': 'Attachmate Reflection',
        'BEA Systems JRockit': 'BEA Systems JRockit',
        'Diverse IBM-producten (zie "Mogelijke oplossingen")': 'IBM',
        'Diverse IBM-producten (zie &quot;Mogelijke oplossingen&quot;)': 'IBM',
        'edge': 'Microsoft Edge',
        'Edge': 'Microsoft Edge',
        'Excel': 'Microsoft Excel',
        'Google Chrome': 'Google Chrome',
        'JScript': 'JScript',
        'JRE': 'Oracle Java',
        'Jre': 'Oracle Java',
        'JDK': 'Oracle Java',
        'Jdk': 'Oracle Java',
        'IBM Java': 'IBM Java',
        'IBM Websphere Application Server': 'IBM WebSphere',
        'IBM WebSphere Application Server': 'IBM WebSphere',
        'IBM WebSphere MQ': 'IBM WebSphere',
        'IBM Websphere Message Broker': 'IBM WebSphere',
        'Internet Explorer': 'Microsoft Internet Explorer',
        'Macromedia Flash': 'Macromedia Flash',
        'Microsoft .NET': 'Microsoft .NET',
        'Microsoft Biztalk Server': 'Microsoft Biztalk Server',
        'Microsoft Commerce Server': 'Microsoft Commerce Server',
        'Microsoft Edge': 'Microsoft Edge',
        'Microsoft Excel Viewer': 'Microsoft Excel',
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
        'Microsoft Office Word Viewer': 'Microsoft Word',
        'Microsoft Office for Mac': 'Microsoft Office',
        'Microsoft Office for Mac 2011': 'Microsoft Office',
        'Microsoft Office for Mac 2016': 'Microsoft Office',
        'Microsoft Outlook': 'Microsoft Outlook',
        'Microsoft PowerPoint Viewer': 'Microsoft PowerPoint',
        'Microsoft Powerpoint Viewer': 'Microsoft PowerPoint',
        'Microsoft PowerShell': 'Microsoft PowerShell',
        'Microsoft SQL Server 2005': 'Microsoft SQL Server',
        'Microsoft SQLServer': 'Microsoft SQL Server',
        'Microsoft Sharepoint': 'Microsoft SharePoint',
        'Microsoft SharePoint': 'Microsoft SharePoint',
        'Microsoft Sharepoint Server 2010, 2013': 'Microsoft SharePoint',
        'Microsoft Sharepoint Server 2013': 'Microsoft SharePoint',
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
        'Office': 'Microsoft Office',
        'Office 2003 SP3': 'Microsoft Office',
        'Office 2004 for Mac': 'Microsoft Office',
        'Office 2008 for Mac': 'Microsoft Office',
        'Office Compatibility Pack for Word Excel and PowerPoint 2007 File Formats SP1/SP2': 'Microsoft Office',
        'Office Excel Viewer 2003 SP3': 'Microsoft Excel',
        'Office Excel Viewer SP1/SP2': 'Microsoft Excel',
        'Office XP SP3': 'Microsoft Office',
        'Open XML File Converter for Mac': 'Microsoft Office',
        'Oracle Java': 'Oracle Java',
        'Oracle Java SE': 'Oracle Java',
        'Oracle OpenJDK': 'Oracle Java',
        'PowerPoint': 'Microsoft PowerPoint',
        'Powerpoint': 'Microsoft PowerPoint',
        'RARLAB WinRAR': 'RARLAB',
        'RIM BlackBerry': 'RIM',
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
        'Word': 'Microsoft Word',
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
        'excel': 'Microsoft Excel',
        'excel_viewer': 'Microsoft Excel',
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
        '2007 office system sp1/sp2': 'Microsoft Office',
        'office 2003 sp3': 'Microsoft Office',
        'office 2004 for mac': 'Microsoft Office',
        'office 2008 for mac': 'Microsoft Office',
        'open_xml_file_format_converter': 'Microsoft Office',
        'opensuse': 'Linux',
        'powerpoint': 'Microsoft PowerPoint',
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
        'windows-nt': 'Microsoft Windows',
        'windows_2000': 'Microsoft Windows',
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
        'Apple iOS &lt; 10.0.1': 'Apple iOS',
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

        if security_dataset == "APT":
            data["product"] = data["product"].apply(lambda x: self.replace_values_apt(x, product_mapping))
            data["os"] = data["os"].apply(lambda x: self.replace_values_apt(x, os_mapping))
            data['version'] = data['version'].apply(lambda x: self.extract_version_apt(x) if x else x)

        elif security_dataset == "NCSC":
            data["Toepassingen"] = data["Toepassingen"].apply(lambda x: self.replace_values_ncsc(x, product_mapping))
            data["Platformen"] = data["Platformen"].apply(lambda x: self.replace_values_ncsc(x, os_mapping))
            data['Versies'] = data['Versies'].apply(lambda x: self.extract_version_ncsc(x) if x else x)

        return data
    
    def extract_version_ncsc(self, x):
        pattern = r'(\d+(?=\.))'
        versions = []
        for item in x:
            match = re.search(pattern, item)
            if match:
                version = match.group(0)
                if version.isdigit():
                    versions.append(version)
        return versions if versions else ["Unrecovered"]

    def extract_version_apt(self, x):
        pattern = r'(\d+(?=\.))'
        match = re.search(pattern, x)
        if match:
            version = match.group(0)
            if version.isdigit(): 
                return version
        return "Unrecovered"