var bstop = false;
var count = 0;
function loop() {
  count++;
  if (count > 5) {
    load_status();
    // count=0;
  }
  setTimeout(loop, 1000);
}
function loadonce() {
  gethostname();
  loop();
  console.log("send playlist request");
  polpulatesl();
  polpulatepl();
  // colorscheme.setAttribute('href', 'cscheme.css');
  load_status();
  //   initWebSocket();

  // loadvol();
}
function loadvol() {
  var ajax_request = new XMLHttpRequest();
  var tbl = document.getElementById("svol");
  ajax_request.open("GET", "oradio.php?cmd=volume", true);
  ajax_request.onreadystatechange = function () {
    if (ajax_request.readyState == 4 && ajax_request.status == 200) {
      tbl.value = ajax_request.responseText;
    } else {
      // document.getElementById("loadingtbl").style.display = "block";
    }
  };

  ajax_request.send();
}

function setvol() {
  var ajax_request = new XMLHttpRequest();
  var tbl = document.getElementById("svol");
  ajax_request.open("GET", "oradio.php?cmd=mpc volume " + tbl.value, true);
  // ajax_request.onreadystatechange = function () {
  //     if (ajax_request.readyState == 4 && ajax_request.status == 200) {
  //         tbl.value = ajax_request.responseText;
  //     }
  //     else {
  //         // document.getElementById("loadingtbl").style.display = "block";
  //     }
  // }

  ajax_request.send();
}

function getsleep() {
  // console.log("get sleep")
  var ajax_request = new XMLHttpRequest();
  var sinfo = document.getElementById("sleepinfo");
  ajax_request.open("GET", "oradio.php?getsleep", true);
  ajax_request.onreadystatechange = function () {
    if (ajax_request.readyState == 4 && ajax_request.status == 200) {
      var toHHMMSS = (secs) => {
        var sec_num = parseInt(secs, 10);
        var hours = Math.floor(sec_num / 3600);
        var minutes = Math.floor(sec_num / 60) % 60;
        var seconds = sec_num % 60;

        return [hours, minutes, seconds]
          .map((v) => (v < 10 ? "0" + v : v))
          .filter((v, i) => v !== "00" || i > 0)
          .join(":");
      };
      const obj = JSON.parse(this.responseText);
      // console.log(this.responseText)
      if (obj.enable === true) {
        var sscond;
        sscond = obj.seconds;
        // console.log(obj.seconds)
        sinfo.innerHTML = "player sleep in > " + toHHMMSS(sscond);
      }
    } else {
      // document.getElementById("loadingtbl").style.display = "block";
    }
  };

  ajax_request.send();
}

function load_status() {
  // document.getElementById("loadingtbl").style.display = "block";
  // alert("hai");
  // console.log("load status")
  var tbl = document.getElementById("radiostatus");

  var ajax_request = new XMLHttpRequest();

  // ajax_request.open('POST', 'oradio.php');
  ajax_request.open("GET", "oradio.php?cmd=status", true);

  // ajax_request.send(form_data);

  // new Response(form_data).text().then(console.log)
  ajax_request.onreadystatechange = function () {
    if (ajax_request.readyState == 4 && ajax_request.status == 200) {
      tbl.innerHTML = ajax_request.responseText;
      updatevolslider(ajax_request.responseText);
      playbutton(ajax_request.responseText);
      getsleep();
      polpulatesl2();
      count = 0;
      // setTimeout(load_status, 5000); //repeat call this function
    } else {
      // document.getElementById("loadingtbl").style.display = "block";
    }
  };
  // alert("getdata.php?d=" + dokter);
  ajax_request.send();
}
function updatevolslider(txt) {
  // var vol = txt.substring(txt.length - 3, txt.length - 1);

  var vol = txt.substring(txt.indexOf("volume") + 7, txt.length - 1);
  var tbl = document.getElementById("svol");
  // console.log("vol=" + vol);
  tbl.value = parseInt(vol);
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
  var ajax_request = new XMLHttpRequest();

  var tbl = document.getElementById("radiostatus");
  // ajax_request.open('POST', 'oradio.php');
  ajax_request.open("GET", "oradio.php?cmd=" + cmd, true);

  // ajax_request.send(form_data);

  // new Response(form_data).text().then(console.log)
  ajax_request.onreadystatechange = function () {
    if (ajax_request.readyState == 4 && ajax_request.status == 200) {
      tbl.innerHTML = ajax_request.responseText;
      // if (this.responseText.includes("stopped")) {
      //     document.getElementById('bstop').style.display = "none";
      // } else {
      //     document.getElementById('bstop').style.display = "initial";

      // }
      playbutton(this.responseText);
      polpulatesl2();
    } else {
      // document.getElementById("loadingtbl").style.display = "block";
    }
  };
  // alert("getdata.php?d=" + dokter);
  ajax_request.send();
}
function playurl() {
  iu = document.getElementById("purl").value;
  sendcmd("mcp play " + iu);
}
function gethostname() {
  var ajax_request = new XMLHttpRequest();
  var tbl = document.getElementById("colorscheme");
  // ajax_request.open('POST', 'oradio.php');
  ajax_request.open("GET", "oradio.php?cmd=hostname", true);

  // ajax_request.send(form_data);

  // new Response(form_data).text().then(console.log)
  ajax_request.onreadystatechange = function () {
    if (ajax_request.readyState == 4 && ajax_request.status == 200) {
      // alert("hn=" + this.responseText);
      document.title = this.responseText + " radio";
      if (this.responseText.includes("banana")) {
        colorscheme.setAttribute("href", "cscheme.css");
        // spn.style.cssText = 'display:inline-flex !important';
        document.getElementById("title").innerHTML =
          this.responseText + " radio &#x1F34C";
      } else if (this.responseText.includes("orange")) {
        colorscheme.setAttribute("href", "orange.css");
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
  ajax_request.open("GET", "oradio.php?cmd=playlist", true);
  ajax_request.onreadystatechange = function () {
    if (ajax_request.readyState == 4 && ajax_request.status == 200) {
      stations.innerHTML = this.responseText;
      // setTimeout(polpulatesl, 15000); //repeat call this function
    } else {
      stations.innerHTML =
        '<button class="button1" onclick="sendcmd(\'mpc status\')"><a>reload page</a></button>';
    }
  };
  ajax_request.send();
}
function polpulatesl2() {
  // console.log("refresh playlist button")
  var ajax_request = new XMLHttpRequest();
  var stations = document.getElementById("stations");
  ajax_request.open("GET", "oradio.php?cmd=playlist", true);
  ajax_request.onreadystatechange = function () {
    if (ajax_request.readyState == 4 && ajax_request.status == 200) {
      stations.innerHTML = this.responseText;
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
  ajax_request.open("GET", "oradio.php?cmd=iplaylist", true);
  ajax_request.onreadystatechange = function () {
    if (ajax_request.readyState == 4 && ajax_request.status == 200) {
      stations.innerHTML = this.responseText;
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
    ajax_request.open("GET", "oradio.php?sleep=" + tval, true);
    ajax_request.onreadystatechange = function () {
      if (ajax_request.readyState == 4 && ajax_request.status == 200) {
        stations.innerHTML = this.responseText;
        it.value = "";
      } else {
        stations.innerHTML = "set sleep timer failed";
      }
    };
    ajax_request.send();
  }
}
