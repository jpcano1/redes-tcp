import subprocess

for i in range(10):
    proc = subprocess.Popen("python clienteUDP.py", shell=True, stdout=subprocess.PIPE)