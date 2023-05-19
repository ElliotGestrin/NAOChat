import subprocess

def main():
    command = "python2.7 nao_listner.py"
    pipe = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    
    while True:
        for line in pipe.stdout:
            line = line.decode().strip()  
            if not line:
                continue
            print(line)
    
if __name__ == "__main__":
    main()