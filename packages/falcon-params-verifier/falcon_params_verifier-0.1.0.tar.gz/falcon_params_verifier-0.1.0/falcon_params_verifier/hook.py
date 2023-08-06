import falcon


class ParamVerifier(object):
    """ Hook to process all req.params in a Falcon request """

    def __init__(self, required_parameters):
        self._required_params = required_parameters

    def __verify_params(self, request_object):
        for param_required in self._required_params:
            check_param = request_object.get_param(param_required)
            if check_param:
                if check_param == "" or check_param == '""':
                    return False
            else:
                return False
        return True

    def __call__(self, req, resp, resource, params):
        if self.__verify_params(request_object=req) == False:
            raise falcon.HTTPBadRequest(  # pylint: disable=no-member
                description="A required parameter has not been supplied."
            )
