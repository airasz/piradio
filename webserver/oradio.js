
function loadonce() {
    load_status();
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
            setTimeout(load_status, 5000);//repeat call this function
        }
        else {
            // document.getElementById("loadingtbl").style.display = "block";
        }
    }
    // alert("getdata.php?d=" + dokter);
    ajax_request.send();
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