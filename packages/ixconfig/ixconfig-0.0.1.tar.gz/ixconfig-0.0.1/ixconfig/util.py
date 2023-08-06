import re
import subprocess


def matchmany(out, patterns):
    matches = [
        re.search(pattern, line) for line in out.splitlines()
        for pattern in patterns]
    return {
        k: v for match in matches if match
        for k, v in match.groupdict().items()}


def execmatch(cmd, patterns, error_msgs=None):
    '''Perform re.match against all the patterns after running the bash command.

    Arguments:
        command (str): bash command to execute.
        patterns (list(str)): list of regex patterns to match against

    Returns:
        dict containing the group name (as passed in pattern element)
        and value as the matched value.
    '''
    try:
        cmdargs = cmd.split(' ') if isinstance(cmd, str) else cmd
        out = subprocess.run(cmdargs, check=True, capture_output=True).stdout.decode('utf-8')
        if any(msg.lower() in out.lower() for msg in as_tuple(error_msgs)):
            return {}

        return matchmany(out, patterns)
    except subprocess.CalledProcessError:
        return {}

def as_tuple(x):
    return x if isinstance(x, tuple) else (x,) if x else ()
