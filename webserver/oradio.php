<?php
//  $cmd = $_GET["cmd"];
//  if($cmd!=""){
//     shell_exec($cmd);
// }
// $status = $_GET["status"];

if (isset($_GET["cmd"])) {
    $dt = $_GET["cmd"];
    if ($dt === "status") {
        $status = shell_exec("mpc");
        formatstatus($status);
    } else if ($dt === "volume") {
        $status = shell_exec("mpc");

        formatstatus($status);
        $newlinepos = strpos($status, "\n"); // find line break in status
        $volumepos = strpos($status, "volume");
        echo substr($status, $volumepos + 7, 4); // display current volume
    } else if ($dt === "hostname") {
        $status = shell_exec($dt);
        echo $status; // display current volume
    } else if ($dt === "playlist") {
        $status = shell_exec("mpc playlist");
        $status = str_replace("http://", "", $status);
        $starr = explode("\n", $status);

        $length = count($starr);
        for ($i = 0; $i < ($length - 1); $i++) {
            echo "<button class=\"button1\" onclick=\"sendcmd('mpc play " . strval($i + 1) . "')\"><a>" . strval($i + 1) . ". " . $starr[$i] . "</a></button>";
        }

    } else {

        $status = shell_exec($dt);
        formatstatus($status);

        updateoled();
        // echo $status;
    }
}

if (isset($_GET["sleep"])) {
    $dt = $_GET["sleep"];
    if ($dt !== "") {


        // $status = shell_exec("echo \"40\" /tmp/mpcst.star");
        // echo($status);

        //$myfile = /*fopen("/home/orangepi/mpcst.star", "w") or die("Unable to open file!");

        //fwrite($myfile, $dt);
        //fclose($*/myfile);
        // echo "create sleep timer in " . $dt;

        $tmpfname = tempnam(sys_get_temp_dir(), "mpcst.star");
        echo "will create file" . $tmpfname;
        $handle = fopen($tmpfname, "w");
        fwrite($handle, "writing to tempfile");
        fclose($handle);

        // do something here

        //unlink($tmpfname);


    }
}
function formatstatus($status)
{
    $newlinepos = strpos($status, "\n"); // find line break in status
    $volumepos = strpos($status, "volume");


    if ($volumepos == 0) {
        echo "player stopped<br><br>";
    } else {
        $stnname = substr($status, 0, $newlinepos); // get station name
        echo $stnname . "<br>"; // display station name
        $playpos = strpos($status, "[");
        $scrv = strpos($status, "(");
        // echo  substr($status, $playpos, $volumepos); // get station name
        echo substr($status, $playpos, $scrv - $playpos); // get station name
        // echo "<br>";

        // $state = substr($status, 27, 28); // get station name
        // echo $state;
        // echo "<br>";
        // echo "playpos=".$playpos."|scrv=".$scrv;
        echo "<br>";
    }
    // echo $status;
    echo PHP_EOL;
    echo substr($status, $volumepos, 11); // display current volume
}
function updateoled()
{
    $status = shell_exec("hostname");
    if (str_contains($status, "orangepi")) {
        shell_exec("/usr/bin/python3 /root/updateOLED.py");
    }
}

?>