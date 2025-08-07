Of course. Here is the complete raw markdown source for the "Phygital Storage Capacity by Pack Count" document, formatted as a single indented code block to prevent rendering.

### The "Digital Curio" Model: A Single Card, A Single Treasure

```
This is an excellent alternative model. Instead of a large, distributed file that requires a full collection to unlock (the "Chimera Codex"), this approach treats each card as its own self-contained digital treasure box. A 5-pack of cards would give a collector five distinct, tiny digital artifacts.

This "Digital Curio" model is perfect for series that emphasize variety and individual discovery over a single, grand puzzle. It lowers the barrier to a rewarding experience; the user gets instant gratification from every single card they scan.

---

#### **Single Card Capacity Revisited**

To explore this model, let's zoom in on the capacity of a single card. Based on our chosen **NXP NTAG215** chip, after allocating space for the URL and ID, we have approximately **404 bytes of free space** per card.

Here is what that single card's 404 bytes could realistically hold:

* **Text:**
    * Roughly **~400 characters**.
    * This is enough for a short, self-contained piece of micro-fiction, a detailed caption for the card's artwork, a poem, or a single "blessing."

* **Image (Bitmap):**
    * A tiny, icon-sized **11x11 pixel** bitmap with 24-bit color.
    * This is extremely small, suitable only for a simple glyph, a single pixel-art character sprite, or a tiny abstract pattern.


* **Image (Bitmap - Black & White):**
    * A 1-bit monochrome bitmap uses only 1 bit per pixel, whereas a 24-bit color bitmap uses 24 bits. This makes the black and white version **24 times smaller** for the same number of pixels.
    * With 404 bytes of free space, we can now store a much more detailed icon-sized image of approximately **52x52 pixels**.
    * This is a significant improvement over the 11x11 color version and is large enough to clearly render a complex logo, a QR code, or a detailed character sprite.


* **Sound (.wav):**
    * Approximately **0.03 seconds** of low-fidelity mono audio.
    * This is not long enough for a word, but it is enough to store a unique "click," "pop," or "chime" sound effect. A 5-card pack could contain five distinct notification sounds.
```
```

### Phygital Storage Capacity by Pack Count

This table outlines the total addressable data capacity based on the number of 52-card packs collected in a series.

| **Pack Count** | **Card Count** | **Total Bytes (Free)** | **Pages (Text)** | **Image Quality (Approx.)** | **Sound Quality** | **Sound Duration (Seconds)** | 
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | 52 | 21.0 KB | ~10 | 84x84 Bitmap (24-bit) | Low-Fi Mono | ~1.5 sec | 
| **5** | 260 | 105.0 KB | ~51 | 189x189 Bitmap (24-bit) | Low-Fi Mono | ~7.3 sec | 
| **10** | 520 | 210.1 KB | ~102 | 267x267 Bitmap (24-bit) | Low-Fi Mono | ~14.7 sec | 
| **15** | 780 | 315.1 KB | ~153 | 327x327 Bitmap (24-bit) | Low-Fi Mono | ~22.0 sec | 
| **20** | 1,040 | 420.2 KB | ~205 | 378x378 Bitmap (24-bit) | Low-Fi Mono | ~29.3 sec | 
| **25** | 1,300 | 525.2 KB | ~256 | 422x422 Bitmap (24-bit) | Low-Fi Mono | ~36.6 sec | 
| **30** | 1,560 | 630.2 KB | ~307 | 462x462 Bitmap (24-bit) | Low-Fi Mono | ~43.9 sec | 
| **35** | 1,820 | 735.3 KB | ~359 | 499x499 Bitmap (24-bit) | Low-Fi Mono | ~51.3 sec | 
| **40** | 2,080 | 840.3 KB | ~410 | 534x534 Bitmap (24-bit) | Low-Fi Mono | ~58.6 sec | 
| **45** | 2,340 | 945.4 KB | ~461 | 567x567 Bitmap (24-bit) | Low-Fi Mono | ~65.9 sec | 
| **50** | 2,600 | 1.05 MB | ~512 | 597x597 Bitmap (24-bit) | Low-Fi Mono | ~73.3 sec | 
| **55** | 2,860 | 1.16 MB | ~564 | 626x626 Bitmap (24-bit) | Low-Fi Mono | ~80.6 sec | 
| **60** | 3,120 | 1.26 MB | ~615 | 653x653 Bitmap (24-bit) | Low-Fi Mono | ~87.9 sec | 
| **65** | 3,380 | 1.37 MB | ~667 | 678x678 Bitmap (24-bit) | Low-Fi Mono | ~95.2 sec | 
| **70** | 3,640 | 1.47 MB | ~718 | 702x702 Bitmap (24-bit) | Low-Fi Mono | ~102.5 sec | 
| **75** | 3,900 | 1.58 MB | ~770 | 725x725 Bitmap (24-bit) | Low-Fi Mono | ~109.8 sec | 
| **80** | 4,160 | 1.68 MB | ~820 | 748x748 Bitmap (24-bit) | Low-Fi Mono | ~117.2 sec | 
| **85** | 4,420 | 1.79 MB | ~872 | 770x770 Bitmap (24-bit) | Low-Fi Mono | ~124.5 sec | 
| **90** | 4,680 | 1.89 MB | ~923 | 791x791 Bitmap (24-bit) | Low-Fi Mono | ~131.8 sec | 
| **95** | 4,940 | 1.99 MB | ~975 | 812x812 Bitmap (24-bit) | Low-Fi Mono | ~139.1 sec | 
| **100**| 5,200 | 2.10 MB | ~1025 | 832x832 Bitmap (24-bit) | Low-Fi Mono | ~146.5 sec | 

---
#### **Implications and Insights**

This table clearly demonstrates the incredible potential of scaling up a collection.

* **Text & Code:** Even a single 52-card pack provides enough space for a substantial text document. A small collection of 5 packs could hold a lengthy short story or a significant codebase.

* **Sound:** Meaningful audio becomes viable very quickly. A collection of just 10 packs could hold a 15-second audio message—more than enough for a detailed blessing, a spoken poem, or a unique soundscape. A full minute of audio is achievable with just 40-45 packs.

* **Images (Bitmap):** The trade-off for the "slow reveal" experience is image resolution. A single pack can only hold a small icon (`84x84`). A respectable medium-sized image (`~600x600`) requires a substantial collection of 50 packs. Achieving a large, high-resolution image would require a very large collection, making it a true "grail" for dedicated collectors.

This model allows us to design series with a specific digital artifact in mind, creating a powerful incentive for collectors to complete a set to unlock the full, embedded digital asset.
```

