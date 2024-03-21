import re
import subprocess
import sys

if len(sys.argv) != 2:
    print('Usage: gerritify.py <first_commit>')
    quit()

commits = subprocess.run(['git', 'log', '--pretty=format:"%H"'], stdout=subprocess.PIPE).stdout.decode('utf-8')
commits = commits.split('\n')

subprocess.run(['git', 'reset', '--hard', sys.argv[1]])

changes = []
for commit in commits:
    if re.search('^"[a-z0-9]{40}"$', commit):
        # this is, in fact, a commit
        commit = commit.replace('"', '')
        print('Found '+commit)
        if commit == sys.argv[1]:
            # thats it
            break
        else:
            changes.append(commit)
    else:
        raise Exception("Didn't encounter a commit")

# gerritify
changes.reverse()
for change in changes:
    print('Applying '+change)
    subprocess.run(['git', 'cherry-pick', '-n', change])
    subprocess.run(['git', 'commit', '--no-edit', '-c', change])
