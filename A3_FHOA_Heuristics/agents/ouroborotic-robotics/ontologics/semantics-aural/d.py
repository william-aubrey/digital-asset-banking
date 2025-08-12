import wave as W,math as M,struct as S
r=44100;n=int(.25*r);b=bytearray()
for i in range(n):b.extend(S.pack('h',int(32767*M.sin(2*M.pi*(500+1500*i/n)*i/r))))
with W.open('d.wav','wb') as o:o.setnchannels(1);o.setsampwidth(2);o.setframerate(r);o.writeframes(b)
