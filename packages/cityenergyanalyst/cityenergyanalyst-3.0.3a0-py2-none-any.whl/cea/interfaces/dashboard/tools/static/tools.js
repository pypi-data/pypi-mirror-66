/*jslint browser:true */
/*global $, Tabulator, io, console, window */

/**
 * Functions to run a tool from the tools page.
 */

/**
 * Read out the value of the parameter as defined by the form input - this depends on the parameter_type.
 */
function read_value(element) {
    "use strict";
    let value = null;
    switch (element.dataset.ceaParameterTypename) {
    case "ChoiceParameter":
    case "ScenarioNameParameter":
        value = $(element)[0].value;
        break;
    case "WeatherPathParameter":
        value = $(element)[0].value;
        break;
    case "BooleanParameter":
        value = $(element)[0].checked;
        break;
    case "PathParameter":
        value = $(element)[0].value;
        break;
    case "MultiChoiceParameter":
    case "BuildingsParameter":
        value = $(element).val();
        if (value) {
            value = value;
        } else {
            value = [];
        }
        break;
    case "SubfoldersParameter":
        value = $(element).val();
        break;
    case "JsonParameter":
        value = JSON.parse($(element).val());
        break;
    default:
        // handle the default case
        value = $(element)[0].value;
    }
    return value;
}

/**
 * Read the values of all the parameters.
 */
function get_parameter_values() {
    "use strict";
    let result = {};
    $(".cea-parameter").not("bootstrap-select").each(function (index, element) {
        console.log(`Reading parameter: ${element.id}`);
        result[element.id] = read_value(element);
    });
    console.log("get_parameter_values(): result=", result);
    return result;
}

function cea_run(script) {
    "use strict";
    if (!$("#cea-tool-parameters").parsley().isValid()) {
        return false;
    }

    let new_job_info = {"script": script, "parameters": get_parameter_values()};
    $.ajax({
        type: "post",
        url: "/server/jobs/new",
        data: JSON.stringify(new_job_info),
        contentType: "application/json; charset=utf-8",
        traditional: true,
        success: function (job_info) {
            $.post(`start/${job_info.id}`, function () {
                window.location.href = "/tools";
            });
        }
    });
}

function cea_save_config(script) {
    "use strict";
    if (!$("#cea-tool-parameters").parsley().isValid()) {
        return false;
    }
    let $cea_save_config_modal = $("#cea-save-config-modal");
    $cea_save_config_modal.modal({"show": true, "backdrop": "static"});
    $.post(`save-config/${script}`, get_parameter_values(), null, "json");
    $cea_save_config_modal.modal("hide");
}


/**
 * Update the div#cea-console-output-body with the output of the script until it is done.
 * @param script
 */
function update_output(script) {
    "use strict";
    $.getJSON(`read/${script}`, {}, function (msg) {
        if (msg === null) {
            $.getJSON(`is-alive/${script}`, {}, function (msg) {
                if (msg) {
                    setTimeout(update_output, 1000, script);
                } else {
                    $('.cea-modal-close').removeAttr('disabled');
                    $.getJSON('exitcode/' + script, {}, function (msg) {
                        if (msg === 0) {
                            $('.cea-modal-close').addClass('btn-success');
                        } else {
                            $('.cea-modal-close').addClass('btn-danger');
                        }
                    });
                }
            });

        }
        else {
            $('#cea-console-output-body').append(msg.message);
            setTimeout(update_output, 1000, script);
        }
    });
}


/**
 * Show an open file dialog for a cea FileParameter and update the contents of the
 * input field.
 *
 * @param parameter_name
 */
function show_open_file_dialog(parameter_fqname) {
    "use strict";
    $.get(`open-file-dialog/${parameter_fqname}`, {}, function (html) {
        $("#cea-file-dialog .modal-content").html(html);
        $("#cea-file-dialog").modal({"show": true, "backdrop": "static"});
    });
}

/**
 * Navigate the open file dialog to a new folder.
 * @param parameter_fqname
 */
function file_dialog_navigate_to(parameter_fqname, current_folder, folder) {
    "use strict";
    $.get("open-file-dialog/" + parameter_fqname, {current_folder: current_folder, folder: folder}, function (html) {
        $("#cea-file-dialog .modal-content").html(html);
    });
}

/**
 * User selected a file, highlight it.
 * @param link
 * @param file
 */
function select_file(link) {
    "use strict";
    $(".cea-file-listing a").removeClass("bg-primary");
    $(link).addClass("bg-primary");
    $("#cea-file-dialog-select-button").prop("disabled", false);
}

/**
 * Save the selected file name (full path) to the input[type=text] with the id <target_id>.
 * @param target_id
 */
function save_file_name(target_id) {
    "use strict";
    // figure out file path
    let file_path = $(".cea-file-listing a.bg-primary").data("save-file-path");
    $(`#${target_id}`).val(file_path);
}

/**
 * Show an open folder dialog for a cea PathParameter and update the contents of the
 * input field.
 *
 * @param parameter_name
 */
function show_open_folder_dialog(parameter_fqname) {
    "use strict";
    $.get(`open-folder-dialog/${parameter_fqname}`, {}, function (html) {
        $("#cea-folder-dialog .modal-content").html(html);
        $("#cea-folder-dialog").modal({"show": true, "backdrop": "static"});
    });
}

/**
 * Navigate the open file dialog to a new folder.
 * @param parameter_fqname
 * @param current_folder
 * @param folder
 */
function folder_dialog_navigate_to(parameter_fqname, current_folder, folder) {
    $.get(`open-folder-dialog/${parameter_fqname}`, {current_folder: current_folder, folder: folder}, function (html) {
        $("#cea-folder-dialog .modal-content").html(html);
    });
}

/**
 * Save the selected folder name (full path) to the input[type=text] with the id <target_id>.
 * @param target_id
 * @param folder_path
 */
function save_folder_name(target_id, folder_path) {
    // figure out folder path
    $(`#${target_id}`).val(folder_path).trigger("input").trigger("change");
    console.log(target_id);
}
