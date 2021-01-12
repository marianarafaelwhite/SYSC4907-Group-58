"""
Service Function Chaining Flow (SFC Flow)
As per service function chaining architecture:
- https://tools.ietf.org/html/rfc7665

References code from:
https://github.com/abulanov/sfc_app/blob/master/sfc_app.py

"""
import logging
from node_list import NodeList

ID_INCREMENT = 3000


class SFCFlow(NodeList):
    """
    SFCFlow Class

    Attributes
    ----------
    forward_flow_id : int
    reverse_flow_id : int
    bi_flows : dict
        Contains 2 flows (bidirectional)
    """

    def __init__(self, flow_id):
        """
        Initialize the SFCFlow class

        Loosely based on abulanov/sfc_app's sfc's __init__

        Parameters
        ----------
        flow_id : str
            ID of the SFC flow
        """
        logging.debug('*** SFCFlow: constructor entry')
        self.forward_flow_id = int(flow_id)
        self.reverse_flow_id = int(flow_id) + ID_INCREMENT

        # Select flow from sqlite DB
        # If flow not defined, raise exception
        # Else: set flow attributes from flow DB value

        forward_flow = {}
        reverse_flow = self.__create_reverse_flow(forward_flow)
        self.bi_flows = {
            self.forward_flow_id: forward_flow,
            self.reverse_flow_id: reverse_flow}
        logging.debug(
            '*** SFCFlow: Bi-directional flows: {}'.format(self.bi_flows))

        # Select VNF: TODO

        super().__init__(flow_id)

        # call fill (calls append): TODO

    def __str__(self):
        """
        Loosely based on abulanov/sfc_app's sfc's __str__

        Returns
        -------
        list
            List of nodes (forward transversal of list)
        """
        return str(self.get_forward_list())

    def __create_reverse_flow(self, forward_flow):
        """
        Reverse flow
        (i.e., src --> dst, dst --> src)

        Loosely based on abulanov/sfc_app's sfc_cls_app's reverse_flow

        Parameters
        ----------
        forward_flow : dict

        Returns
        -------
        reverse_flow
        """
        # TODO: Logs
        reverse_flow = {}
        for k in forward_flow:
            if 'src' in k:
                reverse_k = k.replace('src', 'dst')
            elif 'dst' in k:
                reverse_k = k.replace('dst', 'src')
            else:
                # Shouldn't reach here
                reverse_k = k

            reverse_flow[reverse_k] = forward_flow[k]

        return reverse_flow
