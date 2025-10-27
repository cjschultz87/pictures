import sys

mode = sys.argv[1]
filein = sys.argv[3]
fileout = sys.argv[4]

try:
    mult = int(sys.argv[2])
except:
    print("multiplier should be an integer")
    
    quit()


def bytetd(array):
    
    delta = 0
    
    for i,a in enumerate(array):
        delta += a * pow(256,i)
        
    return delta


if not(mode == 'q' or mode == 'a'):
    print("first argument should be q (monochrome to colour) or a (colour to monochrome)")
    
    quit()
    
try:
    foxtrot_0 = open(filein, "ab")
except:
    print("input file invalid")
    
    quit()
    
try:
    foxtrot_1 = open(fileout, "ab")
except:
    print("output file invalid")
    
    quit()
    
    
fsize0 = foxtrot_0.tell()
fsize1 = foxtrot_1.tell()

foxtrot_0.close()
foxtrot_1.close()

foxtrot_0 = open(filein, "rb")
foxtrot_1 = open(fileout, "rb")

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

foxtrot_1 = open(fileout, "wb")

index = 0

while index < pixstart1:
    foxtrot_1.write(falpha1[index].to_bytes(1,"big"))
    
    index += 1
    
i_0 = 0
i_1 = 0

alpha0 = falpha0[pixstart0:fsize0]
alpha1 = falpha1[pixstart1:fsize1]

L_alpha0 = len(alpha0)
L_alpha1 = len(alpha1)

if mode == 'q':
    while i_0 < L_alpha0:
        alpha1[((i_1 * 3 * mult) + 2) % L_alpha1] = alpha0[i_0]
        
        i_0 += 3
        i_1 += 1
        
if mode == 'a':
    while i_1 < L_alpha1:
        i_1 += 2
        
        alpha1[i_1] = alpha0[((i_0 * 3 * mult) + 2) % L_alpha0]
        
        i_0 += 1
        i_1 += 1

for a in alpha1:
    foxtrot_1.write(a.to_bytes(1,"big"))
        
        
foxtrot_1.close()

print("file write complete")
