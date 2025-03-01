function playVideo(src) {
    let video = document.getElementById("videoPlayer");
    video.src = src;
    video.style.display = "block";
    video.play();
  }

  function closeVideo() {
    let video = document.getElementById("videoPlayer");
    video.pause();
    video.style.display = "none";
  }