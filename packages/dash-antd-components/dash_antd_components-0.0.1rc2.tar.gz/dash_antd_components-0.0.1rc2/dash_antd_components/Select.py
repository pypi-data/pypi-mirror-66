# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Select(Component):
    """A Select component.


Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks
- value (string | list of strings; optional): The value of the input. If `multi` is false (the default)
then value is just a string that corresponds to the values
provided in the `options` property. If `multi` is true, then
multiple values can be selected at once, and `value` is an
array of items with values corresponding to those in the
`options` prop.
- options (dict; optional): An array of options. options has the following type: list of dicts containing keys 'label', 'value', 'disabled'.
Those keys have the following types:
  - label (string; optional): The checkbox's label
  - value (string; optional): The value of the checkbox. This value
corresponds to the items specified in the
`values` property.
  - disabled (boolean; optional): If true, this checkbox is disabled and can't be clicked on.
- className (string; optional): className of the dropdown element
- allowClear (boolean; default True): Whether or not the dropdown is "clearable", that is, whether or
not a small "x" appears on the right of the dropdown that removes
the selected value.
- disabled (boolean; default False): If true, the option is disabled
- mode (string; default 'multiple'): Set mode of Select ('default' | 'multiple' | 'tags' )
- size (string; optional): Size of Select input. ('default' | 'large' | 'small' )
- showArrow (boolean; optional): Whether to show the dropdown arrow
- placeholder (string; optional): The grey, default text shown when no option is selected"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, value=Component.UNDEFINED, options=Component.UNDEFINED, className=Component.UNDEFINED, allowClear=Component.UNDEFINED, disabled=Component.UNDEFINED, mode=Component.UNDEFINED, size=Component.UNDEFINED, showArrow=Component.UNDEFINED, placeholder=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'value', 'options', 'className', 'allowClear', 'disabled', 'mode', 'size', 'showArrow', 'placeholder']
        self._type = 'Select'
        self._namespace = 'dash_antd_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'value', 'options', 'className', 'allowClear', 'disabled', 'mode', 'size', 'showArrow', 'placeholder']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Select, self).__init__(**args)
