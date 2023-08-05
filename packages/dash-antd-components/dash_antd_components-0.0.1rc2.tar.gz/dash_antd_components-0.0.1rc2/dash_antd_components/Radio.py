# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Radio(Component):
    """A Radio component.


Keyword arguments:
- children (list; optional)
- style (dict; optional)
- options (list; required)
- value (boolean | number | string | dict | list; optional)
- defaultValue (boolean | number | string | dict | list; optional)
- size (string; optional)
- buttonStyle (string; optional)
- name (string; optional)
- disabled (boolean; optional)
- id (string; optional): The ID used to identify this component in Dash callbacks
- className (string; optional): className of the container element"""
    @_explicitize_args
    def __init__(self, children=None, style=Component.UNDEFINED, options=Component.REQUIRED, value=Component.UNDEFINED, defaultValue=Component.UNDEFINED, size=Component.UNDEFINED, buttonStyle=Component.UNDEFINED, name=Component.UNDEFINED, disabled=Component.UNDEFINED, id=Component.UNDEFINED, className=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'style', 'options', 'value', 'defaultValue', 'size', 'buttonStyle', 'name', 'disabled', 'id', 'className']
        self._type = 'Radio'
        self._namespace = 'dash_antd_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'style', 'options', 'value', 'defaultValue', 'size', 'buttonStyle', 'name', 'disabled', 'id', 'className']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['options']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Radio, self).__init__(children=children, **args)
