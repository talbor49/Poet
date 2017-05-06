function poemPls() {
  var socket = io();
  var seed_words = $('#seed-words').val().toLowerCase()
  socket.emit('poet request', seed_words)

  $('#poem').empty()
  socket.on('line feed', function(line) {
    console.log("Got another line: " + line);
    $('#poem').append(line + '\n')
  });
}