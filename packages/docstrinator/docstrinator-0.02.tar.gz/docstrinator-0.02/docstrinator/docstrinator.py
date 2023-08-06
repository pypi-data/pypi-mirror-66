from inspect import getargspec

class NumpyTemplate:
    head \
    ="""
    HIGH LEVEL ANNOTATION

    DESCRIBING TEXT
    """

    paraneters_head =\
    """
    Parameters
    ----------
    """

    parameters_template = \
    """
    {} : {}
        Parameter.
    """

    returns=\
    """
    Returns
    -------
    {}
        Thing that returns.
    """



def class_name(value):
    """
    Function to get class names.

    Parameters
    ----------

    value : object
        Value to check type.

    Returns
    -------
    str
        The name of the value type.
    """
    
    return str(type(value))[8:-2]

class Decor:
    
    templates = {
        'numpy': NumpyTemplate()}


    def __init__(self, TepmlateType):
        """Get name of template"""
        try:
            self.tmplt = self.templates[TepmlateType]
        except:
            tmpl = list(self.templates.keys())
            raise Exception(
            f'Wrong template. Use {tmpl}')



    def create_docstring(self, parameters, result_type): 
        """
        Function to create docstings.

        Parameters
        ----------

        parameters : list
            List of names of the function.
        
        result_type : list
            List of parameter's types.

        Returns
        -------
        str
            Docstrings.
        """
        docstrings = ''
        docstrings += self.tmplt.head 
    
        if parameters:
            docstrings += self.tmplt.paraneters_head
            for parameter_name, parameter_type in parameters:
                docstrings += self.tmplt.parameters_template\
                    .format(parameter_name, parameter_type) 
        
        if result_type:
            docstrings += self.tmplt.returns.format(result_type)
        
        return docstrings

    def decor(self, func):
        """
        Decorator to create docstrings.

        Parameters
        ----------

        func : object
            Function that needs docstrings.

        Returns
        -------
        object
            Standard function output.
        """


        _parameters_names = getargspec(func)[0]
        
        def wrap(*args):
            """
            This function get parameters 
            and outputs of function.

            Parameters
            ----------

            *args : object
                Function parameters.

            Returns
            -------
            object
                Standard function output.
            """

            _parameters = [
                tupl for tupl in zip(
                    _parameters_names, 
                    [class_name(arg) for arg in [*args]]
                )]
            
            _result = func(*args)
            _result_type = class_name(_result)
            
            docs = self.create_docstring(_parameters, _result_type)
            print(docs)
            
            return _result 
        return wrap

