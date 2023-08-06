import paramiko
import re




def command_ssh_proc(host, user, password, port, command):
    data = ''
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=password, port=port)
    stdin, stdout, stderr = client.exec_command(command)
    data = stdout.read() + stderr.read()
    client.close()
    return data


def get_serial(host, user, password, port):
    ret = command_ssh_proc(host, user, password, port, "/system routerboard print")
    #print ret
    serial = re.findall(r'serial-number:\s+(.+)\r\n', ret)
    model = re.findall(r'model:\s+(.+)\r\n', ret)
    board = re.findall(r'board-name:\s+(.+)\r\n', ret)
    answer = {"serial-number": serial[0], "model": model[0]}
    #print answer
    return answer

def get_identity(host, user, password, port):
    ret = command_ssh_proc(host, user, password, port, "/system identity print")
    identity = re.findall(r'name:\s+(.+)\r\n', ret)
    return identity[0]

#
   #
 #   val = a1.group(1)