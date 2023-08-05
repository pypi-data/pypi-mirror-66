from flask import Blueprint, render_template, current_app, jsonify, request, redirect, url_for
import subprocess

import cea.scripts
import cea.inputlocator
import cea.config
import os
import psutil

blueprint = Blueprint(
    'tools_blueprint',
    __name__,
    url_prefix='/tools',
    template_folder='templates',
    static_folder='static',
)

# maintain a list of all subprocess.Popen objects created
worker_processes = {}  # jobid -> subprocess.Popen


def shutdown_worker_processes():
    """When shutting down the flask server, make sure any subprocesses are also terminated. See issue #2408."""
    for jobid in worker_processes.keys():
        kill_job(jobid)


def kill_job(jobid):
    """Kill the processes associated with a jobid"""
    if not jobid in worker_processes:
        return

    popen = worker_processes[jobid]
    # using code from here: https://stackoverflow.com/a/4229404/2260
    # to terminate child processes too
    print("killing child processes of {jobid} ({pid})".format(jobid=jobid, pid=popen.pid))
    try:
        process = psutil.Process(popen.pid)
    except psutil.NoSuchProcess:
        return
    children = process.children(recursive=True)
    for child in children:
        print("-- killing child {pid}".format(pid=child.pid))
        child.kill()
    process.kill()
    del worker_processes[jobid]


@blueprint.route("/")
def route_index():
    return render_template("job_table.html")


@blueprint.route("/workers", methods=["GET"])
def route_workers():
    """Return a list of worker processes"""
    processes = []
    for worker in worker_processes.values():
        processes.append(worker.pid)
        processes.extend(child.pid for child in psutil.Process(worker.pid).children(recursive=True))
    return jsonify(sorted(processes))


@blueprint.route('/start/<int:jobid>', methods=['POST'])
def route_start(jobid):
    """Start a ``cea-worker`` subprocess for the script. (FUTURE: add support for cloud-based workers"""
    print("tools/route_start: {jobid}".format(**locals()))
    worker_processes[jobid] = subprocess.Popen(["python", "-m", "cea.worker", "{jobid}".format(jobid=jobid)])
    return jsonify(jobid)


@blueprint.route('/save-config/<script>', methods=['POST'])
def route_save_config(script):
    """Save the configuration for this tool to the configuration file"""
    for parameter in parameters_for_script(script, current_app.cea_config):
        print('%s: %s' % (parameter.name, request.form.get(parameter.name)))
        parameter.set(parameter.decode(request.form.get(parameter.name)))
    current_app.cea_config.save()
    return jsonify(True)


@blueprint.route('/restore-defaults/<script_name>')
def route_restore_defaults(script_name):
    """Restore the default configuration values for the CEA"""
    config = current_app.cea_config

    for parameter in parameters_for_script(script_name, config):
        if parameter.name != 'scenario':
            parameter.set(parameter.default)
    config.save()

    return redirect(url_for('tools_blueprint.route_tool', script_name=script_name))


@blueprint.route('/open-folder-dialog/<fqname>')
def route_open_folder_dialog(fqname):
    """Return html of folder structure for that parameter"""

    # these arguments are only set when called with the `navigate_to` function on an already open
    # folder dialog
    current_folder = request.args.get('current_folder')
    folder = request.args.get('folder')

    config = current_app.cea_config
    section, parameter_name = fqname.split(':')
    parameter = config.sections[section].parameters[parameter_name]

    if not current_folder:
        # first time calling, use current value of parameter for current folder
        current_folder = os.path.abspath(parameter.get())
        folder = None
    else:
        current_folder = os.path.abspath(os.path.join(current_folder, folder))

    if not os.path.exists(current_folder):
        # use home directory if it doesn't exist
        current_folder = os.path.expanduser('~')

    folders = []
    for entry in os.listdir(current_folder):
        if os.path.isdir(os.path.join(current_folder, entry)):
            folders.append(entry)

    current_folder = os.path.normpath(current_folder)
    breadcrumbs = current_folder.split(os.path.sep)

    return render_template('folder_listing.html', current_folder=current_folder,
                           folders=folders, title=parameter.help, fqname=fqname,
                           parameter_name=parameter.name, breadcrumbs=breadcrumbs)


@blueprint.route('/open-file-dialog/<fqname>')
def route_open_file_dialog(fqname):
    """Return html of file structure for that parameter"""

    # these arguments are only set when called with the `navigate_to` function on an already open
    # file dialog
    current_folder = request.args.get('current_folder')
    folder = request.args.get('folder')

    config = current_app.cea_config
    section, parameter_name = fqname.split(':')
    parameter = config.sections[section].parameters[parameter_name]

    if not current_folder:
        # first time calling, use current value of parameter for current folder
        current_folder = os.path.dirname(parameter.get())
        folder = None
    else:
        current_folder = os.path.abspath(os.path.join(current_folder, folder))

    if not os.path.exists(current_folder):
        # use home directory if it doesn't exist
        current_folder = os.path.expanduser('~')


    folders = []
    files = []
    for entry in os.listdir(current_folder):
        if os.path.isdir(os.path.join(current_folder, entry)):
            folders.append(entry)
        else:
            ext = os.path.splitext(entry)[1]
            if parameter._extensions and ext and ext[1:] in parameter._extensions:
                files.append(entry)
            elif not parameter._extensions:
                # any file can be added
                files.append(entry)

    breadcrumbs = os.path.normpath(current_folder).split(os.path.sep)

    return render_template('file_listing.html', current_folder=current_folder,
                           folders=folders, files=files, title=parameter.help, fqname=fqname,
                           parameter_name=parameter.name, breadcrumbs=breadcrumbs)


@blueprint.route('/<script_name>')
def route_tool(script_name):
    config = current_app.cea_config
    locator = cea.inputlocator.InputLocator(config.scenario)
    script = cea.scripts.by_name(script_name)
    weather_dict = {wn: locator.get_weather(wn) for wn in locator.get_weather_names()}

    parameters = []
    categories = {}
    for _, parameter in config.matching_parameters(script.parameters):
        if parameter.category:
            if parameter.category not in categories:
                categories[parameter.category] = []
            categories[parameter.category].append(parameter)
        else:
            parameters.append(parameter)

    return render_template('tool.html', script=script, parameters=parameters, categories=categories,
                           weather_dict=weather_dict, last_updated=dir_last_updated())


def parameters_for_script(script_name, config):
    """Return a list consisting of :py:class:`cea.config.Parameter` objects for each parameter of a script"""
    import cea.scripts
    parameters = [p for _, p in config.matching_parameters(cea.scripts.by_name(script_name).parameters)]
    return parameters


def dir_last_updated():
    return str(max(os.path.getmtime(os.path.join(root_path, f))
               for root_path, dirs, files in os.walk(os.path.join(os.path.dirname(__file__), 'static'))
               for f in files))