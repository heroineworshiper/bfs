import struct 
f = open( "/dev/input/js0", "rb" ); 
# Open the file in the read-binary mode
while 1:
  data = f.read(24)  # Reads the 3 bytes 
  print struct.unpack('24B',data)  #Unpacks the bytes to integers
