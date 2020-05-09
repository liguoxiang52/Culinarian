#!/usr/bin/env perl

use strict;
use warnings;
use utf8;
use v5.20;

use List::Util qw(shuffle);

use JSON;
use LWP::Simple;
use LWP::UserAgent;

my $today = `date +%Y%m%d`;
my $is_holiday = get("http://tool.bitefu.net/jiari/?d=${today}");
die "Today is holiday." if $is_holiday;

sub _restaurant {
    chomp $_[0];
    my ($n, $l) = split "@", $_[0];
    $l = "https://xa.meituan.com/s/T11 $n" unless defined $l;
    return {
        short => $JSON::true,
        title => $n,
        value => $l,
    }
};

my @lines = shuffle(<DATA>);
my $payload = {
    attachments => [{fallback     => "Lunch Alarm",
                     color        => "#00FF00",
                     author_name  => "Culinarian",
                     author_link  => "https://github.com/PaodingAI/Culinarian",
                     pretext      => "来自 Culinarian 的提醒",
                     title        => "该吃午饭啦！",
                     title_link   => "",
                     text         => q/@all 如果不知道吃什么，何不看看下面的今日推荐：/,
                     fields       => [ map { _restaurant $_ } @lines[0..2] ],
                 }]
};


my $req = HTTP::Request->new('POST', $ENV{MM_INCOME});
$req->header('Content-Type' => 'application/json');
$req->content(encode_json($payload));
my $ua = LWP::UserAgent->new;
$ua->request($req);


__DATA__
汉堡王@https://www.meituan.com/meishi/160585715/
小杨烤肉@https://www.meituan.com/meishi/182487133/
杨翔豆皮涮牛肚@https://www.meituan.com/meishi/160305609/
牧瓦人新疆风情餐厅@https://www.meituan.com/meishi/160353042/
晓宁生煎@https://www.meituan.com/meishi/179775194/
昶丰臭桂鱼@https://www.meituan.com/meishi/175478934/
唐潮记潮汕砂锅粥@https://www.meituan.com/meishi/179126665/
赵小姐创意中餐@https://www.meituan.com/meishi/159237534/
西汉年间@https://www.meituan.com/meishi/179759805/
饺子公馆@https://www.meituan.com/meishi/180564025/
赵家腊汁肉@https://www.meituan.com/meishi/179756401/
炒炒任小米@https://www.meituan.com/meishi/195938245/
