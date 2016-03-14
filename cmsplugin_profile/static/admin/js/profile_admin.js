(function(window, $) {
    if (typeof ProfilePlugin === 'undefined') {
        window.ProfilePlugin = {};
    }

ProfilePlugin.ProfileGridAdmin = function(config) {
    var initial_title,
        initial_description,
        initial_show_title,
        profile_added,
        form_id,
        all_profiles_initial_data, // profile-prefix -> custom-profile-data
        all_profiles_changes_flag, // profile-prefix -> flag if profile has changes
        current_profile_value_before_edit, // input-id -> [input_type, saved_custom_data]
        save_rejected = config.save_rejected;

    function update_changed_status_for_profile(profile_prefix) {
        var initial_data = all_profiles_initial_data[profile_prefix],
            current_data = store_input_data(profile_prefix),
            has_changed = profile_has_changes(initial_data, current_data);

        all_profiles_changes_flag[profile_prefix] = has_changed;
    }

    function update_show_unsaved_warning() {
        var current_title = $("#id_title").val(),
            current_description = $("#id_description").val(),
            current_show_title = $("#id_show_title_on_thumbnails").prop('checked'),

            has_unsaved_changes = save_rejected || profile_added ||
                current_title != initial_title ||
                current_description != initial_description ||
                current_show_title != initial_show_title ||
                profiles_have_changes();

        $("#warning_unsaved").css('display', (has_unsaved_changes ? "block" : "none"));
    }

    function isEmpty(field) {
        return field.find('input[type="text"], textarea').val() === '' ? true : false;
    }

    function addErrorClass(field) {
        field.find('input[type="text"], textarea').addClass('error');
    }

    function removeErrorClass(field) {
        field.find('input[type="text"], textarea').removeClass('error');
    }

    function removeAllErrorClasses() {
        $('.has-error, .error').removeClass('has-error').removeClass('error');
    }

    function is_url_valid(value) {
        has_spaces = value.indexOf(" ") != -1;
        if (has_spaces) {
            return false;
        }
        correct_prefix = value.startsWith("http://") || value.startsWith("https://") || value.startsWith("/");
        return correct_prefix;
    }

    function checkValidLinks(form) {
        var valid = true;

        form.find('.profile-add-links').each(function() {
            var self = $(this);

            // remove all error classes from all links
            self.find('.form-row').each(function() {
                $(this).removeClass('mandatory has-error has-url-error')
                    .find('input[type="text"]').removeClass('error');
            });
            // if the input is not empty, we make it mandatory
            self.find('input[type="text"]').each(function() {
                if ($(this).val().length) {
                    self.find('.form-row').addClass('mandatory');
                }
            });

            self.find('input[id$="url"]').each(function() {
                value = $(this).val();
                if (value.length && !is_url_valid(value)) {
                    self.find('.form-row.profile-add-link-url').addClass('has-url-error');
                    self.find('.help-block-url').show();
                    $(this).addClass('error');
                    valid = false;
                } else {
                    self.find('.form-row.profile-add-link-url').removeClass('has-url-error');
                    self.find('.help-block-url').hide();
                    $(this).removeClass('error');
                }
            });

        });

        return valid;
    }

    function validateProfile(form) {
        var valid = checkValidLinks(form),
            mandatoryFields = form.find('.mandatory'),
            call_to_action = form.find('[id*="call_to_action_url"]'),
            value = call_to_action.val();

        mandatoryFields.each(function(idx, elem) {
            if (isEmpty($(elem))) {
                if ($(elem).parent('.profile-image-panel').length) {
                    $(elem).parent('.profile-image-panel').addClass('has-error');
                } else {
                    $(elem).addClass('has-error');
                }
                addErrorClass($(elem));
                valid = false;
            } else {
                removeErrorClass($(elem));
                $(elem).removeClass('has-error');
                $(elem).parent('.profile-image-panel').removeClass('has-error');
            }
        });

        if (value.length && !is_url_valid(value)) {
            call_to_action.siblings('.help-block').html('Invalid URL!');
            call_to_action.addClass('error').closest('.form-row').addClass('has-error');
            valid = false;
        } else {
            call_to_action.siblings('.help-block').html('This field is mandatory!');
            call_to_action.removeClass('error').closest('.form-row').removeClass('has-error');
        }
        return valid;
    }

    function setLimiter() {
        var inputs = form_id.find('input[type="text"], textarea');
        inputs.inputlimiter({
            remText: '%n character%s left. ',
            limitText: '%n character%s limit.',
            limitTextShow: false,
            remTextHideOnBlur: false,
            lineReturnCount: 2,
        });
    }

    function resizeIframe(toResizeTo, scrollToTop) {
        var insideIframe = (window.location != window.parent.location ? true : false);
        scrollToTop = (scrollToTop === false) ? false : true;

        if (!insideIframe) {
            return;
        }

        var documentHeight = $('body').outerHeight(true);

        if (toResizeTo) {
            documentHeight = Math.max($('body').outerHeight(true),
                toResizeTo.outerHeight(true));
        }

        var margin = 20;
        $(window.frameElement).css('height', (documentHeight + margin) + 'px');

        // anchoring on the top of the iframe
        // the classic version (with <a id="anchor">) does not work here due to iframe
        if (scrollToTop) {
            window.parent.$("body").animate({
                scrollTop: $(window.frameElement).offset().top
            }, 'fast');
        }
    }

    function store_input_data(prefix) {
        // Stores all the input data for a profile in a custom format.
        var data = {};

        $('input[name^="' + prefix + '"]').each(function(index, e) {
            input = $(this);
            if (input.attr("type") === "checkbox") {
                type = "checkbox";
                value = input.prop('checked');
            } else {
                type = "value";
                value = input.val();
            }
            data[input.attr("id")] = [type, value];
        });

        $('select[name^="' + prefix + '"]').each(function(index, e) {
            input = $(this);
            data[input.attr("id")] = ["value", input.val()];
        });

        $('textarea[name^="' + prefix + '"]').each(function(index, e) {
            data[$(this).attr("id")] = ["value", $(this).val()];
        });

        // Save the whole html, must be saved over the normal input values for images
        $.each(['thumbnail_image', 'detail_image'], function(index, image_name) {
            element = $("#id_" + prefix + "-" + image_name);
            input_value = element.val();
            html = element.closest("div.profile-image-panel").html();
            data[element.attr("id")] = ["image_html", [html, input_value]];
        });

        return data;
    }

    function restore_input_data(inputs_data) {
        // Restore the input data from a custom format.
        $.each(inputs_data, function(key, data) {
            type = data[0];
            value = data[1];
            element = $("#" + key);
            if (type === "checkbox") {
                element[0].checked = value;
            } else if (type === "image_html") {
                html = value[0];
                input_value = value[1];
                element.closest("div.profile-image-panel").html(html);
                element = $("#" + key);
                element[0].value = input_value;
            } else {
                element[0].value = value;
            }
        });
    }

    function profile_has_changes(initial_data, current_data) {
        profile_changed = false;
        $.each(initial_data, function(input_id, initial_full_val) {
            current_full_val = current_data[input_id];

            input_type = initial_full_val[0];
            initial_val = initial_full_val[1];
            current_val = current_full_val[1];

            if (input_type === "image_html") {
                initial_id = initial_val[1];
                current_id = current_val[1];
                if (initial_id != current_id) {
                    profile_changed = true;
                }
            } else {
                if (initial_val != current_val) {
                    profile_changed = true;
                }
            }
        });
        return profile_changed;
    }

    function profiles_have_changes() {
        changes_exist = false;
        $.each(all_profiles_changes_flag, function(profile_prefix, changed_flag) {
            if (changed_flag) {
                changes_exist = true;
            }
        });
        return changes_exist;
    }

    //detect change on Title field
    function onChangeTitle() {
        $(document).on("change", "#id_title", function(e) {
            update_show_unsaved_warning();
        });
    }

    //detect change on Description field
    function onChangeDescription() {
        $(document).on("change", "#id_description", function(e) {
            update_show_unsaved_warning();
        });
    }

    //detect change on Show Title on Thumbnails field
    function onChangeShowTitleOnThumbnail() {
        $(document).on("change", "#id_show_title_on_thumbnails", function(e) {
            update_show_unsaved_warning();
        });
    }

    function assert_initial_values_are_saved(prefix) {
        current_profile_value_before_edit = store_input_data(prefix);
        all_profiles_initial_data[prefix] = all_profiles_initial_data[prefix] ||
                                            current_profile_value_before_edit;
    }

    //edit profile item
    function editProfileItem() {
        $(document).on('click', '.profile-item-actions .edit-profile-item', function(e) {
            e.preventDefault();
            $(this).parent('.profile-item-actions').siblings().addClass('visible').closest('.inline-related').addClass('edit-mode');
            $(this).closest('.grid-list').siblings('.overlay').addClass('visible');

            prefix = $(this).data("profile-id-prefix");
            assert_initial_values_are_saved(prefix);

            resizeIframe($('.visible'));
            setLimiter();
        });
    }

    // delete profile edit
    function deleteProfileItem() {
        $(document).on('click', '.profile-item-actions .delete-profile-item', function(e) {
            e.preventDefault();

            profile_prefix = $(this).data("profile-id-prefix");
            assert_initial_values_are_saved(profile_prefix);
            profile = $('#' + profile_prefix);
            delete_input = $('#id_' + profile_prefix + '-DELETE')[0];
            delete_input.checked = !delete_input.checked;
            if (delete_input.checked) {
                profile.addClass("deleted");
            } else {
                profile.removeClass("deleted").removeClass("has-errors");
            }
            update_changed_status_for_profile(profile_prefix);

            update_show_unsaved_warning();
            resizeIframe($('.visible'), false);
        });
    }

    //close profile item edit/add form without saving
    function closeProfileItem() {
        $(document).on('click', '.grid-list .close-profile', function(e) {
            e.preventDefault();

            $(this).closest('.visible').removeClass('visible').closest('.inline-related').removeClass('edit-mode');
            $(this).closest('.grid-list').siblings('.overlay').removeClass('visible');

            profile_prefix = $(this).attr("data-profile-id-prefix");
            profile = $(this).closest('.ui-widget.inline-related');
            is_new = profile.closest('div.new-profile-form').length > 0;
            if (is_new) {
                profile.remove();
            } else {
                restore_input_data(current_profile_value_before_edit);
            }
            removeAllErrorClasses();

            resizeIframe();
        });
    }

    // close profile item edit/add form with saving the updates
    function doneProfileItem() {
        $(document).on('click', '.grid-list .done-profile', function(e) {
            e.preventDefault();

            if (validateProfile($(this).closest('.visible'))) {
                $(this).closest('.visible').removeClass('visible').closest('.inline-related').removeClass('edit-mode');
                $(this).closest('.grid-list').siblings('.overlay').removeClass('visible');

                prefix = $(this).attr("data-profile-id-prefix");
                profile_preview = $("#" + prefix);
                new_profile_container = profile_preview.closest(".new-profile-form");
                if (new_profile_container[0] !== undefined) {
                    // Since we move the input fields, they value will be lost so save
                    // and restore it after
                    new_profile_data = store_input_data(prefix);
                    profile_html = new_profile_container.html();
                    $(profile_html).insertBefore($(".ui-widget.inline-related.empty-form"));
                    profile_preview = $("#" + prefix);
                    profile_preview[0].className = "ui-widget inline-related complete";
                    new_profile_container.html("");
                    restore_input_data(new_profile_data);
                    profile_added = true;
                } else {
                    update_changed_status_for_profile(prefix);
                }

                new_image_url = $("#id_" + prefix + "-thumbnail_image_link_to_file")[0].href;
                profile_preview.css({
                    'background-color': "##efefef",
                    'background-image': "url(" + new_image_url + ")",
                    "background-repeat": "no-repeat",
                    "background-position": "center"
                });
                profile_preview.css('background-size', "contain");

                update_show_unsaved_warning();
                resizeIframe();
            }

        });
    }

    // add new profile item
    function addNewProfileItem() {
        $(document).on('click', '#add_new_profile', function(e) {
            var self = this;
            new_form_index = $('.inline-related').length - 1;
            profile_grid_id = $("#id_profile_set-__prefix__-profile_plugin").attr('value');
            url = '/admin/cmsplugin_profile/new_profile/' + new_form_index + '/';
            if (profile_grid_id !== undefined)
                url += "?profilegrid_id=" + profile_grid_id;
            jQuery.ajax({
                url: url,
                success: function(response) {
                    $('#profile_set-group-grid .new-profile-form').addClass('visible').append(response);
                    $('.overlay').addClass('visible');
                    total = $('#id_profile_set-TOTAL_FORMS');
                    total.val(parseInt(total.val(), 10) + 1);
                    setLimiter();
                },
                error: function(response) {},
                complete: function(response) {
                    resizeIframe($('.visible'));
                }
            });
        });
    }

    // add new additional links to profile item
    function addNewAdditionalLink() {
        $(document).on('click', '.add-profile-link', function(e) {
            link = $(e.currentTarget);
            prefix = link.attr("data-prefix");
            current = parseInt(link.attr("data-current"), 10);
            next_link = $("#" + prefix + current + "container");
            if (next_link !== undefined) {
                next_link.show();
                link.attr("data-current", current + 1);
                is_last_link = $("#" + prefix + (current + 1) + "container")[0] === undefined;
                if (is_last_link) {
                    $(this).closest('p').hide();
                }
            }
            resizeIframe($(this).closest('.visible'), false);
        });
    }

    function attachEvents() {
        onChangeTitle();
        onChangeDescription();
        onChangeShowTitleOnThumbnail();

        addNewProfileItem();
        editProfileItem();
        deleteProfileItem();
        closeProfileItem();
        doneProfileItem();

        addNewAdditionalLink();
    }

    function init() {
        initial_title = $("#id_title").val(),
        initial_description = $("#id_description").val(),
        initial_show_title = $("#id_show_title_on_thumbnails").prop('checked'),
        profile_added = false,
        form_id = $('#profilegrid_form'),
        all_profiles_initial_data = {}, // profile-prefix -> custom-profile-data
        all_profiles_changes_flag = {}, // profile-prefix -> flag if profile has changes
        current_profile_value_before_edit = {}, // input-id -> [input_type, saved_custom_data]
        error_lists = $('.errorlist'),
        first_list = error_lists.first();


        //make entire grid sortable
        $(".grid-list").sortable({
            items: "> .inline-related",
            cancel: ".edit-mode",
            start: function(event, ui) {
                $('[data-rel="popover"]').popover('hide');
            },
            update: function(event, ui) {
                $('.order_field input').each(function(i) {
                    $(this).attr('value', i + 1);
                });
            }
        });

        $(document).off('click').on('click', 'body', function(e) {
            //did not click a popover toggle or popover
            if ($(e.target).data('rel') !== 'popover' && $(e.target).parents('.popover.in').length === 0) {
                $('[data-rel="popover"]').popover('hide');
            }
        });

        // Add all errors to the first list
        error_lists.each(function(index) {
            if (index > 0) {
                first_list.append($(this).html());
                $(this).html("");
            }
        });

        $('[id^=id_profile_set-][id$=-DELETE]').each(function(i, obj) {
            if (obj.checked) {
                $(obj).closest(".ui-widget").addClass("deleted");
            }
        });
        setLimiter();
        attachEvents();
        update_show_unsaved_warning();
    }

    return {
        init: init
    };
};
})(window, jQuery);
