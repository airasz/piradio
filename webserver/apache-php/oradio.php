<?php
//  $cmd = $_GET["cmd"];
//  if($cmd!=""){
//     shell_exec($cmd);
// }
// $status = $_GET["status"];
if (isset($_GET["cmd"])) {
    $dt = $_GET["cmd"];
    // echo $dt;
    if (str_starts_with($dt, "mpc load")){
        $status = shell_exec("ls /var/lib/mpd/playlists/");
        $status = str_replace(".m3u", "", $status);
        $starr = explode("\n", $status);
        $plname= substr($dt, 9);
        echo "plname= ".$plname."...";
        $length = count($starr);
        for ($i = 0; $i < ($length - 1); $i++) {
            if ($plname===$starr[$i]){
                $statu = shell_exec("mpc clear");
                $statu = shell_exec($dt);
                $statu = shell_exec("mpc play");
                break;
            }

        }
        return;
    }
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
    } else if ($dt === "iplaylist") {
        $status = shell_exec("ls /var/lib/mpd/playlists/");
        $status = str_replace(".m3u", "", $status);
        $starr = explode("\n", $status);

        $length = count($starr);
        for ($i = 0; $i < ($length - 1); $i++) {
            echo "<button class=\"button1\" onclick=\"sendcmd('mpc load " . $starr[$i] . "')\"><a>" . strval($i + 1) . ". load " . $starr[$i] . "</a></button>";
        }
        // echo $status; // display current volume
    }  else if ($dt === "playlist") {
        $ns=intval(shell_exec("mpc -f [%position%] | awk 'NR==1 {print}'"));

        $status = shell_exec("mpc playlist");
        // $status = str_replace("http://", "", $status);
        // $status = substr($status.strpos("//")+2);
        $starr = explode("\n", $status);

        $length = count($starr);
        for ($i = 0; $i < ($length - 1); $i++) {
            $stsion = strval($starr[$i]);
            if (strpos($stsion, "//")!==false){
                $stsion = substr($stsion, strpos($stsion,"//")+2);
            }
            if (($i+1)===$ns){
                echo "<button id=\"playing\"class=\"button1 bplay\" nclick=\"sendcmd('mpc play " . strval($i + 1) . "')\"><a>" . strval($i + 1) . ". " . $stsion . "</a></button>";}
            else{
                echo "<button class=\"button1\" onclick=\"sendcmd('mpc play " . strval($i + 1) . "')\"><a>" . strval($i + 1) . ". " . $stsion . "</a></button>";

            }
        }

    }
    // else if($dt==="mpc load koplo") {
    //     echo $dt;
    //     $status = shell_exec("mpc clear");
    //     $status = shell_exec($dt);
    //     $status = shell_exec("mpc play");
    //     // echo $status; // display current volume
    // } else if($dt==="mpc load radio") {
    //     echo $dt;
    //     $status = shell_exec("mpc clear");
    //     $status = shell_exec($dt);
    //     $status = shell_exec("mpc play");
    //     // echo $status; // display current volume
    // }
    // else if( str_contains($dt, "koplo")) {
    //     echo $dt;
    //     $status = shell_exec("mpc clear");
    //     $status = shell_exec($dt);
    //     $status = shell_exec("mpc play");
    //     // echo $status; // display current volume
    // } else if (str_contains($dt, "radio")) {
    //     $status = shell_exec("mpc clear");
    //     $status = shell_exec($dt);
    //     $status = shell_exec("mpc play");
    //     // echo $status; // display current volume
    // }
    else {

        $status = shell_exec($dt);
        formatstatus($status);

        // updateoled();
        // echo $status;
    }
}

if (isset($_GET["sleep"])) {
    $dt = $_GET["sleep"];
    // echo $dt;
    // if ($dt>0){
    //     echo "hai";
    // }
    if ($dt!=="") {
        // echo("try set timer ");
        // $status = shell_exec("/usr/bin/python3 /root/startsleeper.py ".$dt);
        $status = shell_exec("/usr/bin/python /root/startsleeper.py 3");
        // $status = shell_exec("echo \"40\" /tmp/mpcst.star");
        // echo "sleep timer set to ".$status;

        //$myfile = /*fopen("/home/orangepi/mpcst.star", "w") or die("Unable to open file!");

        //fwrite($myfile, $dt);
        //fclose($*/myfile);
        // echo "create sleep timer in " . $dt;
/*
        $tmpfname = tempnam(sys_get_temp_dir(), "mpcst.star");
        echo "will create file" . $tmpfname;
        $handle = fopen($tmpfname, "w");
        fwrite($handle, "writing to tempfile");
        fclose($handle);*/

        // do something here

        //unlink($tmpfname);


    }
    if ($dt!==""){
    //     $array = Array (
    //             "enable" => true,
    //             "startrun => true,
    //             "svalue" => int($dt),
    //             "seconds" => 0
    //
    // );
    //
    // // Encode array to json
    // $json = json_encode($array);
    //
    // // Display it
    // echo "$json";
    //
    // // Generate json file
    // file_put_contents("/root/test._data.json", $json);


    $myJson = new stdClass();
    $myJson->enable = true;
    $myJson->startrun = true;
    $myJson->svalue = intval($dt)*60;
    $sc=intval($dt)*60;
    $myJson->seconds = 0;

    $myJSONvar = json_encode($myJson);

    // echo $myJSONvar;
    echo "star sleep in ".timeformat($sc);
    // Generate json file
    file_put_contents("/home/timer.json", $myJSONvar);
    }

}

if (isset($_GET["getsleep"])) {
    $path = '/home/timer.json';
    $jsonString = file_get_contents($path);
    $jsonData = json_decode($jsonString, true);
    echo $jsonString;
    // var_dump($jsonData);
}


function timeformat($seconds) {
  $t = round($seconds);
  return sprintf('%02d:%02d:%02d', $t/3600, floor($t/60)%60, $t%60);
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
