# Dataset Strategy

## AI Food Freshness Checker

---

## 1. Categories and Labels

### Food Categories (8)
| # | Category | Varieties to Include |
|---|----------|---------------------|
| 1 | Apple | Red, Green, Yellow |
| 2 | Banana | Cavendish (yellow) |
| 3 | Tomato | Red, Roma, Cherry |
| 4 | Potato | White, Russet, Red |
| 5 | Orange | Navel, Valencia |
| 6 | Carrot | Standard orange |
| 7 | Cucumber | Standard green |
| 8 | Strawberry | Standard red |

### Freshness Labels (3)
| Label | Visual Characteristics |
|-------|----------------------|
| **Fresh** | Vibrant color, firm texture, no blemishes, natural sheen |
| **Aging** | Slight discoloration, minor soft spots, light wrinkling, dulled color |
| **High Visible Spoilage Risk** | Significant discoloration, mold, heavy wrinkling, dark spots, mushiness |

### Total Classes
8 foods × 3 freshness states = **24 classes** + 1 "not food/unsupported" = **25 classes**

---

## 2. Dataset Sources

### Primary Sources (License-Verified)

| Source | Description | License | Status |
|--------|------------|---------|--------|
| Kaggle "Fruits Fresh and Rotten" | Fresh/rotten fruits and vegetables | CC0 / Public Domain | ✅ Verified |
| Kaggle "Fruit and Vegetable Image Recognition" | 36 categories of produce | CC BY-SA 4.0 | ✅ Verified |
| Custom collection | Manually photographed and labeled | Owned | ✅ Active |

> **RULE**: Do NOT use any dataset without first verifying its license permits commercial/project use.

### Supplementary Sources
- Web scraping (with license compliance)
- Synthetic data augmentation
- Community contributions (future)

---

## 3. Data Collection Requirements

### Image Quality Standards
- Minimum resolution: 224×224 pixels (model input size)
- Preferred resolution: 512×512+ for quality
- Format: JPEG or PNG
- Single food item per image (primary)
- Varied backgrounds (white, kitchen, natural)
- Varied lighting (natural, artificial, mixed)
- Varied angles (top-down, 45°, side)

### Per-Class Target
| Phase | Images per Class | Total Dataset |
|-------|-----------------|--------------|
| Baseline (MVP) | 100–200 | 2,500–5,000 |
| Production v1 | 500–1,000 | 12,500–25,000 |
| Mature | 1,000+ | 25,000+ |

---

## 4. Data Split

| Split | Percentage | Purpose |
|-------|-----------|---------|
| Training | 70% | Model training |
| Validation | 15% | Hyperparameter tuning |
| Test | 15% | Final evaluation (never seen during training) |

- Stratified split to maintain class balance across splits
- No data leakage between splits (same food item in only one split)

---

## 5. Data Augmentation

### Training-Time Augmentations
| Augmentation | Range | Purpose |
|-------------|-------|---------|
| Random rotation | ±30° | Orientation invariance |
| Horizontal flip | 50% chance | Left-right invariance |
| Brightness adjustment | ±20% | Lighting invariance |
| Contrast adjustment | ±20% | Camera quality invariance |
| Zoom/crop | 80–120% | Scale invariance |
| Gaussian noise | σ=0.01 | Noise robustness |
| Color jitter | ±10% HSV | Color variation |

### NOT Applied
- Vertical flip (food has natural orientation)
- Extreme distortion (unrealistic)
- Cutout/Cutmix (may remove key spoilage indicators)

---

## 6. Class Balance

- Monitor class distribution during collection
- Target roughly equal samples per class
- Use oversampling (augmentation) for underrepresented classes
- Use class weights during training if imbalance persists
- **Priority**: Ensure HIGH VISIBLE SPOILAGE RISK class has sufficient samples

---

## 7. Bias Risks

| Risk | Mitigation |
|------|-----------|
| Lighting bias (mostly studio photos) | Include natural, kitchen, low-light images |
| Background bias (white backgrounds) | Vary backgrounds in collection |
| Variety bias (single apple variety) | Include multiple varieties per food |
| Geographic bias (single region's produce) | Document limitation; expand over time |
| Severity boundary bias (aging vs. spoiled) | Clear labeling guidelines with examples |

---

## 8. Labeling Methodology

### Labeling Guidelines
1. Each image is labeled by category (food type) AND freshness (3 classes)
2. When in doubt between AGING and HIGH VISIBLE SPOILAGE RISK → label as SPOILAGE (err toward caution)
3. When in doubt between FRESH and AGING → label as AGING (err toward caution)
4. Provide reference images for each class boundary

### Quality Assurance
- Cross-validation: minimum 2 labelers per image (future)
- Inter-rater agreement tracking (future)
- Regular labeling guideline reviews

---

## 9. Duplicate Detection

- Perceptual hashing (pHash) to detect near-duplicate images
- Remove exact duplicates
- Flag near-duplicates for manual review
- Ensure no duplicate appears across train/validation/test splits
