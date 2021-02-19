# pyftd
**Note:**  
This is a work in progress and more client functionality for the API calls will be added over time.

This is the refactored, new version of the python FTDClient Library. This library is for interacting with a Cisco Firepower Threat Defense appliance, both physical and virtual. The use-case for this libray would be for an orchestation script(s) to use these calls to configure an FTD from fresh install to production ready use and for day-to-day adds, moves and changes.

The library calls are all structured to use the same attribute names as the native API, making it simple to take the output from an FTD export and create a configuration file in an easy to use format like YAML for orchestration of configuration.

## Requirements
- Python 3.7+
- FTD Version 6.6.0+ managed by FDM (Sorry, not FMC compatible)
- Admin level credentials for the FTD

## Installation
python -m pip install git+https://github.com/aaronhackney/pyftd.git

## Use
The unitests located in the /tests folder should be very helpful as they demonstrate how to use the various client methods. Each method can take any of the parameters as allowed and documented in the API Explorer in FDM.  

###
```
from pyftd import FTDClient

ftd_client = FTDClient(192.168.100.100, admin, "Admin123", verify=False)

net_obj = self.ftd_client.create_network_object(
    {
        "name": "TEST-NET",  
        "value": "10.1.1.0/24",  
        "subType": "NETWORK",  
        "type": "networkobject"  
    }  
)  
``` 


