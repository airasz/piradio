var bstop = false;
var count = 0;
var old_sl = "";
var json_radio_status;
var theme = 0;
var hostname = "";
var isPaused = false;
function loop() {
  count++;
  if (count > 5 && !isPaused) {
    // load_status();
    load_status_json();
    polpulatesl();
    // count=0;
  }
  setTimeout(loop, 1000);
}

function togglePause() {
  isPaused = !isPaused;
  var btn = document.getElementById('pauseButton');
  if (isPaused) {
    btn.classList.add('paused');
    btn.innerHTML = '▶';
    btn.title = 'Resume periodic refresh';
  } else {
    btn.classList.remove('paused');
    btn.innerHTML = '⏸';
    btn.title = 'Pause periodic refresh';
    // Reset count to trigger immediate update on resume
    count = 4;
  }
  console.log('Periodic refresh ' + (isPaused ? 'paused' : 'resumed'));
}
function loadonce() {
  document.getElementById('loading').style.display = 'flex';
  initWebSocket();
  gethostname();
  loop();
  console.log("send playlist request");
  polpulatesl();
  polpulatepl();
  // colorscheme.setAttribute('href', 'cscheme.css');
  // load_status();
  load_status_json();
  load_cofig();
  document.getElementById('loading').style.display = 'none';
  // loadvol();
}
var gateway = `ws://${window.location.hostname}:8888/websocket`;
var websocket;
// window.addEventListener('load', onLoad);
function initWebSocket() {
  console.log("Trying to open a WebSocket connection...");
  websocket = new WebSocket(gateway);
  websocket.onopen = onOpen;
  websocket.onclose = onClose;
  websocket.onmessage = onMessage; // <-- add this line
}

function onOpen(event) {
  console.log("Connection opened");
}

function onClose(event) {
  console.log("Connection closed");
  setTimeout(initWebSocket, 2000);
}
//0=data, 1=weight, 2=timer, 3=info
function onMessage(event) {
  // alert(event.data);
  // console.log("incoming ws message : " + event.data);
  if (event.data.startsWith("btn")) {
    console.log("btn");
  } else if (event.data.startsWith("info")) {
    var sdata = event.data.substring(5);
    var el = document.getElementById("radiostatus");
    el.innerHTML = sdata;
    // console.log("got info");
  } else if (event.data.startsWith("vol")) {
    var sdata = event.data.substring(4);
    document.getElementById("svol").value = parseInt(sdata);
    var color = valueToLinearGradient(parseInt(sdata));
    tbl.style.setProperty("--slider-thumb-bg", color);
    var ivol = document.querySelector("#isvol");
    ivol.innerHTML = "volume : " + volume;
    console.log("updating volume slide");
  } else if (event.data.startsWith("pls")) {
    var sdata = event.data.substring(4);
    var stations = document.getElementById("stations");
    stations.innerHTML = sdata;

    // console.log("got pls");
  } else if (event.data.startsWith("resettimer")) {
    count = 4;
    // var sdata = event.data.substring(2);
    // document.getElementById("light").innerHTML = sdata;// timer clock
    console.log("reset timer");
  }
}
function loadvol() {
  var ajax_request = new XMLHttpRequest();
  var tbl = document.getElementById("svol");
  ajax_request.open("GET", "scmd/volume", true);
  ajax_request.onreadystatechange = function () {
    if (ajax_request.status == 200) {
      if (ajax_request.readyState == 4) tbl.value = ajax_request.responseText;
    } else {
      tbl.value = 0;
    }
  };

  ajax_request.send();
}

function setvol() {
  var tbl = document.getElementById("svol");
  var cmd = "mpc volume " + tbl.value;
  if (theme == 2) {
    var color = valueToLinearGradient(tbl.value);
    tbl.style.setProperty('--slider-thumb-bg', color);
  } else if (theme == 0) {
    var color = valueToRadialGradient(tbl.value);
    tbl.style.setProperty('--slider-thumb-bg', color);
  }
  websocket.send("0>" + cmd);
}

function getsleep() {
  // console.log("get sleep")
  // console.log("sleep timer countdown: ", json_radio_status.sleeptimer.countdown);
  var ajax_request = new XMLHttpRequest();
  var sinfo = document.getElementById("timerinfo");
  ajax_request.open("GET", "scmd/getsleep", true);
  ajax_request.onreadystatechange = function () {
    if (ajax_request.status == 200) {
      if (ajax_request.readyState == 4) {
        document.getElementById("sleepinfo").style.display =
          this.responseText === "off" ? "none" : "block";
        document.getElementById("sleepform").style.display =
          this.responseText === "off" ? "block" : "none";
      }
      sinfo.innerHTML = this.responseText;
    }
  };

  ajax_request.send();
}
function updatesleep(timetxt) {
  document.getElementById("sleepinfo").style.display =
    timetxt === "off" ? "none" : "block";
  document.getElementById("sleepform").style.display =
    timetxt === "off" ? "block" : "none";
  document.getElementById("timerinfo").innerHTML = "stop in > " + timetxt;
}
var scrollcount = 0;
function load_status() {
  var tbl = document.getElementById("radiostatus");
  var ajax_request = new XMLHttpRequest();
  ajax_request.open("GET", "scmd/status", true);
  ajax_request.onreadystatechange = function () {
    if (ajax_request.status == 200) {
      if (ajax_request.readyState == 4) {
        tbl.innerHTML = ajax_request.responseText.substring(
          0,
          ajax_request.responseText.indexOf("repeat"),
        );
        // playbutton(ajax_request.responseText);
        // updatevolslider(ajax_request.responseText);
        polpulatesl();
        // getsleep();
        load_status_json();
      }
      // setTimeout(load_status, 5000); //repeat call this function
    } else {
      // document.getElementById("loadingtbl").style.display = "block";
    }
  };
  // alert("getdata.php?d=" + dokter);
  ajax_request.send();
}
function load_status_json() {
  var ajax_request = new XMLHttpRequest();
  ajax_request.open("GET", "scmd/sttsjson", true);
  ajax_request.onreadystatechange = function () {
    if (ajax_request.status == 200) {
      if (ajax_request.readyState == 4) {
        json_radio_status = JSON.parse(ajax_request.responseText);

        // var radiostatus = ((json_radio_status.artist == null || typeof json_radio_status.artist === "undefined") ? "" : (json_radio_status.artis + " - ")) +
        //   (json_radio_status.title == null ? "" : json_radio_status.title);

        var radiostatus =
          (json_radio_status.artist == null ||
            typeof json_radio_status.artist === "undefined"
            ? ""
            : json_radio_status.artist + " - ") +
          (json_radio_status.title == null ? "" : json_radio_status.title);
        document.getElementById("radiostatus").innerHTML = radiostatus;
        updatevolslider(json_radio_status.volume);
        if (json_radio_status.time.total_seconds > 0) {
          document.getElementById("track-progress-container").style.display = "block";
          updateauidoprogress(
            json_radio_status.time.elapsed_seconds,
            json_radio_status.time.total_seconds,
            json_radio_status.time.elapsed,
            json_radio_status.time.total,
            json_radio_status.progress_percent,
          );
        } else {
          document.getElementById("track-progress-container").style.display = "none";
        }
        update_play_mode(
          json_radio_status.repeat,
          json_radio_status.random,
          json_radio_status.single,
          json_radio_status.consume,
        );
        updatesleep(json_radio_status.sleeptimer.countdown);
        update_control_button(
          json_radio_status.is_stopped,
          json_radio_status.is_playing,
        );
      }
    }
  };
  ajax_request.send();
}
function load_cofig() {
  var ajax_request = new XMLHttpRequest();
  ajax_request.open("GET", "scmd/config", true);
  ajax_request.onreadystatechange = function () {
    if (ajax_request.status == 200) {
      if (ajax_request.readyState == 4) {
        var json_config = JSON.parse(ajax_request.responseText);
        console.log("web theme: ", json_config.web.client_web_theme);
        theme = json_config.web.client_web_theme;
        if (json_config.web.client_web_theme == 0) {
          colorscheme.setAttribute("href", "blurry.css");
        } else if (json_config.web.client_web_theme == 1) {
          colorscheme.setAttribute("href", "bordered.css");
        } else if (json_config.web.client_web_theme == 2) {
          colorscheme.setAttribute("href", "neumorphism.css");
        } else if (json_config.web.client_web_theme == 3) {
          colorscheme.setAttribute("href", "glass.css");
        }
      }
    }
  };
  ajax_request.send();
}

function scroll_to() {
  var el = document.getElementById("stations");
  if (hasVerticalScrollbar(el)) {
    var bplaying = document.getElementById("playing");
    if (bplaying !== null) bplaying.focus();
    // console.log("has vertical scrollbar");
  }
}
function hasVerticalScrollbar(element) {
  return element.scrollHeight > element.clientHeight;
}

function restart() {
  var ajax_request = new XMLHttpRequest();
  ajax_request.open("GET", "scmd/restart", true);
  ajax_request.onreadystatechange = function () {
    if (ajax_request.status == 200) {
      alert(this.responseText);
      // if (ajax_request.readyState == 4) { alert(this.responseText); }
    }
  };
  ajax_request.send();
}
function updatevolslider2(txt) {
  var tbl = document.getElementById("svol");
  const match = txt.match(/volume:\s*(\d+)%/);

  if (match) {
    const volume = parseInt(match[1], 10);
    tbl.value = volume;
    if (theme == 2) {
      var color = valueToLinearGradient(volume);
      tbl.style.setProperty('--slider-thumb-bg', color);
    } else if (theme == 0) {
      var color = valueToRadialGradient(volume);
      tbl.style.setProperty('--slider-thumb-bg', color);
    }
    var ivol = document.querySelector("#isvol");
    ivol.innerHTML = "volume : " + volume;
    // console.log("Volume:", volume); // Output: 39
  } else {
    // console.log("Volume not found");
  }
}
function updatevolslider(volume) {
  // console.log("update volume slider: ", volume);
  var tbl = document.getElementById("svol");
  tbl.value = volume;
  if (theme == 2) {
    var color = valueToLinearGradient(volume);
    tbl.style.setProperty('--slider-thumb-bg', color);
  } else if (theme == 0) {
    var color = valueToRadialGradient(volume);
    tbl.style.setProperty('--slider-thumb-bg', color);
  } else if (theme == 1) {
    var gradient = valueToLinearGradient(volume);
    var color = gradient.match(/rgb\([^)]+\)/)[0];
    tbl.style.setProperty('--slider-thumb-bg', color);
  }
  var ivol = document.querySelector("#isvol");
  ivol.innerHTML = "volume : " + volume;
}
function update_play_mode(repeat, random, single, consume) {
  // console.log("update play mode: ", repeat, random, single, consume);
  document.getElementById("radiorepeat").checked = repeat;
  document.getElementById("radiorandom").checked = random;
  document.getElementById("radiosingle").checked = single;
  document.getElementById("radioconsume").checked = consume;
}
function set_play_mode(mode) {
  var cmd =
    "mpc " +
    mode +
    (document.getElementById("radio" + mode).checked ? " on" : " off");
  websocket.send("0>" + cmd);
  console.log("set play mode: ", cmd);
}

function updateauidoprogress(current, total, scurent, stotal, progress) {
  var slider = document.getElementById("track-progress");
  slider.max = total;
  slider.value = current;
  if (theme == 2) {
    var color = valueToLinearGradient(progress);
    console.log("update audio progress: ", progress, color);
    slider.style.setProperty('--slider-thumb-bg-progress', color);
  } else if (theme == 0) {
    var color = valueToRadialGradient(progress);
    console.log("update audio progress: ", progress, color);
    slider.style.setProperty('--slider-thumb-bg-progress', color);
  } else if (theme == 1) {
    var gradient = valueToLinearGradient(progress);
    var color = gradient.match(/rgb\([^)]+\)/)[0];
    console.log("update audio progress: ", progress, color);
    slider.style.setProperty('--slider-thumb-bg-progress', color);
  }
  var iprog = document.querySelector("#isprogress");
  iprog.innerHTML = scurent + "/" + stotal;
}

function seekaudio() {
  var slider = document.getElementById("track-progress");
  var seekto = slider.value;
  websocket.send("0>mpc seek " + seekto);
  // console.log("seeking to: ", seekto);
}
function formatSeconds(seconds) {
  if (isNaN(seconds) || seconds < 0) {
    return "Invalid input";
  }

  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const remainingSeconds = seconds % 60;

  const pad = (num) => String(num).padStart(2, "0");

  const formattedHours = hours > 0 ? `${hours}:` : "";
  const formattedMinutes = pad(minutes);
  const formattedSeconds = pad(remainingSeconds);

  return `${formattedHours}${formattedMinutes}:${formattedSeconds}`;
}

// Example usage:
// console.log(formatSeconds(3665)); // "1:01:05"
// console.log(formatSeconds(65));    // "01:05"
// console.log(formatSeconds(3600));  // "1:00:00"
// console.log(formatSeconds(5));     // "00:05"

function playbutton(txt) {
  let ps = txt.match(/\[([^\]]+)\]/)?.[1];

  if (ps) {
    document.getElementById("bplay").innerHTML =
      ps == "playing" ? "pause" : "play";
    if (document.getElementById("bstop") !== null)
      document.getElementById("bstop").style.display = txt.includes("stopped")
        ? "none"
        : "initial";
  }
}
function update_control_button(stopped, isplaying) {
  if (stopped) {
    document.getElementById("bstop").style.display = "none";
    document.getElementById("bplay").innerHTML = "play";
  } else {
    document.getElementById("bstop").style.display = "initial";
    document.getElementById("bplay").innerHTML = isplaying ? "pause" : "resume";
  }
}

function sendcmd(cmd) {
  websocket.send("0>" + cmd);
  count = 4;
}
function sendwsm(cmd) {
  websocket.send("1>" + cmd);
  count = 4;
}
function playurl() {
  iu = document.getElementById("purl").value;
  sendcmd("mcp play " + iu);
}
function gethostname() {
  var ajax_request = new XMLHttpRequest();
  ajax_request.open("GET", "scmd/hostname", true);
  ajax_request.onreadystatechange = function () {
    if (ajax_request.status == 200) {
      if (ajax_request.readyState == 4)
        // alert("hn=" + this.responseText);
        console.log("hostname :" + this.responseText);
      document.title = this.responseText + " radio";
      const body = document.body;
      if (this.responseText.includes("banana")) {
        // colorscheme.setAttribute("href", "blurry.css");
        // spn.style.cssText = 'display:inline-flex !important';
        hostname = this.responseText;
        document.querySelector("#nav").style.display = "block";
        document.getElementById("title").innerHTML =
          this.responseText + " radio &#x1F34C";
        body.style.setProperty('--main-background-color-gradient',
          'linear-gradient(135deg, #245f93 0%, #327125 25%, #8c851f 50%, #1f5135 75%, #246464 100%)')
      } else if (this.responseText.includes("orange")) {
        // colorscheme.setAttribute("href", "bordered.css");
        hostname = this.responseText;
        document.querySelector("#nav").style.display = "block";
        document.getElementById("title").innerHTML =
          this.responseText + " radio &#x1F34A";
        body.style.setProperty('--main-background-color-gradient',
          'linear-gradient(135deg, #248393 0%, #23429e 25%, #7026a0 50%, #a42d69 75%, #912e3e 100%)')
      }
      hostname = hostname.replace("\n", "");
    } else {
      // document.getElementById("loadingtbl").style.display = "block";
    }
  };
  // alert("getdata.php?d=" + dokter);
  ajax_request.send();
}
//populate station list to button
function polpulatesl() {
  // console.log("refresh playlist button")
  var ajax_request = new XMLHttpRequest();
  var stations = document.getElementById("stations");
  ajax_request.open("GET", "scmd/playlist", true);
  ajax_request.onreadystatechange = function () {
    // console.log("xhr code: " + ajax_request.status);
    // console.log("ajax_request.readyState: " + ajax_request.readyState);
    if (ajax_request.status == 200) {
      if (ajax_request.readyState == 4) {
        // console.log("got playlist");
        if (this.responseText != old_sl) {
          // console.log("got playlist");
          stations.innerHTML = this.responseText;
          old_sl = this.responseText;
        }
        stations.innerHTML = this.responseText;
        scrollcount++;
        if (scrollcount > 3) {
          scroll_to();
          scrollcount = 0;
        }
        count = 0;
      }
      // setTimeout(polpulatesl, 15000); //repeat call this function
    } else {
      console.log("failed get playist");
      stations.innerHTML =
        '<button class="button1" onclick="windows.location.reload()"><a>reload page</a></button>';
    }
  };
  ajax_request.send();
}
//populate playlist to button
function polpulatepl() {
  var ajax_request = new XMLHttpRequest();
  var stations = document.getElementById("playlists");
  ajax_request.open("GET", "scmd/iplaylist", true);
  ajax_request.onreadystatechange = function () {
    if (ajax_request.status == 200) {
      if (ajax_request.readyState == 4) stations.innerHTML = this.responseText;
    } else {
      stations.innerHTML = "station list failed to loaded";
    }
  };
  ajax_request.send();
}

function setsleep() {
  var etval = document.getElementById("tval");
  var tval = etval.value;
  var itval = parseInt(tval);
  var stations = document.getElementById("sleepinfo");
  var it = document.getElementById("tval");
  if (itval > 0) {
    var ajax_request = new XMLHttpRequest();
    // console.log("set sleeep" + tval);
    ajax_request.open("GET", "scmd/sleep=" + tval, true);
    ajax_request.onreadystatechange = function () {
      if (ajax_request.status == 200) {
        if (ajax_request.readyState == 4) {
          stations.innerHTML = this.responseText;
          it.value = "";
        }
      } else {
        stations.innerHTML = "set sleep timer failed";
      }
    };
    ajax_request.send();
  }
}
// var vol = document.querySelector("#isvol");
// var _range = document.querySelector("#svol");
// _range.addEventListener(
//   "input",
//   function () {
//     vol.innerHTML = "volume : " + this.value;
//   },
//   false,
// );

function valueToLinearGradient(value) {
  // Ensure value is within 0-100
  value = Math.max(0, Math.min(100, value));

  var r, g, b;
  // console.log(`hostname: -${hostname}-`);
  // hostname = "orange";
  if (value <= 50) {
    // 0-50: Turquoise (173, 240, 228) to Yellow (242, 227, 105)
    r = hostname == "banana" ? Math.floor(173 + 1.38 * value) : Math.floor(5.1 * value);
    g = hostname == "banana" ? Math.floor(240 - 0.26 * value) : Math.floor(100 + 3.1 * value);
    b = hostname == "banana" ? Math.floor(228 - 2.46 * value) : 0;
  } else {
    // 50-100: Yellow (242, 227, 105) to Dark Yellow (178, 145, 45)
    r = hostname == "banana" ? Math.floor(242 - 1.28 * (value - 50)) : 255;
    g = hostname == "banana" ? Math.floor(227 - 1.64 * (value - 50)) : Math.floor(255 - 1.8 * (value - 50));
    b = hostname == "banana" ? Math.floor(105 - 1.2 * (value - 50)) : 0;
  }

  // Calculate darker color
  var darker = 0.6;
  var r2 = Math.floor(r * darker);
  var g2 = Math.floor(g * darker);
  var b2 = Math.floor(b * darker);

  return (
    "linear-gradient(135deg, rgb(" +
    r +
    "," +
    g +
    "," +
    b +
    "), rgb(" +
    r2 +
    "," +
    g2 +
    "," +
    b2 +
    "))"
  );
}

function valueToRadialGradient(value) {
  // Ensure value is within 0-100
  value = Math.max(0, Math.min(100, value));

  // Inner color: yellowish-green
  var innerColor = hostname == "banana" ? "rgba(196, 209, 8, 1)" : "rgba(221, 169, 0, 1)";

  // Outer color: cyan
  var outerColor = hostname == "banana" ? "rgba(2, 214, 214, 1)" : "rgba(2, 71, 33, 1)";

  var innerValue, outerValue;

  if (value <= 50) {
    // For value 0-50: outervalue goes from 0 to 100
    innerValue = 0;
    outerValue = (value / 50) * 100; // Maps 0-50 to 0-100
  } else {
    // For value 51-100: innervalue goes from 0 to 100
    innerValue = ((value - 50) / 50) * 100; // Maps 51-100 to 0-100
    outerValue = 100;
  }

  return (
    "radial-gradient(circle, " +
    innerColor + " " + innerValue + "%, " +
    outerColor + " " + outerValue + "%)"
  );
}
