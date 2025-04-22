# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2018 Rob Magee.  All rights reserved.
'''
The events module contains the base python implementations of the
fundamental EPCIS event classes.  The intent of these classes is to
implement the EPCIS events along with their business rules and no
other type of implementation features.  The idea here is that the classes
in this module will be inherited and extended by other classes (such
as those in this package's template_events module).

In addition to the base classes defined there are some enumerations and
classes that cover common sections and valued shared across the
primary EPCIS event types.
'''

import gettext
import hashlib
import re
import uuid

from setuptools import namespaces

from EPCIS.masterdata import LocationNode, ProductNode

_ = gettext.gettext

from datetime import datetime, timezone
from enum import Enum

from EPCIS.errors import ValidationError
from EPCIS.helpers import get_iso_8601_regex

iso_regex = get_iso_8601_regex()


class EventType(Enum):
    '''
    A helper Enum for comparing and using event types.
    '''
    Transaction = 'TransactionEvent'
    Object = 'ObjectEvent'
    Transformation = 'TransformationEvent'
    Aggregation = 'AggregationEvent'
    Association = 'AssociationEvent'


class Action(Enum):
    '''
    The Action type says how an event relates to the lifecycle of the entity
    being described. See section 7.3.2 of the EPCIS 1.2 standard.
    '''
    add = 'ADD'
    '''
    The entity in question has been created or added to.
    '''
    observe = 'OBSERVE'
    '''
    The entity in question has not been changed: it has neither been
    created, added to, destroyed, or removed from.
    '''
    delete = 'DELETE'
    '''
    The entity in question has been removed from or destroyed altogether.
    '''

    def __str__(self):
        return self.value


class EPCISExtension(object):
    def __init__(self, name_sapce, key, content):
        self._name_sapce = name_sapce
        self._key = key
        self._content = content

    @property
    def name_sapce(self):
        return self._name_sapce

    @name_sapce.setter
    def name_sapce(self, value):
        self._name_sapce = value

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = value

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        self._content = content

    @property
    def epcis_key(self):
        return f"{self._name_sapce}:{self._key}"


class EPCISExtensionCollection(object):
    def __init__(self):
        self._extensions = {}

    @property
    def extensions(self):
        return self._extensions

    def add_extension(self, extension: EPCISExtension):
        self._extensions[extension.epcis_key] = extension

    def remove_extension(self, epcis_key: str = None, name_sapce: str = None, key: str = None):
        if epcis_key:
            del self._extensions[epcis_key]
        elif name_sapce and key:
            epcis_key = f"{name_sapce}:{key}"
            del self._extensions[epcis_key]



class BusinessTransaction(object):
    '''
    A BusinessTransaction identifies a particular business
    transaction. An example of a business
    transaction is a specific purchase order. Business Transaction
    information may be included in EPCIS
    events to record an event’s participation in particular
    business transactions.
    As defined in section 7.3.5.3 of the protocol.
    '''

    def __init__(self, biz_transaction, type=None):
        '''
        :param biz_transaction: An identifier that denotes a specific
            business transaction.
        :param type: (Optional) An identifier that indicates what kind of
            business transaction this BusinessTransaction denotes.
        '''
        self.biz_transaction = biz_transaction
        self.type = type


class InstanceLotMasterDataAttribute(object):
    '''
    Base class for ILMD nodes.
    '''

    def __init__(self, name: str, value: str):
        '''
        An ILMD attribute.  If you are using the CBV compliant
        events see the :class:`EPCPyYes.core.v1_2.CBV.instance_lot_master_data.
        InstanceLotMasterDataAttribute`
        class.

        :param name: The name of the attribute (will be the name of the
            element in the ILMD section)
        :param value: Will be the element value in the ILMD section.
        '''
        self._name = name
        self._value = value

    @property
    def name(self):
        '''
        Gets and sets the name of the ILMD node. This value should
        be XML safe and is not auto-escaped.
        '''
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def value(self):
        '''
        Gets and sets the value of the ILMD node.  This value should
        be XML safe and is not auto-escaped.
        '''
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class SourceDest(object):
    def __init__(self, type: str):
        self.type = type


class Source(SourceDest):
    '''
    A Source or Destination is used to provide
    additional business context when an EPCIS event is
    part of a business transfer; that is, a process
    in which there is a transfer of ownership,
    responsibility, and/or custody of physical or digital objects.

    See the `EPCPyYes.core.v1_2.CBV.source_destination` module for standard
    source types.
    '''

    def __init__(self, source_type: str, source: str):
        '''
        :param source_type: An identifier that indicates what kind of
            source or destination this Source or Destination
            (respectively) denotes.
        :param source: An identifier that denotes a specific
            source or destination.
        '''
        super().__init__(source_type)
        self.source = source


class Destination(SourceDest):
    '''
    A Source or Destination is used to provide
    additional business context when an EPCIS event is
    part of a business transfer; that is, a process
    in which there is a transfer of ownership,
    responsibility, and/or custody of physical or digital objects.

    See the `EPCPyYes.core.v1_2.CBV.source_destination` module for standard
    source types.
    '''

    def __init__(self, destination_type: str, destination: str):
        '''
        :param source_type: An identifier that indicates what kind of
            source or destination this Source or Destination
            (respectively) denotes.
        :param source: An identifier that denotes a specific
            source or destination.
        '''
        super().__init__(destination_type)
        self.destination = destination


class ErrorDeclaration(object):
    '''
    As defined by the working group?...yikes.
    '''

    def __init__(self,
                 declaration_time: datetime = datetime.utcnow().isoformat(),
                 reason: str = None,
                 corrective_event_ids=[]):
        self.declaration_time = declaration_time
        self.reason = reason
        self.corrective_event_ids = corrective_event_ids


class QuantityElement(object):
    '''
    The EPCIS QuantityElement as outlined in section 7.3.3.3 of the protocol.
    '''

    def __init__(self, epc_class: str, quantity: float = None, uom=None):
        self.epc_class = epc_class
        self.quantity = quantity
        self.uom = uom


class EPCISEvent(object):
    '''
    The base EPCIS event as defined by GS1 on page 38 of the EPCIS 1.2 draft.
    '''

    # TODO: add getter setters
    def __init__(self, type, event_time: str = None, event_timezone_offset: str = None,
                 record_time: str = None, event_id: str = None,
                 error_declaration: ErrorDeclaration = None):
        '''
        The base EPCIS event class contains common properties shared
        across each of the Aggregation, Object, Transaction and
        Transformation events.

        :param event_time: The date and time at which the EPCIS Capturing
            Applications asserts the event occurred.
        :param event_timezone_offset: The time zone offset in effect at the
            time and place the event occurred, expressed as an offset from UTC.
        :param record_time: The date and time at which this event was
            recorded by an EPCIS Repository.
        :param event_id: An identifier for this event as specified by the
            capturing application, globally unique across all events
            other than error declarations.
        :param error_declaration:  If present, indicates that this event
            serves to assert that the assertions made by a prior event are in
            error.
        :param id: If present is used to store a reference to a database
            primary key.  This will NOT be rendered in the XML EPCIS documents.
            Use the id parameter and class property according to development
            needs.
        '''
        self._type = type
        self._event_timezone_offset = event_timezone_offset or '+00:00'
        self._event_time = event_time or datetime.now()
        self._record_time = record_time or datetime.now()
        self._event_id = event_id or hashlib.sha256(uuid.uuid4().hex.encode('utf-8')).hexdigest()
        self._error_declaration = error_declaration
        self._extension = EPCISExtensionCollection()
        self._children = []

    @property
    def type(self):
        return self._type

    @property
    def event_time(self):
        return self._event_time

    @event_time.setter
    def event_time(self, value):
        self._event_time = value

    @property
    def event_timezone_offset(self):
        return self._event_timezone_offset

    @event_timezone_offset.setter
    def event_timezone_offset(self, value):
        self._event_timezone_offset = value

    @property
    def record_time(self):
        return self._record_time

    @record_time.setter
    def record_time(self, value):
        self._record_time = value

    @property
    def event_id(self):
        return self._event_id

    @event_id.setter
    def event_id(self, value):
        self._event_id = value

    @property
    def error_declaration(self):
        return self._error_declaration

    @error_declaration.setter
    def error_declaration(self, value):
        self._error_declaration = value

    @property
    def extension_collection(self):
        return self._extension

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, value):
        self._children = value

    def clean(self):
        '''
        Implement this function to Validate an event based on rules defined
        in the EPCIS protocol or custom business rules if neccessary.
        :return: None or a EPCPyYes.core.errors.ValidationError
        '''
        msgs = []
        if self.record_time and isinstance(self.record_time, str):
            match = iso_regex.match(self.record_time)
            if not match:
                msgs.append(_('The record_time field is malformed.'))
        if isinstance(self.event_time, str):
            match = iso_regex.match(self.event_time)
            if not match:
                msgs.append(_('The event_time field is malformed.'))
        match = re.search(r'[\+\-][0-9]{2}:[0-9]{2}',
                          self.event_timezone_offset)
        if not match:
            msgs.append(_('The event_timezone_offset field is malformed.'))
        if len(msgs) > 0:
            raise ValidationError(''.join(msgs))


class EPCISBusinessEvent(EPCISEvent):
    '''
    For super-classes with an Action, biz step, biz location, etc...basically
    every main EPCIS class except the TransformationEvent class.
    '''

    # TODO: add getter setters
    def __init__(self, type, event_time: datetime = None, event_timezone_offset: str = None,
                 record_time: datetime = None, action: str = Action.add.value,
                 biz_step: str = None, disposition: str = None,
                 read_point: str = None,
                 biz_location: str = None, event_id: str = None,
                 error_declaration: ErrorDeclaration = None,
                 source_list=None,
                 destination_list=None,
                 business_transaction_list=None):
        '''

        :param event_time: Inherited from :class:`~EPCISEvent`
        :param event_timezone_offset: Inherited from :class:`~EPCISEvent`
        :param record_time: Inherited from :class:`~EPCISEvent`
        :param action: How this event relates to the lifecycle of the
            EPCs named in this event.
        :param biz_step: The business step of which this event was a part.
        :param disposition: The business condition of the objects associated
            with the EPCs, presumed to hold true until
            contradicted by a subsequent event.
        :param read_point: The read point at which the event took place.
        :param biz_location: The business location where the objects
            associated with the EPCs may be found, until contradicted
            by a subsequent event.
        :param event_id: Inherited from :class:`~EPCISEvent`
        :param error_declaration: Inherited from :class:`~EPCISEvent`
        :param source_list:  An unordered list of Source elements
            that provide context about the originating endpoint of a
            business transfer of which this event is a part.
        :param destination_list: An unordered list of Destination elements
            that provide context about
            the terminating endpoint of a business transfer of which
            this event is a part. Class
            :class:`EPCPyYes.core.v1_2.CBV.source_destination.SourceDestinationTypes`
            can be used to generate the appropriate XML values for this.
        :param business_transaction_list: An unordered list of business
            transactions that define the context of this event.
        '''
        super().__init__(type, event_time, event_timezone_offset, record_time,
                         event_id, error_declaration)

        self._action = action
        self._biz_step = biz_step
        self._disposition = disposition
        self._read_point = read_point
        self._biz_location = biz_location
        self._source_list = source_list or []
        self._destination_list = destination_list or []
        self._business_transaction_list = business_transaction_list or []

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, value):
        self._action = value

    @property
    def biz_step(self):
        return self._biz_step

    @biz_step.setter
    def biz_step(self, value):
        self._biz_step = value

    @property
    def disposition(self):
        return self._disposition

    @disposition.setter
    def disposition(self, value):
        self._disposition = value

    @property
    def read_point(self):
        return self._read_point

    @read_point.setter
    def read_point(self, value):
        self._read_point = value

    @property
    def biz_location(self):
        return self._biz_location

    @biz_location.setter
    def biz_location(self, value):
        self._biz_location = value

    @property
    def source_list(self):
        return self._source_list

    @source_list.setter
    def source_list(self, value):
        self._source_list = value

    @property
    def destination_list(self):
        return self._destination_list

    @destination_list.setter
    def destination_list(self, value):
        self._destination_list = value

    @property
    def business_transaction_list(self):
        return self._business_transaction_list

    @business_transaction_list.setter
    def business_transaction_list(self, value):
        self._business_transaction_list = value


class ObjectEvent(EPCISBusinessEvent):
    '''
    A python implementation of the EPCIS Object event as outlined in
    section 7.4.2 of the standard.
    '''

    def __init__(self, event_time: datetime = None, event_timezone_offset: str = None,
                 record_time: datetime = None, action: str = Action.add.value,
                 epc_list: list = None, biz_step=None, disposition=None,
                 read_point=None,
                 biz_location=None, event_id: str = None,
                 error_declaration: ErrorDeclaration = None,
                 source_list: list = None,
                 destination_list: list = None,
                 business_transaction_list: list = None,
                 ilmd: str = None,
                 quantity_list: list = None):
        '''
        A python representation of an EPCIS ObjectEvent instance.

        :param event_time: Inherited from :class:`~EPCISEvent`
        :param event_timezone_offset: Inherited from :class:`~EPCISEvent`
        :param record_time: Inherited from :class:`~EPCISEvent`
        :param action: Inherited from :class:`~EPCISBusinessEvent`
        :param epc_list: An unordered list of one or more EPCs
            naming specific objects to which the event pertained
        :param biz_step: Inherited from :class:`~EPCISBusinessEvent`
        :param disposition: Inherited from :class:`~EPCISBusinessEvent`
        :param read_point: Inherited from :class:`~EPCISBusinessEvent`
        :param biz_location: Inherited from :class:`~EPCISBusinessEvent`
        :param event_id: Inherited from :class:`~EPCISEvent`
        :param error_declaration: Inherited from :class:`~EPCISEvent`
        :param source_list: Inherited from :class:`~EPCISBusinessEvent`
        :param destination_list: Inherited from :class:`~EPCISBusinessEvent`
        :param business_transaction_list: Inherited from :class:`~EPCISBusinessEvent`
        :param ilmd:  Instance/Lot master data (Section 7.3.6)
            that describes the objects created during this event. An ObjectEvent
            SHALL NOT contain ilmd if action is OBSERVE or DELETE.
        :param quantity_list: An unordered list of one or more QuantityElements
            identifying (at the class level) objects to which the event pertained.
        :parm enforce_rules: whether or not to enforce EPCIS rules during
            the initilization of the class.  Default is false.
        '''
        super().__init__('ObjectEvent', event_time, event_timezone_offset, record_time,
                         action, biz_step, disposition, read_point,
                         biz_location, event_id, error_declaration,
                         source_list, destination_list,
                         business_transaction_list)

        self._epc_list = epc_list or []
        self._quantity_list = quantity_list or []

        self._ilmd = ilmd or []

    def clean(self):
        '''
        Validate the event.
        :return: None or raises a ValidationError
        '''
        super().clean()
        if not self.epc_list and not self.quantity_list:
            raise ValidationError(_('There must be either an epc_list or a '
                                    'quantity_list specified during '
                                    'initialization.'))
        if self.ilmd and self.action != 'ADD':
            raise ValidationError(_('An ILMD section can only be included in '
                                    'ObjectEvents of type ADD.'))

    @property
    def epc_list(self):
        return self._epc_list

    @epc_list.setter
    def epc_list(self, value):
        self._epc_list = value

    @property
    def quantity_list(self):
        return self._quantity_list

    @quantity_list.setter
    def quantity_list(self, value):
        self._quantity_list = value

    @property
    def ilmd(self):
        return self._ilmd

    @ilmd.setter
    def ilmd(self, value):
        self._ilmd = value


class AggregationEvent(EPCISBusinessEvent):
    '''
    The event type AggregationEvent describes events that apply to objects
    that have been aggregated to one another. In such an event, there is a
    set of “contained” objects that have been aggregated within a “containing”
    entity that’s meant to identify the aggregation itself.
    '''

    def __init__(self, event_time: datetime = None, event_timezone_offset: str = None,
                 record_time: datetime = None, action: str = Action.add.value,
                 parent_id: str = None, child_epcs: list = None,
                 child_quantity_list: list = None,
                 biz_step: str = None, disposition: str = None,
                 read_point: str = None, biz_location: str = None,
                 event_id: str = None,
                 error_declaration: ErrorDeclaration = None, source_list=None,
                 destination_list=None, business_transaction_list=None):
        '''
        Creates a new python AggregationEvent instance.

        :param event_time: Inherited from :class:`~EPCISEvent`
        :param event_timezone_offset: Inherited from :class:`~EPCISEvent`
        :param record_time: Inherited from :class:`~EPCISEvent`
        :param action: Inherited from :class:`~EPCISBusinessEvent`
        :param parent_id: The identifier of the parent of the association.
        :param child_epcs: An unordered list of the EPCs of contained objects
            identified by instance-level identifiers.
        :param child_quantity_list: An unordered list of one or more
            QuantityElements identifying (at the class level) contained objects.
        :param biz_step: Inherited from :class:`~EPCISBusinessEvent`
        :param disposition: Inherited from :class:`~EPCISBusinessEvent`
        :param read_point: Inherited from :class:`~EPCISBusinessEvent`
        :param biz_location: Inherited from :class:`~EPCISBusinessEvent`
        :param event_id: Inherited from :class:`~EPCISEvent`
        :param error_declaration: Inherited from :class:`~EPCISEvent`
        :param source_list: Inherited from :class:`~EPCISBusinessEvent`
        :param destination_list: Inherited from :class:`~EPCISBusinessEvent`
        :param business_transaction_list: Inherited from :class:`~EPCISBusinessEvent`
        '''
        super().__init__('AggregationEvent', event_time, event_timezone_offset, record_time,
                         action, biz_step, disposition, read_point,
                         biz_location, event_id, error_declaration,
                         source_list, destination_list,
                         business_transaction_list)

        self._parent_id = parent_id
        self._child_epcs = child_epcs or []
        self._child_quantity_list = child_quantity_list or []

    def clean(self):
        super().clean()
        if not self.parent_id and self.action != Action.observe.value:
            raise ValidationError(
                _('Parent ID is required in aggregation events '
                  'where the Action is ADD or DELETE.'))
        if self.child_epcs == None and self.child_quantity_list == None:
            raise ValidationError(
                _('An aggregation event must have a non empty '
                  'childEPCs list or a non-empty child quantity '
                  'list.'))

    @property
    def parent_id(self):
        '''
        Gets or sets identifier of the parent of the association.
        '''
        return self._parent_id

    @parent_id.setter
    def parent_id(self, value):
        self._parent_id = value

    @property
    def child_epcs(self):
        '''
        Gets or sets an unordered list of the EPCs of contained objects
        identified by instance-level identifiers.
        '''
        return self._child_epcs

    @child_epcs.setter
    def child_epcs(self, value):
        self._child_epcs = value

    @property
    def child_quantity_list(self):
        '''
        Gets or sets the unordered list of one or more QuantityElements
        identifying contained objects
        '''
        return self._child_quantity_list

    @child_quantity_list.setter
    def child_quantity_list(self, value):
        self._child_quantity_list = value


class AssociationEvent(EPCISBusinessEvent):
    '''
    The event type AggregationEvent describes events that apply to objects
    that have been aggregated to one another. In such an event, there is a
    set of “contained” objects that have been aggregated within a “containing”
    entity that’s meant to identify the aggregation itself.
    '''

    def __init__(self, event_time: datetime = None, event_timezone_offset: str = None,
                 record_time: datetime = None, action: str = Action.add.value,
                 parent_id: str = None, child_epcs: list = None,
                 child_quantity_list: list = None,
                 biz_step: str = None, disposition: str = None,
                 read_point: str = None, biz_location: str = None,
                 event_id: str = None,
                 error_declaration: ErrorDeclaration = None, source_list=None,
                 destination_list=None, business_transaction_list=None):
        '''
        Creates a new python AggregationEvent instance.

        :param event_time: Inherited from :class:`~EPCISEvent`
        :param event_timezone_offset: Inherited from :class:`~EPCISEvent`
        :param record_time: Inherited from :class:`~EPCISEvent`
        :param action: Inherited from :class:`~EPCISBusinessEvent`
        :param parent_id: The identifier of the parent of the association.
        :param child_epcs: An unordered list of the EPCs of contained objects
            identified by instance-level identifiers.
        :param child_quantity_list: An unordered list of one or more
            QuantityElements identifying (at the class level) contained objects.
        :param biz_step: Inherited from :class:`~EPCISBusinessEvent`
        :param disposition: Inherited from :class:`~EPCISBusinessEvent`
        :param read_point: Inherited from :class:`~EPCISBusinessEvent`
        :param biz_location: Inherited from :class:`~EPCISBusinessEvent`
        :param event_id: Inherited from :class:`~EPCISEvent`
        :param error_declaration: Inherited from :class:`~EPCISEvent`
        :param source_list: Inherited from :class:`~EPCISBusinessEvent`
        :param destination_list: Inherited from :class:`~EPCISBusinessEvent`
        :param business_transaction_list: Inherited from :class:`~EPCISBusinessEvent`
        '''
        super().__init__('AssociationEvent', event_time, event_timezone_offset, record_time,
                         action, biz_step, disposition, read_point,
                         biz_location, event_id, error_declaration,
                         source_list, destination_list,
                         business_transaction_list)

        self._parent_id = parent_id
        self._child_epcs = child_epcs or []
        self._child_quantity_list = child_quantity_list or []

    def clean(self):
        super().clean()
        if not self.parent_id and self.action != Action.observe.value:
            raise ValidationError(
                _('Parent ID is required in aggregation events '
                  'where the Action is ADD or DELETE.'))
        if self.child_epcs == None and self.child_quantity_list == None:
            raise ValidationError(
                _('An aggregation event must have a non empty '
                  'childEPCs list or a non-empty child quantity '
                  'list.'))

    @property
    def parent_id(self):
        '''
        Gets or sets identifier of the parent of the association.
        '''
        return self._parent_id

    @parent_id.setter
    def parent_id(self, value):
        self._parent_id = value

    @property
    def child_epcs(self):
        '''
        Gets or sets an unordered list of the EPCs of contained objects
        identified by instance-level identifiers.
        '''
        return self._child_epcs

    @child_epcs.setter
    def child_epcs(self, value):
        self._child_epcs = value

    @property
    def child_quantity_list(self):
        '''
        Gets or sets the unordered list of one or more QuantityElements
        identifying contained objects
        '''
        return self._child_quantity_list

    @child_quantity_list.setter
    def child_quantity_list(self, value):
        self._child_quantity_list = value


class TransactionEvent(EPCISBusinessEvent):
    '''
    A python implementation of and EPCIS TransactionEvent.
    '''

    def __init__(self, event_time: datetime, event_timezone_offset: str = None,
                 record_time: datetime = None, action: Action = Action.add.value,
                 parent_id: str = None, epc_list: list = None,
                 biz_step: str = None, disposition: str = None,
                 read_point: str = None, biz_location: str = None,
                 event_id: str = None,
                 error_declaration: ErrorDeclaration = None, source_list=None,
                 destination_list=None, business_transaction_list=None,
                 quantity_list: list = None):
        '''
        Initializes a new python representation of an EPCIS TransactionEvent.

        :param event_time: Inherited from :class:`~EPCISEvent`
        :param event_timezone_offset: Inherited from :class:`~EPCISEvent`
        :param record_time: Inherited from :class:`~EPCISEvent`
        :param action: Inherited from :class:`~EPCISBusinessEvent`
        :param parent_id: The identifier of the parent of the association.
        :param epc_list: An unordered list of one or more EPCs
            naming specific objects to which the event pertained
        :param biz_step: Inherited from :class:`~EPCISBusinessEvent`
        :param disposition: Inherited from :class:`~EPCISBusinessEvent`
        :param read_point: Inherited from :class:`~EPCISBusinessEvent`
        :param biz_location: Inherited from :class:`~EPCISBusinessEvent`
        :param event_id: Inherited from :class:`~EPCISEvent`
        :param error_declaration: Inherited from :class:`~EPCISEvent`
        :param source_list: Inherited from :class:`~EPCISBusinessEvent`
        :param destination_list: Inherited from :class:`~EPCISBusinessEvent`
        :param business_transaction_list: Inherited from :class:`~EPCISBusinessEvent`
        :param quantity_list: Inherited from :class:`~EPCISBusinessEvent`
        '''
        super().__init__('TransactionEvent', event_time, event_timezone_offset, record_time,
                         action, biz_step, disposition, read_point,
                         biz_location, event_id, error_declaration,
                         source_list, destination_list,
                         business_transaction_list)
        self._parent_id = parent_id
        self._epc_list = epc_list or []
        self._quantity_list = quantity_list or []

    @property
    def parent_id(self):
        return self._parent_id

    @parent_id.setter
    def parent_id(self, value: str):
        self._parent_id = value

    @property
    def epc_list(self):
        return self._epc_list

    @epc_list.setter
    def epc_list(self, value):
        self._epc_list = value

    @property
    def quantity_list(self):
        return self._quantity_list

    @quantity_list.setter
    def quantity_list(self, value: list):
        self._quantity_list = value


class TransformationEvent(EPCISBusinessEvent):
    '''
    A python implementation for the EPCIS TransformationEvent from
    section 7.4.6 of the GS1 standard.
    '''

    def __init__(self, event_time: datetime = None, event_timezone_offset: str = None,
                 record_time: datetime = None, event_id: str = None,
                 input_epc_list=None, input_quantity_list=None,
                 output_epc_list=None, output_quantity_list=None,
                 transformation_id=None, biz_step: str = None,
                 disposition: str = None,
                 read_point: str = None,
                 biz_location: str = None,
                 business_transaction_list=None,
                 source_list=None,
                 destination_list=None,
                 ilmd=None,
                 error_declaration: ErrorDeclaration = None):
        '''

        :param event_time: Inherited from :class:`~EPCISEvent`
        :param event_timezone_offset: Inherited from :class:`~EPCISEvent`
        :param record_time: Inherited from :class:`~EPCISEvent`
        :param event_id: Inherited from :class:`~EPCISEvent`
        :param input_epc_list: An unordered list of one or more EPCs identifying
            (at the instance level) objects that were inputs to the transformation.
        :param input_quantity_list: An unordered list of one or more
            QuantityElements identifying (at the class level) objects
            that were inputs to the transformation.
        :param output_epc_list: An unordered list of one or more EPCs naming
            (at the instance level) objects that were outputs from the transformation.
        :param output_quantity_list: An unordered list of one or more
            QuantityElements identifying (at the class level) objects that were
            outputs from the transformation
        :param transformation_id: A unique identifier that links this event
            to other TransformationEvents having an identical value of
            transformationID.
        :param biz_step: The business step of which this event was a part.
        :param disposition: The business condition of the objects associated
            with the EPCs, presumed to hold true until
            contradicted by a subsequent event.
        :param read_point: The read point at which the event took place.
        :param biz_location: The business location where the objects
            associated with the EPCs may be found, until contradicted
            by a subsequent event.
        :param business_transaction_list: An unordered list of business
            transactions that define the context of this event.
        :param source_list:  An unordered list of Source elements
            that provide context about the originating endpoint of a
            business transfer of which this event is a part.
        :param destination_list: An unordered list of Destination elements
            that provide context about
            the terminating endpoint of a business transfer of which
            this event is a part. Class
            :class:`EPCPyYes.core.v1_2.CBV.source_destination.SourceDestinationTypes`
            can be used to generate the appropriate XML values for this.
        :param ilmd:  Instance/Lot master data (Section 7.3.6)
            that describes the output objects created during this event.
        :param error_declaration: Inherited from :class:`~EPCISEvent`
        '''
        super().__init__('TransformationEvent', event_time, event_timezone_offset, record_time,
                         None, biz_step, disposition, read_point,
                         biz_location, event_id, error_declaration,
                         source_list, destination_list,
                         business_transaction_list)
        self._input_epc_list = input_epc_list or []
        self._input_quantity_list = input_quantity_list or []
        self._output_epc_list = output_epc_list or []
        self._output_quantity_list = output_quantity_list or []
        self._transformation_id = transformation_id
        self._ilmd = ilmd or []

    @property
    def input_epc_list(self):
        return self._input_epc_list

    @input_epc_list.setter
    def input_epc_list(self, value):
        self._input_epc_list = value

    @property
    def input_quantity_list(self):
        return self._input_quantity_list

    @input_quantity_list.setter
    def input_quantity_list(self, value):
        self._input_quantity_list = value

    @property
    def output_epc_list(self):
        return self._output_epc_list

    @output_epc_list.setter
    def output_epc_list(self, value):
        self._output_epc_list = value

    @property
    def output_quantity_list(self):
        return self._output_quantity_list

    @output_quantity_list.setter
    def output_quantity_list(self, value):
        self._output_quantity_list = value

    @property
    def transformation_id(self):
        return self._transformation_id

    @transformation_id.setter
    def transformation_id(self, value):
        self._transformation_id = value

    @property
    def ilmd(self):
        return self._ilmd

    @ilmd.setter
    def ilmd(self, value):
        self._ilmd = value


class EPCISDocument(object):
    '''
    Represents the higher-level container for an aggregation of EPCIS
    events.
    '''

    def __init__(self,
                 location_masterdata: dict = None,
                 product_masterdata: dict = None,
                 events: dict = None,
                 created_date: str = None,
                 namespaces: dict=None,

                 ):
        '''
        Initializes the EPCIS Document with the constituent object, aggregation,
        transaction and transformation events.

        :param object_events: A list of ObjectEvent instances.
        :param aggregation_events: A list of AggregationEvent instances
        :param transaction_events: A list of TransactionEvent instances
        :param transformation_events: A list of TransformationEvent instances.
        '''

        self._events = events or {}
        self._created_date = created_date or datetime.now(timezone.utc).isoformat(
            sep='T')
        self._location_masterdata = location_masterdata or {}
        self._product_masterdata = product_masterdata or {}
        self._namespaces = namespaces or {
                "cbvmda": "urn:epcglobal:cbv:mda:"
            }


    @property
    def location_masterdata(self):
        return self._location_masterdata

    @location_masterdata.setter
    def location_masterdata(self, value):
        self._location_masterdata = value

    @property
    def product_masterdata(self):
        return self._product_masterdata

    @product_masterdata.setter
    def product_masterdata(self, value):
        self._product_masterdata = value

    @property
    def events(self):
        return self._events

    @property
    def created_date(self):
        return self._created_date.isoformat(sep='T') \
            if isinstance(self._created_date, datetime) \
            else self._created_date

    @created_date.setter
    def created_date(self, value: datetime):
        self._created_date = value

    @property
    def namespaces(self):
        return self._namespaces

    def add_location_masterdata(self, location: LocationNode | list):
        if isinstance(location, list):
            for item in location:
                self._location_masterdata[item.id] = item
        elif isinstance(location, LocationNode):
            self._location_masterdata[location.id] = location

    def add_product_masterdata(self, product: ProductNode | list):
        if isinstance(product, list):
            for item in product:
                self._product_masterdata[item.id] = item
        elif isinstance(product, ProductNode):
            self._product_masterdata[product.id] = product

    def add_event(self, event: ObjectEvent | TransformationEvent | AggregationEvent | AssociationEvent | TransactionEvent):
        if event.event_id not in self._events:
            self._events[event.event_id] = event
        return self._events[event.event_id]

    def add_namespaces(self, key, value):
        self._namespaces[key] = value
