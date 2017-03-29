# RAMS Plugin Template
This skeleton repository is intended to help developers when creating a new plugin.


## How do I use this template?
1. Clone this repository into the same directory as the "rams" plugin and any other Sideboard plugins you have installed.
2. Rename the plugin. Be sure to change the name everywhere it says `plugin_template` (including directory names). Plugin names should be separated_by_underscore.
3. Begin development!

## What can I do with this template?
RAMS plugins fall into two broad categories:
1. **Event plugins** or event-specific plugins are used to implement any business logic specific to your event. These plugins often make heavy use of _template overrides_ to change text or hide fields on the pre-registration pages, plus _model mixins_ to add new fields to, e.g., the Attendee model and _validations_ for those new fields.
2. **Feature plugins** add entirely new functionality intended for use by any event. These plugins often add entirely new _site sections_ with their own templates, plus new model classes.

### Template overrides
Templates in RAMS plugins can _override_ templates in other plugins. The plugin that is loaded last will take precedence -- for this reason, the RAMS core plugin is loaded first by default.

We recommend you use template overrides sparingly. The templating system is in the midst of being changed, and these techniques will (hopefully soon) become out of date. However, in the meantime, most of your template overriding will likely be done in `templates/regextra.html`. This template is included on every page that involves viewing or editing attendee details, including the pre-registration page. A very simple example of some things you might want to do in this page:
```html
<script type="text/javascript">
// Use jQuery to hide an existing field, called 'oldfield', that you don't want to collect data for
$.field('oldfield').parents('.form-group').hide();

// Use jQuery to position our new field, called 'newfield', on the page before our 'staffing' field
$.field('newfield').parents('.form-group').insertBefore($.field('staffing').parents('.form-group'));
</script>

<!-- add a row for our 'newfield' field -->
<div class="form-group">
    <label class="col-sm-2 control-label">New Field</label>
    <div class="col-sm-6">
        <input type="text" name="newfield" value="{{ attendee.newfield }}" class="form-control" placeholder="Placeholder text for your new field">
    </div>
</div>
```

### Model mixins
Let's say you wanted to add a field called `newfield` to collect from Attendees. We've added the field on the pre-reg pages in our template overrides, but this field doesn't exist in the database yet.

If you redefine the `Attendee` class in your `models.py` file, none of the existing fields will be included -- we obviously don't want that. Instead, we make use of the `model_mixin` decorator. Below is a simple example of what you might put in your plugin's `models.py` file:
```python
from plugin_template import *

@Session.model_mixin
class Attendee:
    newfield      = Column(UnicodeText, default='')

    @property
    def new_property(self):
        # A new property you want to add to the Attendee class
    
    @presave_adjustment
    def alter_newfield(self):
        # You can also add new 'presave adjustments' to work with your new field
```

### Validations
While adding a new field or removing an old field, you may want to change the server-side validations performed. Here's a simple example of what you might put in `model_checks.py` if you wanted to stop validating a field called `oldfield` and add a validation for `newfield`.
```python
from plugin_template import *

@validation.Attendee
def oldfield_validation(attendee):
    # Redefining a function name 'overrides' it in Python
    pass

@prereg_validation.Attendee
def newfield_validation(attendee):
    # Perform your validation here
```
