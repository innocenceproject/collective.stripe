import stripe
from five import grok
from zope.interface import Interface
from zope.site.hooks import getSite
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from collective.stripe.controlpanel import IStripeSettings

def get_settings():
    registry = getUtility(IRegistry)
    return registry.forInterface(IStripeSettings, False)

class IStripeUtility(Interface):
    """ A global utility providing methods to access the Stripe API """

    def get_stripe_api():
        """ returns the stripe api module with the api_key set from the control panel """

    def charge_card(token, amount, description, **kwargs):
        """ charges a card (represented by a Stripe.js card token) """

    def charge_customer(customer_id, amount, description, **kwargs):
        """ charges a customer looked up by customer_id.  customer must already exist """

    def create_customer(token, description, **kwargs):
        """ creates a customer using a card token from Stripe.js """

    def subscribe_customer(customer_id, plan, quantity, **kwargs):
        """ subscribe and existing customer to a plan.  if subscription
            already exists for the plan, the subscription is updated """

class StripeUtility(object):
    grok.implements(IStripeUtility)

    def get_stripe_api(self):
        settings = get_settings()
        if settings.mode == "live":
            stripe.api_key = settings.live_secret_key
        else:
            stripe.api_key = settings.test_secret_key
        return stripe

    def get_mode_for_context(self):
        pass 

    def charge_card(self, token, amount, description, **kwargs):
        settings = get_settings()
        stripe = self.get_stripe_api()
        res = stripe.Charge.create(
            amount = amount,
            currency = settings.currency,
            card = token,
            description = description,
            **kwargs
        )
        return res

    def charge_customer(self, customer_id, amount, description, **kwargs):
        settings = get_settings()
        stripe = self.get_stripe_api()
        res = stripe.Charge.create(
            amount = amount,
            currency = settings.currency,
            card = token,
            description = description,
            **kwargs
        )
        return res

    def create_customer(self, token, description, **kwargs):
        settings = get_settings()
        stripe = self.get_stripe_api()
        res = stripe.Customer.create(
            card = token,
            description = description,
            **kwargs
        )
        return res

    def subscribe_customer(self, customer_id, plan, quantity, **kwargs):
        settings = get_settings()
        stripe = self.get_stripe_api()
        cu = stripe.Customer.retrieve(customer_id)
        res = cu.update_subscription(
            plan=plan, 
            quantity=quantity,
            **kwargs
        )
        return res

grok.global_utility(StripeUtility, provides=IStripeUtility)
