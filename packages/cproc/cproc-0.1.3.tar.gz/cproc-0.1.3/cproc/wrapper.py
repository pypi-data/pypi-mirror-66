import psutil
from subprocess import Popen
import os


probes = [
    psutil.Process.name,
    psutil.Process.cmdline,
    psutil.Process.cwd,
    psutil.Process.environ,
    psutil.Process.uids,
    psutil.Process.gids,
    psutil.Process.exe
]


def set_uid_gid(uid: int, gid: int):
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


def capture_process(proc: psutil.Process):
    global probes
    process_info = {'pid': proc.pid}
    for p in probes:
        try:
            process_info[p.__name__] = p(proc)
        except psutil.Error as e:
            print("Probing %s: %s" % (p.__name__, e))
    return process_info


def get_toplevel(proc: psutil.Process) -> psutil.Process:
    next_parent = proc
    while True:
        if next_parent.parent() is None: # init process
            return next_parent
        if next_parent.parent().parent() is None:
            return next_parent
        next_parent = next_parent.parent()


def process_tree(proc: psutil.Process, tree_dict=None) -> psutil.Process:
    if tree_dict is None:
        tree_dict = capture_process(proc)
    tree_dict['children'] = list(map(lambda x: process_tree(x), proc.children()))
    return tree_dict


def capture(pid: int, toplevel_tree=False, child_tree=False):
    try:
        proc = psutil.Process(pid)
    except psutil.Error as e:
        print(e)
        return

    result = {
        'target': capture_process(proc),
        'toplevel': capture_process(get_toplevel(proc))
    }
    if result['target']['pid'] != result['toplevel']['pid']:
        result['parent'] = capture_process(proc.parent())

    if toplevel_tree:
        result['toplevel_tree'] = process_tree(get_toplevel(proc))

    if child_tree:
        result['child_tree'] = process_tree(proc)

    return result


def spawn_process(pinfo_in, wait=True, parent=False, toplevel=False, inherit_env=False):
    pinfo = pinfo_in.get('target')

    if parent and toplevel:
        print("Error: parent and toplevel are mutually exclusive.")
        return

    if parent:
        pinfo = pinfo_in.get('parent')
        if pinfo is None:
            print("Error: The process capture has no parent.")
            return

    if toplevel:
        pinfo = pinfo_in.get('toplevel')

    uid = pinfo.get('uids')[0]
    gid = pinfo.get('gids')[0]
    if inherit_env:
        environ = dict(os.environ)
        environ.update(pinfo.get('environ', {}))
    else:
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
