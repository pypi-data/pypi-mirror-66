
FeedbackModal = function (url) {

    var $target = $('[data-role=feedback-modal]');

    $target.click(function () {

        $.get(url, function (response) {

            var $modal = $(response).modal();

            function toggleSubmitBtn(isActive) {
                $modal.find('[data-role=submit-btn]').prop('disabled', !isActive);
            }

            function handleFormSubmit(event) {

                event.preventDefault();

                toggleSubmitBtn(false);

                $.ajax({
                    method: 'POST',
                    url: url,
                    data: $modal.find('form').serialize(),
                    success: handleFormSubmitSuccess,
                    error: handleFormSubmitError,
                    complete: function () {
                        toggleSubmitBtn(true);
                    }
                });
            }

            function handleSubmitBtnClick() {
                $modal.find('form').submit();
            }

            function removeModal() {
                $modal.remove();
            }

            function handleFormSubmitSuccess(response) {
                $modal.modal('hide');

                if ($.notify) {
                    $.notify({message: response}, {type: 'success'});
                }
            }

            function handleFormSubmitError(response) {
                $modal.find('form').replaceWith(response.responseText);
            }

            $modal.on('submit', 'form', handleFormSubmit);

            $modal.on('click', '[data-role=submit-btn]', handleSubmitBtnClick);

            $modal.on('hidden.bs.modal', removeModal);

        });

    });

    if ($.fn.tooltip) {
        $target.tooltip();
    }

};

FeedbackForm = function (url) {

    var $container = $('[data-role=feedback-form]');

    function loadForm() {
        $.get(url, renderForm);
    }

    function renderForm(response) {
        $container.html(response);
        $container.on('submit', 'form', handleFormSubmit);
    }

    function handleFormSubmit(event) {
        event.preventDefault();

        $.ajax({
            method: 'POST',
            url: url,
            data: $container.find('form').serialize(),
            success: handleFormSubmitSuccess,
            error: handleFormSubmitError
        });
    }

    function handleFormSubmitSuccess(response) {
        if ($.notify) {
            $.notify({message: response}, {type: 'success'});
        }
        loadForm();
    }

    function handleFormSubmitError(response) {
        $container.find('form').replaceWith(response.responseText);
    }

    loadForm();
};
