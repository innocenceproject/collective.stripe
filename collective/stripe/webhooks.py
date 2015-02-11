import json
from five import grok
from zope.component import getUtility
from zope.event import notify
from Products.CMFPlone.interfaces import IPloneSiteRoot
from collective.stripe.utils import IStripeUtility

from collective.stripe.interfaces import (
    IAccountUpdatedEvent,
    IAccountApplicationDeauthorizedEvent,
    IApplicationFeeCreatedEvent,
    IApplicationFeeRefundedEvent,
    IBalanceAvailableEvent,
    IChargeSucceededEvent,
    IChargeFailedEvent,
    IChargeRefundedEvent,
    IChargeCapturedEvent,
    IChargeUpdatedEvent,
    IChargeDisputeCreatedEvent,
    IChargeDisputeUpdatedEvent,
    IChargeDisputeClosedEvent,
    IChargeDisputeFundsWithdrawnEvent,
    IChargeDisputeFundsReinstatedEvent,
    ICustomerCreatedEvent,
    ICustomerUpdatedEvent,
    ICustomerDeletedEvent,
    ICustomerCardCreatedEvent,
    ICustomerCardUpdatedEvent,
    ICustomerCardDeletedEvent,
    ICustomerSubscriptionCreatedEvent,
    ICustomerSubscriptionUpdatedEvent,
    ICustomerSubscriptionDeletedEvent,
    ICustomerSubscriptionTrialWillEndEvent,
    ICustomerDiscountCreatedEvent,
    ICustomerDiscountUpdatedEvent,
    ICustomerDiscountDeletedEvent,
    IInvoiceCreatedEvent,
    IInvoiceUpdatedEvent,
    IInvoicePaymentSucceededEvent,
    IInvoicePaymentFailedEvent,
    IInvoiceItemCreatedEvent,
    IInvoiceItemUpdatedEvent,
    IInvoiceItemDeletedEvent,
    IPlanCreatedEvent,
    IPlanUpdatedEvent,
    IPlanDeletedEvent,
    ICouponCreatedEvent,
    ICouponDeletedEvent,
    IRecipientCreatedEvent,
    IRecipientUpdatedEvent,
    IRecipientDeletedEvent,
    ITransferCreatedEvent,
    ITransferUpdatedEvent,
    ITransferCanceledEvent,
    ITransferPaidEvent,
    ITransferFailedEvent,
    IPingEvent)


EVENTS_MAP = {
    'account.updated': IAccountUpdatedEvent,
    'account.application.deauthorized': IAccountApplicationDeauthorizedEvent,
    'application_fee.created': IApplicationFeeCreatedEvent,
    'application_fee.refunded': IApplicationFeeRefundedEvent,
    'balance.available': IBalanceAvailableEvent,
    'charge.succeeded': IChargeSucceededEvent,
    'charge.failed': IChargeFailedEvent,
    'charge.refunded': IChargeRefundedEvent,
    'charge.captured': IChargeCapturedEvent,
    'charge.updated': IChargeUpdatedEvent,
    'charge.dispute.created': IChargeDisputeCreatedEvent,
    'charge.dispute.updated': IChargeDisputeUpdatedEvent,
    'charge.dispute.closed': IChargeDisputeClosedEvent,
    'charge.dispute.funds_withdrawn': IChargeDisputeFundsWithdrawnEvent,
    'charge.dispute.funds_reinstated': IChargeDisputeFundsReinstatedEvent,
    'customer.created': ICustomerCreatedEvent,
    'customer.updated': ICustomerUpdatedEvent,
    'customer.deleted': ICustomerDeletedEvent,
    'customer.card.created': ICustomerCardCreatedEvent,
    'customer.card.updated': ICustomerCardUpdatedEvent,
    'customer.card.deleted': ICustomerCardDeletedEvent,
    'customer.subscription.created': ICustomerSubscriptionCreatedEvent,
    'customer.subscription.updated': ICustomerSubscriptionUpdatedEvent,
    'customer.subscription.deleted': ICustomerSubscriptionDeletedEvent,
    'customer.subscription.trial_will_end': (
        ICustomerSubscriptionTrialWillEndEvent),
    'customer.discount.created': ICustomerDiscountCreatedEvent,
    'customer.discount.updated': ICustomerDiscountUpdatedEvent,
    'customer.discount.deleted': ICustomerDiscountDeletedEvent,
    'invoice.created': IInvoiceCreatedEvent,
    'invoice.updated': IInvoiceUpdatedEvent,
    'invoice.payment_succeeded': IInvoicePaymentSucceededEvent,
    'invoice.payment_failed': IInvoicePaymentFailedEvent,
    'invoiceitem.created': IInvoiceItemCreatedEvent,
    'invoiceitem.updated': IInvoiceItemUpdatedEvent,
    'invoiceitem.deleted': IInvoiceItemDeletedEvent,
    'plan.created': IPlanCreatedEvent,
    'plan.updated': IPlanUpdatedEvent,
    'plan.deleted': IPlanDeletedEvent,
    'coupon.created': ICouponCreatedEvent,
    'coupon.deleted': ICouponDeletedEvent,
    'recipient.created': IRecipientCreatedEvent,
    'recipient.updated': IRecipientUpdatedEvent,
    'recipient.deleted': IRecipientDeletedEvent,
    'transfer.created': ITransferCreatedEvent,
    'transfer.updated': ITransferUpdatedEvent,
    'transfer.canceled': ITransferCanceledEvent,
    'transfer.paid': ITransferPaidEvent,
    'transfer.failed': ITransferFailedEvent,
    'ping': IPingEvent,
}


class StripeWebhooksView(grok.View):
    grok.name('stripe-webhooks')
    grok.require('zope2.Public')
    grok.context(IPloneSiteRoot)

    # These events will not be verified by an API callback
    unverified = ['ping']

    def render(self):
        event_json = json.loads(self.request.get('BODY'))
        stripe_util = getUtility(IStripeUtility)

        mode = 'live'
        if not event_json['livemode']:
            mode = 'test'
        stripe_api = stripe_util.get_stripe_api(mode=mode)

        # Make sure we have a mapping for the event
        event_class = EVENTS_MAP[event_json['type']]

        # Fetch the event to verify authenticity,
        # unless it is in the unverified list.
        if event_json['type'] in self.unverified:
            data = event_json
        else:
            data = stripe_api.Event.retrieve(event_json['id'])

            # Verify that the id, type, and created date of the event match
            if data['id'] != event_json['id']:
                raise ValueError('Event id failed verification')
            if data['type'] != event_json['type']:
                raise ValueError('Event type failed verification')
            if data['created'] != event_json['created']:
                raise ValueError('Event creation date failed verification')

        # Send the event with data
        event = event_class(data)
        notify(event)

        return 'OK'
