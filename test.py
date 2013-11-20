import applescript

from subprocess import Popen, PIPE


scpt = "say 'hello'"


code = 'tell application "Google Chrome" to return URL of active tab of front window'
# scpt = '''
#  tell application 'Google Chrome' to return URL of active tab of front window
# '''


def run_this_scpt(scpt, args=[]):
    p = Popen(['osascript', '-'] + args, stdin=PIPE, stdout=PIPE,
              stderr=PIPE)
    stdout, stderr = p.communicate(scpt)
    print stderr
    print stdout
    return stdout




url =run_this_scpt(code)
print url


# p = Popen(['osascript', '-'] , stdin=PIPE, stdout=PIPE,
#           stderr=PIPE)
# stdout, stderr = p.communicate(scpt)
# print (p.returncode, stdout, stderr)







