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
