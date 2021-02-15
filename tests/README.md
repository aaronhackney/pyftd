# How to prepare UnitTests
These test run against an actual FTD device
Required environment variables for most of these tests:  

## Required environment test variables
```
FTDIP = ip of the FTD we are testing against  
FTDUSER = username of an admin user of the FTD  
FTDPASS = password of the FTDUSER  
```  
## Example
In most shells:
```  
export FTDIP="192.168.3.22"  
export FTDUSER="admin"  
export FTDPASS="myadminpassword"  
```