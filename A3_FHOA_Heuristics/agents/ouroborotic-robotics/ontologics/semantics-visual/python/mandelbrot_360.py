from PIL import Image;w,h,m=1200,800,100;p=Image.new('L',(w,h));d=p.load()
for r in range(h):
 for c in range(w):
  x,y,i=0,0,0
  cy,cx=r/h*2-1,c/w*3-2
  while x*x+y*y<4 and i<m:x,y=x*x-y*y+cx,2*x*y+cy;i+=1
  d[c,r]=i%m*2
p.save('mandelbrot_360.png')