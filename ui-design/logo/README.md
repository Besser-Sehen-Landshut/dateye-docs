# DATEYE Logo System

Complete logo system for the DATEYE medical device integration platform.

## File Structure

```
logo/
├── README.md           # This file
├── logo-showcase.html  # Visual preview of all logo variants
├── dateye-main.svg     # Main logo (6642×2800 ViewBox)
├── dateye-icon.svg     # App icon (256×256)
├── dateye-tray.svg     # System tray icon (16×16)
├── dateye-loading.svg  # Animated logo for loading screens
├── dateye-about.svg    # About dialog with tagline
└── dateye-favicon.svg  # Browser favicon (32×32)
```

## Logo Design

### Brand Identity
The DATEYE logo consists of two typographic elements:
- **"DAT"**: Gray with 69% Opacity (`fill-opacity:0.69`)
- **"EYE"**: Light blue (`#0087ba`)

### Typography
- Geometric sans-serif font
- Bold stroke weight
- Tight letter spacing
- No gap between "DAT" and "EYE"

### Logo Construction
- ViewBox: 0 0 6642 2800 (aspect ratio 2.37:1)
- Transparent background
- Pure typography without container
- Scalable vector graphic

## Color Specification

```css
/* Primary colors */
--dateye-dat-gray: rgba(0, 0, 0, 0.69);  /* DAT text */
--dateye-eye-blue: #0087ba;              /* EYE text */

/* Semantic colors (from app) */
--dateye-primary: #0087ba;               /* Primary color */
--dateye-active: #16A34A;                /* Active/Success */
--dateye-export: #EA580C;                /* Export/Orange */
--dateye-error: #DC2626;                 /* Error */
```

## Usage Guidelines

### Minimum Clear Space
Minimum distance around the logo equals the height of the "E" letter.

### Minimum Sizes
- Main logo: 120px width
- App icon: 32×32px (recommended: 256×256px)
- System tray: 16×16px (monochrome)
- Favicon: 16×16px (recommended: 32×32px)

### Background Compatibility
- Transparent - works on all backgrounds
- Optimal visibility on light to medium backgrounds
- On dark backgrounds: increase DAT opacity to 100%

### Prohibited Uses
- Do not change colors
- Do not distort proportions
- Do not add effects (shadows, gradients)
- Do not modify letter forms
- Do not place on backgrounds that impair readability

## Implementation

### HTML Integration
```html
<!-- Inline SVG with responsive size -->
<img src="logo/dateye-main.svg" alt="DATEYE Logo" style="width: 200px; height: auto;">

<!-- As favicon -->
<link rel="icon" type="image/svg+xml" href="logo/dateye-favicon.svg">
```

### Flutter Integration
```dart
// App icon
SvgPicture.asset(
  'assets/logo/dateye-main.svg',
  width: 200,
  fit: BoxFit.contain,
),

// System tray (monochrome variant)
SystemTray.setIcon('assets/logo/dateye-tray.svg'),
```

### CSS Integration
```css
.dateye-logo {
  background: url('dateye-main.svg') no-repeat center;
  background-size: contain;
  width: 200px;
  height: 84px; /* Maintain 2.37:1 aspect ratio */
}
```

## Logo Variants

### Main Logo (`dateye-main.svg`)
- **Usage**: Marketing, documentation, UI headers
- **Format**: Complete "DATEYE" text
- **Optimizations**: Fully readable from 120px width

### App Icon (`dateye-icon.svg`)
- **Usage**: Desktop icon, About dialogs
- **Format**: Square, simplified representation
- **Optimizations**: Recognizable from 32×32px

### System Tray (`dateye-tray.svg`)
- **Usage**: Windows/macOS/Linux system tray
- **Format**: Monochrome, maximally simplified
- **Optimizations**: Readable at 16×16px

### Favicon (`dateye-favicon.svg`)
- **Usage**: Browser tabs, bookmarks
- **Format**: High contrast for minimal sizes
- **Optimizations**: Recognizable at 16×16px

### Loading Animation (`dateye-loading.svg`)
- **Usage**: Splash screens, loading states
- **Format**: Animated, 1.0 second duration
- **Animation**: "DAT" fade-in (0-0.8s), "EYE" slide-in (0.4-1.0s)

### About Dialog (`dateye-about.svg`)
- **Usage**: Info dialogs with tagline
- **Format**: Logo + "Medical Device Integration Platform"
- **Layout**: Vertically stacked or horizontal

## Adaptive Display

### Responsive Strategies

| Screen Width | Logo Variant | Implementation |
|--------------|--------------|----------------|
| > 1200px | Full logo + tagline | `dateye-about.svg` |
| 800-1200px | Full logo | `dateye-main.svg` |
| 400-800px | Compact logo | `dateye-icon.svg` |
| < 400px | Icon only | `dateye-favicon.svg` |

### Size Recommendations

| Context | Width | Height | File |
|---------|-------|--------|------|
| Header (Desktop) | 180-220px | auto | `dateye-main.svg` |
| Header (Tablet) | 140-180px | auto | `dateye-main.svg` |
| Header (Mobile) | 100-140px | auto | `dateye-main.svg` |
| App Icon | 64-256px | 64-256px | `dateye-icon.svg` |
| Favicon | 16-32px | 16-32px | `dateye-favicon.svg` |

## Technical Specifications

### SVG Optimization
All logo files are optimized for performance:
- Minimal SVG syntax
- No unnecessary groups or transformations
- Optimized path definitions
- Embedded font avoidance (outline paths)

### Color Space and Export
- Color space: sRGB
- Alpha transparency: Supported
- Vector format: Infinitely scalable
- Browser compatibility: All modern browsers

### Accessibility
- Sufficient contrast (WCAG AA compliant)
- Alternative text descriptions provided
- Scalable for visual impairments
- Monochrome fallback option available

## Quality Control

### Pre-Implementation Checklist
- [ ] Logo is readable at target size
- [ ] Colors match specifications
- [ ] Transparency works on all backgrounds
- [ ] SVG code is optimized and valid
- [ ] Alternative text is meaningful
- [ ] Browser tests performed

### Performance Criteria
- SVG file size < 5KB for main logo
- SVG file size < 2KB for icons
- Load time < 100ms on standard connection
- Render time < 16ms for 60fps animations

## License and Usage Rights

The DATEYE logo is copyrighted. Use only with express permission.

© 2024 DATEYE - All rights reserved.

## Technical Support

For questions about logo implementation or customization:
- Documentation: `/docs/ui-design/`
- Design System: `/docs/ui-design/design-system.md`
- Code Examples: `/repository/lib/presentation/widgets/`
