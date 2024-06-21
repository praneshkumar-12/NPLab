set ns [new Simulator]

set tracefile [open "cong_control.tr" w]
$ns trace-all $tracefile

set node(0) [$ns node]
set node(1) [$ns node]

$ns duplex-link $node(0) $node(1) 10Mb 10ms DropTail

set tcp [new Agent/TCP]
$tcp set class_ 2
$ns attach-agent $node(0) $tcp

set sink [new Agent/TCPSink]
$ns attach-agent $node(1) $sink

$ns connect $tcp $sink

set ftp [new Application/FTP]
$ftp attach-agent $tcp
$ns at 0.1 "$ftp start"

$tcp set cong_algorithm NewReno

$ns duplex-link-op $node(0) $node(1) orient right-down

$ns color 1 Blue
$ns color 2 Red

$ns at 10.0 "$ns finish"

$ns run

$ns flush-trace
close $tracefile

set namfile [open "out.nam" w]
$ns nametrace-all $namfile
$ns nam-end-wireless $nam

$ns halt
$ns delete