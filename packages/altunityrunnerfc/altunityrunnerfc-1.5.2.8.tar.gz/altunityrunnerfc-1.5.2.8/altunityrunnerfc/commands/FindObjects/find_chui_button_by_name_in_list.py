from altunityrunnerfc.commands.command_returning_alt_elements import CommandReturningAltElements
import json
class FindChuiButtonByNameInList(CommandReturningAltElements):
    def __init__(self, socket,request_separator,request_end,appium_driver,alt_objects,value):
        super(FindChuiButtonByNameInList, self).__init__(socket,request_separator,request_end,appium_driver)
        self.alt_objects=alt_objects
        self.value = value
    
    def execute(self):
        serialized = "["
        i = 0
        for o in self.alt_objects:
            i += 1
            serialized += o.toJSON()
            if (i < len(self.alt_objects)):
                serialized += ","
        serialized += "]"
        data = self.send_data(self.create_command('findChuiButtonByNameInList',serialized, self.value))
        return self.get_alt_element(data)
