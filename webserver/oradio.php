<?php
//  $cmd = $_GET["cmd"];
//  if($cmd!=""){
//     shell_exec($cmd);
// }
// $status = $_GET["status"];

if (isset($_GET["cmd"])) {
    $dt = $_GET["cmd"];
    if ($dt === "status") {
        $status =shell_exec("mpc");
        $newlinepos = strpos($status , "\n"); // find line break in status
        $volumepos = strpos($status, "volume");


        if ($volumepos == 0) {
            echo "paused";
        } else {
            $stnname = substr($status, 0, $newlinepos); // get station name
            echo $stnname; // display station name
        }
        // echo $status;
        echo PHP_EOL;
    echo substr($status, $volumepos+7, 4); // display current volume
    }  else {
        
        $status = shell_exec($dt);
        echo $status;
    }
}

 ?>