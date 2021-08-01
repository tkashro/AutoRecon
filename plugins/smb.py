from autorecon import ServiceScan

class NmapSMB(ServiceScan):

    def __init__(self):
        super().__init__()
        self.name = "Nmap SMB"
        self.tags = ['default', 'smb', 'active-directory']

    def configure(self):
        self.add_service_match(['^smb', '^microsoft\-ds', '^netbios'])

    def manual(self):
        self.add_manual_commands('Nmap scans for SMB vulnerabilities that could potentially cause a DoS if scanned (according to Nmap). Be careful:', [
            'nmap {nmap_extra} -sV -p {port} --script="smb-vuln-ms06-025" --script-args="unsafe=1" -oN "{scandir}/{protocol}_{port}_smb_ms06-025.txt" -oX "{scandir}/xml/{protocol}_{port}_smb_ms06-025.xml" {address}',
            'nmap {nmap_extra} -sV -p {port} --script="smb-vuln-ms07-029" --script-args="unsafe=1" -oN "{scandir}/{protocol}_{port}_smb_ms07-029.txt" -oX "{scandir}/xml/{protocol}_{port}_smb_ms07-029.xml" {address}',
            'nmap {nmap_extra} -sV -p {port} --script="smb-vuln-ms08-067" --script-args="unsafe=1" -oN "{scandir}/{protocol}_{port}_smb_ms08-067.txt" -oX "{scandir}/xml/{protocol}_{port}_smb_ms08-067.xml" {address}'
        ])

    async def run(self, service):
        await service.execute('nmap {nmap_extra} -sV -p {port} --script="banner,(nbstat or smb* or ssl*) and not (brute or broadcast or dos or external or fuzzer)" -oN "{scandir}/{protocol}_{port}_smb_nmap.txt" -oX "{scandir}/xml/{protocol}_{port}_smb_nmap.xml" {address}')

class Enum4Linux(ServiceScan):

    def __init__(self):
        super().__init__()
        self.name = "Enum4Linux"
        self.tags = ['default', 'enum4linux', 'active-directory']

    def configure(self):
        self.add_service_match(['^ldap', '^smb', '^microsoft\-ds', '^netbios'])
        self.add_port_match('tcp', [139, 389, 445])
        self.add_port_match('udp', 137)
        self.run_once(True)

    async def run(self, service):
        await service.execute('enum4linux -a -M -l -d {address} 2>&1', outfile='enum4linux.txt')

class NBTScan(ServiceScan):

    def __init__(self):
        super().__init__()
        self.name = "nbtscan"
        self.tags = ['default', 'netbios', 'active-directory']

    def configure(self):
        self.add_service_match(['^smb', '^microsoft\-ds', '^netbios'])
        self.add_port_match('udp', 137)
        self.run_once(True)

    async def run(self, service):
        await service.execute('nbtscan -rvh {address} 2>&1', outfile='nbtscan.txt')

class SMBClient(ServiceScan):

    def __init__(self):
        super().__init__()
        self.name = "SMBClient"
        self.tags = ['default', 'smb', 'active-directory']

    def configure(self):
        self.add_service_match(['^smb', '^microsoft\-ds', '^netbios'])
        self.add_port_match('tcp', [139, 445])
        self.run_once(True)

    async def run(self, service):
        await service.execute('smbclient -L\\\\ -N -I {address} 2>&1', outfile='smbclient.txt')

class SMBMap(ServiceScan):

    def __init__(self):
        super().__init__()
        self.name = "SMBMap"
        self.tags = ['default', 'smb', 'active-directory']

    def configure(self):
        self.add_service_match(['^smb', '^microsoft\-ds', '^netbios'])

    async def run(self, service):
        await service.execute('smbmap -H {address} -P {port} 2>&1', outfile='smbmap-share-permissions.txt')
        await service.execute('smbmap -u null -p "" -H {address} -P {port} 2>&1', outfile='smbmap-share-permissions.txt')
        await service.execute('smbmap -H {address} -P {port} -R 2>&1', outfile='smbmap-list-contents.txt')
        await service.execute('smbmap -u null -p "" -H {address} -P {port} -R 2>&1', outfile='smbmap-list-contents.txt')
        await service.execute('smbmap -H {address} -P {port} -x "ipconfig /all" 2>&1', outfile='smbmap-execute-command.txt')
        await service.execute('smbmap -u null -p "" -H {address} -P {port} -x "ipconfig /all" 2>&1', outfile='smbmap-execute-command.txt')
