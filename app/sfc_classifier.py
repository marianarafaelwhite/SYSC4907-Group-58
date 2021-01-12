"""
SFC Classifier

Developed with reference to the following:
- https://github.com/faucetsdn/ryu/blob/master/ryu/app/wsgi.py
- https://github.com/abulanov/sfc_app

More information on the Ryu WSGI API (to work with REST API):
- https://osrg.github.io/ryu-book/en/html/rest_api.html
"""
from ryu.app.wsgi import ControllerBase, route
from webob import Response
import logging
import json
from sfc_flow import SFCFlow

OK = 200
NOT_FOUND = 404
INTERNAL_SERVER_ERROR = 500


class SFCClassifier(ControllerBase):
    """
    SFC classifier

    Controller class can accept HTTP requests to the REST API.
    This class is created by the SDN Controller upon WSGI registration

    Attributes
    ----------
    __sdn_controller : SDNController
    __flows : dict
        Contains all the SFC flows
    """

    def __init__(self, req, link, data, **config):
        """
        Initialize the SFCClassifier

        Loosely based on abulanov/sfc_app's SFCController's __init__

        Parameters
        ----------
        req
        link
        data : dict
            Pass in the SDN controller
        **config
        """
        super(SFCClassifier, self).__init__(req, link, data, **config)
        self.__sdn_controller = data.get('sdn_controller', None)
        self.__flows = {}

    @route('add_flow', '/add_flow/{flow_id}', methods=['GET'])
    def add_flow(self, req, **kwargs):
        """
        Create SFC path (flow)

        @route(name, path, ...) decorator directs
        curl command to this method

        Loosely based on abulanov/sfc_app's SFCController's api_add_flow

        Parameters
        ----------
        req : Request
        **kwargs
            keyworded variable length of args

        Returns
        -------
        Reponse
            WSGI response
        """
        logging.debug('*** SFCClassifier: add_flow() entry')
        status = NOT_FOUND
        flow_id = kwargs['flow_id']
        logging.debug(
            '*** SFCClassifier: add_flow() flow_id: {}'.format(flow_id))

        # Create SFC flow & add to SDN controller
        try:
            self.__flows[flow_id] = SFCFlow(flow_id)
            self.__sdn_controller.add_catching_rule(self.__flows[flow_id])
            status = OK
        except ValueError:
            status = NOT_FOUND
        except BaseException as e:
            logging.error('*** SFCClassifier: error - {}'.format(e))
            status = INTERNAL_SERVER_ERROR

        return self.__response(status)

    @route('delete_flow', '/delete_flow/{flow_id}', methods=['GET'])
    def delete_flow(self, req, **kwargs):
        """
        Delete SFC path (flow)

        @route(name, path, ...) decorator directs
        curl command to this method

        Loosely based on abulanov/sfc_app's SFCController's api_delete_flow

        Parameters
        ----------
        req : Request
        **kwargs
            keyworded variable length of args

        Returns
        -------
        Reponse
            WSGI response
        """
        logging.debug('*** SFCClassifier: delete_flow() entry')
        status = NOT_FOUND
        flow_id = kwargs['flow_id']
        logging.debug(
            '*** SFCClassifier: delete_flow() flow_id: {}'.format(flow_id))

        # TODO: other logic

        # Attempt to delete flow
        try:
            del self.__flows[flow_id]
            logging.debug('*** SFCClassifier: Flow deleted')
            status = OK
        except KeyError:
            logging.error('*** SFCClassifier: Flow not found!')
            status = NOT_FOUND

        return self.__response(status)

    @route('show_flow', '/show_flow/{flow_id}', methods=['GET'])
    def show_flow(self, req, **kwargs):
        """
        Display SFC path (flow)

        @route(name, path, ...) decorator directs
        curl command to this method

        Loosely based on abulanov/sfc_app's SFCController's api_show_flow

        Parameters
        ----------
        req : Request
        **kwargs
            keyworded variable length of args

        Returns
        -------
        Reponse
            WSGI response
        """
        logging.debug('*** SFCClassifier: show_flow() entry')
        status = NOT_FOUND
        message = None
        flow_id = kwargs['flow_id']
        logging.debug(
            '*** SFCClassifier: show_flow() flow_id: {}'.format(flow_id))

        try:
            flow_dict = {flow_id: str(self.__flows[flow_id])}
            message = json.dumps(flow_dict)
            status = OK
            logging.debug('*** SFCClassifier: Flow retrieved')
        except KeyError:
            logging.error('*** SFCClassifier: Flow not found!')
            status = NOT_FOUND

        return self.__response(status, body=message)

    @route('show_all_flows', '/show_all_flows', methods=['GET'])
    def show_all_flows(self, req, **kwargs):
        """
        Display all SFC paths (flows)

        @route(name, path, ...) decorator directs
        curl command to this method

        Loosely based on abulanov/sfc_app's SFCController's api_show_flows

        Parameters
        ----------
        req : Request
        **kwargs
            keyworded variable length of args

        Returns
        -------
        Reponse
            WSGI response
        """
        logging.debug('*** SFCClassifier: show_all_flows() entry')
        message = json.dumps(str(self.__flows))
        return self.__response(OK, body=message)

    def __response(self, status, body=None):
        """
        Helper method to compose & send response message
        based on HTTP status

        Parameters
        ----------
        status : int
            HTTP status
        body : JSON str
            Optional message

        Returns
        -------
        Reponse
            WSGI response
        """
        messages = {OK: 'Success!',
                    INTERNAL_SERVER_ERROR: 'Something went wrong!',
                    NOT_FOUND: 'Not found'}
        if not body:
            msg = {'Result': messages.get(status, '')}
            body = json.dumps(msg)

        return Response(content_type='application/json',
                        body=body.encode('utf-8'),
                        status=status)
