#!/usr/bin/perl
use strict;
use LWP::UserAgent;
use Data::Dumper;

my $ua = LWP::UserAgent->new;
$ua->timeout(10);
$ua->env_proxy;

my $data = "
[Group B]
Company Name,Last Sale,+ or -,Quote Buy,Quote Sell
Bank of Qld,9.57,-1.0,9.55,9.57
Bendigo & Adelaide Bk,10.29,3.0,10.25,10.29
BlueScope Steel,4.9,1.0,4.89,4.9
Boral,4.97,3.0,4.96,4.97
Brambles,8.4,7.0,8.4,8.41
Brickworks,13.0,-6.0,13.0,13.05
[Group A]
Company Name,Last Sale,+ or - ,Quote Buy,Quote Sell
Adelaide Brighton,3.34,-6.0,3.33,3.34
AGL Energy,15.56,21.0,15.51,15.56
ALS,10.31,-22.0,10.27,10.33
Amcor,9.67,19.0,9.61,9.67
AMP,5.15,9.0,5.15,5.16
Ansell,15.12,-29.0,15.12,15.16
ANZ Banking Grp,28.69,44.0,28.67,28.7
APA Grp stp,6.12,-4.0,6.12,6.14
Aristocrat Leisure,3.71,2.0,3.71,3.73
ASX,36.62,18.0,36.61,36.65
Aurizon Hldgs,3.94,-4.0,3.94,3.95
Aust Foundation,5.38,-7.0,5.38,5.41
Aust Infrastructure Fd unt,3.11,3.0,3.1,3.11
Australand Prop stp,3.58,4.0,3.57,3.58
";

#$ua->cookie_jar({ csrfmiddlewaretoken => "tZjv3PlQqQfOxQszQqlt8jc0yqcOJ6Gu" });

my $params ={
	     action => 'generate',
	     appkey => 'APPDEMO_EXCEL',
	     data => $data,
	     format => 'text',
csrfmiddlewaretoken => 'tZjv3PlQqQfOxQszQqlt8jc0yqcOJ6Gu',
};

#warn Dumper $data;

my $response = $ua->get('http://127.0.0.1/report/gencsrf/');
warn Dumper $response;
exit;
$response = $ua->post('http://127.0.0.1/report/generate/');


if ($response->is_success) {

  print $response->decoded_content;  # or whatever
} else {
  
 die $response->status_line;
}
