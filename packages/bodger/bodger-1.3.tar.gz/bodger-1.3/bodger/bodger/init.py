# Import python libs
import subprocess
import fnmatch


def __init__(hub):
    # Remember not to start your app in the __init__ function
    # This function should just be used to set up the plugin subsystem
    # Add another function to call from your run.py to start the app
    hub.pop.sub.add(dyne_name="corn")


def cli(hub):
    hub.pop.config.load(["bodger"], cli="bodger")
    hub.corn.init.standalone()
    hub.bodger.init.match()


def match(hub):
    """
    Find the command to execute in the config, match the corn data and run
    """
    runs = []
    cmd = hub.OPT["bodger"]["cmd"]
    if cmd not in hub.OPT["bodger"]:
        print(f"Command {cmd} not found!")
        return
    for tgt in hub.OPT["bodger"][cmd]:
        corn, glob = tgt.split(":")
        val = hub.corn.CORN[corn]
        if fnmatch.fnmatch(val, glob):
            tcmd = hub.OPT.bodger[cmd][tgt]
            if isinstance(tcmd, str):
                runs.append(tcmd)
            else:
                runs.extend(tcmd)
    for run in runs:
        subprocess.run(run, shell=True)
