
def null_validator(*args, **kwargs):
    """A validator that doesn't validate anything.
    
    This is somewhat lame, but if you have a "Cancel" type button that
    won't want to validate the form, you need something like this.
    
    @form.action("Cancel", validator=null_validator)
    """
    return ()