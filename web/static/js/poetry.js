function poemPls(random_poem) {
  var socket = io();
  var seed_words = random_poem ? '' : $('#seed-words').val().toLowerCase();
  socket.emit('poet request', seed_words);

  var poem_p_id = random_poem ? '#random-poem' : '#word-seeded-poem';

  $(poem_p_id).empty()
  socket.on('line feed', function(line) {
    console.log("Got another line: " + line);
    $(poem_p_id).append(line)
  });
}