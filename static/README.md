# Static Assets Directory

This directory contains static assets for the Task Master Todo App.

## Structure

- **css/** - Contains CSS stylesheets
  - `custom.css` - Custom styles for the application

- **js/** - Contains JavaScript files
  - `app.js` - Main application JavaScript with UI enhancements

- **images/** - Contains images used in the application
  - Add images such as logos, icons, etc. here

## Usage

When deploying to production, consider:

1. Minifying CSS and JavaScript files
2. Optimizing images
3. Setting up proper cache headers
4. Using a CDN for better performance

In Flask, these files are automatically served from the `/static` URL path.

Example usage in templates:
```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/custom.css') }}">
<script src="{{ url_for('static', filename='js/app.js') }}"></script>
<img src="{{ url_for('static', filename='images/logo.png') }}">
``` 