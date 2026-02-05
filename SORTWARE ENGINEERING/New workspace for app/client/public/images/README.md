# Images Directory

This directory contains all images for the food ordering application.

## Directory Structure

- `/logos/` - Company and restaurant logos
- `/menu/` - Menu item images

## Required Images

### Producer Logo
- **File**: `logos/producer-logo.png`
- **Recommended size**: 150x150 pixels (square)
- **Format**: PNG with transparent background
- **Usage**: Splash screen branding

### Buroko's Kitchen Logo
- **File**: `logos/burokos-kitchen-logo.png`
- **Recommended size**: 200x200 pixels (square)
- **Format**: PNG with transparent background
- **Usage**: Restaurant vendor card on landing page

### Menu Images (for Buroko's Kitchen)
Place menu item images in the `/menu/` directory with descriptive names:
- `menu/burger-classic.jpg`
- `menu/pizza-margherita.jpg`
- `menu/chicken-wings.jpg`
- etc.

## Image Guidelines

- **Logo files**: Use PNG format with transparent backgrounds
- **Menu images**: Use JPG format, minimum 300x300 pixels
- **File naming**: Use lowercase with hyphens (kebab-case)
- **File size**: Keep under 500KB for optimal loading

## Adding Images

1. Place your images in the appropriate subdirectory
2. Update the component files to reference the correct image paths
3. Test that images load correctly with fallback emoji support

## Fallback Behavior

If an image fails to load, the application will automatically show:
- Emoji icons for logos
- Placeholder content for missing images
