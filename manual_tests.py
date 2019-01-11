import staintools
import datetime

# Set up
METHOD = 'vahadane'
STANDARDIZE_BRIGHTNESS = True
RESULTS_DIR = './results ' + str(datetime.datetime.now()) + '/'

# Read the images
i1 = staintools.read_image("./data/i1.png")
i2 = staintools.read_image("./data/i2.png")
i3 = staintools.read_image("./data/i3.png")
i4 = staintools.read_image("./data/i4.png")
i5 = staintools.read_image("./data/i5.png")

# Plot
stack = staintools.make_image_stack([i1, i2, i3, i4, i5])
titles = ["Target"] + ["Original"] * 4
staintools.plot_image_stack(stack, width=5, title_list=titles, \
                            save_name=RESULTS_DIR + 'original-images.png', show=0)

# =========================
# Brightness standarization
# (Can skip but can help with tissue mask detection)
# =========================

if STANDARDIZE_BRIGHTNESS:

    # Standardize brightness
    standardizer = staintools.BrightnessStandardizer()
    i1 = standardizer.transform(i1)
    i2 = standardizer.transform(i2)
    i3 = standardizer.transform(i3)
    i4 = standardizer.transform(i4)
    i5 = standardizer.transform(i5)

    # Plot
    stack = staintools.make_image_stack([i1, i2, i3, i4, i5])
    titles = ["Target standardized"] + ["Original standardized"] * 4
    staintools.plot_image_stack(stack, width=5, title_list=titles, \
                                save_name=RESULTS_DIR + 'original-images-standardized.png', show=0)

# ===================
# Stain normalization
# ===================

# Normalize to stain of first image
normalizer = staintools.StainNormalizer(method=METHOD)
normalizer.fit(i1)
i2_normalized = normalizer.transform(i2)
i3_normalized = normalizer.transform(i3)
i4_normalized = normalizer.transform(i4)
i5_normalized = normalizer.transform(i5)

# Plot
stack = staintools.make_image_stack([i1, i2_normalized, i3_normalized, i4_normalized, i5_normalized])
titles = ["Target"] + ["Stain normalized"] * 4
staintools.plot_image_stack(stack, width=5, title_list=titles, \
                            save_name=RESULTS_DIR + 'stain-normalized-images.png', show=0)

# ==================
# Stain augmentation
# ==================

# Augment the first image
augmentor = staintools.StainAugmentor(method=METHOD, sigma1=0.4, sigma2=0.4)
augmentor.fit(i1)
augmented_images = []
for _ in range(10):
    augmented_image = augmentor.pop()
    augmented_images.append(augmented_image)

# Plot
stack = staintools.make_image_stack(augmented_images)
titles = ["Augmented"] * 10
staintools.plot_image_stack(stack, width=5, title_list=titles, \
                            save_name=RESULTS_DIR + 'stain-augmented-images.png', show=0)