# HEALTHY COOKING READ ME

## Complete Line-by-Line Code Explanation

This document provides a detailed explanation of every line in the `healthy-cooking/index.html` file.

---

## Document Structure

### Line 1: `<!DOCTYPE html>`
- **Purpose:** Declares this as an HTML5 document
- **What it does:** Tells the browser to render the page using HTML5 standards

### Line 2: `<html lang="en">`
- **Purpose:** Opens the HTML document
- **`lang="en"`:** Specifies the document language is English (helps screen readers and search engines)

### Line 3: `<head>`
- **Purpose:** Opens the head section
- **What it contains:** Metadata, title, styles, and other information not directly displayed on the page

---

## Head Section (Meta Information)

### Line 4: `<meta charset="UTF-8">`
- **Purpose:** Sets character encoding to UTF-8
- **What it does:** Ensures proper display of special characters, symbols, and international text

### Line 5: `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
- **Purpose:** Makes the page responsive on mobile devices
- **`width=device-width`:** Sets viewport width to match device screen width
- **`initial-scale=1.0`:** Sets initial zoom level to 100%

### Line 6: `<meta name="description" content="...">`
- **Purpose:** Provides page description for search engines
- **What it does:** This text appears in search engine results below the page title

### Line 7: `<title>Healthy Cooking - High Protein, Low Calorie Meals</title>`
- **Purpose:** Sets the page title shown in browser tabs
- **What it does:** This text appears in bookmarks, search results, and the browser tab

### Line 8: `<style>`
- **Purpose:** Opens internal CSS styling section
- **What it contains:** All visual styling rules for the page

---

## CSS Styling Explanation

### Lines 9-13: Body Styling
```css
body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    margin: 0;
    padding: 0;
    background-image: url('../WHOLE FOODS.jpg');
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
}
```
- **`font-family: Arial, sans-serif`:** Sets default font (Arial, or generic sans-serif as fallback)
- **`line-height: 1.6`:** Sets spacing between lines (1.6 times font size for readability)
- **`margin: 0`:** Removes default browser margins
- **`padding: 0`:** Removes default browser padding
- **`background-image: url('../WHOLE FOODS.jpg')`:** Sets background image using downloaded whole foods photo
- **`background-size: cover`:** Scales image to cover entire viewport
- **`background-attachment: fixed`:** Keeps background fixed while scrolling (parallax effect)
- **`background-position: center`:** Centers the background image

### Lines 14-18: Header Styling
```css
header {
    background: #35424a;
    color: #ffffff;
    padding: 20px;
    text-align: center;
}
```
- **`background: #35424a`:** Dark blue-gray background color
- **`color: #ffffff`:** White text color
- **`padding: 20px`:** 20 pixels of space inside the header on all sides
- **`text-align: center`:** Centers all text horizontally

### Lines 19-23: Navigation Bar Styling
```css
nav {
    background: #35424a;
    color: #ffffff;
    padding: 10px;
    text-align: center;
}
```
- **Purpose:** Styles the navigation bar with same colors as header
- **`padding: 10px`:** Less padding than header for compact appearance

### Lines 24-28: Navigation Links Styling
```css
nav a {
    color: #ffffff;
    margin: 0 15px;
    text-decoration: none;
    font-weight: bold;
}
```
- **`color: #ffffff`:** White link text
- **`margin: 0 15px`:** 15px space on left and right of each link
- **`text-decoration: none`:** Removes default underline from links
- **`font-weight: bold`:** Makes link text bold

### Lines 29-31: Navigation Link Hover Effect
```css
nav a:hover {
    color: #e8491d;
}
```
- **`:hover`:** Pseudo-class that activates when mouse hovers over link
- **`color: #e8491d`:** Changes link color to orange on hover

### Lines 32-37: Main Content Area Styling
```css
main {
    max-width: 1200px;
    margin: 20px auto;
    padding: 20px;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(5px);
}
```
- **`max-width: 1200px`:** Limits content width to 1200px for readability
- **`margin: 20px auto`:** 20px top/bottom, auto left/right (centers the content)
- **`padding: 20px`:** 20px internal spacing
- **`background: rgba(255, 255, 255, 0.95)`:** Semi-transparent white background (95% opacity) allows background image to show through subtly
- **`backdrop-filter: blur(5px)`:** Applies blur effect to background image behind content for better readability

### Lines 38-42: Section Styling
```css
section {
    margin-bottom: 30px;
    padding: 20px;
    border-left: 4px solid #35424a;
}
section#about {
    background-image: url('../WHOLE FOODS 2.png');
    background-size: cover;
    background-position: center;
    padding: 30px;
    border-radius: 10px;
    color: #000;
    background-blend-mode: overlay;
    background-color: rgba(255, 255, 255, 0.85);
}
```
- **`margin-bottom: 30px`:** Space between sections
- **`padding: 20px`:** Internal spacing
- **`border-left: 4px solid #35424a`:** 4px dark blue-gray left border accent
- **`section#about`:** Specific styling for the about section only
- **`background-image: url('../WHOLE FOODS 2.png')`:** Sets WHOLE FOODS 2 image as background for about section
- **`background-size: cover`:** Scales image to cover section
- **`background-position: center`:** Centers the background
- **`padding: 30px`:** Extra padding for about section
- **`border-radius: 10px`:** Rounded corners
- **`background-blend-mode: overlay`:** Blends background image with color
- **`background-color: rgba(255, 255, 255, 0.85)`:** Semi-transparent white overlay for readability

### Lines 43-47: Article Styling
```css
article {
    margin-bottom: 20px;
    padding: 15px;
    background: #f9f9f9;
    border-radius: 5px;
}
```
- **`background: #f9f9f9`:** Very light gray background
- **`border-radius: 5px`:** Rounds corners by 5px
- **Purpose:** Creates card-like appearance for recipe entries

### Lines 48-52: Aside (Sidebar) Styling
```css
aside {
    background: #e8f5e9;
    padding: 20px;
    margin: 20px 0;
    border-radius: 5px;
}
```
- **`background: #e8f5e9`:** Light green background
- **`margin: 20px 0`:** 20px top and bottom margin
- **Purpose:** Highlights tip boxes with distinct color

### Lines 53-56: Figure Styling
```css
figure {
    margin: 20px 0;
    text-align: center;
}
```
- **Purpose:** Centers images and their captions
- **`margin: 20px 0`:** Adds vertical spacing

### Lines 57-61: Figure Caption Styling
```css
figcaption {
    font-style: italic;
    color: #666;
    margin-top: 10px;
}
```
- **`font-style: italic`:** Makes caption text italic
- **`color: #666`:** Medium gray color
- **`margin-top: 10px`:** Space above caption

### Lines 62-67: Footer Styling
```css
footer {
    background: #35424a;
    color: #ffffff;
    text-align: center;
    padding: 20px;
    margin-top: 40px;
}
```
- **Purpose:** Matches header styling
- **`margin-top: 40px`:** Extra space above footer

### Lines 68-70: Heading Color
```css
h1, h2, h3 {
    color: #35424a;
}
```
- **Purpose:** Sets all headings to dark blue-gray color for consistency

### Lines 71-76: Recipe Card Styling
```css
.recipe-card {
    background: #fff;
    padding: 15px;
    margin: 10px 0;
    border: 1px solid #ddd;
    border-radius: 5px;
}
```
- **`.recipe-card`:** Class selector (applies to elements with class="recipe-card")
- **`border: 1px solid #ddd`:** Light gray border
- **Purpose:** Creates distinct boxes for each recipe

### Lines 77-82: Nutrition Info Box Styling
```css
.nutrition-info {
    background: #e3f2fd;
    padding: 10px;
    margin: 10px 0;
    border-radius: 5px;
}
```
- **`.nutrition-info`:** Class selector
- **`background: #e3f2fd`:** Light blue background
- **Purpose:** Highlights nutritional benefits

### Line 83: `</style>`
- **Purpose:** Closes the style section

### Line 84: `</head>`
- **Purpose:** Closes the head section

---

## Body Section (Visible Content)

### Line 85: `<body>`
- **Purpose:** Opens the body section containing all visible page content

---

## Header Element

### Line 86: `<header>`
- **Purpose:** Semantic HTML5 element representing page header
- **Contains:** Main title and tagline

### Line 87: `<h1>🍳 Healthy Cooking Journey</h1>`
- **`<h1>`:** Heading level 1 (main page title)
- **Purpose:** Most important heading on the page
- **🍳:** Emoji for visual appeal

### Line 88: `<p>High Protein, Low Fat, Whole Foods - Creatively Prepared for Your Health Goals</p>`
- **`<p>`:** Paragraph element
- **Purpose:** Subtitle/tagline explaining the page focus

### Line 89: `</header>`
- **Purpose:** Closes the header element

---

## Navigation Element

### Line 91: `<nav>`
- **Purpose:** Semantic HTML5 element for navigation links
- **What it does:** Groups navigation links together

### Lines 92-97: Navigation Links
```html
<a href="#about">About</a>
<a href="#techniques">Cooking Techniques</a>
<a href="#recipes">Recipes</a>
<a href="#tips">Tips & Benefits</a>
<a href="#contact">Contact</a>
```
- **`<a>`:** Anchor (link) element
- **`href="#about"`:** Links to element with id="about" on same page
- **#:** Indicates internal page anchor
- **Purpose:** Creates clickable navigation menu that jumps to page sections

### Line 98: `</nav>`
- **Purpose:** Closes the navigation element

---

## Main Content Element

### Line 100: `<main>`
- **Purpose:** Semantic HTML5 element for main page content
- **What it means:** Contains the primary content of the page

---

## About Section

### Line 101: `<section id="about">`
- **`<section>`:** Semantic HTML5 element for thematic grouping of content
- **`id="about"`:** Unique identifier (used for navigation anchor and CSS targeting)

### Line 102: `<h2>My Cooking Philosophy</h2>`
- **`<h2>`:** Heading level 2 (section title)
- **Purpose:** Second-level heading hierarchy

### Line 103: `<p>Welcome to my healthy cooking showcase!...</p>`
- **Purpose:** Introductory paragraph explaining the page focus

### Lines 104-110: Unordered List
```html
<ul>
    <li><strong>High Protein:</strong> Building and maintaining muscle...</li>
    <li><strong>Low Fat:</strong> Minimizing unnecessary fats...</li>
    ...
</ul>
```
- **`<ul>`:** Unordered list (bullet points)
- **`<li>`:** List item
- **`<strong>`:** Bold text (semantic emphasis for importance)
- **Purpose:** Lists key cooking principles

### Lines 112-114: Figure Element
```html
<figure>
    <img src="../WHOLE FOODS.jpg" alt="Fresh whole foods including vegetables, lean proteins, and grains" width="600" height="400">
    <figcaption>Fresh whole foods - the foundation of healthy cooking</figcaption>
</figure>
```
- **`<figure>`:** Semantic container for images with captions
- **`<img>`:** Image element
- **`src="../WHOLE FOODS.jpg"`:** Relative path to actual downloaded image in parent directory (Task names folder)
- **`alt="..."`:** Alternative text for screen readers and if image fails to load
- **`width` and `height`:** Image dimensions in pixels
- **`<figcaption>`:** Caption describing the image
- **Note:** `../` navigates up one directory from healthy-cooking/ to Task names/

### Line 116: `</section>`
- **Purpose:** Closes the about section

---

## Cooking Techniques Section

### Line 118: `<section id="techniques">`
- **Purpose:** Section about cooking methods

### Line 119: `<h2>Creative Cooking Techniques</h2>`
- **Purpose:** Section heading

### Line 120: `<p>I utilize various cooking methods...</p>`
- **Purpose:** Introductory text for the section

### Lines 122-129: Article Element (Grilling)
```html
<article>
    <h3>🔥 Grilling & Broiling</h3>
    <p>Perfect for achieving caramelization...</p>
    <div class="nutrition-info">
        <strong>Benefits:</strong> Excess fat drips away...
    </div>
</article>
```
- **`<article>`:** Semantic element for self-contained content
- **`<h3>`:** Heading level 3 (sub-section title)
- **`<div class="nutrition-info">`:** Division with nutrition-info class (styled with light blue background)
- **Purpose:** Each article describes one cooking technique

### Lines 131-138: Article Element (Air Frying)
- **Same structure as grilling article**
- **Purpose:** Explains air frying technique

### Lines 140-147: Article Element (Baking & Roasting)
- **Same structure**
- **Purpose:** Explains baking/roasting technique

### Lines 149-156: Article Element (Steaming & Poaching)
- **Same structure**
- **Purpose:** Explains steaming/poaching technique

### Line 157: `</section>`
- **Purpose:** Closes the techniques section

---

## Aside Element (Tip Box)

### Lines 159-162: Aside Element
```html
<aside>
    <h3>💡 Quick Tip</h3>
    <p>Season your proteins with herbs...</p>
</aside>
```
- **`<aside>`:** Semantic element for tangentially related content
- **Purpose:** Highlights a helpful tip separate from main content flow
- **Visual:** Green background box

---

## Recipes Section

### Line 164: `<section id="recipes">`
- **Purpose:** Main recipes section

### Line 165: `<h2>My Favorite Healthy Meals</h2>`
- **Purpose:** Section heading

### Lines 167-185: Recipe Card - Tropical Muesli
```html
<article class="recipe-card">
    <figure style="margin: 0 0 15px 0;">
        <img src="../TROPICAL MUESLI.webp" alt="Tropical muesli with nuts and yogurt" width="100%" style="border-radius: 5px; max-height: 300px; object-fit: cover;">
    </figure>
    <h3>🥣 Tropical Muesli Power Bowl</h3>
    <p><strong>Prep Time:</strong> 5 minutes | <strong>Meal Type:</strong> Breakfast</p>
    <p><strong>Ingredients:</strong></p>
    <ul>
        <li>Tropical muesli</li>
        <li>Crushed pecans</li>
        ...
    </ul>
    <p><strong>Method:</strong> Combine muesli in a bowl...</p>
    <div class="nutrition-info">
        <strong>Benefits:</strong> High in protein...
    </div>
</article>
```
- **`<figure style="...">`:** Inline-styled figure with no bottom margin except 15px
- **`<img src="../TROPICAL MUESLI.webp">`:** Actual downloaded image of tropical muesli
- **`width="100%"`:** Makes image full width of container
- **`border-radius: 5px`:** Rounded corners matching recipe card
- **`max-height: 300px`:** Limits image height
- **`object-fit: cover`:** Crops image to fit while maintaining aspect ratio
- **`class="recipe-card"`:** Applies recipe card styling
- **Purpose:** Complete recipe with actual food photo, ingredients, method, and benefits

### Lines 187-204: Recipe Card - Fried Eggs with Sardines
- **Same structure as previous recipe**
- **Purpose:** Second recipe

### Lines 206-232: Recipe Card - Baked Protein & Carb Combo
```html
<article class="recipe-card">
    <figure style="margin: 0 0 15px 0;">
        <img src="../BAKED CHICKEN BREAST.webp" alt="Baked chicken breast with vegetables" width="100%" style="border-radius: 5px; max-height: 300px; object-fit: cover;">
    </figure>
    <h3>🍗 Baked Protein & Carb Combo</h3>
    <p><strong>Prep Time:</strong> 10 minutes | <strong>Cook Time:</strong> 50-60 minutes | <strong>Meal Type:</strong> Main Meal</p>
    ...
    <p><strong>Spice Blend:</strong></p>
    <ul>
        <li>Garlic</li>
        <li>Paprika</li>
        <li>Black pepper</li>
        <li>Six Gun Grill Spice</li>
        <li>Rosemary</li>
        <li>Ginger</li>
    </ul>
    <p><strong>Method:</strong> Season protein of choice with spice blend. Bake in oven at 190°C for 35-45 minutes without oil for less fatty food, then grill for 10-15 minutes at 190°C for perfect texture and color...</p>
    <p><strong>💡 Tip:</strong> When baking in an oven, try not using oil for less fatty food - the spices provide plenty of flavor!</p>
</article>
```
- **`<img src="../BAKED CHICKEN BREAST.webp">`:** Actual downloaded image of baked chicken breast
- **Cook Time:** 50-60 minutes total (baking + grilling)
- **Spice Blend:** Custom blend of garlic, paprika, black pepper, Six Gun Grill Spice, rosemary, and ginger
- **Method:** Two-stage cooking process - bake without oil first, then grill to finish
- **Oil-free cooking:** Emphasized in method and additional tip for reduced fat content
- **Temperature:** 190°C (approximately 374°F) for both baking and grilling
- **Extended recipe with multiple options**
- **Contains:** Three separate ingredient lists (carbs, proteins, and spices), plus actual food photo and detailed cooking instructions
- **Purpose:** Customizable main meal recipe with precise cooking method, custom spice blend, and visual representation

### Lines 234-245: Recipe Card - Dark Chocolate Snack
```html
<article class="recipe-card">
    <h3>🍫 Dark Chocolate Snack</h3>
    <p><strong>Prep Time:</strong> 0 minutes | <strong>Meal Type:</strong> Snack</p>
    <p><strong>Serving:</strong> One block per day</p>
    <p><strong>Ingredients:</strong></p>
    <ul>
        <li>100% dark chocolate</li>
    </ul>
    <p><strong>Method:</strong> Enjoy one block as a daily healthy snack between meals</p>
    <p><strong>⚠️ Important:</strong> Consult with a doctor before consuming 100% dark chocolate regularly, especially if you have any health conditions</p>
    <div class="nutrition-info">
        <strong>Benefits:</strong> Rich in antioxidants, no added sugar, satisfies sweet cravings, contains beneficial minerals like magnesium and iron, assists with cognitive function and brain health
    </div>
</article>
```
- **Serving size:** One block per day
- **Method:** Updated to reflect daily consumption of one block
- **Medical disclaimer:** Added warning paragraph to consult doctor before regular consumption
- **`⚠️`:** Warning emoji for visual emphasis on important health information
- **Benefits updated:** Now includes cognitive function and brain health benefits
- **Purpose:** Simplified snack with important health considerations

### Lines 247-249: Figure with Image
```html
<figure>
    <img src="../BAKED CHICKEN BREAST AND POTATO PLATE.webp" alt="My go-to meal - baked chicken breast with potato on a plate" width="600" height="400">
    <figcaption>My go-to main meal: baked chicken breast with potato - simple, nutritious, and delicious</figcaption>
</figure>
```
- **`<img src="../BAKED CHICKEN BREAST AND POTATO PLATE.webp">`:** Actual downloaded image showing complete plated meal
- **Purpose:** Visual representation of go-to main meal combining protein and carbohydrate
- **Located:** At end of recipes section

### Line 250: `</section>`
- **Purpose:** Closes recipes section

---

## Tips & Benefits Section

### Line 252: `<section id="tips">`
- **Purpose:** Section for helpful information

### Line 253: `<h2>Tips & Health Benefits</h2>`
- **Purpose:** Section heading

### Lines 255-263: Article - Meal Prep Strategies
```html
<article>
    <h3>🎯 Meal Prep Strategies</h3>
    <ul>
        <li>Batch-cook proteins on Sunday...</li>
        <li>Pre-cut vegetables for quick assembly...</li>
        ...
    </ul>
</article>
```
- **Purpose:** Practical meal prep advice in list format

### Lines 265-276: Article - Benefits
- **Purpose:** Lists health benefits of this cooking style
- **Structure:** Unordered list with `<strong>` titles

### Lines 278-287: Article - Essential Tools
```html
<article>
    <h3>🔪 Essential Kitchen Tools</h3>
    <ul>
        <li>Cooking stove with an oven for baking and grilling</li>
        <li>Air fryer for crispy, low-fat results</li>
        <li>Grill pan or outdoor grill for char and flavor</li>
        <li>Quality non-stick bakeware</li>
        <li>Instant-read thermometer for perfect protein cooking</li>
        <li>Spice grinder for fresh seasonings</li>
    </ul>
</article>
```
- **Purpose:** Lists recommended kitchen equipment
- **Structure:** Simple unordered list
- **Key tool added:** Cooking stove with an oven - essential for the baking and grilling method used in main recipes

### Line 288: `</section>`
- **Purpose:** Closes tips section

---

## Second Aside Element

### Lines 290-293: Aside - Did You Know
```html
<aside>
    <h3>📊 Did You Know?</h3>
    <p>Cooking methods matter!...</p>
</aside>
```
- **Purpose:** Interesting fact highlighting benefit of healthy cooking
- **Visual:** Green background box

---

## Contact Section

### Line 295: `<section id="contact">`
- **Purpose:** Contact information section

### Line 296: `<h2>Connect & Share</h2>`
- **Purpose:** Section heading

### Line 297: `<p>I love connecting with fellow health-conscious...</p>`
- **Purpose:** Inviting message

### Lines 298-303: Address Element
```html
<address>
    <p><strong>Email:</strong> <a href="mailto:pfarelochannel@gmail.com">pfarelochannel@gmail.com</a></p>
    <p><strong>Instagram:</strong> @healthy_cooking_journey</p>
    <p><strong>Location:</strong> CNR Malibongwe and Northumberland Roodepoort 2118</p>
</address>
```
- **`<address>`:** Semantic element for contact information
- **`href="mailto:pfarelochannel@gmail.com"`:** Creates clickable email link that opens email client with actual email address
- **Email:** pfarelochannel@gmail.com - actual contact email
- **Location:** CNR Malibongwe and Northumberland Roodepoort 2118 - actual physical address
- **Purpose:** Provides multiple ways to connect with real contact information

### Line 304: `</section>`
- **Purpose:** Closes contact section

### Line 305: `</main>`
- **Purpose:** Closes main content area

---

## Footer Element

### Lines 307-311: Footer
```html
<footer>
    <p>&copy; 2025 Healthy Cooking Journey | All Rights Reserved</p>
    <p>Dedicated to promoting nutritious, delicious, and creative whole food cooking</p>
    <p><small>Disclaimer: Nutritional information is approximate. A doctor should be consulted prior to beginning this diet. Consult with a healthcare provider for personalized dietary advice.</small></p>
</footer>
```
- **`<footer>`:** Semantic element for page footer
- **`&copy;`:** HTML entity for copyright symbol (©)
- **`<small>`:** Semantic element for fine print/smaller text
- **Disclaimer updated:** Now emphasizes consulting a doctor before beginning the diet, in addition to general healthcare advice
- **Purpose:** Copyright, description, and legal/medical disclaimer
```
- **`<footer>`:** Semantic element for page footer
- **`&copy;`:** HTML entity for copyright symbol (©)
- **`<small>`:** Semantic element for fine print/smaller text
- **Purpose:** Copyright, description, and legal disclaimer

### Line 312: `</body>`
- **Purpose:** Closes body section

### Line 313: `</html>`
- **Purpose:** Closes HTML document

---

## Summary of Semantic HTML Elements Used

### Required Elements (5):
1. **`<header>`** - Page header with title
2. **`<nav>`** - Navigation menu
3. **`<main>`** - Main content container
4. **`<section>`** - Thematic content sections (5 total: about, techniques, recipes, tips, contact)
5. **`<footer>`** - Page footer

### Additional HTML5 Elements (7):
6. **`<article>`** - Self-contained content (recipes, techniques, tips)
7. **`<aside>`** - Tangentially related content (tip boxes)
8. **`<figure>`** - Images with captions
9. **`<figcaption>`** - Image captions
10. **`<address>`** - Contact information
11. **`<strong>`** - Important text (semantic emphasis)
12. **`<small>`** - Fine print text

---

## Key HTML Concepts Demonstrated

### 1. **Semantic HTML**
- Uses meaningful element names that describe content purpose
- Improves accessibility, SEO, and code maintainability

### 2. **Document Structure**
- Proper hierarchy: `<html>` → `<head>` + `<body>`
- Logical content organization with semantic elements

### 3. **Accessibility Features**
- `alt` attributes on images
- Semantic elements for screen readers
- `lang` attribute for language specification

### 4. **Internal Navigation**
- `id` attributes create anchors
- `href="#id"` links jump to specific sections

### 5. **CSS Classes**
- `.recipe-card` and `.nutrition-info` apply consistent styling
- Separates content from presentation

### 6. **Responsive Design**
- Viewport meta tag for mobile compatibility
- Max-width on main content for readability

---

## File Location
**Path:** `c:\Users\pfare\OneDrive\Documentos\ACADEMICS\SORTWARE ENGINEERING\Task names\healthy-cooking\index.html`

---

## How to Use This Page
1. Navigate to the healthy-cooking folder
2. Double-click `index.html` to open in your default browser
3. Click navigation links to jump between sections
4. The page uses actual food photos from the Task names folder
5. Images are loaded using relative paths (../ goes up to parent directory)

## Images Used
- **WHOLE FOODS.jpg** - Body background (fixed parallax effect)
- **WHOLE FOODS 2.png** - About section background
- **TROPICAL MUESLI.webp** - Tropical muesli recipe image
- **BAKED CHICKEN BREAST.webp** - Baked protein recipe image
- **BAKED CHICKEN BREAST AND POTATO PLATE.webp** - Go-to main meal image (complete plated meal)

**Note:** All images must remain in the Task names folder for proper display

---

**Created:** December 20, 2025  
**Purpose:** Educational project demonstrating semantic HTML5 for a hobby showcase webpage
