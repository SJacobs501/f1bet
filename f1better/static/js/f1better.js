$(document).ready(() => {

  $('.racebox').on('mouseenter', event => {
    $(event.currentTarget).css('background-color', 'lightgray');
  }).on('mouseleave', event => {
    $(event.currentTarget).css('background-color', 'white');
  });
});
