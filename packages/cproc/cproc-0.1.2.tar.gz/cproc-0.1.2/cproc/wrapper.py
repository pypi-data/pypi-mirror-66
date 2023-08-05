import psutil
from subprocess import Popen
import sys
import time
import logging
import logging.config
import os
import json

probes = [
    psutil.Process.cmdline,
    psutil.Process.cwd,
    psutil.Process.environ,
    psutil.Process.uids,
    psutil.Process.gids,
    psutil.Process.exe
]


def capture_process(pid):
    global probes
    process_info = {'pid': pid}
    try:
        proc = psutil.Process(pid)
    except psutil.Error as e:
        print(e)
        return
    for p in probes:
        try:
            process_info[p.__name__] = p(proc)
        except psutil.Error as e:
            print("Probing %s: %s" % (p.__name__, e))
    return process_info


def set_uid_gid(uid, gid):
    def result():
        print('starting demotion')
        try:
            os.setuid(uid)
            os.setgid(gid)
        except PermissionError as e:
            print("Error during uid/gid setup (%d/%d): %s" % (uid, gid, e))
            raise e
        print('finished demotion')
    return result


def spawn_process(pinfo, wait=True):
    uid = pinfo.get('uids')[0]
    gid = pinfo.get('gids')[0]
    environ = pinfo.get('environ', {})
    cmdline = pinfo.get('cmdline', [])
    cwd = pinfo.get('cwd', '')
    try:
        proc = Popen(
            cmdline,
            cwd=cwd,
            env=environ,
            preexec_fn=set_uid_gid(uid, gid))
        if wait:
            proc.wait()
            return proc.returncode
    except Exception as e:
        print("Error during call: %s" % e)
    return
