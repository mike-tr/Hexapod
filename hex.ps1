param([Parameter(Position=0)][string]$cmd)

$PI   = "miket@hexapi.local"
$ROOT = "~/Hexapod"

switch ($cmd) {
    "sync"     { scp -r "${PI}:${ROOT}/calibration/images" ./calibration/ }
    "push"     { scp ./calibration/camera_calib.npz "${PI}:${ROOT}/calibration/" }
    "shutdown" { ssh $PI "sudo shutdown -h now" }
    "reboot"   { ssh $PI "sudo reboot" }
    "temp"     { ssh $PI "vcgencmd measure_temp; vcgencmd get_throttled" }
    "server"   { ssh $PI "cd $ROOT && hexapod/bin/python code/server.py" }
    "ssh"      { ssh $PI }
    default    { Write-Host "usage: .\hex.ps1 {sync|push|shutdown|reboot|temp|server|ssh}" }
}