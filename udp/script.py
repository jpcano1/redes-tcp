import subprocess

proc = subprocess.Popen("python clienteUDP.py", shell=True, stdout=subprocess.PIPE)
print(proc.stdout.read())