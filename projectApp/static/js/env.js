$(document).ready(function () {


    $("form#env-conf").submit(function(e) {
        e.preventDefault();

        var data = $(this).serialize();

        $.post($(this).attr('action'), data, function (json) {
            if (json.result == "error") {
                //console.log(json.errors);
                srv.showServerMessages(json.errors);
            }
            else {
                document.forms[0].reset();
                window.location.reload();
            }
        })
    });


    $(".remove").click(function(e) {

        var item = $(this);
        $("#id").val(item.attr('item-id'));
        $("#modal-title").text(item.attr('item-name'));

    });


    $("#agree").click(function(e) {
        e.preventDefault();
        var form = $("#form_delete");
        var data = form.serialize();

        $.post(form.attr('action'), data, function (json) {
            if (json['result'] == 'error') {
                console.log('Ajax: Error.')
            }
            else {
                window.location.reload();
            }
        })
    });


    // @env
    var tableOptEnv = $('.tableOptEnvironment').find('tbody');
    var tableOptServ = $('.tableOptServer').find('tbody');
    var env = $('#environment');


    var makeRowSelect = function (opt, index) {
        var prefix = '';
        var idx = '';
        if (index != undefined) {
            prefix = '[]';
            idx = index;
        }

        var s = $('<select id="' + opt.name + idx + '" name="'+ opt.name + prefix + '"  class="form-control" />');
        for(var i = 0; i < opt.values.length; i++) {
            $("<option />", {value: opt.values[i].name, text: opt.values[i]}).appendTo(s);
        }

        var cell = $('<td></td>');
        s.appendTo(cell);

        var row = $('<tr><td><label for="' + opt.name + idx + '">' + opt.displayName + '</label></td></tr>');
        cell.appendTo(row);

        return row
    };


    function generateIn(table, opt, index) {
        var prefix = '';
        var idx = '';
        if (index != undefined) {
            prefix = '[]';
            idx = index;
        }

        if (opt.type == 'ListBox') {
            table.append(makeRowSelect(opt, index));
        } else if (opt.type == 'String') {
            table.append(
                '<tr>' +
                '<td><label for="' + opt.name + '">' + opt.displayName + '</label></td>' +
                '<td><input type="text" name="' + opt.name + prefix + '" id="' + opt.name + idx + '" class="form-control" /></td>' +
                '</tr>');
        } else if (opt.type == 'Integer') {
            table.append(
                '<tr>' +
                '<td><label for="' + opt.name + '">' + opt.displayName + '</label></td>' +
                '<td><input type="number" value="1" name="' + opt.name + prefix + '" id="' + opt.name + idx + '" class="form-control" /></td>' +
                '</tr>');
        } else if (opt.name == 'options') {
            var radios = '';
            for (var index = 0; index < opt.values.length; index++) {
                radios += '<div class="radio-inline"><label><input value="'+opt.values[index]+'" type="radio" name="'+opt.name+'" id="'+opt.name+'" />'+opt.values[index]+'</label></div>';
            }
            table.append('<tr>' +
                '<td><label for="">' + opt.displayName + '</label></td>' +
                '<td>' + radios + '</td>' +
                '</tr>');
        }
    }


    var generateServerParameters = function(id, t) {
        tableOptServ.empty();

        var servParams = options[id].createParameters.serversParameters[t];
        var serverCount = $('input[name=serverCount]').val();

        if (t == 'identical') {
            serverCount = 1;
        }

        for(var cnt = 0; cnt < serverCount; cnt++) {
            tableOptServ.append('<tr><td colspan="2" class="info">Server #' + (cnt + 1) + '</td></tr>');
            for(var i = 0; i < servParams.length; i++) {
                generateIn(tableOptServ, servParams[i], cnt);
            }
        }
    };


    var getOptEnv = function (id) {
        tableOptEnv.empty();

        // add images
        var images = options[id].type.images;
        var selectTag = $('<select id="image" name="image"  class="form-control" />'); // !!! imageS -> image !!! WRONG NAME in JSON!!!
        for(var i = 0; i < images.length; i++) {
            $("<option />", { value: images[i], text: images[i] }).appendTo(selectTag);
        }

        var cell = $('<td></td>');
        selectTag.appendTo(cell);
        var row = $('<tr><td><label for="image">Image</label></td></tr>');
        cell.appendTo(row);

        tableOptEnv.append(row);
        // end add images
        var envParams = options[id].createParameters.enviromentParameters;
        for(var i = 0; i < envParams.length; i++){
            var opt = options[id].createParameters.enviromentParameters[i];
            generateIn(tableOptEnv, opt);
        }

        var radioBtn = $('input[type=radio]');

        if (radioBtn.length != 0) {
            radioBtn.change(function() {
                generateServerParameters(id, this.value);
            });
            $("input:radio:first").attr('checked', true).trigger('change');
        } else {
            generateServerParameters(id, 'identical');
        }
    };


    env.change(function () {
        getOptEnv($(this).val());
    });


    for(var i = 0; i < options.length; i++) {
        options[options[i].type.id] = options[i];
        env.append( $('<option value="'+options[i].type.id+'">'+options[i].type.id+'</option>'));
    }
    env.trigger("change");


});