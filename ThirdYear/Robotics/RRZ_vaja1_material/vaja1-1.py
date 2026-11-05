# %%
import cv2
import matplotlib.pyplot as plt
import numpy as np

# %%
ime_slike = 'umbrellas.jpg'
im = cv2.imread(ime_slike)
im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

print (f'{im.shape=}')
print (f'{im.dtype=}')

plt.clf()
plt.imshow(im)
plt.show()

# %%
img_float = im.astype(np.float32) / 255.0

print(f'{img_float.shape=}')

#R + G + B / 3
gray = np.mean(img_float, axis=2)

plt.imshow(gray, cmap='gray')

# %%
cropped = im[20:200, 400:600]
marked_section = im.copy()
marked_section[20:200, 400:600, 2] = 0

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.imshow(marked_section)
plt.title("Original z oznacenim obmocjem")

plt.subplot(1, 2, 2)
plt.imshow(cropped)
plt.title("Izrez")

plt.show()


# %%
inverted = gray.copy()
inverted [0:360, 320:650] = 1 - inverted[0:360, 320:650]

print(f'{inverted.shape=}')
print(f'{inverted.dtype=}')
print(f'{inverted[0,0]=}')
plt.imshow(inverted, cmap='gray')

# %%
binarno = gray.copy()
binarno = (binarno * 255).astype(np.uint8)

print(f'{gray.shape=}')

binarno[binarno < 150] = 0
binarno[binarno >= 150] = 255

plt.imshow(binarno, cmap='gray')

# %% [markdown]
# ## 2. Kamera
# 
# #### a.)
# 
# f = 10cm  
# Z = 14m  
# H = 5m  
# 
# $$h = -f\frac{H}{Z}$$
# $$h = -10cm\frac{5m}{14m}$$
# $$h = -10cm\frac{500cm}{1400cm}$$
# $$h = -3.57cm
# 

# %% [markdown]
# #### b.)
# 
# f = 10cm  
# Z = 10m  
# H = 2.5m  
# a = 0.5 $\frac{m}{s^2}$  
# t = 30s  
# interval = 10m

# %%
def camera_size (focal_length, real_size, distance):
    return abs((-focal_length * real_size) / distance)

# %%

sizes = []
times = []
acceleration = 50
time = 0

for time in range(0, 300):
    sizes.append(camera_size(10, 250, 1000 + (0.5 * acceleration * time/10 * time/10)))
    times.append(time/10)
    
    

plt.plot(times,sizes)
plt.xlabel("Time [s]")
plt.ylabel("Size [cm]")
    

# %% [markdown]
# #### c.)
# Lece so veliko drazje in bolj kompleksne kot kamere z luknjico, imajo pa veliko prednost, da lahko osredotocajo svetlobo na senzor, kar vodi k svetlejsim slikam.

# %% [markdown]
# #### d.)
# 
# f = 60mm  
# Z = 95m  
# h(px) = 250px
# p = 2500 DPI
# 
# conversion: 1 inch = 2.54cm
# 
# 
# $$ h = \frac {h(px)}{p} $$
# $$ h = \frac {200px}{2500 px/inch} $$
# $$ h = 0.08 inch$$
# $$ h = 0.2032 cm$$
# $$ h = 2.032 mm$$
# 
# ---
# $$ H = \frac {hZ}{f} $$
# $$ H = \frac {2.032mm * 95m}{60mm} $$
# $$ H = \frac {193040000mm}{60mm} $$
# $$ H = 3217333 mm $$
# $$ H = 3.22m $$
# 
# 

# %% [markdown]
# #### e.)

# %%

distances = np.array([30, 40, 50, 60, 70])
heights = np.array([1040, 677, 511, 404, 336])

plt.plot(distances, heights, 'o-')
plt.xlabel("Razdalja [cm]")
plt.ylabel("Višina pločevinke [px]")
plt.grid()
plt.show()


# %% [markdown]
# $$ \frac {h1}{h2} = \frac {Z1}{Z2} $$
# $$ {h2} = h1* \frac {Z1}{Z2} $$
# $$ {h2} = 336px * \frac {70cm}{80cm} $$
# $$ h2 = 294px $$
# ---
# Actual measured = 287px

# %%
predicted = 336 * (70 / 80)
measured = 287

error = abs(predicted - measured)
relative_error = error / measured * 100

print(f"Predicted: {predicted:.1f} px")
print(f"Error: {error:.1f} px ({relative_error:.2f}%)")

# %% [markdown]
# ## 3. Histogrami
# 
# #### a.)

# %%
values = range(8)
frequencies = [3, 8, 2, 4, 1, 3, 1, 3]

plt.bar(values, frequencies)
plt.xlabel("Vrednost")
plt.ylabel("Frekvenca")
plt.show()

# %%

# Kumulativni histogram
cumulative = np.cumsum(frequencies)

plt.title("Kumulativni histogram")
plt.bar(values, cumulative)
plt.xlabel("Vrednost")
plt.ylabel("Kumulativna frekvenca")
plt.show()

# %% [markdown]
# #### c.)
# 
# Ce bi bila matrika 4 bitna bi sle vrednosti na njej do 16. Histogram bi bil se enkrat vecji.

# %%

histogram = np.histogram(gray, bins=8)

plt.bar(
    histogram[1][:-1],
    histogram[0],
    width=np.diff(histogram[1]),
    align='edge',
    edgecolor='black'
)

plt.xlabel("Sivinska vrednost")
plt.ylabel("Frekvenca")
plt.show()


# %%
def histogram_stretch(image):
    
    min_val = np.min(image)
    max_val = np.max(image)
    
    image = 255 * ((image - min_val) / (max_val - min_val))
    return image

# %%
phone = cv2.imread('phone.jpg', cv2.IMREAD_GRAYSCALE)
type(phone)
phone.shape

phone8 = phone.astype(np.uint8)

# %%

phone = cv2.imread('phone.jpg', cv2.IMREAD_GRAYSCALE)

fig, ax = plt.subplots(2, 2, figsize=(12, 7))

images = [phone, histogram_stretch(phone)]
titles = ["Original", "Modified"]

for i in range(2):
    ax[0, i].imshow(images[i], cmap='gray', vmin=0, vmax=255)
    ax[0, i].set_title(titles[i])
    ax[0, i].axis('off')

    histogram = np.histogram(images[i], bins=256, range=(0, 256))

    ax[1, i].bar(
        histogram[1][:-1],
        histogram[0],
        width=np.diff(histogram[1]),
        align='edge',
        edgecolor='black'
    )

    ax[1, i].set_xlabel("Sivinska vrednost")
    ax[1, i].set_ylabel("Frekvenca")

plt.subplots_adjust(hspace=0.15, wspace=0.2)
plt.show()


# %%
threshold, binary = cv2.threshold(phone, 0, 255, cv2.THRESH_OTSU)

print(f"{threshold=}")

plt.imshow(binary)


# %% [markdown]
# #### g.)
# Deluje najbolje ko imamo subjekt in ozadje, ki imata med sabo visok kontrast. Ali bolj natancno ko imamo bimodalni histogram (histogram z dvema vrhovoma)

# %% [markdown]
# ## 4. Barvni prostor

# %%
import matplotlib

print(matplotlib.colors.rgb_to_hsv([1,34/255,126/255]))

# %% [markdown]
# #### a.)
# Pretvori RGB v HSV: (255,34,126)
# 
# $$ M = max(255, 34, 126) $$
# $$ M = 255 (R) $$
# <br>
# 
# $$ m = min(255, 34, 126) $$
# $$ m = 34 $$
# 
# <br>
# 
# $$ d = M - m $$
# $$ d = 255 - 34 $$
# $$ d = 221 $$
# 
# ---
# 
# $$ H = 60 * (\frac {G - B} d + 6 mod 6) $$
# $$ H = 60 * (\frac {-92} {221} + 6 mod 6)$$
# $$ H = 60 * (\frac {1234} {221} mod 6)$$
# $$ H = 60 * 5.583 $$
# $$ H = 335.02 $$
#  <br>
# 
# $$ S = \frac d M $$
# $$ S = \frac {221} {255} $$
# $$ S = 0.87 $$
# <br>
# 
# $$ V = M $$
# $$ V = 255 $$
# 
# ---
# 
# $$ HSV = (335, 0.87, 1) $$
# 
# 

# %% [markdown]
# #### b.)
# HSV 2 RGB -> (0.65, 0.7, 0.15)
# 
# $$ C = S * V $$
# $$ C = 0.7 * 0.15 $$
# $$ C = 0.105$$
# <br>
# 
# $$ X = C * (1-|(6H mod 2) - 1|) $$
# $$ X = 0.105 * (1 - |(6 * 0.65 mod 2) - 1|) $$
# $$ X = 0.105 * (1 - |1.9 - 1|) $$
# $$ X = 0.105 * (1 - 0.9) $$
# $$ X = 0.105 * 0.1 $$
# $$ X = 0.0105 $$
# <br>
# 
# $$ m = V - C $$
# $$ m = 0.15 - 0.105 $$
# $$ m = 0.045 $$
# 
# ---
# 
# $$ RGB = (R' + m, G' + m, B' + m) $$
# $$ RGB = (0 + m, X + m, C + m) $$
# $$ RGB = (0.045, 0.0105 + 0.045, 0.105 + 0.045) $$
# $$ RGB = (0.045, 0.0555, 0.15)
# 
# 

# %%
matplotlib.colors.hsv_to_rgb([0.65, 0.7, 0.15])

# %%
trucks = cv2.imread("trucks.jpg")
trucks_rgb = cv2.cvtColor(trucks, cv2.COLOR_BGR2RGB)

plt.imshow(trucks_rgb)
plt.show()

# %%
R = trucks_rgb[:, :, 0]
G = trucks_rgb[:, :, 1]
B = trucks_rgb[:, :, 2]

fig, ax = plt.subplots(1, 3, figsize=(12, 4))

ax[0].imshow(R, cmap="gray", vmin=0, vmax=255)
ax[0].set_title("Red")

ax[1].imshow(G, cmap="gray", vmin=0, vmax=255)
ax[1].set_title("Green")

ax[2].imshow(B, cmap="gray", vmin=0, vmax=255)
ax[2].set_title("Blue")

plt.show()

# %%
rgb_float = trucks_rgb.astype(np.float32) / 255.0

hsv = cv2.cvtColor(rgb_float, cv2.COLOR_RGB2HSV)

#hsv rabimo med 0 in 1 ne med 0 in 360

hsv[:, :, 0] /= 360

H = hsv[:, :, 0]
S = hsv[:, :, 1]
V = hsv[:, :, 2]

fig, ax = plt.subplots(1, 3, figsize=(12, 4))

ax[0].imshow(H, cmap="gray", vmin=0, vmax=1)
ax[0].set_title("Hue")

ax[1].imshow(S, cmap="gray", vmin=0, vmax=1)
ax[1].set_title("Saturation")

ax[2].imshow(V, cmap="gray", vmin=0, vmax=1)
ax[2].set_title("Value")

plt.show()

# %%
def blue_threshold(img, threshold = 150):
    _, binary = cv2.threshold(img[:,:,2], threshold, 255, cv2.THRESH_BINARY)
    return binary

# %%
fig, ax = plt.subplots(1, 2, figsize=(15, 6))
ax[0].imshow(trucks_rgb)
ax[1].imshow(blue_threshold(trucks_rgb), cmap = 'grey')

# %%
#Brez keepdims nam sestevanje da 2 dimenzinalno matriko
rgb_sum = np.sum(rgb_float,axis=2,keepdims=True)
#Delimo modro iz originalne slike z vsemi kanali sestetimi kot v formuli
rgb_normalized = np.divide(rgb_float, rgb_sum)

fig, ax = plt.subplots(1, 2, figsize=(15, 6))
ax[0].imshow(trucks_rgb)
ax[1].imshow(blue_threshold(rgb_normalized, 0.5), cmap = 'grey')


# %%
plt.figure()
plt.imshow(np.meshgrid(np.linspace(0, 1, 255), np.ones((10, 1)))[0], 
cmap=plt.cm.hsv)
plt.show()

# %%
def hsv_threshold(img, min, max):
    
    H = img[:,:, 0]
    
    mask = (H>=min) & (H<=max)
    return mask

# %%
fig, ax = plt.subplots(1, 2, figsize=(15, 6))
ax[0].imshow(trucks_rgb)
ax[1].imshow(hsv_threshold(hsv, 134/255, 150/255), cmap = 'grey')

# %%
umbrellas_hsv = cv2.cvtColor(im.astype(np.float32) / 255.0, cv2.COLOR_RGB2HSV)

fig, ax = plt.subplots(1, 2, figsize=(15, 6))
ax[0].imshow(im)
ax[1].imshow(hsv_threshold(umbrellas_hsv, 15, 40), cmap = 'grey')

# %%
def im_mask(image, mask):
    
    masked_image = image.copy()
    masked_image[~mask] = 0
    return masked_image


# %%
plt.imshow(im_mask(trucks_rgb, hsv_threshold(hsv, 134/255, 150/255)))

# %% [markdown]
# ## 5. Regije in morfološke operacije

# %%
img = cv2.imread("tabela.png")

plt.figure(figsize=(12, 8))
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.show()

# %%
regije = cv2.imread('regions.png', cv2.IMREAD_GRAYSCALE)

_, mask = cv2.threshold(regije, 125, 255, cv2.THRESH_BINARY)

count, labels = cv2.connectedComponents(mask)

plt.imshow(regije)
plt.title(f"stevilo regij {count}: ")


# %%
from matplotlib.patches import Rectangle

count, labels, stats, centroids = cv2.connectedComponentsWithStats(mask)


fig, ax = plt.subplots(figsize=(10, 6))
ax.imshow(mask, cmap='gray')

for i in range(1, count):  # skip background

    # Bounding box
    x, y, w, h, area = stats[i]

    cx, cy = centroids[i]

    rect = Rectangle((x, y), w, h, fill=False, edgecolor='red', linewidth=2)
    ax.add_patch(rect)
    
    ax.scatter(cx, cy)


# %%
img = cv2.imread("morph.png")

plt.figure(figsize=(12, 8))
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.show()

# %%
regije = cv2.imread('regions_noise.png', cv2.IMREAD_GRAYSCALE)

_, mask = cv2.threshold(regije, 125, 255, cv2.THRESH_BINARY)

count, labels = cv2.connectedComponents(mask)

plt.imshow(regije)
plt.title(f"stevilo regij {count}: ")


# %%
def openIm(image, kernel):
    eroded = cv2.erode(image, kernel)
    diluded = cv2.dilate(eroded, kernel)
    
    return diluded

def closeIm(image, kernel):
    diluded = cv2.dilate(image, kernel)
    eroded = cv2.erode(diluded, kernel)
    
    return eroded

# %%

kernel = np.ones((3, 3), dtype=np.uint8)

regije = cv2.imread('regions_noise.png', cv2.IMREAD_GRAYSCALE)
_, mask = cv2.threshold(regije, 125, 255, cv2.THRESH_BINARY)

images = [
    openIm(mask, kernel),
    cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel),
    closeIm(mask, kernel),
    cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
]

titles = ["Opening", "Opening OpenCV", "Closing", "Closing OpenCV"]

fig, ax = plt.subplots(2, 2, figsize=(10, 8))

for i in range(4):
    count, labels = cv2.connectedComponents(images[i])

    a = ax[i // 2, i % 2]
    a.imshow(images[i], cmap='gray')
    a.set_title(f"{titles[i]}\nRegije: {count}")
    a.axis('off')

plt.tight_layout()
plt.show()


# %%

import ipywidgets as widgets

bird = cv2.imread('bird.jpg')
bird_gray = cv2.cvtColor(bird, cv2.COLOR_BGR2GRAY)
kernel = np.ones((3, 3), dtype=np.uint8)

def show_bird(threshold=50):
    _, mask = cv2.threshold(bird_gray, threshold, 255, cv2.THRESH_BINARY)

    opened = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    cleaned = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)

    fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    ax[0].imshow(cv2.cvtColor(bird, cv2.COLOR_BGR2RGB))
    ax[0].set_title("Original")

    ax[1].imshow(cleaned, cmap='gray', vmin=0, vmax=255)
    ax[1].set_title(f"Final mask (threshold={threshold})")

    for a in ax:
        a.axis('off')

    plt.tight_layout()
    plt.show()

widgets.interact(
    show_bird,
    threshold=widgets.IntSlider(value=50, min=0, max=255, step=1)
)


# %%
'''cap = cv2.VideoCapture(1)  # 0 = privzeta spletna kamera
# Namesto številke lahko podamo tudi ime video datoteke

# Zanka za pridobitev naslednje slike
while(True):
    # Poskusimo pridobiti trenutno sliko s spletne kamere
    ret, frame = cap.read()
    
    # Če to ni mogoče (kamera izključena, itd.), končamo z izvajanjem funkcije
    if not ret:
        break

    # Prikaži trenutno sliko
    cv2.imshow('frame', frame)
    
    # Ob pritisku tipke 'q' prekini izvajanje funkcije
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Zapri kamero in okno
cap.release()
cv2.destroyAllWindows()'''

# %%
'''cap = cv2.VideoCapture(1)  # 0 = privzeta spletna kamera
# Namesto številke lahko podamo tudi ime video datoteke

# Zanka za pridobitev naslednje slike
while(True):
    # Poskusimo pridobiti trenutno sliko s spletne kamere
    ret, frame = cap.read()
    
    # Če to ni mogoče (kamera izključena, itd.), končamo z izvajanjem funkcije
    if not ret:
        break

    # Prikaži trenutno sliko
    flipped = cv2.flip(frame, 1)
    gray = cv2.cvtColor(flipped, cv2.COLOR_BGR2GRAY)
    gray_brg = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)


    combined = cv2.hconcat([frame, gray_brg])

    cv2.imshow('Camera - Color | Grayscale', combined)
    
    # Ob pritisku tipke 'q' prekini izvajanje funkcije
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Zapri kamero in okno
cap.release()
cv2.destroyAllWindows()'''

# %%
cap = cv2.VideoCapture(1)  # 0 = privzeta spletna kamera
# Namesto številke lahko podamo tudi ime video datoteke

# Zanka za pridobitev naslednje slike
while(True):
    # Poskusimo pridobiti trenutno sliko s spletne kamere
    ret, frame = cap.read()
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    mask = hsv_threshold(hsv, 95, 120)
    contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)
    
    
    
    # Če to ni mogoče (kamera izključena, itd.), končamo z izvajanjem funkcije
    if not ret:
        break

    # Prikaži trenutno sliko
    cv2.imshow('frame', frame)
    
    # Ob pritisku tipke 'q' prekini izvajanje funkcije
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Zapri kamero in okno
cap.release()
cv2.destroyAllWindows()


