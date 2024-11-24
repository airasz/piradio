
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN">
<html xmlns>
<head>
<meta name="viewport" content="width=device-width; initial-scale=1.0; maximum-scale=1.0; user-scalable=0;"/>
<meta http-equiv="content-type" content="text/html; charset=ISO-8859-1">
<title>Internet Radio</title>
<link rel="stylesheet" type="text/css" href="radio.css">
<link rel="Shortcut Icon" type="image/ico" href="favicon.ico">              

<script type="text/javascript">
function load(id)
{
// setTimeout("location.href = 'http://192.168.1.120/radio/index.php';", 5000);
var url =window.location.href;
url =url.substring(0, (url.indexOf("o/")+2));
var toutID;
// console.log("url="+url );
if (id===1){
 toutID= setTimeout(()=>{"location.href = '"+url+"';"}, 5000);
console.log("tout id =" + toutID);

}
else{
    clearTimeout(toutID);
	console.log("timeout cancelled");
}
// window.location.href
}
</script>
<body onload="load(1)">

<?php

// added this function to replace em dashes in last.fm tracklistings
function convert_dash($string)
{
        $string = preg_replace( '/[^[:print:]][^[:print:]][^[:print:]]/', '-',$string);
        return $string;
}


function lastfm($lastfmuser)
{
    require_once('/usr/share/nginx/www/php/autoloader.php');

    // We'll process this feed with all of the default options.
    $feed = new SimplePie();

    // Set which feed to process.
    $feedurl = "http://ws.audioscrobbler.com/2.0/user/$lastfmuser/recenttracks.rss?limit=3";

    //added to ensure it gets fresh copy
    $feed->set_cache_duration(120);

    $feed->set_feed_url($feedurl);

    // Run SimplePie.
    $feed->init();

    // This makes sure that the content is sent to the browser as text/html and the UTF-8 character set (since we didn't change it).
    $feed->handle_content_type();

        echo "<hr><div class=\"tracklistheader\">";
    echo "<a href=\"";
    echo $feed->get_permalink();
    echo "\">";
    echo $feed->get_title();
    echo "</a>";
        echo "</div>";

        /*
        Here, we'll loop through all of the items in the feed, and $item represents the current item in the loop.
        */
        foreach ($feed->get_items() as $item):

                echo "<div class=\"tracklistsong\">";
                echo "<a href=\"";
                echo $item->get_permalink();
                echo "\">";
                echo convert_dash($item->get_title());
                echo "</a></div>";
                echo "<div class=\"tracklistdate\">";
                echo $item->get_date('j F Y | g:i a');
                echo "</div>";

        endforeach;

}

?>

<style type="text/css">

a:link {
color: #FFFFFF;
 text-decoration: none;
}

a:visited {
color: #FFFFFF;
}

a:hover {
    color: #FF0F0F;
    text-decoration: none;
}

a:active {
    text-decoration: none;
}

  .logo {
    font-family: AvenirNextCondensed-Bold, Helvetica, sans-serif;
    color: #FFFFFF;
    background-color: #7EA76B;
    -webkit-text-size-adjust: 150%;
    -moz-border-radius: 7px;
        border-radius: 7px;
    padding:2px;
     }

  .station {
    font-family: AvenirNextCondensed-Bold, Helvetica, sans-serif;
    color: #FF0000;
    font-size: 26px;
    -webkit-text-size-adjust: 200%;
     }

  .volume {
    color: #AAAAFF;
     }
   a.stationlinks:link {
    color: #000000;
    font-family: AvenirNextCondensed-Bold, Helvetica, sans-serif;
}

   a.stationlinks:visited {
    color: #000000;
}

   a.stationlinks:active {
    background-color: #FF0000;
}

   a.stationlinks:hover {
    background-color: #FF0000;
}

  .stationlinks {
    -moz-border-radius: 5px;
        border-radius: 5px;
    padding:0px;
    background: #A8E099;
    font-family: AvenirNextCondensed-Bold, Helvetica, sans-serif;
    }

   a.volcontrol:link {
    color: #000000;
}

   a.volcontrol:visited {
    color: #000000;
}

   a.volcontrol:active {
    background-color: #FF0000;
}

   a.volcontrol:hover {
    background-color: #FF0000;
}

  .volcontrol {
    font-family: AvenirNextCondensed-Bold, Helvetica, sans-serif;
    background: #C6DEEA;
    -moz-border-radius: 5px;
        border-radius: 5px;
    padding:0px;
   }

  .commands {
    background: #128f7f;
    color: #F0F0F0;
    -moz-border-radius: 5px;
        border-radius: 5px;
    padding:0px;
    }

  .tracklistheader {
    font-family: AvenirNextCondensed-Bold, Helvetica, sans-serif;
   }

  .tracklistsong {
   }

   .tracklistdate {
    -webkit-text-size-adjust: 75%;
      }

</style>
</head>
<body>
<center>
<h1>** Internet Radio **</h1>
<span class="station">
<?php
$stn=$_GET['station'];
exec("mpc play $stn");
#echo "sts".$stn."\n"; 
$com=$_GET['command'];
exec("mpc $com");
$status = shell_exec('mpc'); // get mpc status
$newlinepos = strpos($status , "\n"); // find line break in status
$volumepos = strpos($status, "volume");


if ($volumepos == 0) {
    echo "paused";
} else {
    $stnname = substr($status, 0, $newlinepos); // get station name
    echo $stnname; // display station name
}
echo "</span>";
?>

</span>
<br/><p><br>
<button class="button" ><a href="?command=volume -3" > VOL-</a>&nbsp;&nbsp;</button>
<button class="button" ><a href="?command=volume 60" > NORMAL</a>&nbsp;&nbsp;</button>
<button class="button" ><a href="?command=volume %2B3" >VOL+ </a>&nbsp;&nbsp;</button>


<button class="button buttons">
<?php
echo substr($status, $volumepos+7, 4); // display current volume
?>
</button>

<br/>

<button class="button" ><a href="?command=stop">&#x1F507 Pause</a></button>
<button class="button" ><a href="?command=play">&#x25B6; Play</a></button>
<button class="button" ><a href="." >Refresh</a></button>
<button class="button" onclick="load(0)" id="rstop"><a>Stop</a></button>
<br><p><br><p>
<button class="button" ><a href="?station=1" >Radio Rodja 756 AM dan 100.1 FM</a></button>
<button class="button" ><a href="?station=2" >Radio Radio Muslim Jogja</a>  </button>
<button class="button" ><a href="?station=3" >Radio Kita Cirebon</a> </button>
<button class="button" ><a href="?station=4" >Radio Idzaatulkhair Ponorogo</a></button>
<button class="button" ><a href="?station=5" >Radio DCS Madiun</a> </button>
<button class="button" ><a href="?station=6" >Radio Madinah 107.7 FM Madiun</a></button>
<button class="button" ><a href="?station=7" >Radio Rodja Bandung</a></button>
<button class="button" ><a href="?station=8" >Radio Hidayah 103.4 FM Pekanbaru</a></button>
<br>
<button class="button" ><a href="?station=9" >Radio Rodja Majalengka</a></button>
<button class="button" ><a href="?station=10" >Rodja TV</a>  </button>
<button class="button" ><a href="?station=11" >Radio Tarbiyah Sunnah</a> </button>
<button class="button" ><a href="?station=12" >Radio Shahabat Muslim</a></button>
<button class="button" ><a href="?station=13" >Radio Muadz</a> </button>
<button class="button" ><a href="?station=14" >Radio Suara Al-Iman</a></button>
<button class="button" ><a href="?station=16" >Reggae 2</a></button>
<br>

<br/><p><br/>

</body>
</html>
