/* get list of plots to work on... */

$(document).ready(function() {
    $( ".table-dialog" ).dialog({
        autoOpen: false, height: "auto", width: "auto",

        open: function (event, ui) {
            $(`#${event.target.id}`).dialog( "option", "minWidth", event.target.offsetParent.offsetWidth)
        },
        resize: function( event, ui ) {
            event.target.style.width = '100%';
        },
        resizeStop: function( event, ui ) {
            event.target.style.width = '100%';
        }

    });
    load_all_plots();

    var categories = JSON.parse($('#cea-dashboard-add-plot').attr('data-cea-categories'));
    console.log("assigned categories!");
    console.log(categories);

    $("[id|=cea-plot-category]").on("change", function(){
        let category_name = this.value;
        $("[id|=cea-plot-name]").empty();
        $.each(categories[category_name]["plots"], function(i, p){
            console.log(p);
            $("[id|=cea-plot-name]").append($("<option></option>").attr("value", p.id).text(p.name));
        });

        console.log(categories[category_name]["plots"]);
    });

    $("#cea-dashboard-edit-plot").on("show.bs.modal", function (e) {
        let plot_index = e.relatedTarget.dataset.plotIndex;
        let dashboard_index = e.relatedTarget.dataset.dashboardIndex;
        let url = `plot-parameters/${dashboard_index}/${plot_index}`;
        $.get(url, function (data) {
            $("#cea-dashboard-edit-plot-form").html(data)
                .attr("action", url)
                .attr("method", "POST");
            $(".selectpicker").selectpicker({"actionsBox": true});
            $(".js-switch").each(function(_, checkbox){
                console.log("setting up Switchery");
                console.log(checkbox);
                switcher = new Switchery(checkbox);
            });
        }).fail(function (data) {
            console.log("something went terribly wrong?!");
            console.log(data);
        });
    });

    $("#cea-dashboard-replace-plot").on("show.bs.modal", function (e) {
        let plot_index = e.relatedTarget.dataset.plotIndex;
        let dashboard_index = e.relatedTarget.dataset.dashboardIndex;
        let url = `replace-plot/${dashboard_index}/${plot_index}`;
        $("#cea-dashboard-replace-plot-form").attr("action", url)
            .attr("method", "POST");
    });

    $("#cea-dashboard-edit-plot-form").submit(function (e) {
        e.preventDefault();
        $.post($("#cea-dashboard-edit-plot-form").attr("action"), get_parameter_values(), function(data){
            console.log(data);
            location.reload();
        }, "json");
        return false;
    });

    $("#dashboard-selector").val(window.location.href.split('/').pop().replace(/[^0-9]/g, ''))
        .change(function () {
            let value = $(this).val();
            if(value === "manage") {
                window.location.href = "./manage";
            } else if(value !== "new") {
                window.location.href = `./${value}`;
            }
        });
});

function load_all_plots() {
    $(".cea-plot").map(function() {
        let dashboard_index = this.dataset.ceaDashboardIndex;
        let plot_index = this.dataset.ceaPlotIndex;
        let content_div = $(`#x_content-${dashboard_index}-${plot_index}`);
        let table_div = $(`#x_table-${dashboard_index}-${plot_index}`);

        $.get(`../div/${dashboard_index}/${plot_index}`, function(data){
            content_div.children().replaceWith(data);
        }).fail(function(data) {
            // Server error
            if (data.status === 500) {
                content_div.children().replaceWith("ERROR: " + $(data.responseText).filter("p").text());
                console.log("error creating plot: ", `#x_content-${dashboard_index}-${plot_index}`);
                console.log(data);
            }
            // Missing files
            if (data.status === 404) {
                content_div.children().replaceWith(data.responseText);
            }
        });

        $.get(`../table/${dashboard_index}/${plot_index}`, function(data){
            // When data is not empty
            if(data.length) {
                table_div.empty().append(data);
                $('#table-btn-'+plot_index).show();
            }
        }).fail(function(data) {
            table_div.children().replaceWith("");
            console.log("error creating plot:", `table-${dashboard_index}-${plot_index}`);
            console.log(data);
        });
    });
}

function duplicate_dashboard(dashboard_index) {
    $.get(`./duplicate/${dashboard_index}`, {}, function(html) {
        $('#cea-prompt .modal-content').html(html);
        $('#cea-prompt').modal({'show': true, 'backdrop': 'static'});
    });
}

function add_new_dashboard() {
    $.get("new", function (html) {
        $("#cea-prompt .modal-content").html(html);
        $("#cea-prompt").modal({"show": true, "backdrop": "static"});
    });
}

function open_table(element) {
    $( `#x_table-${element.dataset.dashboardIndex}-${element.dataset.plotIndex}`).dialog( "open" );
}

window.addEventListener('resize', function () {
    console.log('resizing');
    $.each($('.plotly-graph-div.js-plotly-plot'), function () {
        Plotly.Plots.resize($(this).attr('id'));
    });
});