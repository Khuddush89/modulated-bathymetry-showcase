"""Original numerical and visual construction for the modulated-bathymetry showcase.
No external images, source files, trajectories, or datasets are downloaded.
Run from any directory. Dependencies are installed separately, never vendored.
"""
from pathlib import Path
import json, math, platform, hashlib
import numpy as np
import scipy
from scipy.linalg import eigh, solve
from scipy.sparse.linalg import expm_multiply
from PIL import Image, ImageDraw, ImageFont
import PIL

ROOT=Path(__file__).resolve().parents[1]
ASSET=ROOT/'assets'
for sub in ['header','animations','figures','section_headers','icons']:(ASSET/sub).mkdir(parents=True,exist_ok=True)
(ROOT/'results').mkdir(exist_ok=True)
BG='#081426'; PANEL='#101f35'; GRID='#24374e'; WHITE='#eef6ff'; MUTED='#9cb2ca'
CYAN='#49dbe5'; PURPLE='#ad9cff'; GOLD='#f8c56b'; GREEN='#71dfb1'; RED='#fc91ab'
FONT_DIR=Path('/usr/share/fonts/truetype/dejavu')
FONT_CACHE={}
def font(size,bold=False):
    key=(size,bold)
    if key not in FONT_CACHE:
        name='DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf'
        # Pillow also searches installed font names on other platforms.
        try:FONT_CACHE[key]=ImageFont.truetype(str(FONT_DIR/name),size)
        except OSError:FONT_CACHE[key]=ImageFont.truetype(name,size)
    return FONT_CACHE[key]
def text(d,xy,s,size=20,fill=WHITE,bold=False,anchor=None):d.text(xy,s,font=font(size,bold),fill=fill,anchor=anchor)
def canvas(w,h):
    im=Image.new('RGB',(w,h),BG);d=ImageDraw.Draw(im)
    d.rounded_rectangle((1,1,w-2,h-2),radius=24,outline=GRID,width=2)
    return im,d
def panel(d,box):d.rounded_rectangle(box,radius=16,fill=PANEL,outline=GRID,width=1)
def curve(d,box,x,y,xlim,ylim,color=CYAN,width=3):
    l,t,r,b=box;x=np.asarray(x);y=np.asarray(y)
    px=l+(x-xlim[0])/(xlim[1]-xlim[0])*(r-l)
    py=b-(y-ylim[0])/(ylim[1]-ylim[0])*(b-t)
    pts=list(zip(px.tolist(),py.tolist()))
    if len(pts)>1:d.line(pts,fill=color,width=width,joint='curve')
    return pts

def axes(d,box,xlim,ylim,xticks,yticks,xlabel='',ylabel=''):
    l,t,r,b=box
    for value,label in xticks:
        xx=l+(value-xlim[0])/(xlim[1]-xlim[0])*(r-l)
        d.line((xx,t,xx,b),fill=GRID,width=1);text(d,(xx,b+10),label,14,MUTED,anchor='mt')
    for value,label in yticks:
        yy=b-(value-ylim[0])/(ylim[1]-ylim[0])*(b-t)
        d.line((l,yy,r,yy),fill=GRID,width=1);text(d,(l-10,yy),label,14,MUTED,anchor='rm')
    if xlabel:text(d,((l+r)/2,b+35),xlabel,15,MUTED,anchor='mt')
    if ylabel:text(d,(l,t-28),ylabel,16,MUTED)

def dot(d,p,col,r=5):d.ellipse((p[0]-r,p[1]-r,p[0]+r,p[1]+r),fill=col)
def legend(d,x,y,items):
    for label,col in items:
        d.line((x,y+8,x+25,y+8),fill=col,width=3);text(d,(x+34,y),label,15,MUTED)
        x+=int(len(label)*8.5+67)

# Linear effective flow in an odd periodic collocation grid.
N=65;L=2*np.pi;x=np.arange(N)*L/N
frequencies=np.fft.fftfreq(N,1/N)
D=np.fft.ifft(1j*frequencies[:,None]*np.fft.fft(np.eye(N),axis=0),axis=0).real
A=.5+.2*np.cos(x)
m=lambda a:1/(4*np.pi**2*(1+np.sqrt(1-a*a)))
Mcell=m(A);G=D@np.diag(A);K=G.T@np.diag(Mcell)@G
Komit=D.T@np.diag(A*A*Mcell)@D
eps=.35;I=np.eye(N);M=I+eps**2*K

def generator(kmat):
    return np.block([[np.zeros((N,N)),-D],[-solve(I+eps**2*kmat,D,assume_a='pos'),np.zeros((N,N))]])
B=generator(K);Bo=generator(Komit);B0=generator(np.zeros_like(K))
frames=80;T=2*np.pi;times=np.linspace(0,T,frames)
z0=.2*np.cos(x)+.1*np.sin(2*x);initial=np.r_[z0,z0]
travel=expm_multiply(B,initial,start=0,stop=T,num=frames)
omitted=expm_multiply(Bo,initial,start=0,stop=T,num=frames)
flat=expm_multiply(B0,initial,start=0,stop=T,num=frames)
standing=expm_multiply(B,np.r_[.2*np.cos(x)+.06*np.cos(2*x),np.zeros(N)],start=0,stop=T,num=frames)
Z=travel[:,:N];Q=travel[:,N:];ZS=standing[:,:N];QS=standing[:,N:]
energies=.5*(np.einsum('ij,ij->i',ZS,ZS)+np.einsum('ij,jk,ik->i',QS,M,QS))/N
potential=.5*np.mean(ZS*ZS,axis=1);kinetic=energies-potential

# Fresh low-frequency comparisons, built directly from the Fourier coefficients of H.
def full_spectrum(e,cutoff):
    modes=np.arange(-cutoff,cutoff+1)
    kk,nn=np.meshgrid(modes,modes,indexing='ij');kk=kk.ravel();nn=nn.ravel()
    dk=kk[:,None]-kk;dn=nn[:,None]-nn
    Hhat=((dk==0)&(dn==0)).astype(float)
    Hhat-=.25*((dk==0)&(abs(dn)==1))
    Hhat-=.05*((abs(dk)==1)&(abs(dn)==1))
    matrix=(kk[:,None]*kk+(2*np.pi/e)**2*nn[:,None]*nn)*Hhat
    return eigh(matrix,subset_by_index=[0,6],eigvals_only=True)[1:]

def reduced_spectrum(e,kmat):return eigh(D.T@D,I+e*e*kmat,subset_by_index=[0,6],eigvals_only=True)[1:]
spectral=[]
for e in [.8,.4,.2,.1]:
    ff=full_spectrum(e,12);rr=reduced_spectrum(e,K);oo=reduced_spectrum(e,Komit)
    spectral.append(dict(epsilon=e,complete_error=float(np.max(abs(ff-rr))),omitted_error=float(np.max(abs(ff-oo))),full_squared_frequencies=ff.tolist()))
for j,row in enumerate(spectral):row['observed_order']=None if j==0 else float(np.log2(spectral[j-1]['complete_error']/row['complete_error']))
refinement=float(np.max(abs(full_spectrum(.4,14)-full_spectrum(.4,12))))
form_error=float(abs(z0@(K@z0)-np.sum(Mcell*(D@(A*z0))**2)))
energy_drift=float(np.max(abs(energies/energies[0]-1)))
assert form_error<1e-10 and energy_drift<1e-10
assert all(r['observed_order']>3.8 for r in spectral[1:])
assert refinement<1e-8
metrics=dict(schema_version=1,model='linear effective modulated-bathymetry system',epsilon=eps,grid=N,domain=[0,float(L)],time_interval=[0,float(T)],frames=frames,
 spectral=spectral,checks=dict(form_identity_absolute_error=form_error,relative_energy_drift=energy_drift,spectral_cutoff_12_to_14_change_at_epsilon_0_4=refinement),
 environment=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,pillow=PIL.__version__),
 scope='Animations show computed linear effective flow and coefficient sweeps. No nonlinear homogenization theorem or field-data validation is claimed.')
(ROOT/'results/showcase_metrics.json').write_text(json.dumps(metrics,indent=2)+'\n')
print('Numerical checks:',metrics['checks'],flush=True)

# Keep animation frames indexed to a single palette to avoid colour flicker.
PALETTE=Image.new('P',(1,1));colors=[]
for rr in range(6):
    for gg in range(6):
        for bb in range(6):colors.extend((round(rr*255/5),round(gg*255/5),round(bb*255/5)))
for col in [BG,PANEL,GRID,WHITE,MUTED,CYAN,PURPLE,GOLD,GREEN,RED]:
    colors.extend(tuple(int(col[i:i+2],16) for i in (1,3,5)))
while len(colors)<768:colors.extend((0,0,0))
PALETTE.putpalette(colors[:768])
ASSETS=[]
def save_animation(relative,draw_frame,count=80,duration=60,poster=None):
    sequence=[]
    for f in range(count):
        frame=draw_frame(f,count)
        sequence.append(frame.quantize(palette=PALETTE,dither=Image.Dither.NONE))
        if poster is not None and f==count//3:frame.save(ASSET/'figures'/poster,optimize=True)
    p=ASSET/relative
    sequence[0].save(p,save_all=True,append_images=sequence[1:],duration=duration,loop=0,optimize=True,disposal=1)
    with Image.open(p) as check:
        assert check.n_frames>1
        dimensions=list(check.size);actual=check.n_frames
        delays=[]
        for j in range(actual):
            check.seek(j);delays.append(check.info['duration'])
    ASSETS.append(dict(path='assets/'+relative,dimensions=dimensions,frames=actual,requested_frame_duration_ms=duration,encoded_frame_durations_ms=delays,total_duration_ms=sum(delays),bytes=p.stat().st_size))
    print(relative,round(p.stat().st_size/1024),'KiB',flush=True)

def idx(f,n):return round(f*(frames-1)/max(1,n-1))
xx=np.r_[x,L]
def periodic(v):return np.r_[v,v[0]]

# Fixed bottom map, created from the model, not imported artwork.
def bottom_map(w,h):
    xs=np.linspace(0,L,w);ys=np.linspace(0,1,h)
    depth=1-(.5+.2*np.cos(xs))[None,:]*np.cos(2*np.pi*ys[:,None])
    u=(depth-.3)/1.4
    stops=np.array([[22,35,66],[49,91,119],[73,219,229],[231,247,239]])
    q=u*3;j=np.minimum(q.astype(int),2);z=q-j
    pixels=stops[j]*(1-z[:,:,None])+stops[j+1]*z[:,:,None]
    return Image.fromarray(pixels.astype(np.uint8))
heat=bottom_map(638,98)

def hero(f,n):
    i=idx(f,n);im,d=canvas(1200,510)
    text(d,(42,31),'MODULATED BATHYMETRY  /  RESEARCH SHOWCASE',15,CYAN,True)
    text(d,(42,92),'Waves shaped',44,WHITE,True);text(d,(42,148),'by geometry.',44,CYAN,True)
    text(d,(44,227),'Fixed mean depth.',23,WHITE)
    text(d,(44,261),'Changing transverse structure.',20,MUTED)
    text(d,(44,325),'Kₐw = −A ∂ₓ[m(A) ∂ₓ(Aw)]',22,PURPLE)
    d.rounded_rectangle((44,387,440,433),radius=12,fill=PANEL,outline=GRID)
    text(d,(60,402),'CELL → OPERATOR → WAVE',16,GREEN,True)
    text(d,(44,468),'ORIGINAL COMPUTATION  •  LINEAR EFFECTIVE MODEL',12,MUTED)
    panel(d,(493,74,1170,319));text(d,(519,88),'Evolving averaged surface',20,WHITE,True)
    text(d,(1148,94),f'ε = {eps:.2f}',16,CYAN,anchor='rt')
    box=(528,145,1147,270)
    axes(d,box,(0,L),(-.34,.34),[(0,'0'),(np.pi,'π'),(L,'2π')],[(-.3,'−.3'),(0,'0'),(.3,'.3')],'x','Z')
    curve(d,box,xx,periodic(Z[i]),(0,L),(-.34,.34),CYAN,3)
    probe=times[i]%L;px=box[0]+probe/L*(box[2]-box[0]);d.line((px,box[1],px,box[3]),fill=GOLD,width=1)
    text(d,(514,343),'Stationary resting depth H(x,Y)',17,WHITE,True)
    im.paste(heat,(518,373));d=ImageDraw.Draw(im)
    scan=518+int(probe/L*637);d.line((scan,373,scan,470),fill=GOLD,width=2)
    text(d,(514,487),f't = {times[i]:.2f}  ·  one displayed interval, then restart',13,MUTED)
    return im
save_animation('header/research-wave.gif',hero,80,65,'header-poster.png')

# Parameter animation uses a closed loop in A, not an evolution equation.
gridA=np.linspace(0,.92,300)
def sweep(f,n):
    aa=.075+.825*(1-np.cos(2*np.pi*f/n))/2
    im,d=canvas(940,500);text(d,(30,25),'A cell coefficient, built from transverse geometry',25,WHITE,True)
    text(d,(30,66),f'PARAMETER SWEEP   A = {aa:.3f}   •   mean depth = 1',16,CYAN)
    panel(d,(23,108,450,448));panel(d,(466,108,917,448))
    box=(86,173,421,377);ys=np.linspace(0,1,250)
    axes(d,box,(0,1),(0,2),[(0,'0'),(.5,'½'),(1,'1')],[(0,'0'),(1,'1'),(2,'2')],'Y','H = 1 − A cos(2πY)')
    curve(d,box,ys,1-aa*np.cos(2*np.pi*ys),(0,1),(0,2),CYAN)
    box2=(542,173,889,377)
    axes(d,box2,(0,.92),(0,.016),[(0,'0'),(.45,'.45'),(.9,'.90')],[(0,'0'),(.008,'.008'),(.016,'.016')],'A','μ(A) = A²m(A)')
    curve(d,box2,gridA,gridA**2*m(gridA),(0,.92),(0,.016),PURPLE)
    dot(d,(box2[0]+aa/.92*(box2[2]-box2[0]),box2[3]-aa*aa*m(aa)/.016*(box2[3]-box2[1])),GOLD,6)
    text(d,(30,470),'Closed-form cosine cell • A varies; this is not a time-dependent bottom.',15,MUTED)
    return im
save_animation('animations/cell-coefficient.gif',sweep,72,65,'cell-coefficient.png')

max_difference=float(np.max(abs(Z-flat[:,:N])));limit=max_difference*1.12

def comparison(f,n):
    i=idx(f,n);im,d=canvas(1000,570)
    text(d,(32,25),'Resolving the dispersive correction',27,WHITE,True)
    text(d,(32,67),f'COMPUTED LINEAR FLOW  •  t = {times[i]:.2f}  •  ε = {eps:.2f}',16,MUTED)
    box=(88,145,950,298)
    axes(d,box,(0,L),(-.34,.34),[(0,'0'),(np.pi,'π'),(L,'2π')],[(-.3,'−.3'),(0,'0'),(.3,'.3')],'','averaged surface Z')
    curve(d,box,xx,periodic(flat[i,:N]),(0,L),(-.34,.34),GOLD,2)
    curve(d,box,xx,periodic(Z[i]),(0,L),(-.34,.34),CYAN,3)
    legend(d,95,324,[('Complete',CYAN),('Nondispersive',GOLD)])
    box2=(88,405,950,493)
    axes(d,box2,(0,L),(-limit*1e3,limit*1e3),[(0,'0'),(np.pi,'π'),(L,'2π')],[(-limit*1e3,f'{-limit*1e3:.1f}'),(0,'0'),(limit*1e3,f'{limit*1e3:.1f}')],'x','difference × 10³ (complete minus comparison)')
    curve(d,box2,xx,periodic((Z[i]-flat[i,:N])*1e3),(0,L),(-limit*1e3,limit*1e3),GOLD,2)
    curve(d,box2,xx,periodic((Z[i]-omitted[i,:N])*1e3),(0,L),(-limit*1e3,limit*1e3),PURPLE,2)
    legend(d,95,545,[('Nondispersive',GOLD),('Geometry term omitted',PURPLE)])
    return im
save_animation('animations/wave-comparison.gif',comparison,80,65,'wave-comparison.png')

probe_index=round(N/6);pxs=ZS[:,probe_index];pqs=QS[:,probe_index];phase_limit=max(abs(pxs).max(),abs(pqs).max())*1.2

def phase_energy(f,n):
    i=idx(f,n);im,d=canvas(940,500)
    text(d,(30,24),'Phase motion and conserved linear energy',26,WHITE,True)
    text(d,(30,67),f'STANDING-WAVE INITIAL DATA  •  x* = {x[probe_index]:.3f}  •  t = {times[i]:.2f}',15,MUTED)
    box=(92,159,440,386)
    axes(d,box,(-phase_limit,phase_limit),(-phase_limit,phase_limit),[(-.1,'−.1'),(0,'0'),(.1,'.1')],[(-.1,'−.1'),(0,'0'),(.1,'.1')],'Z(x*,t)','q(x*,t)')
    curve(d,box,pxs,pqs,(-phase_limit,phase_limit),(-phase_limit,phase_limit),GRID,2)
    pts=curve(d,box,pxs[:i+1],pqs[:i+1],(-phase_limit,phase_limit),(-phase_limit,phase_limit),PURPLE,3)
    dot(d,pts[-1],GOLD,6)
    text(d,(525,131),'ENERGY EXCHANGE',18,GREEN,True)
    fractions=[potential[i]/energies[0],kinetic[i]/energies[0],energies[i]/energies[0]]
    for j,(lab,col) in enumerate([('Surface part',CYAN),('Velocity + cell part',PURPLE),('Total / initial',GREEN)]):
        yy=184+j*72;text(d,(525,yy-23),lab,16,MUTED)
        d.rounded_rectangle((525,yy,885,yy+19),radius=5,fill=GRID)
        d.rounded_rectangle((525,yy,525+max(1,360*fractions[j]),yy+19),radius=5,fill=col)
        text(d,(885,yy-24),f'{fractions[j]:.4f}',16,col,anchor='rt')
    text(d,(30,467),'E = ½ meanₓ {Z² + q² + ε²m(A)[∂ₓ(Aq)]²}  •  fixed coefficients',17,MUTED)
    return im
save_animation('animations/phase-energy.gif',phase_energy,80,65,'phase-energy.png')

es=np.array([v['epsilon'] for v in spectral]);errors=np.array([v['complete_error'] for v in spectral]);errs_o=np.array([v['omitted_error'] for v in spectral])

def convergence(f,n):
    u=f/(n-1);stage=min(3,int(u*4));im,d=canvas(940,500)
    text(d,(30,25),'Four scale values. One asymptotic check.',27,WHITE,True)
    text(d,(30,68),'PROGRESSIVE REVEAL OF COMPUTED SPECTRAL ERRORS',15,MUTED)
    box=(95,145,598,390)
    lx=(np.log10(.09),np.log10(.9));ly=(-6,-1.7)
    xt=[(np.log10(a),str(a)) for a in [.1,.2,.4,.8]]
    axes(d,box,lx,ly,xt,[(v,'10'+str(v).translate(str.maketrans('-0123456789','⁻⁰¹²³⁴⁵⁶⁷⁸⁹'))) for v in [-6,-5,-4,-3,-2]],'ε (log scale)','max error in first six nonzero ω²')
    refx=np.linspace(.1,.8,100);refy=errors[0]*(refx/.8)**4
    curve(d,box,np.log10(refx),np.log10(refy),lx,ly,GRID,3)
    for vals,col in [(errors,CYAN),(errs_o,GOLD)]:
        pts=curve(d,box,np.log10(es[:stage+1]),np.log10(vals[:stage+1]),lx,ly,col,3)
        for p in pts:dot(d,p,col,5)
    text(d,(650,148),'SELECTED SCALE',15,MUTED,True)
    text(d,(650,181),f'ε = {es[stage]:.1f}',32,WHITE,True)
    text(d,(650,249),'Complete operator',16,CYAN)
    text(d,(650,279),f'{errors[stage]:.3e}',25,WHITE,True)
    text(d,(650,334),'Observed order',16,MUTED)
    val=spectral[stage]['observed_order'];text(d,(650,361),'—' if val is None else f'{val:.3f}',28,GREEN,True)
    legend(d,96,444,[('Complete',CYAN),('Geometry omitted',GOLD)])
    text(d,(31,478),'Order refers to ε. The dark reference curve is proportional to ε⁴.',14,MUTED)
    return im
save_animation('animations/spectral-convergence.gif',convergence,72,65,'spectral-convergence.png')

HEADERS=[('overview','01 / RESEARCH OVERVIEW','A fixed mean. A changing cell.',CYAN),('framework','02 / MATHEMATICAL FRAMEWORK','Derive the operator. Retain the geometry.',PURPLE),('results','03 / NUMERICAL RESULTS','Compare the resolved wave and correction.',GOLD),('verification','04 / VERIFICATION','Track invariants and asymptotic error.',GREEN)]
for kind,title,subtitle,col in HEADERS:
    def section(f,n,kind=kind,title=title,subtitle=subtitle,col=col):
        im,d=canvas(1100,134);text(d,(29,28),title,24,col,True);text(d,(30,75),subtitle,18,MUTED)
        b=(758,24,1069,107);i=idx(f,n)
        for yy in [45,66,87]:d.line((758,yy,1069,yy),fill=GRID)
        if kind=='overview':
            ys=np.linspace(0,1,120);aa=.5+.2*np.cos(2*np.pi*f/n)
            curve(d,b,ys,1-aa*np.cos(2*np.pi*ys),(0,1),(.2,1.8),col,3)
        elif kind=='framework':
            curve(d,b,gridA,gridA**2*m(gridA),(0,.92),(0,.016),col,3)
            aa=.46*(1-np.cos(2*np.pi*f/n));dot(d,(758+aa/.92*311,107-aa*aa*m(aa)/.016*83),GOLD,5)
        elif kind=='results':curve(d,b,xx,periodic(Z[i]),(0,L),(-.34,.34),col,3)
        else:
            curve(d,b,np.arange(i+1),potential[:i+1]/energies[0],(0,frames-1),(0,1),CYAN,2)
            curve(d,b,np.arange(i+1),kinetic[:i+1]/energies[0],(0,frames-1),(0,1),PURPLE,2)
            d.line((758,24,1069,24),fill=GREEN,width=2)
        return im
    save_animation('section_headers/'+kind+'.gif',section,48,80)

# A single exact constant-coefficient Fourier mode yields a seamless separator.
def separator(f,n):
    im=Image.new('RGB',(1100,32),BG);d=ImageDraw.Draw(im);xx=np.linspace(0,2*np.pi,600)
    curve(d,(0,4,1099,28),xx,np.sin(4*xx-2*np.pi*f/n),(0,2*np.pi),(-1.4,1.4),CYAN,2)
    return im
save_animation('section_headers/wave-divider.gif',separator,40,70)

# Original SVG badges, local navigation tiles, and a compact workflow.
def svgtext(x,y,s,size=16,color=WHITE,bold=False):
    import html
    return f'<text x="{x}" y="{y}" font-family="DejaVu Sans,Arial,sans-serif" font-size="{size}" fill="{color}"'+(' font-weight="700"' if bold else '')+'>'+html.escape(s)+'</text>'
def svgfile(name,w,h,body):
    (ASSET/'icons'/name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="10" fill="{PANEL}" stroke="{GRID}"/>'+body+'</svg>\n')
for name,label,value,col,w in [('model','MODEL','Linear waves',CYAN,265),('theory','THEORY','Positive energy',PURPLE,250),('visuals','VISUALS','Original',GREEN,220),('scope','SCOPE','No manuscripts',GOLD,270)]:
    svgfile(name+'.svg',w,34,svgtext(12,23,label,11,col,True)+svgtext(84,23,value,13,WHITE))
for slug,label,col in [('overview','Overview',CYAN),('mathematics','Mathematics',PURPLE),('gallery','Motion gallery',GOLD),('verification','Verification',GREEN)]:
    svgfile('nav-'+slug+'.svg',180,42,svgtext(17,27,label,15,col,True)+svgtext(153,27,'→',17,col))
body='';labels=['Geometry','Cell coefficient','Dispersive form','Linear flow','Verification']
for j,label in enumerate(labels):
    left=18+j*214
    body+=f'<rect x="{left}" y="45" width="190" height="76" rx="12" fill="{PANEL}" stroke="{[CYAN,PURPLE,GOLD,CYAN,GREEN][j]}"/>'
    body+=svgtext(left+14,73,str(j+1).zfill(2),13,MUTED,True)+svgtext(left+14,101,label,16,WHITE,True)
    if j<4:body+=f'<path d="M {left+195} 83 h 12 m -4 -4 l 4 4 -4 4" fill="none" stroke="{MUTED}" stroke-width="2"/>'
(ASSET/'figures/workflow.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="150" viewBox="0 0 1100 150"><rect width="1100" height="150" rx="18" fill="{BG}"/>'+body+'</svg>\n')
(ROOT/'results/asset_manifest.json').write_text(json.dumps(ASSETS,indent=2)+'\n')
print('Total GIF size:',round(sum(a['bytes'] for a in ASSETS)/1024**2,2),'MiB',flush=True)
