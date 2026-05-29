from django import forms
from django.utils.safestring import mark_safe
import json


# Predefined curated palette for Dar Safeera
BRAND_COLORS = [
    {"name": "Midnight Black",  "hex": "#0a0a0a"},
    {"name": "Charcoal",        "hex": "#2c2c2c"},
    {"name": "Warm White",      "hex": "#faf8f5"},
    {"name": "Ivory Cream",     "hex": "#f5f0e8"},
    {"name": "Blush Rose",      "hex": "#e8c5b5"},
    {"name": "Dusty Mauve",     "hex": "#c4a0a0"},
    {"name": "Warm Gold",       "hex": "#c9a96e"},
    {"name": "Champagne",       "hex": "#f7e7ce"},
    {"name": "Forest Green",    "hex": "#2d5a3d"},
    {"name": "Sage",            "hex": "#7a9e7e"},
    {"name": "Midnight Navy",   "hex": "#1a2744"},
    {"name": "Slate Blue",      "hex": "#4a6fa5"},
    {"name": "Bordeaux",        "hex": "#6b2737"},
    {"name": "Dusty Rose",      "hex": "#d4a0a0"},
    {"name": "Camel",           "hex": "#c19a6b"},
    {"name": "Sand",            "hex": "#d2b48c"},
    {"name": "Mocha",           "hex": "#6f4e37"},
    {"name": "Pearl Grey",      "hex": "#d8d0c8"},
    {"name": "Lavender Mist",   "hex": "#c5b8d4"},
    {"name": "Deep Plum",       "hex": "#4a1942"},
]


class ColorPickerWidget(forms.Widget):
    """
    A multi-select color swatch widget that outputs a comma-separated
    list of selected color names into a hidden input.
    """

    def __init__(self, attrs=None):
        super().__init__(attrs)

    class Media:
        css = {
            "all": ("css/color_picker.css",)
        }
        js = ("js/color_picker.js",)

    def render(self, name, value, attrs=None, renderer=None):
        widget_id = attrs.get("id", f"id_{name}") if attrs else f"id_{name}"
        colors_json = json.dumps(BRAND_COLORS)

        # Current value is a comma-separated string of color names
        current_value = value or ""

        html = f"""
<div class="ds-color-picker" id="cp_{widget_id}" data-field="{widget_id}">
  <div class="ds-color-picker__swatches" role="group" aria-label="Select colors">
    {self._render_swatches(current_value)}
  </div>
  <div class="ds-color-picker__custom">
    <label class="ds-color-picker__custom-label">
      <input type="color" class="ds-color-picker__custom-input" id="cp_custom_{widget_id}" value="#c9a96e" />
      <span>Add Custom Color</span>
    </label>
    <button type="button" class="ds-color-picker__add-btn" onclick="dsAddCustomColor('cp_{widget_id}', 'cp_custom_{widget_id}')">
      + Add
    </button>
  </div>
  <div class="ds-color-picker__selected-label">Selected: <span class="ds-color-picker__count">0</span></div>
</div>
<input type="hidden" name="{name}" id="{widget_id}" value="{current_value}" class="ds-color-hidden" />
<script>
  document.addEventListener('DOMContentLoaded', function() {{
    dsColorPickerInit('cp_{widget_id}', '{widget_id}', {colors_json});
  }});
</script>
"""
        return mark_safe(html)

    def _render_swatches(self, current_value):
        selected_names = [c.strip() for c in current_value.split(",") if c.strip()]
        swatches = []
        standard_names = {color["name"].lower() for color in BRAND_COLORS}
        
        # 1. Render standard swatches
        for color in BRAND_COLORS:
            is_selected = any(color["name"].lower() == s.lower() for s in selected_names)
            sel_class = " ds-swatch--selected" if is_selected else ""
            swatches.append(
                f'<button type="button" class="ds-swatch{sel_class}" '
                f'style="background:{color["hex"]};" '
                f'title="{color["name"]}" '
                f'data-name="{color["name"]}" data-hex="{color["hex"]}" '
                f'aria-pressed="{"true" if is_selected else "false"}">'
                f'<span class="ds-swatch__check">✓</span>'
                f'</button>'
            )
            
        # 2. Render any custom swatches that are currently selected in the record
        for name in selected_names:
            if name.lower() not in standard_names:
                # Simple fallback color logic for common keywords or hex value itself
                color_hex = name if name.startswith("#") else "#888888"
                swatches.append(
                    f'<button type="button" class="ds-swatch ds-swatch--custom ds-swatch--selected" '
                    f'style="background:{color_hex};" '
                    f'title="{name}" '
                    f'data-name="{name}" data-hex="{color_hex}" '
                    f'aria-pressed="true">'
                    f'<span class="ds-swatch__check">✓</span>'
                    f'</button>'
                )
        return "\n".join(swatches)

    def value_from_datadict(self, data, files, name):
        return data.get(name, "")
