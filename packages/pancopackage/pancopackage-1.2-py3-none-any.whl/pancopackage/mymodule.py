""" Short Description of module by using Docstrings format

	more detail information after a blank line
"""


class Display:
    """ This is a description of class """

    def displaymessage(self, guestname):
        """ 
            This function is for displaying message

            Parameters:
            path (str): this the part of string content

            Returns:
            str: The return value
        """
        print(f"this message is from mymodule of mypackage, {guestname}")
        return "ok"
