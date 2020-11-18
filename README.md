# piHoleMonitor

A simple monitor for the piHole to output and be controlled by the Adafruit 16X2 RBG LCD pi Plate.  This is a pretty thrown together project at this point in time.  Everyone is welcome to use it, please feel free to clone and open PRs for anything you see that is an issue, I would greatly appreciate any help with the project.

## Screen Output
```pre
!HostName!
----------
###.###.###.###
up: # days
updated: # days
Blocked: ##.#%
----------
```
The screen responds to the up and down buttons on the pi plate to scroll up and down the output in an wrapping loop.

## Output
### HostName
The system hostname (limited to 16 characters)

### ip
The first line after the line of '-' is the ipv4 address for the piHole machine

### up:
This is the system uptime in days

### updated:
This is the time in days since the last block list update for the piHole

### Blocked:
This is the percentage of the DNS rquests that have been blocked today by the piHole

### ToDo
[ ] document deployment steps with dependencies 