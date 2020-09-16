#!/usr/bin/php
<?php
$period = '2020-09';
$TOKEN = '3j4kl5ny;jk35ny4y34jl5nyj36nl';
$mailto = 'nat@mydomain.ru';
$to = "37635675";
$message = "File for $period uploaded";
$message_fail = "File for $period NOT uploaded";
$filename = "/root/.scripts/$period.txt";



exec("/root/.scripts/./getfiledata.pl $period > /root/.scripts/$period.txt");

if(file_exists($filename)){
   exec("curl -6 --header 'Content-Type: application/json' --request 'POST' --data '{\"chat_id\":$to,\"text\":\"$message\"}' \"https://api.telegram.org/bot$TOKEN/sendMessage\"");
   exec("mpack -s '$message' $filename $mailto");
}else{
   exec("curl -6 --header 'Content-Type: application/json' --request 'POST' --data '{\"chat_id\":$to,\"text\":\"$message_fail\"}' \"https://api.telegram.org/bot$TOKEN/sendMessage\"");
}
?>
