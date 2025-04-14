# NekoConnect  
All your networking needs into one simple server, extensible with plugins  
NekoConnect makes running and deploying services much easier, connect to the NC socket and have it send packets to plugins you create, the packets are sent via a context object that extends methods for a custom socket connection and connecting to the log GUI  
Also features a small database for mini applications that require a small data storage like planners and todo apps  
With NekoConnect the sky is the limit, from chat apps to full game servers, "you think it, you code it"  
  
# Specs  
Custom API with crappy authentication (as always :3)  
Packet Spec:  
```cpp
[4b: packet len][1b: op code len][1b: greeter len][4b: data len][1b: hash len][1b: next random string len][greeter][op code][random string][data][hash]
```
each plugin has its own greeter so that packets can be routed to the correct plugin  
the op code is up to the plugin developer to use, its useful so why not, integer values only  
the random string sent is hashed and sent in the next packet to check the authentication  
op codes are also used for status returns, e.g. 200 for an ok response, 400 for an auth error and so on  
Example packet from the server:  
```cpp
[len][len][len][len][len][len]["nekoconnect-server"][200][8b23$c][data, in case of server status messages its the same as the op code][hash, in case of server responses its always "server"]
```
Example packet from a client:  
```cpp
[len][len][len][len][len][len]["plugin"][op code, up to the plugin creator to decide][a generated random string to be used in the authentication process][data, pretty much up to the devs][hash, in case of first packet it will hash the client random string]
```
Authentication sequence:  
client sends {greet: "auth", op_code: 200, random: random_string, data: 200, hash: hash_of_client_randomstr}  
server sends {greet: "nekoconnect-server", op_code: 200, random: "RANDOM_STRING", data: 200, hash: hash_of_client_randomstr}  
the client will hash its own random string on first packet only, next packets will include hashes of server random strings  
this implementation of the client also sending a random string to the server to hash will also help in client side authentication validation if the client developers choose to add, otherwise it can be discarded (not recommended)  
then the client sends any packet in any form the plugin developers create and as long as the hash is valid the response stays authorized else it disconnects with an op_code 400  
  
# Plugins  
Developers! developers! developers! developers! developers! developers! developers!  
We do the heavy lifting and you do the rest  
You can copy and import the `context.py` file and use it as a typeset when writing your plugins  
each plugin consists of 2 files, the spec sheet and the logic file  
the spec sheet contains info like the version, name, greeter and the logic filename  
the logic file is the python script that contains a `Logic` class with a `recv` method, this method gets called when a packet is routed to the plugin, accepts 1 argument being the context  
Examples are here at `plugins/`  
otherwise you can write anything custom that comes to mind and uses the data/recv/send methods from the context object  
  
# Installation  
Setup a virtual environment.  
Install the requirements.  
Run.  
  
# Neko and Connect :3  
as funny as it might be to create a plugin on a self hosted NekoConnect server and have people who wanna "connect" use that but it aint practical :3  
but the contact information are always found at my [github personal repo](https://github.com/NekoMimiOfficial/NekoMimiOfficial) just scroll to the bottom :3   
