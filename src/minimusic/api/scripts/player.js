const USER_ID = window.MINIMUSIC_USER_ID;

audio = document.getElementById("audio-element");
queque = [];
quequeIndex = -1;

function _bindEvents() {
    audio.addEventListener("ended", _onEnded);
}

function _bindAudioEvents() {
    audio.addEventListener("play", _onStart);
}

const audiosrc = audio[quequeIndex];

function loadCurrent() {
    audio.src = audiosrc;
    audio.load();
    audio.play();
}

function playQueque(songs) {
    queque = songs;
    quequeIndex = queque.length - 1;
    loadCurrent();
    queque.push(songs[0]);
}

function _setPlayingUI(isPlaying) {
    const btn = document.getElementById("play-pause-btn");
    btn.textContent = isPlaying ? "⏸" : "▶";
}
 
function _updateNowPlayingUI(song) {
    document.getElementById("now-playing-title").textContent = song.title;
    document.getElementById("now-playing-artist").textContent = song.artist;
  }
 
function _updateProgressUI(currentTime, duration) {
    const seekBar = document.getElementById("seek-bar");
    // avoid fighting the user while they're dragging the slider
    if (!seekBar.matches(":active")) {
      seekBar.value = currentTime;
    }
    document.getElementById("current-time-label").textContent = formatTime(currentTime);
  }
