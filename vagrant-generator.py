import os
import datetime
import subprocess
import argparse
from render import render

# default bootstrap filepath
bootstrap_template_file = "./bootstrap.tpl"
def launch():
    """launches script and does argument handling and sanity-checking.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--environment", default='local', help="specify environment template you want to base provisioning on (default = 'local').")
    parser.add_argument("--render", action='store_true', help="creates a new bootstrap.sh for provisioning based on --environment (default environment = 'local').")
    parser.add_argument("--db_time", help="Not Currently Implemented") # not implemented
    parser.add_argument("--base", action='store_true', help="creates a base box if one does not exist")
    control = parser.add_mutually_exclusive_group()
    control.add_argument("--start", action='store_true', help="starts vagrant, building from base box if needed.")
    control.add_argument("--stop", action='store_true', help="stops vagrant, equivalent to 'vagrant halt'.")
    control.add_argument("--destroy", action='store_true', help="destroys vagrant vm completely, equivalent to 'vagrant destroy'")
    control.add_argument("--rebuild", action='store_true', help="destroys current VM, then rebuilds it from the base box")
    control.add_argument("--from_scratch", action='store_true', help="tears down everything, rebuilds bootstrap.sh, base box, and VM. WILL TAKE A LONG TIME, BE CAREFUL.")
    return parser.parse_args()

def bootstrap_render(environment):
    """ creates a bootstrap.sh file based on an environment variable you specify.
    """
    env_file = "env-{}.yml".format(environment)
    if not os.path.exists(env_file):
        raise IOError("Cannot find environment yaml file for {}".format(environment))
    if not os.path.exists(bootstrap_template_file):
        raise IOError("no bootstrap template exists!")
    print "Rendering bootstrap.sh from provided environment configuration ({})".format(environment)
    render_bootstrap = render(env_file, bootstrap_template_file)
    render_bootstrap.to_file('bootstrap.sh')
    if not os.path.exists('bootstrap.sh'):
        raise IOError("cannot create bootstrap.sh")
    else:
        print "Created a new bootstrap.sh file!"
        return True

def get_database(timestamp):
    """ retrieves either the most recent
    timestamped database or retrieves a database from a specified database
    """
    pass

def start_vagrant():
    """ starts a vagrantvm that runs using a rendered bootstrap.sh file.
    """
    if not os.path.abspath('bootstrap.sh'):
        print "Missing bootstrap.sh. please run jf-setup.py --render to create it."
    else:
        run_vagrant_up = vagrant_cmds("up")
        if run_vagrant_up == 0:
            vagrant_ssh = raw_input("VM Started. Would you like to enter the VM now? [y/N]")
            if vagrant_ssh.lower() == 'y':
                vagrant_ssh = vagrant_cmds("ssh")
            else:
                print "VM created. Use 'vagrant ssh' from this directory to enter the VM.'"
                exit()
        else:
            print "Error starting VM via Vagrant."

def vagrant_cmds(cmdstring):
    cmd = ["vagrant"]
    subcmd = cmdstring.split(' ')
    cmd += subcmd
    print cmd
    return subprocess.call(cmd)


def create_base():
    os.chdir(os.path.abspath('./base'))
    if not os.path.exists('base.sh'):
        print "missing base.sh file used for provisioning."
    else:
        run_vagrant_clear = vagrant_cmds("destroy -f")
        run_vagrant_up = vagrant_cmds("up")
        if run_vagrant_up == 0:
            print "VM jf-base created. packaging now."
            run_vagrant_package = vagrant_cmds("package --output jf-base.box")
            if (run_vagrant_package == 0) and os.path.exists('jf-base.box'):
                print "base box created. Full VM can be created from base box now."
                run_vagrant_destroy = vagrant_cmds("destroy -f")
                os.chdir(os.path.abspath('../'))
        

if __name__ == "__main__":
    setup_app = launch()
    if setup_app.render:
        if bootstrap_render(setup_app.environment):
            print "Created a new bootstrap.sh file\
                    based on environment {}".format(setup_app.environment)
        else:
            print "You must specify an environment name with the render command"
    elif setup_app.start:
        start_vagrant()
    elif setup_app.base:
        create_base()
    elif setup_app.stop:
        print "Stopping Vagrant VM"
        if vagrant_cmds("halt") == 0:
            print "VM stopped successfully"
        else:
            print "problems starting VM. Was it started?"
    elif setup_app.rebuild:
        print "Destroying VM..."
        if vagrant_cmds("destroy -f") == 0:
            print "VM Destroyed. Starting VM...."
            start_vagrant()
        else:
            print "Could not destroy VM. Will attempt to start VM."
            start_vagrant()
    elif setup_app.destroy:
        if vagrant_cmds("destroy -f") == 0:
            print "VM Destroyed."
        else:
            print "Could not destroy VM."
    elif setup_app.from_scratch:
        print "Creating everything from scratch."
        # render bootstrap
        if bootstrap_render(setup_app.environment):
            print "Created bootstrap.sh file for {} environment".format(setup_app.environment)
        else:
            print "Could not create bootstrap.sh file!"
            exit()
        # make sure current vm is down.
        if vagrant_cmds("destroy -f") == 0:
            print "VM Destroyed."
        else:
            print "VM Not Destroyed. Likely it is not up."
        # create base
        create_base()
        # now build VM
        start_vagrant()
