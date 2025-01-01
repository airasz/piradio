var bstop = false;
var count = 0;
var old_sl = "";
function loop() {
  count++;
  if (count > 5) {
    load_status();
    // count=0;
  }
  setTimeout(loop, 1000);
}
function loadonce() {
  initWebSocket();
  gethostname();
  loop();
  console.log("send playlist request");
  polpulatesl();
  polpulatepl();
  // colorscheme.setAttribute('href', 'cscheme.css');
  load_status();

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
  console.log("incoming ws message : " + event.data);
  if (event.data.startsWith("btn")) {
    // var sdata = event.data.substring(2);
    // if (sdata.startsWith("tab")) {
    //     var iss = parseInt(sdata.substring(3));
    //     document.getElementById(iss).click();
    // } else if (sdata.startsWith("stimer")) {
    //     document.getElementById("divtimer").style.display = "block"
    // } else if (sdata.startsWith("htimer")) {
    //     document.getElementById("divtimer").style.display = "none"
    // }

    console.log("btn");
  } else if (event.data.startsWith("info")) {
    var sdata = event.data.substring(5);
    var el = document.getElementById("radiostatus");
    el.innerHTML = sdata;
    console.log("got info");
  } else if (event.data.startsWith("vol")) {
    var sdata = event.data.substring(4);
    document.getElementById("svol").value = parseInt(sdata);
    console.log("updating volume slide");
  } else if (event.data.startsWith("pls")) {
    var sdata = event.data.substring(4);
    var stations = document.getElementById("stations");
    stations.innerHTML = sdata;

    console.log("got pls");
  } else if (event.data.startsWith("resettimer")) {
    count = 4;
    // var sdata = event.data.substring(2);
    // document.getElementById("light").innerHTML = sdata;// timer clock
    console.log("reset timer");
  }
  // else {
  //
  //     var sdata = event.data.substring(2);
  //     printInfo(parseInt(event.data.substring(0, 1)), sdata);
  // }

  // document.getElementById('state').innerHTML = state;
}
function loadvol() {
  var ajax_request = new XMLHttpRequest();
  var tbl = document.getElementById("svol");
  ajax_request.open("GET", "scmd/volume", true);
  ajax_request.onreadystatechange = function () {
    if (ajax_request.status == 200) {
      if (ajax_request.readyState == 4) tbl.value = ajax_request.responseText;
    } else {
      // document.getElementById("loadingtbl").style.display = "block";
    }
  };

  ajax_request.send();
}

function setvol() {
  var ajax_request = new XMLHttpRequest();
  var tbl = document.getElementById("svol");
  ajax_request.open("GET", "scmd/mpc volume " + tbl.value, true);
  // ajax_request.onreadystatechange = function () {
  //     if (ajax_request.readyState == 4 && ajax_request.status == 200) {
  //         tbl.value = ajax_request.responseText;
  //     }
  //     else {
  //         // document.getElementById("loadingtbl").style.display = "block";
  //     }
  // }

  // ajax_request.send();
  var cmd = "mpc volume " + tbl.value;
  websocket.send("0>" + cmd);
}

function getsleep() {
  // console.log("get sleep")
  var ajax_request = new XMLHttpRequest();
  var sinfo = document.getElementById("timerinfo");
  ajax_request.open("GET", "scmd/getsleep", true);
  ajax_request.onreadystatechange = function () {
    if (ajax_request.status == 200) {
      if (ajax_request.readyState == 4)
        if (this.responseText === "off") {
          document.getElementById("sleepinfo").style.display = "none";
          document.getElementById("sleepform").style.display = "block";
        } else {
          document.getElementById("sleepinfo").style.display = "block";
          document.getElementById("sleepform").style.display = "none";
        }
      sinfo.innerHTML = this.responseText;
      // var toHHMMSS = (secs) => {
      //   var sec_num = parseInt(secs, 10);
      //   var hours = Math.floor(sec_num / 3600);
      //   var minutes = Math.floor(sec_num / 60) % 60;
      //   var seconds = sec_num % 60;
      //
      //   return [hours, minutes, seconds]
      //     .map((v) => (v < 10 ? "0" + v : v))
      //     .filter((v, i) => v !== "00" || i > 0)
      //     .join(":");
      // };
      // const obj = JSON.parse(this.responseText);
      // // console.log(this.responseText)
      // if (obj.enable === true) {
      //   var sscond;
      //   sscond = obj.seconds;
      //   // console.log(obj.seconds)
      //   sinfo.innerHTML = "player sleep in > " + toHHMMSS(sscond);
      // }
    } else {
      // document.getElementById("loadingtbl").style.display = "block";
    }
  };

  ajax_request.send();
}
var scrollcount = 0;
function load_status() {
  // document.getElementById("loadingtbl").style.display = "block";
  // alert("hai");
  // console.log("load status")
  var tbl = document.getElementById("radiostatus");

  var ajax_request = new XMLHttpRequest();

  // ajax_request.open('POST', 'oradio.php');
  ajax_request.open("GET", "scmd/status", true);

  // ajax_request.send(form_data);

  // new Response(form_data).text().then(console.log)
  ajax_request.onreadystatechange = function () {
    if (ajax_request.status == 200) {
      if (ajax_request.readyState == 4) {
        tbl.innerHTML = ajax_request.responseText.substring(
          0,
          ajax_request.responseText.indexOf("repeat"),
        );
        playbutton(ajax_request.responseText);
        updatevolslider(ajax_request.responseText);
        polpulatesl();
        getsleep();
        scrollcount++;
        if (scrollcount > 2) {
          scroll_to();
          scrollcount = 0;
        }
        count = 0;
      }
      // setTimeout(load_status, 5000); //repeat call this function
    } else {
      // document.getElementById("loadingtbl").style.display = "block";
    }
  };
  // alert("getdata.php?d=" + dokter);
  ajax_request.send();
}

function scroll_to() {
  var el = document.getElementById("stations");
  var bplaying = document.getElementById("playing");
  if (bplaying !== null) bplaying.focus();
}

function updatevolslider(txt) {
  // var vol = txt.substring(txt.length - 3, txt.length - 1);

  var vol = txt.substring(
    txt.indexOf("volume") + 7,
    txt.indexOf("volume") + 10,
  );
  var tbl = document.getElementById("svol");
  // console.log("vol=" + vol);
  tbl.value = parseInt(vol);
  var ivol = document.querySelector("#isvol");
  ivol.innerHTML = "volume : " + vol;
}
function playbutton(txt) {
  var ps = txt.substring(txt.indexOf("[") + 1, txt.indexOf("]"));
  var tbl = document.getElementById("bplay");

  // console.log("ps=" + ps);
  tbl.innerHTML = ps == "playing" ? "pause" : "play";
  if (document.getElementById("bstop") !== null)
    document.getElementById("bstop").style.display = txt.includes("stopped")
      ? "none"
      : "initial";
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
  var tbl = document.getElementById("colorscheme");
  // ajax_request.open('POST', 'oradio.php');
  ajax_request.open("GET", "scmd/hostname", true);

  // ajax_request.send(form_data);

  // new Response(form_data).text().then(console.log)
  ajax_request.onreadystatechange = function () {
    if (ajax_request.status == 200) {
      if (ajax_request.readyState == 4)
        // alert("hn=" + this.responseText);
        document.title = this.responseText + " radio";
      if (this.responseText.includes("banana")) {
        colorscheme.setAttribute("href", "cscheme.css");
        // spn.style.cssText = 'display:inline-flex !important';
        document.getElementById("title").innerHTML =
          this.responseText + " radio &#x1F34C";
      } else if (this.responseText.includes("orange")) {
        colorscheme.setAttribute("href", "blurry.css");
        document.getElementById("title").innerHTML =
          this.responseText + " radio &#x1F34A";
      }
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
function polpulatesl2() {
  // console.log("refresh playlist button")
  var ajax_request = new XMLHttpRequest();
  var stations = document.getElementById("stations");
  ajax_request.open("GET", "scmd/playlist", true);
  ajax_request.onreadystatechange = function () {
    if (ajax_request.status == 200) {
      if (ajax_request.readyState == 4) stations.innerHTML = this.responseText;
    } else {
      stations.innerHTML =
        '<button class="button1" onclick="sendcmd(\'mpc status\')"><a>reload page</a></button>';
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
