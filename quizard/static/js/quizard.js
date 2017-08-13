function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


$(function() {
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
      }
    }
  });

  $(document).on('click', 'a.answer', function(e) {
    e.preventDefault();
    $('.active').removeClass('active');
    $(e.target).closest('a.answer').addClass('active')

    $('button.submit-answer').show();
  });

  $(document).on('click', 'button.submit-answer', function(e) {
    var elm = $(e.target).closest('button.submit-answer');
    elm.addClass('disabled').removeClass('btn-success');
    elm.find('span').hide();
    elm.find('i').show();

    var answer = $('a.answer.active input').val();
    $.post('.', {'answer': answer}, function(data, status, xhr) {
      $('a#next-question').attr('href', data.next_url);
      elm.find('span').show();
      elm.find('i').hide();
    });
  });
});