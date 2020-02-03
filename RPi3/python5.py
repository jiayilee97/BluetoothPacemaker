# Using Hexiwear with Python
import pexpect
import time
#from time import gmtime, strftime

DEVICE = "5C:31:3E:8C:31:20"
 
print("Hexiwear address:"),
print(DEVICE)
 
# Run gatttool interactively.
print("Run gatttool...")
child = pexpect.spawn("gatttool -I")
 
# Connect to the device.
print("Connecting to "),
print(DEVICE),
child.sendline("connect {0}".format(DEVICE))
child.expect("Connection successful", timeout=5)
print(" Connected!")
 
#this is for Hexiwear
unixTime = int(time.time())
# Write local time
command = "char-write-req 61 0304{0:02x}{1:02x}{2:02x}{3:02x}0000000000000000000000000000".format(unixTime&0xff,(unixTime>>8)&0xff, (unixTime>>16)&0xff, (unixTime>>24)&0xff)
print(command)
child.sendline(command)
print "log"
#child.expect("Characteristic value was written successfully", timeout=10)
#code for Hexiwear ends

print("done!")
# function to transform hex string like "0a cd" into signed integer
def hexStrToInt(hexstr):
	val = int(hexstr[0:2],16) + (int(hexstr[3:5],16)<<8)
	if ((val&0x8000)==0x8000): # treat signed 16bits
	 val = -((val^0xffff)+1)
	return val
 
#while True:
# Accelerometer
child.sendline("char-read-hnd 0x30")
child.expect("Characteristic value/descriptor: ", timeout=10)
child.expect("\r\n", timeout=10)
print("Accel: "),
print(child.before), #00 00
print(float(hexStrToInt(child.before[0:5]))/100), #0.0
#print(float(hexStrToInt(child.before[6:11]))/100), 
#print(float(hexStrToInt(child.before[12:17]))/100)
 
# Accelerometer
child.sendline("char-read-hnd 0x34")
child.expect("Characteristic value/descriptor: ", timeout=10)
child.expect("\r\n", timeout=10)
print("Gyro: "),
print(child.before),
print(float(hexStrToInt(child.before[0:5]))/100),
#print(float(hexStrToInt(child.before[6:11]))/100),
#print(float(hexStrToInt(child.before[12:17]))/100)
 
# Magnetometer
child.sendline("char-read-hnd 0x38")
child.expect("Characteristic value/descriptor: ", timeout=10)
child.expect("\r\n", timeout=10)
print("Magneto:"),
print(child.before),
print(hexStrToInt(child.before[0:5])),
#print(hexStrToInt(child.before[6:11])),
#print(hexStrToInt(child.before[12:17]))

# Magnetometer
child.sendline("char-write-cmd 0x0025 16")
child.sendline("char-write-cmd 0x38 0100")
child.expect("Notification handle = 0x0037 value: ", timeout=10)
print("buffer","a")
child.expect("\r\n", timeout=10)
print("Temp:"),
print(child.before),

