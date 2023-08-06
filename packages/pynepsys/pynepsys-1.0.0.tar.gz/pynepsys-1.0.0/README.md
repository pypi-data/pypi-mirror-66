PyNepSys
====

Python package to interface with the `Neptune Systems Apex`. 
Tested against an Apex Classic, handles reading probe and
outlet state, and setting outlets to ON, OFF, AUTO modes.

Usage
-----

```python
from pynepsys import Apex
apex = Apex('192.168.0.2','admin','pass')

connection_status = await apex.validate_connection()
if connection_status != 'success':
 raise Exception('Cannot connect to Apex: ' + connection_status)
# connect and pull metadata about probes and outlets.
await apex.fetch_current_state()

outlet = apex.outlets['KalkMixer']
# This just updates the local copy to auto mode
outlet.enable_auto()
# Push the state to the Apex
await apex.update_outlet(outlet)
# The mode is auto, but we don't know if it's on or off
# until we refetch state. We can hold on to the outlet instance.
assert not outlet.is_on() and not outlet.is_off()
# Fetch again
await apex.fetch_current_state()

assert outlet.is_auto() == True
assert outlet.is_on() or outlet.is_off()
```

Neptune Systems Apex Aquacontroller: 
-----
http://www.neptunesystems.com/products/apex-controllers/apex-controller-system/