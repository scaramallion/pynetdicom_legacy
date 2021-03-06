#!/usr/bin/env python

import logging
import unittest
from unittest.mock import patch

from pydicom.uid import UID

from pynetdicom.primitives import *
from pynetdicom.PDU import A_ASSOCIATE_RQ_PDU, A_ABORT_PDU, P_DATA_TF_PDU
from pynetdicom.utils import wrap_list, PresentationContext


logger = logging.getLogger('pynetdicom')
handler = logging.NullHandler()
for h in logger.handlers:
    logger.removeHandler(h)
logger.addHandler(handler)
logger.setLevel(logging.ERROR)


# hexa = wrap_list(item.encode())
# for h in hexa:
#    print(h)


class TestPrimitive_MaximumLengthNegotiation(unittest.TestCase):
    def test_assignment_and_exceptions(self):
        """ Check incorrect types/values for maximum_length_received raise exceptions """
        primitive = MaximumLengthNegotiation()
        
        # Check default assignment
        self.assertTrue(primitive.maximum_length_received == 16382)
        
        # Check new assignment
        primitive.maximum_length_received = 45
        self.assertTrue(primitive.maximum_length_received == 45)

        # Check exceptions
        with self.assertRaises(TypeError):
            primitive.maximum_length_received = 45.2

        with self.assertRaises(ValueError):
            primitive.maximum_length_received = -1
            
        with self.assertRaises(TypeError):
            primitive.maximum_length_received = 'abc'

    def test_conversion(self):
        """ Check converting to PDU item works correctly """
        ## Check conversion to item using default value
        primitive = MaximumLengthNegotiation()
        item = primitive.from_primitive()
        
        # \x3F\xFE = 16382
        self.assertTrue(item.encode() == b"\x51\x00\x00\x04\x00\x00\x3f\xfe")
        
        ## Check conversion using 0 (unlimited)
        primitive.maximum_length_received = 0
        item = primitive.from_primitive()
        
        # \x00\x00 = 0
        self.assertTrue(item.encode() == b"\x51\x00\x00\x04\x00\x00\x00\x00")


class TestPrimitive_ImplementationClassUIDNotification(unittest.TestCase):
    def test_assignment_and_exceptions(self):
        """ Check incorrect types/values for implementation_class_uid raise exceptions """
        primitive = ImplementationClassUIDNotification()
        
        ## Check assignment
        reference_uid = UID('1.2.826.0.1.3680043.9.3811.0.9.0')
        
        # bytes
        primitive.implementation_class_uid = b'1.2.826.0.1.3680043.9.3811.0.9.0'
        self.assertTrue(primitive.implementation_class_uid == reference_uid)
        
        # str
        primitive.implementation_class_uid = '1.2.826.0.1.3680043.9.3811.0.9.0'
        self.assertTrue(primitive.implementation_class_uid == reference_uid)
        
        # UID
        primitive.implementation_class_uid = UID('1.2.826.0.1.3680043.9.3811.0.9.0')
        self.assertTrue(primitive.implementation_class_uid == reference_uid)
        

        ## Check exceptions
        primitive = ImplementationClassUIDNotification()
        
        # No value set
        with self.assertRaises(ValueError):
            item = primitive.from_primitive()
        
        # Non UID, bytes or str
        with self.assertRaises(TypeError):
            primitive.implementation_class_uid = 45.2

        with self.assertRaises(TypeError):
            primitive.implementation_class_uid = 100

        with self.assertRaises(ValueError):
            primitive.implementation_class_uid = 'abc'

    def test_conversion(self):
        """ Check converting to PDU item works correctly """
        primitive = ImplementationClassUIDNotification()
        primitive.implementation_class_uid = UID('1.2.826.0.1.3680043.9.3811.0.9.0')
        item = primitive.from_primitive()
        
        self.assertTrue(item.encode() ==     b"\x52\x00\x00\x20\x31\x2e\x32\x2e\x38\x32\x36\x2e\x30\x2e\x31" \
                                         b"\x2e\x33\x36\x38\x30\x30\x34\x33\x2e\x39\x2e\x33\x38\x31\x31\x2e" \
                                         b"\x30\x2e\x39\x2e\x30")


class TestPrimitive_ImplementationVersionNameNotification(unittest.TestCase):
    def test_assignment_and_exceptions(self):
        """ Check incorrect types/values for implementation_version_name raise exceptions """
        primitive = ImplementationVersionNameNotification()
        
        ## Check assignment
        reference_name = b'PYNETDICOM_090'
        
        # bytes
        primitive.implementation_version_name = b'PYNETDICOM_090'
        self.assertTrue(primitive.implementation_version_name == reference_name)
        
        # str
        primitive.implementation_version_name = 'PYNETDICOM_090'
        self.assertTrue(primitive.implementation_version_name == reference_name)
        
        ## Check exceptions
        primitive = ImplementationVersionNameNotification()
        
        # No value set
        with self.assertRaises(ValueError):
            item = primitive.from_primitive()
        
        # Non UID, bytes or str
        with self.assertRaises(TypeError):
            primitive.implementation_version_name = 45.2

        with self.assertRaises(TypeError):
            primitive.implementation_version_name = 100

        with self.assertRaises(ValueError):
            primitive.implementation_version_name = 'ABCD1234ABCD12345'

    def test_conversion(self):
        """ Check converting to PDU item works correctly """
        primitive = ImplementationVersionNameNotification()
        primitive.implementation_version_name = b'PYNETDICOM_090'
        item = primitive.from_primitive()

        self.assertTrue(item.encode() == b'\x55\x00\x00\x0e\x50\x59\x4e\x45\x54\x44\x49\x43\x4f\x4d\x5f\x30\x39\x30')


class TestPrimitive_AsynchronousOperationsWindowNegotiation(unittest.TestCase):
    def test_assignment_and_exceptions(self):
        """ Check incorrect types/values for properties raise exceptions """
        primitive = AsynchronousOperationsWindowNegotiation()
        
        ## Check default assignment
        self.assertTrue(primitive.maximum_number_operations_invoked == 1)
        self.assertTrue(primitive.maximum_number_operations_performed == 1)
        
        ## Check assignment
        primitive.maximum_number_operations_invoked = 10
        self.assertTrue(primitive.maximum_number_operations_invoked == 10)
        
        primitive.maximum_number_operations_performed = 11
        self.assertTrue(primitive.maximum_number_operations_performed == 11)
        
        ## Check exceptions
        with self.assertRaises(TypeError):
            primitive.maximum_number_operations_invoked = 45.2

        with self.assertRaises(ValueError):
            primitive.maximum_number_operations_invoked = -1

        with self.assertRaises(TypeError):
            primitive.maximum_number_operations_invoked = 'ABCD1234ABCD12345'

        with self.assertRaises(TypeError):
            primitive.maximum_number_operations_performed = 45.2

        with self.assertRaises(ValueError):
            primitive.maximum_number_operations_performed = -1

        with self.assertRaises(TypeError):
            primitive.maximum_number_operations_performed = 'ABCD1234ABCD12345'

    def test_conversion(self):
        """ Check converting to PDU item works correctly """
        primitive = AsynchronousOperationsWindowNegotiation()
        primitive.maximum_number_operations_invoked = 10
        primitive.maximum_number_operations_performed = 0
        item = primitive.from_primitive()
        
        self.assertTrue(item.encode() == b'\x53\x00\x00\x04\x00\x0a\x00\x00')


class TestPrimitive_SCP_SCU_RoleSelectionNegotiation(unittest.TestCase):
    def test_assignment_and_exceptions(self):
        """ Check incorrect types/values for properties raise exceptions """
        primitive = SCP_SCU_RoleSelectionNegotiation()
        
        ## Check assignment
        # SOP Class UID
        reference_uid = UID('1.2.840.10008.5.1.4.1.1.2')
        
        primitive.sop_class_uid = b'1.2.840.10008.5.1.4.1.1.2'
        self.assertTrue(primitive.sop_class_uid == reference_uid)
        
        primitive.sop_class_uid = '1.2.840.10008.5.1.4.1.1.2'
        self.assertTrue(primitive.sop_class_uid == reference_uid)
        
        primitive.sop_class_uid = UID('1.2.840.10008.5.1.4.1.1.2')
        self.assertTrue(primitive.sop_class_uid == reference_uid)
        
        # SCP Role
        primitive.scp_role = False
        self.assertTrue(primitive.scp_role == False)
        
        # SCU Role
        primitive.scu_role = True
        self.assertTrue(primitive.scu_role == True)
        
        ## Check exceptions
        with self.assertRaises(TypeError):
            primitive.sop_class_uid = 10
        
        with self.assertRaises(TypeError):
            primitive.sop_class_uid = 45.2
        
        with self.assertRaises(ValueError):
            primitive.sop_class_uid = 'abc'
        
        with self.assertRaises(TypeError):
            primitive.scp_role = 1

        with self.assertRaises(TypeError):
            primitive.scp_role = 'abc'

        with self.assertRaises(TypeError):
            primitive.scu_role = 1

        with self.assertRaises(TypeError):
            primitive.scu_role = 'abc'
        
        # No value set 
        primitive = SCP_SCU_RoleSelectionNegotiation()
        with self.assertRaises(ValueError):
            item = primitive.from_primitive()
        
        primitive.sop_class_uid = b'1.2.840.10008.5.1.4.1.1.2'
        with self.assertRaises(ValueError):
            item = primitive.from_primitive()

        primitive.scp_role = False
        with self.assertRaises(ValueError):
            item = primitive.from_primitive()
            
        primitive = SCP_SCU_RoleSelectionNegotiation()
        primitive.sop_class_uid = b'1.2.840.10008.5.1.4.1.1.2'
        primitive.scu_role = True
        with self.assertRaises(ValueError):
            item = primitive.from_primitive()
        
        primitive = SCP_SCU_RoleSelectionNegotiation()
        primitive.scp_role = True
        primitive.scu_role = True
        with self.assertRaises(ValueError):
            item = primitive.from_primitive()

    def test_conversion(self):
        """ Check converting to PDU item works correctly """
        primitive = SCP_SCU_RoleSelectionNegotiation()
        primitive.sop_class_uid = b'1.2.840.10008.5.1.4.1.1.2'
        primitive.scp_role = True
        primitive.scu_role = False
        item = primitive.from_primitive()
        
        self.assertTrue(item.encode() == b'\x54\x00\x00\x1d\x00\x19\x31\x2e\x32\x2e\x38\x34\x30\x2e\x31\x30' \
                                         b'\x30\x30\x38\x2e\x35\x2e\x31\x2e\x34\x2e\x31\x2e\x31\x2e\x32\x00' \
                                         b'\x01')


class TestPrimitive_SOPClassExtendedNegotiation(unittest.TestCase):
    def test_assignment_and_exceptions(self):
        """ Check incorrect types/values for properties raise exceptions """
        primitive = SOPClassExtendedNegotiation()
        
        ## Check assignment
        # SOP Class UID
        reference_uid = UID('1.2.840.10008.5.1.4.1.1.2')
        
        primitive.sop_class_uid = b'1.2.840.10008.5.1.4.1.1.2'
        self.assertTrue(primitive.sop_class_uid == reference_uid)
        
        primitive.sop_class_uid = '1.2.840.10008.5.1.4.1.1.2'
        self.assertTrue(primitive.sop_class_uid == reference_uid)
        
        primitive.sop_class_uid = UID('1.2.840.10008.5.1.4.1.1.2')
        self.assertTrue(primitive.sop_class_uid == reference_uid)
        
        # Service Class Application Information
        primitive.service_class_application_information = b'\x02\x00\x03\x00\x01\x00'
        self.assertTrue(primitive.service_class_application_information == b'\x02\x00\x03\x00\x01\x00')
        
        ## Check exceptions
        # SOP Class UID
        with self.assertRaises(TypeError):
            primitive.sop_class_uid = 10
        
        with self.assertRaises(TypeError):
            primitive.sop_class_uid = 45.2
        
        with self.assertRaises(ValueError):
            primitive.sop_class_uid = 'abc'
        
        # Service Class Application Information
        with self.assertRaises(TypeError):
            primitive.service_class_application_information = 10
        
        with self.assertRaises(TypeError):
            primitive.service_class_application_information = 45.2
        
        with self.assertRaises(TypeError):
            primitive.service_class_application_information = 'abc'
            
        # No value set
        primitive = SOPClassExtendedNegotiation()
        with self.assertRaises(ValueError):
            item = primitive.from_primitive()
            
        primitive.sop_class_uid = b'1.2.840.10008.5.1.4.1.1.2'
        with self.assertRaises(ValueError):
            item = primitive.from_primitive()
            
        primitive = SOPClassExtendedNegotiation()
        primitive.service_class_application_information = b'\x02\x00\x03\x00\x01\x00'
        with self.assertRaises(ValueError):
            item = primitive.from_primitive()
        
    def test_conversion(self):
        """ Check converting to PDU item works correctly """
        primitive = SOPClassExtendedNegotiation()
        primitive.sop_class_uid = b'1.2.840.10008.5.1.4.1.1.2'
        primitive.service_class_application_information = b'\x02\x00\x03\x00\x01\x00'
        item = primitive.from_primitive()
        
        self.assertTrue(item.encode() == b'\x56\x00\x00\x21\x00\x19\x31\x2e\x32\x2e\x38\x34\x30\x2e\x31\x30' \
                                         b'\x30\x30\x38\x2e\x35\x2e\x31\x2e\x34\x2e\x31\x2e\x31\x2e\x32\x02' \
                                         b'\x00\x03\x00\x01\x00')


class TestPrimitive_SOPClassCommonExtendedNegotiation(unittest.TestCase):
    def test_assignment_and_exceptions(self):
        """ Check incorrect types/values for properties raise exceptions """
        primitive = SOPClassCommonExtendedNegotiation()
        
        ## Check assignment
        # SOP Class UID
        reference_uid = UID('1.2.840.10008.5.1.4.1.1.2')
        
        primitive.sop_class_uid = b'1.2.840.10008.5.1.4.1.1.2'
        self.assertTrue(primitive.sop_class_uid == reference_uid)
        
        primitive.sop_class_uid = '1.2.840.10008.5.1.4.1.1.2'
        self.assertTrue(primitive.sop_class_uid == reference_uid)
        
        primitive.sop_class_uid = UID('1.2.840.10008.5.1.4.1.1.2')
        self.assertTrue(primitive.sop_class_uid == reference_uid)
        
        # Service Class UID
        primitive.service_class_uid = b'1.2.840.10008.5.1.4.1.1.2'
        self.assertTrue(primitive.service_class_uid == reference_uid)
        
        primitive.service_class_uid = '1.2.840.10008.5.1.4.1.1.2'
        self.assertTrue(primitive.service_class_uid == reference_uid)
        
        primitive.service_class_uid = UID('1.2.840.10008.5.1.4.1.1.2')
        self.assertTrue(primitive.service_class_uid == reference_uid)
        
        # Related General SOP Class Identification
        ref_uid_list = [UID('1.2.840.10008.5.1.4.1.1.2'),
                        UID('1.2.840.10008.5.1.4.1.1.3'),
                        UID('1.2.840.10008.5.1.4.1.1.4')]
        
        uid_list = []
        uid_list.append(b'1.2.840.10008.5.1.4.1.1.2')
        uid_list.append('1.2.840.10008.5.1.4.1.1.3')
        uid_list.append(UID('1.2.840.10008.5.1.4.1.1.4'))
        primitive.related_general_sop_class_identification = uid_list
        
        self.assertTrue(primitive.related_general_sop_class_identification == ref_uid_list)
        
        ## Check exceptions
        # SOP Class UID
        with self.assertRaises(TypeError):
            primitive.sop_class_uid = 10
        
        with self.assertRaises(TypeError):
            primitive.sop_class_uid = 45.2
        
        with self.assertRaises(ValueError):
            primitive.sop_class_uid = 'abc'
            
        # Service Class UID
        with self.assertRaises(TypeError):
            primitive.service_class_uid = 10
        
        with self.assertRaises(TypeError):
            primitive.service_class_uid = 45.2
        
        with self.assertRaises(ValueError):
            primitive.service_class_uid = 'abc'
            
        # Related General SOP Class Identification
        with self.assertRaises(TypeError):
            primitive.related_general_sop_class_identification = [10]
        
        with self.assertRaises(TypeError):
            primitive.related_general_sop_class_identification = [45.2]
        
        with self.assertRaises(ValueError):
            primitive.related_general_sop_class_identification = ['abc']
            
        # No value set
        primitive = SOPClassCommonExtendedNegotiation()
        with self.assertRaises(ValueError):
            item = primitive.from_primitive()
            
        primitive.sop_class_uid = b'1.2.840.10008.5.1.4.1.1.2'
        with self.assertRaises(ValueError):
            item = primitive.from_primitive()
            
        primitive = SOPClassCommonExtendedNegotiation()
        primitive.service_class_uid = b'1.2.840.10008.5.1.4.1.1.2'
        with self.assertRaises(ValueError):
            item = primitive.from_primitive()

    def test_conversion(self):
        """ Check converting to PDU item works correctly """
        primitive = SOPClassCommonExtendedNegotiation()
        primitive.sop_class_uid = b'1.2.840.10008.5.1.4.1.1.4'
        primitive.service_class_uid = b'1.2.840.10008.4.2'
        primitive.related_general_sop_class_identification = ['1.2.840.10008.5.1.4.1.1.88.22']
        item = primitive.from_primitive()
        
        self.assertTrue(item.encode() == b'\x57\x00\x00\x4d\x00\x19\x31\x2e\x32\x2e\x38\x34\x30\x2e\x31\x30' \
                                         b'\x30\x30\x38\x2e\x35\x2e\x31\x2e\x34\x2e\x31\x2e\x31\x2e\x34\x00' \
                                         b'\x11\x31\x2e\x32\x2e\x38\x34\x30\x2e\x31\x30\x30\x30\x38\x2e\x34' \
                                         b'\x2e\x32\x00\x1d\x00\x1d\x31\x2e\x32\x2e\x38\x34\x30\x2e\x31\x30' \
                                         b'\x30\x30\x38\x2e\x35\x2e\x31\x2e\x34\x2e\x31\x2e\x31\x2e\x38\x38' \
                                         b'\x2e\x32\x32')


class TestPrimitive_A_ASSOCIATE(unittest.TestCase):
    def test_assignment(self):
        """ Check assignment works correctly """
        assoc = A_ASSOCIATE()

        assoc.mode = "test value"
        self.assertTrue(assoc.mode == "normal")
        
        assoc.presentation_requirements = "test value2"
        self.assertTrue(assoc.presentation_requirements == "Presentation Kernel")
        
        assoc.session_requirements = "test value3"
        self.assertTrue(assoc.session_requirements == "")
        
        assoc.application_context_name = "1.2.840.10008.3.1.1.1"
        self.assertTrue(assoc.application_context_name == UID('1.2.840.10008.3.1.1.1'))
        assoc.application_context_name = b"1.2.840.10008.3.1.1.1"
        self.assertTrue(assoc.application_context_name == UID('1.2.840.10008.3.1.1.1'))
        assoc.application_context_name = UID("1.2.840.10008.3.1.1.1")
        self.assertTrue(assoc.application_context_name == UID('1.2.840.10008.3.1.1.1'))
        
        assoc.calling_ae_title = 'ABCD1234ABCD12345'
        self.assertTrue(assoc.calling_ae_title == b'ABCD1234ABCD1234')
        
        assoc.called_ae_title = 'ABCD1234ABCD12345'
        self.assertTrue(assoc.called_ae_title == b'ABCD1234ABCD1234')
        self.assertTrue(assoc.responding_ae_title == b'ABCD1234ABCD1234')
        
        max_length = MaximumLengthNegotiation()
        max_length.maximum_length_received = 31222
        assoc.user_information.append(max_length)
        self.assertTrue(assoc.user_information[0].maximum_length_received == 31222)
        
        assoc.result = 0
        self.assertTrue(assoc.result == 0)
        assoc.result = 1
        self.assertTrue(assoc.result == 1)
        assoc.result = 2
        self.assertTrue(assoc.result == 2)
        
        assoc.result_source = 1
        self.assertTrue(assoc.result_source == 1)
        assoc.result_source = 2
        self.assertTrue(assoc.result_source == 2)
        assoc.result_source = 3
        self.assertTrue(assoc.result_source == 3)
        
        assoc.diagnostic = 1
        self.assertTrue(assoc.diagnostic == 1)
        assoc.diagnostic = 2
        self.assertTrue(assoc.diagnostic == 2)
        assoc.diagnostic = 3
        self.assertTrue(assoc.diagnostic == 3)
        assoc.diagnostic = 7
        self.assertTrue(assoc.diagnostic == 7)
        
        assoc.calling_presentation_address = ('10.40.94.43', 105)
        self.assertTrue(assoc.calling_presentation_address == ('10.40.94.43', 105))
        
        assoc.called_presentation_address = ('10.40.94.44', 106)
        self.assertTrue(assoc.called_presentation_address == ('10.40.94.44', 106))
        
        assoc.presentation_context_definition_list = [PresentationContext(1)]
        self.assertTrue(assoc.presentation_context_definition_list == [PresentationContext(1)])
        
        assoc.presentation_context_definition_results_list = [PresentationContext(1)]
        self.assertTrue(assoc.presentation_context_definition_results_list == [PresentationContext(1)])
        
        assoc = A_ASSOCIATE()
        # No MaximumLengthNegotiation present
        assoc.maximum_length_received = 31223
        self.assertTrue(assoc.user_information[0].maximum_length_received == 31223)
        self.assertTrue(assoc.maximum_length_received == 31223)
        
        # MaximumLengthNegotiation already present
        assoc.maximum_length_received = 31224
        self.assertTrue(assoc.maximum_length_received == 31224)
        
        # No ImplementationClassUIDNegotiation present
        assoc.implementation_class_uid = '1.1.2.3.4'
        self.assertTrue(assoc.user_information[1].implementation_class_uid == UID('1.1.2.3.4'))
        self.assertTrue(assoc.implementation_class_uid == UID('1.1.2.3.4'))
        
        # ImplementationClassUIDNegotiation already present
        assoc.implementation_class_uid = '1.1.2.3.4'
        self.assertTrue(assoc.implementation_class_uid == UID('1.1.2.3.4'))
        
    def test_exceptions(self):
        """ Check incorrect types/values for properties raise exceptions """
        assoc = A_ASSOCIATE()
        
        # application_context_name
        with self.assertRaises(TypeError):
            assoc.application_context_name = 10
        
        with self.assertRaises(TypeError):
            assoc.application_context_name = 45.2
        
        with self.assertRaises(ValueError):
            assoc.application_context_name = 'abc'
        
        # calling_ae_title
        with self.assertRaises(TypeError):
            assoc.calling_ae_title = 45.2

        with self.assertRaises(TypeError):
            assoc.calling_ae_title = 100
        
        with self.assertRaises(ValueError):
            assoc.calling_ae_title = ''
        
        with self.assertRaises(ValueError):
            assoc.calling_ae_title = '    '
        
        # called_ae_title
        with self.assertRaises(TypeError):
            assoc.called_ae_title = 45.2

        with self.assertRaises(TypeError):
            assoc.called_ae_title = 100
        
        with self.assertRaises(ValueError):
            assoc.called_ae_title = ''
            
        with self.assertRaises(ValueError):
            assoc.called_ae_title = '    '
        
        # user_information
        with self.assertRaises(TypeError):
            assoc.user_information = 45.2
        
        # result
        with self.assertRaises(ValueError):
            assoc.result = -1
        
        with self.assertRaises(ValueError):
            assoc.result = 3
            
        # result_source
        with self.assertRaises(ValueError):
            assoc.result_source = 0
        
        # result_source
        with self.assertRaises(ValueError):
            assoc.result_source = 4
        
        # diagnostic
        with self.assertRaises(ValueError):
            assoc.diagnostic = 0
        
        with self.assertRaises(ValueError):
            assoc.diagnostic = 4
        
        with self.assertRaises(ValueError):
            assoc.diagnostic = 5
        
        with self.assertRaises(ValueError):
            assoc.diagnostic = 6
        
        with self.assertRaises(ValueError):
            assoc.diagnostic = 8
            
        # calling_presentation_addresss
        with self.assertRaises(TypeError):
            assoc.calling_presentation_address = ['10.40.94.43', 105]
        
        with self.assertRaises(TypeError):
            assoc.calling_presentation_address = (105, '10.40.94.43')
        
        # called_presentation_addresss
        with self.assertRaises(TypeError):
            assoc.called_presentation_address = ['10.40.94.43', 105]
        
        with self.assertRaises(TypeError):
            assoc.called_presentation_address = (105, '10.40.94.43')
        
        # presentation_context_definition_list
        with self.assertRaises(TypeError):
            assoc.presentation_context_definition_list = 45.2
        
        # presentation_context_definition_results_list
        with self.assertRaises(TypeError):
            assoc.presentation_context_definition_results_list = 45.2
        
        # implementation_class_uid
        with self.assertRaises(ValueError):
            x = assoc.implementation_class_uid
            
        imp_uid = ImplementationClassUIDNotification()
        assoc.user_information.append(imp_uid)
        with self.assertRaises(ValueError):
            x = assoc.implementation_class_uid
        
    def test_conversion(self):
        """ Check conversion to a PDU produces the correct output """
        assoc = A_ASSOCIATE()
        assoc.application_context_name = "1.2.840.10008.3.1.1.1"
        assoc.calling_ae_title = 'ECHOSCU'
        assoc.called_ae_title = 'ANY-SCP'
        assoc.maximum_length_received = 16382
        assoc.implementation_class_uid = '1.2.826.0.1.3680043.9.3811.0.9.0'
        
        imp_ver_name = ImplementationVersionNameNotification()
        imp_ver_name.implementation_version_name = 'PYNETDICOM_090'
        assoc.user_information.append(imp_ver_name)
        
        assoc.presentation_context_definition_list = \
            [PresentationContext(1, '1.2.840.10008.1.1', ['1.2.840.10008.1.2'])]
        
        pdu = A_ASSOCIATE_RQ_PDU()
        pdu.FromParams(assoc)
        data = pdu.encode()

        ref = b"\x01\x00\x00\x00\x00\xd1\x00\x01\x00\x00\x41\x4e\x59\x2d\x53\x43" \
              b"\x50\x20\x20\x20\x20\x20\x20\x20\x20\x20\x45\x43\x48\x4f\x53\x43" \
              b"\x55\x20\x20\x20\x20\x20\x20\x20\x20\x20\x00\x00\x00\x00\x00\x00" \
              b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
              b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x15\x31\x2e" \
              b"\x32\x2e\x38\x34\x30\x2e\x31\x30\x30\x30\x38\x2e\x33\x2e\x31\x2e" \
              b"\x31\x2e\x31\x20\x00\x00\x2e\x01\x00\x00\x00\x30\x00\x00\x11\x31" \
              b"\x2e\x32\x2e\x38\x34\x30\x2e\x31\x30\x30\x30\x38\x2e\x31\x2e\x31" \
              b"\x40\x00\x00\x11\x31\x2e\x32\x2e\x38\x34\x30\x2e\x31\x30\x30\x30" \
              b"\x38\x2e\x31\x2e\x32\x50\x00\x00\x3e\x51\x00\x00\x04\x00\x00\x3f" \
              b"\xfe\x52\x00\x00\x20\x31\x2e\x32\x2e\x38\x32\x36\x2e\x30\x2e\x31" \
              b"\x2e\x33\x36\x38\x30\x30\x34\x33\x2e\x39\x2e\x33\x38\x31\x31\x2e" \
              b"\x30\x2e\x39\x2e\x30\x55\x00\x00\x0e\x50\x59\x4e\x45\x54\x44\x49" \
              b"\x43\x4f\x4d\x5f\x30\x39\x30"
        
        self.assertTrue(data == ref)


class TestPrimitive_A_RELEASE(unittest.TestCase):
    def test_assignment(self):
        """ Check assignment works correctly """
        assoc = A_RELEASE()
        self.assertEqual(assoc.reason, "normal")
        
        assoc.result = "affirmative"
        self.assertEqual(assoc.result, "affirmative")
    
    def test_exceptions(self):
        """ Check incorrect types/values for properties raise exceptions """
        assoc = A_RELEASE()
        
        with self.assertRaises(AttributeError):
            assoc.reason = "something"
            
        with self.assertRaises(ValueError):
            assoc.result = "accepted"


class TestPrimitive_A_ABORT(unittest.TestCase):
    def test_assignment(self):
        """ Check assignment works correctly """
        primitive = A_ABORT()
        primitive.abort_source = 0
        self.assertEqual(primitive.abort_source, 0)
        primitive.abort_source = 2
        self.assertEqual(primitive.abort_source, 2)
        
    def test_exceptions(self):
        """ Check incorrect types/values for properties raise exceptions """
        primitive = A_ABORT()
        
        with self.assertRaises(ValueError):
            primitive.abort_source = 1

    def test_conversion(self):
        """ Check conversion to a PDU produces the correct output """
        primitive = A_ABORT()
        primitive.abort_source = 0
        
        pdu = A_ABORT_PDU()
        pdu.FromParams(primitive)
        data = pdu.encode()
        
        self.assertEqual(data, b"\x07\x00\x00\x00\x00\x04\x00\x00\x00\x00")


class TestPrimitive_A_P_ABORT(unittest.TestCase):
    def test_assignment(self):
        """ Check assignment works correctly """
        primitive = A_P_ABORT()
        primitive.provider_reason = 0
        self.assertEqual(primitive.provider_reason, 0)
        primitive.provider_reason = 1
        self.assertEqual(primitive.provider_reason, 1)
        primitive.provider_reason = 2
        self.assertEqual(primitive.provider_reason, 2)
        primitive.provider_reason = 4
        self.assertEqual(primitive.provider_reason, 4)
        primitive.provider_reason = 5
        self.assertEqual(primitive.provider_reason, 5)
        primitive.provider_reason = 6
        self.assertEqual(primitive.provider_reason, 6)
        
    def test_exceptions(self):
        """ Check incorrect types/values for properties raise exceptions """
        primitive = A_P_ABORT()
        
        with self.assertRaises(ValueError):
            primitive.provider_reason = 3

    def test_conversion(self):
        """ Check conversion to a PDU produces the correct output """
        primitive = A_P_ABORT()
        primitive.provider_reason = 4
        
        pdu = A_ABORT_PDU()
        pdu.FromParams(primitive)
        data = pdu.encode()
        
        self.assertEqual(data, b"\x07\x00\x00\x00\x00\x04\x00\x00\x02\x04")


class TestPrimitive_P_DATA(unittest.TestCase):
    def test_assignment(self):
        """ Check assignment works correctly """
        primitive = P_DATA()
        primitive.presentation_data_value_list = [[1, b'\x00']]
        self.assertEqual(primitive.presentation_data_value_list, [[1, b'\x00']])
    
    def test_exceptions(self):
        """ Check incorrect types/values for properties raise exceptions """
        primitive = P_DATA()
        
        with self.assertRaises(TypeError):
            primitive.presentation_data_value_list = ([1, b'\x00'])
        
        with self.assertRaises(TypeError):
            primitive.presentation_data_value_list = [1, b'\x00']
        
        with self.assertRaises(TypeError):
            primitive.presentation_data_value_list = [[b'\x00', 1]]
        
    def test_conversion(self):
        """ Check conversion to a PDU produces the correct output """
        primitive = P_DATA()
        pdv = b"\x03\x00\x00\x00\x00" \
              b"\x04\x00\x00\x00\x42\x00\x00\x00\x00\x00\x02\x00\x12\x00\x00\x00" \
              b"\x31\x2e\x32\x2e\x38\x34\x30\x2e\x31\x30\x30\x30\x38\x2e\x31\x2e" \
              b"\x31\x00\x00\x00\x00\x01\x02\x00\x00\x00\x30\x80\x00\x00\x20\x01" \
              b"\x02\x00\x00\x00\x01\x00\x00\x00\x00\x08\x02\x00\x00\x00\x01\x01" \
              b"\x00\x00\x00\x09\x02\x00\x00\x00\x00\x00"
        primitive.presentation_data_value_list = [[1, pdv]]
        
        pdu = P_DATA_TF_PDU()
        pdu.FromParams(primitive)
        data = pdu.encode()
        
        self.assertEqual(data, b"\x04\x00\x00\x00\x00\x54\x00\x00\x00\x50\x01" + pdv)

if __name__ == "__main__":
    unittest.main()
