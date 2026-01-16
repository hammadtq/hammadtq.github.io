# Image Setup Guide

## Required Images for SEO & Social Sharing

### 1. og-default.png (REQUIRED)
- **Size**: 1200x630 pixels (optimal for social sharing)
- **Purpose**: Default Open Graph image for social media sharing
- **Design suggestions**:
  - Include your name "Hammad Tariq"
  - Add tagline: "AI, Web3 & Infrastructure"
  - Use a professional color scheme
  - Keep text minimal and readable at small sizes

### 2. default-teaser.png (REQUIRED)
- **Size**: 500x300 pixels
- **Purpose**: Fallback teaser image for blog posts without images

### 3. bio-photo.jpg (RECOMMENDED)
- **Size**: 300x300 pixels (square)
- **Purpose**: Author profile photo in sidebar

### 4. Favicons (RECOMMENDED)
Generate at: https://realfavicongenerator.net/

Required files:
- apple-touch-icon.png (180x180)
- favicon-32x32.png (32x32)
- favicon-16x16.png (16x16)
- favicon.ico

## Quick Generation Options

### Option A: Use Canva (Free)
1. Go to canva.com
2. Create design with dimensions 1200x630
3. Use a template or create custom
4. Download as PNG

### Option B: Use DALL-E/Midjourney
Prompt: "Professional blog header image for a tech founder's blog about AI and Web3, minimal design, blue and dark theme, with subtle circuit patterns, 1200x630"

### Option C: Simple Text-Based Image
Use any image editor to create a solid color background with:
- Your name in large text
- Tagline below
- Simple geometric accents

## After Creating Images

1. Place og-default.png in this directory
2. Place default-teaser.png in this directory
3. Place bio-photo.jpg in this directory
4. Rebuild the Jekyll site: `bundle exec jekyll build`
5. Verify at: https://www.opengraph.xyz/
