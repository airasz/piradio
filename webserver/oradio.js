var bstop = false;
function loadonce() {
    load_status();
    // loadvol();
}

function loadvol() {
    var ajax_request = new XMLHttpRequest();
    var tbl = document.getElementById('svol');
    ajax_request.open("GET", "oradio.php?cmd=volume", true);
    ajax_request.onreadystatechange = function () {
        if (ajax_request.readyState == 4 && ajax_request.status == 200) {
            tbl.value = ajax_request.responseText;
        }
        else {
            // document.getElementById("loadingtbl").style.display = "block";
        }
    }

    ajax_request.send();
}

function setvol() {
    var ajax_request = new XMLHttpRequest();
    var tbl = document.getElementById('svol');
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
function load_status() {
    // document.getElementById("loadingtbl").style.display = "block";
    // alert("hai");
    var tbl = document.getElementById('radiostatus');

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
            setTimeout(load_status, 5000);//repeat call this function
        }
        else {
            // document.getElementById("loadingtbl").style.display = "block";
        }
    }
    // alert("getdata.php?d=" + dokter);
    ajax_request.send();
}
function updatevolslider(txt) {
    // var vol = txt.substring(txt.length - 3, txt.length - 1);

    var vol = txt.substring(txt.indexOf("volume") + 7, txt.length - 1);
    var tbl = document.getElementById('svol');
    console.log("vol=" + vol);
    tbl.value = parseInt(vol);

}
function playbutton(txt) {
    var ps = txt.substring(txt.indexOf("[") + 1, txt.indexOf("]"));
    var tbl = document.getElementById('bplay');

    // console.log("ps=" + ps);
    tbl.innerHTML = (ps == "playing") ? "pause" : "play";
}
function sendcmd(cmd) {
    var ajax_request = new XMLHttpRequest();

    var tbl = document.getElementById('radiostatus');
    // ajax_request.open('POST', 'oradio.php');
    ajax_request.open("GET", "oradio.php?cmd=" + cmd, true);

    // ajax_request.send(form_data);


    // new Response(form_data).text().then(console.log)
    ajax_request.onreadystatechange = function () {
        if (ajax_request.readyState == 4 && ajax_request.status == 200) {
            tbl.innerHTML = ajax_request.responseText;
        }
        else {
            // document.getElementById("loadingtbl").style.display = "block";
        }
    }
    // alert("getdata.php?d=" + dokter);
    ajax_request.send();
}