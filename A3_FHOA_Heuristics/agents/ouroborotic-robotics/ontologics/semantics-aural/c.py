import wave as W,math as M,struct as S
f="c.wav"
r=44100.0
d=0.25
s=500
e=2000
a=32767.0
n=int(d*r)
c=1
w=2
b=bytearray()
for i in range(n):
 q=s+(e-s)*(i/n)
 v=M.sin(2*M.pi*q*(i/r))
 p=S.pack('h',int(a*v))
 b.extend(p)
with W.open(f,'wb') as o:
 o.setnchannels(c)
 o.setsampwidth(w)
 o.setframerate(r)
 o.writeframes(b)