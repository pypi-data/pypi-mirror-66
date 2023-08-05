import subprocess

class CliHandler:
    def __init__(self):
        self.process = {}
        self.returncode = {}

    def call(self, name, cmd, shell=True):
        """
        this function is used to spawn new subprocess
        if this function is called with same name more than one time
        and while previous process is not finished, it will return the
        previous process and will not spawn new subprocess
        """
        if name in self.process:
            return name
        else:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=shell)
            self.process[name] = p
            self.returncode[name] = None
            return name

    def get(self, name):
        """
        this will return subprocess object corrosponding
        to given name as input
        """
        if name in self.process:
            return self.process[name]

    def return_code(self, name):
        if name in self.returncode:
            return self.returncode[name]

    def reset(self, name):
        if name in self.process:
            del self.process[name]
        if name in self.returncode:
            del self.returncode[name]

    def list_process(self):
        """
        return all registered process
        """
        return self.process

    def capture(self, name):
        """
        once a subprocess is spawned, it's output
        can be captured via this function as an iterator
        """
        if name in self.process:
            p = self.process[name]

            while True:
                # returns None while subprocess is running
                retcode = p.poll()
                line = p.stdout.readline()
                line = line.decode().strip()
                if len(line) > 0 and name in self.process: yield line

                if retcode is not None:
                    if name in self.process:
                        self.returncode[name] = retcode
                        del self.process[name]
                    break

    def kill(self, name):
        """
        kill the spawned subrocess by it's name
        """
        if name in self.process:
            p = self.process[name]
            p.kill()
            self.returncode[name] = 130
            del self.process[name]
            return 130

    def __repr__(self):
        return str(self.__class__.__name__)+'({})'.format(self.process)

    def __len__(self):
        return len(self.process)

    def __getitem__(self, position):
        return list(self.process.items())[position]
