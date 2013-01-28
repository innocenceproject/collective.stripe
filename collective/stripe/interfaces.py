from zope.interface import Interface

class IStripeModeChooser(Interface):
    """ Interface for content types which can control 
        the Stripe mode, overriding the global control 
        panel setting 
    """

    def get_stripe_mode():
        """ Returns either 'live' or 'test' """

class IStripeEnabledView(Interface):
    """ Interface for views using Stripe """

    def show_stripe():
        """ Returns boolean for whether or not to include the stripe javascript """
