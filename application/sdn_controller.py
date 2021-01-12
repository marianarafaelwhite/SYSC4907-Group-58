"""
SDN Controller

Developed with reference to the following:
- https://github.com/abulanov/sfc_app
- https://github.com/faucetsdn/ryu/blob/master/ryu/app/simple_switch.py
- https://github.com/faucetsdn/ryu/blob/master/ryu/app/simple_switch_13.py

More information on Ryu:
- https://ryu.readthedocs.io/en/latest/api_ref.html
"""
from ryu.base.app_manager import RyuApp
from ryu.controller.ofp_event import (EventOFPPacketIn,
                                      EventOFPSwitchFeatures,
                                      EventOFPStateChange)
from ryu.controller.handler import (set_ev_cls,
                                    MAIN_DISPATCHER,
                                    CONFIG_DISPATCHER,
                                    DEAD_DISPATCHER)
from ryu.app.wsgi import WSGIApplication
from sfc_classifier import SFCClassifier
import logging

MASK = 0xFFFFFFFF


class SDNController(RyuApp):
    """
    SDN Controller

    Attributes
    ----------
    _CONTEXTS : dict
        Specify contexts for RyuApp to use, as per documentation.
    __wsgi : WSGIApplication
        Web Server Gateway Interface
    __datapaths : dict
        Datapaths for SDN controller to manage
    """
    _CONTEXTS = {'wsgi': WSGIApplication}

    def __init__(self, *args, **kwargs):
        """
        Initialize the SDN Controller
        (Initializes the SFC Classifier)

        Loosely based on abulanov/sfc_app's sfc_app_cls' __init__

        Parameters
        ----------
        *args
        **kwargs
        """
        logging.debug('*** SDNController: constructor entry')
        super(SDNController, self).__init__(*args, **kwargs)

        # SFC related content
        self.__wsgi = kwargs.get('wsgi', None)
        data = {'sdn_controller': self}
        self.__wsgi.register(SFCClassifier, data)

        # To store the datapaths (empty for now)
        self.__datapaths = {}

    @set_ev_cls(EventOFPStateChange, [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def ___state_change_handler(self, ev):
        """
        Handles incoming state change messages
        (Occurs upon running ryu-manager sdn_controller.py)

        Decorator: set_ev_cls() (per documentation)
        When Ryu receives an OpenFlow switch_features message,
        this decorator indicates that this function should be called

        State is dead when Mininet datapath is dead and is main
        when Mininet datapath is alive
        (i.e., exit on the mininet topology program)

        Loosely based on abulanov/sfc_app's _state_change_handler

        Parameters
        ----------
        ev : EventOFPStateChange
            Type of event for a state change message
        """
        logging.debug('*** SDNController: __state_change_handler() entry')
        action = 'N/A'
        datapath = ev.datapath
        datapath_id = datapath.id
        state = ev.state

        if state == MAIN_DISPATCHER and (datapath_id not in self.__datapaths):
            self.__datapaths[datapath_id] = datapath
            action = 'Registered'
        elif state == DEAD_DISPATCHER and (datapath_id in self.__datapaths):
            del self.__datapaths[datapath_id]
            action = 'Unregistered'

        logging.debug('*** SDNController: {action} datapath: {path}'.format(
            action=action,
            path=datapath_id))
        logging.debug('*** SDNController: __state_change_handler() exit')

    @set_ev_cls(EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def ___switch_features_handler(self, ev):
        """
        Handles incoming switch features messages
        (Occurs upon running ryu-manager sdn_controller.py)

        Decorator: set_ev_cls() (per documentation)
        When Ryu receives an OpenFlow switch_features message,
        this decorator indicates that this function should be called

        Loosely based on switch_features_handler in both
        abulanov/sfc_app's sfc_app.py sfc_app_cls
        & faucetsdn/ryu's swimple_switch_13.py

        Parameters
        ----------
        ev : EventOFPSwitchFeatures
            Type of event for a switch features message
        """
        logging.debug('*** SDNController: __switch_features_handler() entry')
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        ofproto_parser = datapath.ofproto_parser

        # Create a flow match structure for lookup table comparisons later
        default_match = ofproto_parser.OFPMatch()

        # Parameters for default flows to create
        flows = [{'name': 'controller_out',
                  'out_port': ofproto.OFPP_CONTROLLER,
                  'priority': 0,
                  'match': default_match,
                  'table_id': 1},
                 {'name': 'normal_out',
                  'out_port': ofproto.OFPP_CONTROLLER,
                  'priority': 0,
                  'match': default_match,
                  'table_id': 2}]

        for flow in flows:
            logging.debug(
                '*** SDNController: adding flow {}'.format(flow['name']))
            action = ofproto_parser.OFPActionOutput(
                flow['out_port'],
                ofproto.OFPCML_NO_BUFFER)
            actions = [action]
            priority = flow['priority']
            match = flow['match']
            table_id = flow['table_id']

            self.__add_flow(
                datapath,
                priority,
                match,
                actions,
                table_id=table_id)

        logging.debug('*** SDNController: __switch_features_handler() exit')

    @set_ev_cls(EventOFPPacketIn, MAIN_DISPATCHER)
    def __packet_in_handler(self, ev):
        """
        Handles incoming packets

        Decorator: set_ev_cls() (per documentation)
        When Ryu receives an OpenFlow packet_in message,
        this decorator indicates that this function should be called

        See: https://ryu.readthedocs.io/en/latest/writing_ryu_app.html

        Loosely based on abulanov/sfc_app's sfc_app_cls' _packet_in_handler

        Parameters
        ----------
        ev : EventOFPPacketIn
            Type of event for a packet_in message
        """
        logging.debug('*** SDNController: __packet_in_handler() entry')

        # Extract information from packet_in message
        message = ev.msg
        datapath = message.datapath
        ofproto = datapath.ofproto
        ofproto_parser = datapath.ofproto_parser
        # TODO: better log here
        logging.debug('*** SDNController: OFPPacketIn: {}'.format(message))

        # TODO: proper handling

        # Build message to send packet_out message (TODO: delete later, not
        # needed and doesn't help)
        actions = [ofproto_parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
        out_message = ofproto_parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=message.buffer_id,
            in_port=message.match['in_port'],
            actions=actions)
        datapath.send_msg(out_message)

        logging.debug('*** SDNController: __packet_in_handler() exit')

    def __add_flow(self, datapath, priority, match, actions,
                   table_id=0, goto_id=None, metadata=None):
        """
        Modify a flow table

        Loosely based on add_flow in both
        abulanov/sfc_app's sfc_app.py sfc_app_cls
        & faucetsdn/ryu's swimple_switch_13.py

        Parameters
        ----------
        datapath : Datapath
        priority : int
        match : OFPFlowMatch
        actions : list
        table_id : int
        goto_id : int
        """
        logging.debug('*** SDNController: __add_flow() entry')
        ofproto = datapath.ofproto
        ofproto_parser = datapath.ofproto_parser

        # Create modify state message
        instruction_actions = ofproto_parser.OFPInstructionActions(
            ofproto.OFPIT_APPLY_ACTIONS, actions)
        instructions = [instruction_actions]

        # When goto_id set, add a goto-table next-table-id instruction
        if goto_id:
            instructions.append(
                ofproto_parser.OFPInstructionGotoTable(goto_id))

        # When metadata set, add a write-metadata metadata/mask instruction
        if metadata:
            instructions.append(
                ofproto_parser.OFPInstructionWriteMetadata(
                    metadata, MASK))

        modify_state = ofproto_parser.OFPFlowMod(
            datapath=datapath,
            priority=priority,
            match=match,
            instructions=instructions,
            table_id=table_id)

        logging.debug(
            '*** SDNController: OFPFlowMod - {}'.format(modify_state))

        datapath.send_msg(modify_state)
        logging.debug('*** SDNController: __add_flow() exit')

    def __del_flow(self, datapath, match):
        """
        Deletes a flow that is defined by a datapath's match

        Based on del_flow in abulanov/sfc_app's sfc_app.py sfc_app_cls

        Parameters
        ----------
        datapath : Datapath
        match : OFPFlowMatch
        """
        logging.debug('*** SDNController: __del_flow() entry')
        ofproto = datapath.ofproto
        ofproto_parser = datapath.ofproto_parser

        # Create modify state message to delete the flow (at any port that
        # matches)
        modify_state = ofproto_parser.OFPFlowMod(
            datapath=datapath,
            command=ofproto.OFPFC_DELETE,
            out_port=ofproto.OFPP_ANY,
            out_group=ofproto.OFPG_ANY,
            match=match)

        datapath.send(modify_state)
        logging.debug('*** SDNController: __del_flow() exit')

    def __create_match(self, datapath, flow):
        """
        Populates the OFPMatch constructor
        with arguments stored in the SFCFlow

        Parameters
        ----------
        datapath : Datapath
        flow : SFCFlow

        Returns
        -------
        match : OFPMatch
        """
        logging.debug('*** SDNController: __create_match() entry')
        fields = {}
        # In flow's items, if arg present, add to fields dict
        for k, v in flow.items():
            if v:
                fields[k] = v

        # Unpack fields dict as input args to OFPMatch
        match = datapath.ofproto_parser.OFPMatch(**fields)

        logging.debug('*** SDNController: __create_match() exit')
        return match

    def add_catching_rule(self, flow):
        """
        Create rules to catch traffic

        Based on install_catching_rule
        in abulanov/sfc_app's sfc_app.py sfc

        Parameters
        ----------
        flow : SFCFlow
        """
        logging.debug('*** SDNController: add_catching_rule() entry')
        actions = []
        priority = 1
        normal_table_id = 2
        flow_ids = [flow.forward_flow_id, flow.reverse_flow_id]
        
        # For each flow ID, iterate through datapaths & create flow from match
        for flow_id in flow_ids:
            current_flow = flow.bi_flows[flow_id]
            for datapath in self.__datapaths.values():
                match = self.__create_match(datapath, current_flow)
                self.__add_flow(datapath, priority, match, actions,
                              metadata=flow_id, goto_id=normal_table_id)
            
            # If no back reference, stop at forward flow ID
            if not flow.back:
                break

        logging.debug('*** SDNController: add_catching_rule() exit')
