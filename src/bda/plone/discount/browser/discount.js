(function ($) {

    $(document).ready(function () {
    });

    var discount_form = {

        // set search criteria and execute source lookup
        _execute_source_lookup: function(request, callback, url) {
            discount_form.query(url, function(data, status, request) {
                callback(data);
            });
        },

        // autocomplete callback for user field
        autocomplete_user: function(request, callback) {
            discount_form._execute_source_lookup(
                request, callback, '@@autocomplete_user');
        },

        // autocomplete callback for group field
        autocomplete_group: function(request, callback) {
            discount_form._execute_source_lookup(
                request, callback, '@@autocomplete_group');
        },

        // query data for autocomplete dropdown criteria
        query: function(url, success) {
            $.ajax({
                url: url,
                dataType: 'json',
                success: success,
                error: express_form.error,
                cache: false
            });
        },

        // alert error message if JSON request failed
        error: function(request, status, error) {
            bdajax.error('Querying Server Failed');
        }
    };

}(jQuery));
