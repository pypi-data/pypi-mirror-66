import pytest
import gen_browser_header
import gen_browser_header.self.SelfEnum as self_enum
import gen_browser_header.helper.Helper as helper

@pytest.mark.all_values_preDefined
class Test_all_values_preDefined(object):
    def test_empty_values(self):
        assert helper.all_values_preDefined(values=set(),
                                            defined_enum=self_enum.OsType) == \
               True

    def test_all_valid_values(self):
        assert helper.all_values_preDefined(values=set({
            self_enum.OsType.Win64}),
                                            defined_enum=self_enum.OsType) == \
               True

    def test_invalid_values(self):
        assert helper.all_values_preDefined(values=set({'invalid'}),
                                            defined_enum=self_enum.OsType) == \
               False

@pytest.mark.enum_set_check
class Test_enum_set_check():
    def test_value_not_set(self):
        assert helper.enum_set_check(value='str', enum_type=self_enum.OsType) is None

    def test_value_is_set_but_member_not_valid_enum(self):
        assert helper.enum_set_check(value={'str'},
                                     enum_type=self_enum.OsType) is None

    def test_value_include_all(self):
        assert helper.enum_set_check(value={self_enum.OsType.All},
                                     enum_type=self_enum.OsType) == \
               {self_enum.OsType.Win32, self_enum.OsType.Win64}

    def test_value_not_include_all(self):
        assert helper.enum_set_check(value={self_enum.OsType.Win32},
                                     enum_type=self_enum.OsType) == \
               {self_enum.OsType.Win32}
