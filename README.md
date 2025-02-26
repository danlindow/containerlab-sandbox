
# Overview

This lab is a quick proof of concept on using Nornir network automation to interact with containerlab labs.  The main driver in my use case was to be able to sync configurations quickly to container lab devices without rebuilding the lab and/or modifying a bunch of config manually.  As part of this adventure I incorporated some simple templating and a static file source of truth.  

# Repo layout

* `automation_lab` - This contains the actual code to sync the configurations across devices.
* `inventory` - This contains a simple inventory for Nornir. Currently there is not a native way to interact with the containerlab inventory (I'm working on a PR though!) from Nornir without a bit of hacking at the Ansible inventory. For now if you modify your containerlab lab you will want to update the device names and IP addresses accordingly. This directory also contains our mock source of truth data.
* `templates` - This contains the Jinja2 template. It's scrappy but works as a good baseline.
* `topologies` - This contains the containerlab topologies.  Interactions with containerlab are contained within this directory. I included a simple evpn topology to get started (and that is what our inventory uses by default)

# Setup

I've been running containerlab on an M2-pro macbook without issues. I'm utilizing the native devcontainer from containerlab and I've been running it in dood mode (docker outside of docker) on eOS containers without much fight.

## detailed setup

1. clone this repo
2. open this repo in VS Code in dev container mode
3. obtain the latest eOS image from Arista website and import into your docker installation: `docker import cEOSarm-lab-4.33.1-EFT3.tar.tar ceos:4.33-arm`. This is the new ARM image in my case!
4. If you named the image differently, modify `topologies/evpn/topology.clab.yml` to reference the correct image name.
5. launch the `evpn` lab in the containerlab extension within VS Code.
6. wait a few minutes for the lab to launch. if all goes well you should see a few containers launched:  
```bash
$ docker ps
CONTAINER ID   IMAGE                                                  COMMAND                  CREATED          STATUS          PORTS                              NAMES
92c76234d213   alpine:latest                                          "/bin/sh"                11 minutes ago   Up 11 minutes                                      clab-evpn-h4
4a1e25d5839b   alpine:latest                                          "/bin/sh"                11 minutes ago   Up 11 minutes                                      clab-evpn-h3
39c46266341e   alpine:latest                                          "/bin/sh"                11 minutes ago   Up 11 minutes                                      clab-evpn-h1
954e09bdbb0a   alpine:latest                                          "/bin/sh"                11 minutes ago   Up 11 minutes                                      clab-evpn-h2
ff72aa85e09d   ceos:4.33-arm                                          "bash -c '/mnt/flash…"   11 minutes ago   Up 11 minutes                                      clab-evpn-leaf1
a27a740656da   ceos:4.33-arm                                          "bash -c '/mnt/flash…"   11 minutes ago   Up 11 minutes                                      clab-evpn-spine1
51845956062a   ceos:4.33-arm                                          "bash -c '/mnt/flash…"   11 minutes ago   Up 11 minutes                                      clab-evpn-spine2
50b261f238cc   ceos:4.33-arm                                          "bash -c '/mnt/flash…"   11 minutes ago   Up 11 minutes                                      clab-evpn-leaf2
```
7. The topology should look like the following (you can see the same from the containerlab extension):
![eVPN containerlab topology](/assets/evpn_topology.png)
8. In the `Terminal` of VS Code we can now execute the following commands to enable the CLI helper for syncing configurations to these devices:
   1. `pipx install poetry`
   2. `poetry install`
   3. `poetry run automation-lab ./inventory/evpn_hosts.yaml` - This will sync all 4 ceos devices with the templated configuration from our source of truth file.
9. If all is well you should be able to see the eVPN routes on the devices:
```
leaf1#show bgp evpn route-type mac-ip
          Network                Next Hop              Metric  LocPref Weight  Path
 * >      RD: 1:1 mac-ip 10 aac1.ab58.641c
                                 -                     -       -       0       i
 * >Ec    RD: 1:1 mac-ip 10 aac1.ab8a.17ef
                                 2.2.2.2               -       100     0       1000 200 i
 *  ec    RD: 1:1 mac-ip 10 aac1.ab8a.17ef
                                 2.2.2.2               -       100     0       1000 200 i
 * >Ec    RD: 1:1 mac-ip 20 aac1.ab50.8fe1
                                 2.2.2.2               -       100     0       1000 200 i
 *  ec    RD: 1:1 mac-ip 20 aac1.ab50.8fe1
                                 2.2.2.2               -       100     0       1000 200 i
 * >      RD: 1:1 mac-ip 20 aac1.abcc.8605
                                 -                     -       -       0       i
```
10. You can also verify connectivity with the host containers:
```
docker exec -it clab-evpn-h3 ping 20.20.20.20
PING 20.20.20.20 (20.20.20.20): 56 data bytes
64 bytes from 20.20.20.20: seq=0 ttl=64 time=3.313 ms
64 bytes from 20.20.20.20: seq=1 ttl=64 time=2.063 ms
```