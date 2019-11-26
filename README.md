# Sunrise OpenCue Installation

## Render Nodes (RQD)

RQD installed in virtual environment running as daemon. If RQD is installed on a user’s machine, activate NIMBY. NIMBY (Not In My Back Yard) is used to lock a user machine so as not to render while a user is using their machine. An RQD config file is used to activate NIMBY.  
RQD has to run as root and needs access to the logging path. The log directory has to be mounted.  
Environment variable `CUEBOT_HOSTS` need to be set and pointing to a valid cuebot server. Environment variables get set on machine startup.  
RQD is run as a systemd daemon on startup.

- Install location for RQD: `/usr/share/rqd`
  - Virtual environment: `/usr/share/rqd/venv`
  - RQD config: `/usr/share/rqd/rqd.conf`
- Command to run RQD on artist machine: `/usr/share/rqd/venv/bin/rqd -d -c /usr/share/rqd/rqd.conf`
- RQD systemd service location: `/etc/systemd/system/rqd.service`
- Command to run RQD on dedicated render node: `/usr/share/rqd/venv/bin/rqd -d`
- Environment path: `/etc/environment`
- Logging path: `/opencue/logs`

### Setup:
The following steps can be followed to mount the logging directory and install RQD on a new render node.

1. `ansible-playbook -i vars/centos7.yml tasks/rqd_sunrise_host.yml --limit=sunrise123`
2. `ansible-playbook -i vars/centos7.yml tasks/mount-opencue.yml --limit=sunrise123`


## Artist Machines (pycue, pyoutline)

Submitting job outlines to the OpenCue render farm requires the pyoutline and pycue modules on artist machines. Artist machines has access to a central virtual environment with pycue and pyoutline installed. The python interpreter from the virtual environment will be used to run submission scripts.  
The current submission scripts only work for Nuke renders. Submission scripts for other DCC applications can be easily implemented.  
The virtual environment will be mounted from a server location on startup. Environment variable `CUE_PYTHON_PATH` has to point to a valid python interpreter with access to pycue and pyoutline modules. Environment variable `CUEBOT_HOSTS` has to point to a valid cuebot server.

- Environment variables path: `/etc/environment`
- Virtual environment mount location: `/opencue/venv`
- `CUE_PYTHON_PATH` points to: `/opencue/venv/bin/python`
- Currently `CUE_PYTHON_PATH` gets set on launching Nuke, and is set in the following config file, `/sunrise/tools/jbm1/pipeline-jbm1/config/sun_shot_launcher/nuke_environment.yaml`.
  
### Setup:
To setup the environment variables and mount scripts for artists, the following steps can be followed.

1. `ansible-playbook -i vars/centos7.yml tasks/mount-opencue.yml`
2. `ansible-playbook -i vars/centos7.yml tasks/opencue_environment.yml`


## CueGUI installation (wranglers and admins)

Cuegui is the user interface for cuebot; used to manage render jobs and nodes. Cuegui is installed on the server but gets mounted to user machines. Access via the terminal is available to everyone with `/opencue` mounted, but the desktop file has to be installed separately.

- Location: `/opencue/venv/bin/cuegui`

### Setup
To install the cuegui desktop file for a specific user, the following ansible install script can by run.

1. `ansible-playbook -i vars/centos7.yml tasks/cuegui.yml --limit=sunrise123`


## Render Manager (cuebot)

The render manager, cuebot, is run on a server in a Docker container. The Postgres database is also run in a Docker container on the same server as cuebot.  
To change the default logging path for all RQD nodes connected to a specific cuebot instance, the environment variable `CUE_FRAME_LOG_DIR` can be specified on the cuebot container creation.

- Logging path: `CUE_FRAME_LOG_DIR=/opencue/logs`
- Server hostname: `cuebot.sunrise.local`
