from zope.interface import Interface


class IStripeModeChooser(Interface):
    """ Interface for content types which can control
        the Stripe mode, overriding the global control
        panel setting.
    """

    def get_stripe_mode():
        """ Returns either 'live' or 'test' """


class IStripeEnabledView(Interface):
    """ Interface for views using Stripe """

    def show_stripe():
        """
        Returns boolean for whether or not to include the stripe javascript.
        """


# Webhook triggered events


class BaseWebhookEvent(object):
    def __init__(self, data):
        self.data = data


# Account events


class IAccountUpdatedEvent(BaseWebhookEvent):
    """Occurs whenever an account status or property has changed."""


class IAccountApplicationDeauthorizedEvent(BaseWebhookEvent):
    """
    Occurs whenever a user deauthorizes an application. Sent to the related
    application only.
    """


class IApplicationFeeCreatedEvent(BaseWebhookEvent):
    """Occurs whenever an application fee is created on a charge."""


class IApplicationFeeRefundedEvent(BaseWebhookEvent):
    """Occurs whenever an application fee is refunded, whether from
    refunding a charge or from refunding the application fee directly,
    including partial refunds.
    """


# Balance events


class IBalanceAvailableEvent(BaseWebhookEvent):
    """
    Occurs whenever your Stripe balance has been updated (e.g. when a charge
    collected is available to be paid out). By default, Stripe will
    automatically transfer any funds in your balance to your bank account on
    a daily basis.
    """


# Charge events


class IChargeSucceededEvent(BaseWebhookEvent):
    """Occurs whenever a new charge is created and is successful."""


class IChargeFailedEvent(BaseWebhookEvent):
    """Occurs whenever a failed charge attempt occurs."""


class IChargeRefundedEvent(BaseWebhookEvent):
    """Occurs whenever a charge is refunded, including partial refunds."""


class IChargeCapturedEvent(BaseWebhookEvent):
    """Occurs whenever a previously uncaptured charge is captured."""


class IChargeUpdatedEvent(BaseWebhookEvent):
    """Occurs whenever a charge description or metadata is updated."""


class IChargeDisputeCreatedEvent(BaseWebhookEvent):
    """
    Occurs whenever a customer disputes a charge with their bank (chargeback).
    """


class IChargeDisputeUpdatedEvent(BaseWebhookEvent):
    """Occurs when the dispute is updated (usually with evidence)."""


class IChargeDisputeClosedEvent(BaseWebhookEvent):
    """
    Occurs when the dispute is resolved and the dispute status
    changes to won or lost.
    """


# Customer events


class IChargeDisputeFundsWithdrawnEvent(BaseWebhookEvent):
    """Occurs when funds are removed from your account due to a dispute."""


class IChargeDisputeFundsReinstatedEvent(BaseWebhookEvent):
    """
    Occurs when funds are reinstated to your account after a dispute is won.
    """


class ICustomerCreatedEvent(BaseWebhookEvent):
    """Occurs whenever a new customer is created. """


class ICustomerUpdatedEvent(BaseWebhookEvent):
    """Occurs whenever any property of a customer changes."""


class ICustomerDeletedEvent(BaseWebhookEvent):
    """Occurs whenever a customer is deleted."""


class ICustomerCardCreatedEvent(BaseWebhookEvent):
    """Occurs whenever a new card is created for the customer."""


class ICustomerCardUpdatedEvent(BaseWebhookEvent):
    """Occurs whenever a card's details are changed."""


class ICustomerCardDeletedEvent(BaseWebhookEvent):
    """Occurs whenever a card is removed from a customer."""


class ICustomerSubscriptionCreatedEvent(BaseWebhookEvent):
    """
    Occurs whenever a customer with no subscription is signed up for a plan.
    """


class ICustomerSubscriptionUpdatedEvent(BaseWebhookEvent):
    """
    Occurs whenever a subscription changes. Examples would include switching
    from one plan to another, or switching status from trial to active.
    """


class ICustomerSubscriptionDeletedEvent(BaseWebhookEvent):
    """Occurs whenever a customer ends their subscription."""


class ICustomerSubscriptionTrialWillEndEvent(BaseWebhookEvent):
    """
    Occurs three days before the trial period of a subscription is scheduled
    to end.
    """


class ICustomerDiscountCreatedEvent(BaseWebhookEvent):
    """Occurs whenever a coupon is attached to a customer."""


class ICustomerDiscountUpdatedEvent(BaseWebhookEvent):
    """Occurs whenever a customer is switched from one coupon to another."""


class ICustomerDiscountDeletedEvent(BaseWebhookEvent):
    """Occurs whenever a customer's discount is removed."""


# Invoice events


class IInvoiceCreatedEvent(BaseWebhookEvent):
    """
    Occurs whenever a new invoice is created. If you are using webhooks,
    Stripe will wait one hour after they have all succeeded to attempt to pay
    the invoice; the only exception here is on the first invoice, which gets
    created and paid immediately when you subscribe a customer to a plan. If
    your webhooks do not all respond successfully, Stripe will continue
    retrying the webhooks every hour and will not attempt to pay the invoice.
    After 3 days, Stripe will attempt to pay the invoice regardless of
    whether or not your webhooks have succeeded. See how to respond to a
    webhook.
    """


class IInvoiceUpdatedEvent(BaseWebhookEvent):
    """
    Occurs whenever an invoice changes (for example, the amount could change).
    """


class IInvoicePaymentSucceededEvent(BaseWebhookEvent):
    """
    Occurs whenever an invoice attempts to be paid, and the payment succeeds.
    """


class IInvoicePaymentFailedEvent(BaseWebhookEvent):
    """
    Occurs whenever an invoice attempts to be paid, and the payment fails.
    """


class IInvoiceItemCreatedEvent(BaseWebhookEvent):
    """Occurs whenever an invoice item is created."""


class IInvoiceItemUpdatedEvent(BaseWebhookEvent):
    """Occurs whenever an invoice item is updated."""


class IInvoiceItemDeletedEvent(BaseWebhookEvent):
    """Occurs whenever an invoice item is deleted."""


# Plan events


class IPlanCreatedEvent(BaseWebhookEvent):
    """Occurs whenever a plan is created. """


class IPlanUpdatedEvent(BaseWebhookEvent):
    """Occurs whenever a plan is updated."""


class IPlanDeletedEvent(BaseWebhookEvent):
    """Occurs whenever a plan is deleted."""


# Coupon related events


class ICouponCreatedEvent(BaseWebhookEvent):
    """Occurs whenever a coupon is created."""


class ICouponDeletedEvent(BaseWebhookEvent):
    """Occurs whenever a coupon is deleted."""


class IRecipientCreatedEvent(BaseWebhookEvent):
    """Occurs whenever a recipient is created."""


class IRecipientUpdatedEvent(BaseWebhookEvent):
    """Occurs whenever a recipient is updated."""


class IRecipientDeletedEvent(BaseWebhookEvent):
    """Occurs whenever a recipient is deleted."""


# Transfer events


class ITransferCreatedEvent(BaseWebhookEvent):
    """Occurs whenever a new transfer is created. """


class ITransferUpdatedEvent(BaseWebhookEvent):
    """Occurs whenever the amount of a pending transfer is updated."""


class ITransferCanceledEvent(BaseWebhookEvent):
    """Occurs whenever a pending transfer is canceled."""


class ITransferPaidEvent(BaseWebhookEvent):
    """
    Occurs whenever a sent transfer is expected to be available in the
    destination bank account. If the transfer failed, a transfer.failed
    webhook will additionally be sent at a later time.
    """


class ITransferFailedEvent(BaseWebhookEvent):
    """
    Occurs whenever Stripe attempts to send a transfer and that transfer fails.
    """


# Ping event


class IPingEvent(BaseWebhookEvent):
    """
    May be sent by Stripe at any time to see if a provided webhook URL is
    working.
    """
