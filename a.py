from subprocess import Popen, PIPE, STDOUT

p = Popen(['python3', './test.py'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)

grep_stdout = p.communicate(input='HELLO WORLD!\n'.encode())

print(grep_stdout)