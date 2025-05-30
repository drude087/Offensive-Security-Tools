# Set the output file path
$outputFile = "C:\Windows\Temp\enum"

# System Info
$systeminfo = systeminfo | Out-String
$OSInfo = (Get-CimInstance -ClassName Win32_OperatingSystem | Select-Object Caption, OSArchitecture, Version) | Out-String
$Is64Bit = [Environment]::Is64BitOperatingSystem
$Uptime = (Get-CimInstance Win32_OperatingSystem).LastBootUpTime

# User and Group Info
$LoggedInUser = (Get-WmiObject -Class Win32_ComputerSystem | Select-Object UserName) | Out-String
$LocalUsers = (Get-LocalUser) | Out-String
$UserGroups = (whoami /groups) | Out-String

# Network Info
$IPConfig = (Get-NetIPConfiguration) | Out-String
$DNSServers = (Get-DnsClientServerAddress) | Out-String
$ActiveConnections = (Get-NetTCPConnection) | Out-String

# Processes and Services
$RunningProcesses = (Get-Process | Select-Object Name, Id, CPU) | Out-String
$RunningServices = (Get-Service | Select-Object Name, Status) | Out-String

# File System Info
$AccessibleDrives = (Get-PSDrive -PSProvider FileSystem) | Out-String

# Registry Info (HKCU)
$HKCUKeys = (Get-ChildItem -Path HKCU:\Software) | Out-String
$SpecificKeys = (Get-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion") | Out-String

# Installed Software
$InstalledSoftware = (Get-WmiObject -Class Win32_Product | Select-Object Name, Version) | Out-String

# Security Configurations
$DefenderStatus = (Get-MpComputerStatus) | Out-String
$AccountPolicies = (net accounts) | Out-String

# Hardware Info
$ProcessorInfo = (Get-CimInstance -ClassName Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors) | Out-String
$MemoryInfo = (Get-CimInstance -ClassName Win32_PhysicalMemory | Select-Object Capacity, Speed, Manufacturer) | Out-String

# Scheduled Tasks
$ScheduledTasks = (Get-ScheduledTask | Select-Object TaskName, State, Author) | Out-String

# Save the results to the file
Out-File -FilePath $outputFile -Append -InputObject "System Information:`n$systeminfo"
Out-File -FilePath $outputFile -Append -InputObject "Operating System Information:`n$OSInfo"
Out-File -FilePath $outputFile -Append -InputObject "`nIs 64-Bit OS: $Is64Bit"
Out-File -FilePath $outputFile -Append -InputObject "`nSystem Uptime: $Uptime"

Out-File -FilePath $outputFile -Append -InputObject "`nLogged-In User:`n$LoggedInUser"
Out-File -FilePath $outputFile -Append -InputObject "`nLocal Users:`n$LocalUsers"
Out-File -FilePath $outputFile -Append -InputObject "`nUser Groups:`n$UserGroups"

Out-File -FilePath $outputFile -Append -InputObject "`nNetwork Configuration:`n$IPConfig"
Out-File -FilePath $outputFile -Append -InputObject "`nDNS Servers:`n$DNSServers"
Out-File -FilePath $outputFile -Append -InputObject "`nActive TCP Connections:`n$ActiveConnections"

Out-File -FilePath $outputFile -Append -InputObject "`nRunning Processes:`n$RunningProcesses"
Out-File -FilePath $outputFile -Append -InputObject "`nRunning Services:`n$RunningServices"

Out-File -FilePath $outputFile -Append -InputObject "`nFile System Information:`n$AccessibleDrives"

Out-File -FilePath $outputFile -Append -InputObject "`nRegistry Information (HKCU):`n$HKCUKeys"
Out-File -FilePath $outputFile -Append -InputObject "`nSpecific Registry Keys:`n$SpecificKeys"

Out-File -FilePath $outputFile -Append -InputObject "`nInstalled Software:`n$InstalledSoftware"

Out-File -FilePath $outputFile -Append -InputObject "`nWindows Defender Status:`n$DefenderStatus"
Out-File -FilePath $outputFile -Append -InputObject "`nAccount Policies:`n$AccountPolicies"

Out-File -FilePath $outputFile -Append -InputObject "`nProcessor Information:`n$ProcessorInfo"
Out-File -FilePath $outputFile -Append -InputObject "`nPhysical Memory Information:`n$MemoryInfo"

Out-File -FilePath $outputFile -Append -InputObject "`nScheduled Tasks:`n$ScheduledTasks"

# Move Accessible Files section to the end
$AccessibleFiles = (Get-ChildItem -Path "C:\" -Recurse -ErrorAction SilentlyContinue | Select-Object FullName, Length, LastWriteTime) | Out-String
Out-File -FilePath $outputFile -Append -InputObject "`nAccessible Files (C:\):`n$AccessibleFiles"

# Confirm that the file was saved
Write-Host "System information has been saved to: $outputFile"
