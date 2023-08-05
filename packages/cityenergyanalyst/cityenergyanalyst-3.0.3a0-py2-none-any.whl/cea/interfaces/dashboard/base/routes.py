from flask import Blueprint, render_template, redirect, request, url_for, jsonify, current_app

import cea.plots
import cea.glossary


blueprint = Blueprint(
    'base_blueprint',
    __name__,
    url_prefix='',
    template_folder='templates',
    static_folder='static'
)


@blueprint.route('/')
def route_default():
    return redirect(url_for('landing_blueprint.index'))


@blueprint.route('/glossary_search')
def route_glossary_search():
    query = request.args.get('query')
    glossary = cea.glossary.read_glossary_dicts()
    return jsonify(filter(lambda row: query.lower() in row['VARIABLE'].lower(), glossary))


@blueprint.route('/fixed_<template>')
def route_fixed_template(template):
    return render_template('fixed/fixed_{}.html'.format(template))


@blueprint.route('/page_<error>')
def route_errors(error):
    return render_template('errors/page_{}.html'.format(error))

## Login & Registration



@blueprint.route('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

## Errors



@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('errors/page_403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('errors/page_404.html'), 404


@blueprint.app_errorhandler(500)
def internal_error(error):
    import traceback
    error_trace = traceback.format_exc()
    return error_trace, 500
