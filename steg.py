import sys


def bytetd(array):
    
    delta = 0
    
    for i,a in enumerate(array):
        delta += a * pow(256,i)
        
    return delta


if not(sys.argv[1] == 'q' or sys.argv[1] == 'a'):
    print("first argument should be q (monochrome to colour) or a (colour to monochrome)")
    
    quit()
    
try:
    foxtrot_0 = open(sys.argv[2], "ab")
except:
    print("input file invalid")
    
    quit()
    
try:
    foxtrot_1 = open(sys.argv[3], "ab")
except:
    print("output file invalid")
    
    quit()
    
    
fsize0 = foxtrot_0.tell()
fsize1 = foxtrot_1.tell()

foxtrot_0.close()
foxtrot_1.close()

foxtrot_0 = open(sys.argv[2], "rb")
foxtrot_1 = open(sys.argv[3], "rb")

falpha0 = []
falpha1 = []

index = 0

while index < fsize0:
    falpha0.append(foxtrot_0.read(1)[0])
    index += 1

foxtrot_0.close()
    
index = 0

while index < fsize1:
    falpha1.append(foxtrot_1.read(1)[0])
    index += 1
    
foxtrot_1.close()

if len(falpha0) < 40 or len(falpha1) < 40:
    print("file format error")
    
    quit()

if not(bytetd(falpha0[28:30]) == 24 and bytetd(falpha1[28:30]) == 24):
    print("use 24 bit colour depth in each bitmap")
    
    quit()


fsize0 = bytetd(falpha0[2:6])
fsize1 = bytetd(falpha1[2:6])

width0 = bytetd(falpha0[18:22])
width1 = bytetd(falpha1[18:22])

height0 = bytetd(falpha0[22:26])
height1 = bytetd(falpha1[22:26])

pixstart0 = fsize0 - 3*(width0 * height0)
pixstart1 = fsize1 - 3*(width1 * height1)

foxtrot_1 = open(sys.argv[3], "wb")

index = 0

while index < pixstart1:
    foxtrot_1.write(falpha1[index].to_bytes(1,"big"))
    
    index += 1
    

i_0 = pixstart0
i_1 = pixstart1
    
if sys.argv[1] == 'q':

    while i_0 < fsize0 and i_0 - pixstart0 < fsize1 - pixstart1:
        if (i_0 - pixstart0) % 3 == 2:
            foxtrot_1.write(falpha0[i_0].to_bytes(1,"big"))
        else:
            foxtrot_1.write(falpha1[i_1].to_bytes(1,"big"))
        
        i_0 += 1
        i_1 += 1
        
    if fsize1 > fsize0:
        while i_1 < fsize1:
            foxtrot_1.write(falpha1[i_1].to_bytes(1,"big"))
            
            i_1 += 1
        
if sys.argv[1] == 'a':
    
    while i_1 - pixstart1 < fsize0 - pixstart0 and i_1 - pixstart1 < fsize1 - pixstart1:
        foxtrot_1.write(falpha0[i_0 + 2].to_bytes(1,"big"))
        
        if (i_1 - pixstart1) % 3 == 0 and i_0 > pixstart0:
            i_0 += 3
            
        i_1 += 1
        
    if fsize1 > fsize0:
        while i_1 < fsize1:
            foxtrot_1.write(falpha1[i_1].to_bytes(1,"big"))
        
        i_1 += 1
        
foxtrot_1.close()

print("file write complete")