import logging
from typing import Dict, Optional

import stripe
from django.conf import settings

logger = logging.getLogger(__name__)


def create_stripe_product(name: str, description: str = "") -> Dict:
    """
    Создает продукт в Stripe.

    Args:
        name: Название продукта
        description: Описание продукта

    Returns:
        Dict с данными созданного продукта

    Raises:
        stripe.error.StripeError: При ошибке создания продукта
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY

    if not stripe.api_key:
        raise ValueError("STRIPE_SECRET_KEY не настроен в settings")

    product = stripe.Product.create(
        name=name,
        description=description,
    )

    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
    }


def create_stripe_price(product_id: str, amount: float, currency: str = "rub") -> Dict:
    """
    Создает цену в Stripe.

    Args:
        product_id: ID продукта в Stripe
        amount: Сумма в рублях (будет преобразована в копейки)
        currency: Валюта (по умолчанию rub)

    Returns:
        Dict с данными созданной цены

    Raises:
        stripe.error.StripeError: При ошибке создания цены
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY

    if not stripe.api_key:
        raise ValueError("STRIPE_SECRET_KEY не настроен в settings")

    # Преобразуем рубли в копейки
    amount_in_cents = int(amount * 100)

    price = stripe.Price.create(
        product=product_id,
        unit_amount=amount_in_cents,
        currency=currency,
    )

    return {
        "id": price.id,
        "product": price.product,
        "unit_amount": price.unit_amount,
        "currency": price.currency,
    }


def create_stripe_session(price_id: str, success_url: str, cancel_url: str) -> Dict:
    """
    Создает сессию для оплаты в Stripe.

    Args:
        price_id: ID цены в Stripe
        success_url: URL для редиректа после успешной оплаты
        cancel_url: URL для редиректа при отмене оплаты

    Returns:
        Dict с данными созданной сессии

    Raises:
        stripe.error.StripeError: При ошибке создания сессии
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY

    if not stripe.api_key:
        raise ValueError("STRIPE_SECRET_KEY не настроен в settings")

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
    )

    return {
        "id": session.id,
        "url": session.url,
        "payment_status": session.payment_status,
    }


def retrieve_stripe_session(session_id: str) -> Optional[Dict]:
    """
    Получает информацию о сессии оплаты в Stripe.

    Args:
        session_id: ID сессии в Stripe

    Returns:
        Dict с данными сессии или None при ошибке
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return {
            "id": session.id,
            "url": session.url,
            "payment_status": session.payment_status,
            "status": session.status,
        }
    except stripe.error.StripeError as e:
        logger.error(f"❌ Общая ошибка Stripe: {str(e)}")
