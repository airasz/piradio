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
        formatstatus($status);
        // $newlinepos = strpos($status , "\n"); // find line break in status
        // $volumepos = strpos($status, "volume");


        // if ($volumepos == 0) {
        //     echo "paused";
        // } else {
        //     $stnname = substr($status, 0, $newlinepos); // get station name
        //     echo $stnname."<br>"; // display station name
        //     $playpos=strpos($status, "[");
        //     // echo  substr($status, $playpos, $volumepos); // get station name
        //     echo  substr($status, $playpos); // get station name
        //     echo "<br>";
        // }
        // // echo $status;
        // echo PHP_EOL;
        // echo substr($status, $volumepos+7, 4); // display current volume
    } 
    else if ($dt === "volume") {
        $status =shell_exec("mpc");
        formatstatus($status);
        $newlinepos = strpos($status , "\n"); // find line break in status
        $volumepos = strpos($status, "volume");
        echo substr($status, $volumepos+7, 4); // display current volume
    }  else {
        
        $status = shell_exec($dt);
        formatstatus($status);
        // echo $status;
    }
}
function formatstatus($status){
        $newlinepos = strpos($status , "\n"); // find line break in status
        $volumepos = strpos($status, "volume");


        if ($volumepos == 0) {
            echo "player stopped";
        } else {
            $stnname = substr($status, 0, $newlinepos); // get station name
            echo $stnname."<br>"; // display station name
            $playpos = strpos($status, "[");
            $scrv = strpos($status, "(");
            // echo  substr($status, $playpos, $volumepos); // get station name
            echo substr($status, $playpos, $scrv-$playpos); // get station name
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

 ?>