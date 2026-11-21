import cv2, numpy as np, vtracer, cairosvg, sys
soglia=float(sys.argv[1])
im=cv2.imread('originale.jpg').astype(np.float32)
im=cv2.bilateralFilter(im,7,40,5)
K=8
big=cv2.resize(im,None,fx=K,fy=K,interpolation=cv2.INTER_CUBIC)
big=cv2.GaussianBlur(big,(0,0),K*0.45)
C=np.array([[255,255,255],[113,49,6],[48,29,197]],np.float32)
d=((big[:,:,None,:]-C[None,None])**2).sum(-1)
lab=d.argmin(-1).astype(np.uint8)
y0,y1,x0,x1=355*K,378*K,170*K,280*K
lum=big[y0:y1,x0:x1].mean(-1)
z=(lum<soglia).astype(np.uint8)
z=cv2.morphologyEx(z,cv2.MORPH_CLOSE,np.ones((11,1),np.uint8))
lab[y0:y1,x0:x1]=z
for k in (1,2):
    m=(lab==k).astype(np.uint8)
    m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
    m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,np.ones((5,5),np.uint8))
    lab[(lab==k)&(m==0)]=0; lab[(m==1)]=k
cv2.imwrite('quantizzato.png',C[lab].astype(np.uint8))
vtracer.convert_image_to_svg_py('quantizzato.png','logo.svg',colormode='color',hierarchical='stacked',mode='spline',filter_speckle=16,color_precision=8,layer_difference=16,corner_threshold=60,length_threshold=4.0,max_iterations=10,splice_threshold=45,path_precision=3)
cairosvg.svg2png(url='logo.svg',write_to='logo-4000.png',output_width=4000,output_height=4000)
from PIL import Image
Image.open('logo-4000.png').crop((1300,2780,2300,3080)).save('zoom-since.png')
