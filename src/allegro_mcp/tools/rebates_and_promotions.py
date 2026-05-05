# ruff: noqa
"""Generated MCP tools — DO NOT EDIT.

Run ``make gen-tools`` to regenerate from the cached OpenAPI spec.
Tag: Rebates and promotions
"""

from __future__ import annotations

from typing import Any, cast

from ..errors import ErrorResponse
from ._decorators import requires_writes_enabled
from ._runtime import allegro_call, get_client, mcp


@mcp.tool
@allegro_call
@requires_writes_enabled
def create_promotion_using_post_1(
    *, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Create a new promotion

    This endpoint creates a new promotion. You can create promotions only if your base marketplace is `allegro-pl`. Created promotions are visible only on the `allegro-pl` marketplace. You can define the following types of promotions: 1. Large order discount <br> Only company users will see and be eligible for this type of promotion. In order to create a large order discount, you also have to be a company user. Furthermore, you are allowed to have only one active order discount at a time. Define a promotion with a single benefit of type **LARGE_ORDER_DISCOUNT** and a single criterion of type **ALL_OFFERS**. The benefit specification should contain a list of order value based discount thresholds. Threshold's order value defines the minimum total value of an order for which the threshold is applicable (`lowerBound`). Threshold's discount defines the discount percentage applied when the threshold is applied. The percentage's fractional part must be equal to 0. Only the highest applicable threshold (if any) will be applied to the total value of the order. A threshold with a higher order value than another threshold in the order discount must also have a higher discount. Large order discount is assigned automatically to all seller's offers. Moreover, it will be assigned to all newly added seller's offers once activated. Please note that it may take some time to propagate this type of promotion to all of your offers. Read more: <a href="../../tutorials/jak-zarzadzac-rabatami-…


    HTTP: ``POST /sale/loyalty/promotions``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "POST",
        f"/sale/loyalty/promotions",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def list_seller_promotions_using_get_1(
    *,
    limit: int | None = None,
    offset: int | None = None,
    offer_id: str | None = None,
    promotionType: str | None = None,
) -> dict[str, Any] | ErrorResponse:
    """Get the user's list of promotions

    Get a list of promotions defined by the authorized user and filtered by promotion type. <p>Restrictions:</p> <p>Filtering by promotion type is required.</p> <p>Sum of limit and offset must be equal to or lower than 50000. Limit must be equal to or lower than 5000.</p> <p>Example:</p> <p>offset = 49950 and limit = 50 will return promotions</p> <p>offset = 49950 and limit = 51 will return 422 http error</p> <p>offset = 0 and limit = 5000 will return promotions</p> <p>offset = 0 and limit = 5001 will return 422 http error</p> <p>Read more about: Large order discount <a href="../../tutorials/jak-zarzadzac-rabatami-promocjami-yPya2mj6zUP#pobierz-dostepne-rabaty" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-rebates-and-promotions-g05avdL0vT4#retrieve-large-order-discount" target="_blank">EN</a>, Wholesale price list <a href="../../tutorials/jak-zarzadzac-rabatami-promocjami-yPya2mj6zUP#pobierz-dostepne-cenniki" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-rebates-and-promotions-g05avdL0vT4#retrieve-wholesale-price-lists" target="_blank">EN</a>, Multipack <a href="../../tutorials/jak-zarzadzac-rabatami-promocjami-yPya2mj6zUP#pobierz-dostepne-rabaty-ilosciowe" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-rebates-and-promotions-g05avdL0vT4#retrieve-promotional-sets" target="_blank">EN</a>.</p>


    HTTP: ``GET /sale/loyalty/promotions``
    """
    params = {
        "limit": limit,
        "offset": offset,
        "offer.id": offer_id,
        "promotionType": promotionType,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/loyalty/promotions",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_promotion(*, promotionId: str) -> dict[str, Any] | ErrorResponse:
    """Get a promotion data by id

    <br> Use this resource to return the requested promotion. You need to use its unique id. <br> Read more about: Large order discount <a href="../../tutorials/jak-zarzadzac-rabatami-promocjami-yPya2mj6zUP#pobierz-informacje-o-rabacie" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-rebates-and-promotions-g05avdL0vT4#retrieve-information-about-large-order-discount" target="_blank">EN</a>, Wholesale price list <a href="../../tutorials/jak-zarzadzac-rabatami-promocjami-yPya2mj6zUP#pobierz-informacje-o-cenniku" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-rebates-and-promotions-g05avdL0vT4#retrieve-information-about-wholesale-price-list" target="_blank">EN</a>, Multipack <a href="../../tutorials/jak-zarzadzac-rabatami-promocjami-yPya2mj6zUP#pobierz-informacje-o-rabacie-ilosciowym" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-rebates-and-promotions-g05avdL0vT4#information-about-an-quantitative-discount" target="_blank">EN</a>.


    HTTP: ``GET /sale/loyalty/promotions/{promotionId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "GET",
        f"/sale/loyalty/promotions/{promotionId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def update_promotion(
    *, promotionId: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Modify a promotion

    Use this resource to update a promotion by its unique id. <br> It supports editing bundle's discount, wholesale price lists and large order discounts. Read more about: Large order discount <a href="../../tutorials/jak-zarzadzac-rabatami-promocjami-yPya2mj6zUP#edytuj-progi-rabatowe" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-rebates-and-promotions-g05avdL0vT4#edit-discount-thresholds" target="_blank">EN</a>, Wholesale price list <a href="../../tutorials/jak-zarzadzac-rabatami-promocjami-yPya2mj6zUP#edytuj-cennik" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-rebates-and-promotions-g05avdL0vT4#edit-wholesale-price-list" target="_blank">EN</a>.


    HTTP: ``PUT /sale/loyalty/promotions/{promotionId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PUT",
        f"/sale/loyalty/promotions/{promotionId}",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def deactivate_promotion(*, promotionId: str) -> dict[str, Any] | ErrorResponse:
    """Deactivate a promotion by id

    Use this resource to deactivate the requested promotion. You need to use its unique id. <br> Read more about: Large order discount <a href="../../tutorials/jak-zarzadzac-rabatami-promocjami-yPya2mj6zUP#usun-rabat" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-rebates-and-promotions-g05avdL0vT4#remove-large-order-discount" target="_blank">EN</a>, Wholesale price list <a href="../../tutorials/jak-zarzadzac-rabatami-promocjami-yPya2mj6zUP#usun-cennik" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-rebates-and-promotions-g05avdL0vT4#remove-wholesale-price-list" target="_blank">EN</a>, Multipack <a href="../../tutorials/jak-zarzadzac-rabatami-promocjami-yPya2mj6zUP#usun-rabat-ilosciowy" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-rebates-and-promotions-g05avdL0vT4#remove-an-quantitative-discount" target="_blank">EN</a>.


    HTTP: ``DELETE /sale/loyalty/promotions/{promotionId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "DELETE",
        f"/sale/loyalty/promotions/{promotionId}",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def create_or_modify_turnover_discount(
    *, marketplaceId: str, body: dict[str, Any] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Create/modify turnover discount for marketplace

    Create or modify the turnover discount for the specified marketplace. Currently, the only supported marketplace is `allegro-business-cz`. <br/> Turnover discount is assigned to all offers available on the given marketplace. Only B2B users will see and be eligible for this discount. In order to create a turnover discount definition, you also have to be a B2B user. <br/> Created turnover discount becomes visible for B2B users with the first day of the next month. Since that day, B2B users begin cumulating their spending on your offers they purchased. Turnover cumulated within the month translate into appropriate percentage of the discount for all orders of your offers in the following month. <br/> Turnover discount created in a given month is susceptible for change only until the end of that month. After that, as mentioned before, turnover discount becomes available for the users and can no longer be modified instantly. Modifying turnover discount in such case will result in creation of the new definition of the discount. This new definition will become available for the users on the same basis that the previously created one, with the start of the next month. Also, similarly, newly created definition can be modified only until the the end of the month. Read more: <a href="../../tutorials/jak-zarzadzac-rabatami-promocjami-yPya2mj6zUP#utworz-lub-edytuj-rabat-obrotowy" target="_blank">PL</a> / <a href="../..//tutorials/how-to-manage-rebates-and-promotions-g05avdL0vT4#create-or-…


    HTTP: ``PUT /sale/turnover-discount/{marketplaceId}``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PUT",
        f"/sale/turnover-discount/{marketplaceId}",
        json=body,
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
def get_turnover_discounts(
    *, marketplaceId: list[str] | None = None
) -> dict[str, Any] | ErrorResponse:
    """Get the list of turnover discounts

    Get a list of turnover discounts for all supported marketplaces. Read more: <a href="../../tutorials/jak-zarzadzac-rabatami-promocjami-yPya2mj6zUP#pobierz-liste-rabatow-obrotowych" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-rebates-and-promotions-g05avdL0vT4#retrieve-the-list-of-turnover-discounts" target="_blank">EN</a>. Currently, the only supported marketplace is `allegro-business-cz`. <br/> Turnover discount for the marketplace can have one of the three statuses: 1. `ACTIVATING` - neither accumulation of the turnover, nor applying of the discount has started yet. Turnover will be being accumulated from the beginning of the next month. 2. `ACTIVE` - there is ongoing accumulation of the turnover and/or applying of the discount. The latest discount definition does not have fields `cumulatingToDate` and `spendingToDate` set to a specific date. There may be multiple (up to 3) definitions of the discount returned for each marketplace. Only one definition can be accumulated against, and only one definition can be applied at the same time - appropriate periods from different definitions will not overlap. 3. `DEACTIVATING` - there is ongoing accumulation of the turnover and/or applying of the discount. Accumulation of the turnover will be continued until `cumulatingToDate` of the last definition. Applying of the discount will be continued until `spendingToDate` of the last definition.


    HTTP: ``GET /sale/turnover-discount``
    """
    params = {
        "marketplaceId": marketplaceId,
    }
    response = get_client().request_json(
        "GET",
        f"/sale/turnover-discount",
        params=params,
    )
    return cast(dict[str, Any], response)


@mcp.tool
@allegro_call
@requires_writes_enabled
def deactivate_turnover_discounts(*, marketplaceId: str) -> dict[str, Any] | ErrorResponse:
    """Deactivate turnover discount for marketplace

    Deactivate turnover discount for a given marketplace. Read more: <a href="../../tutorials/jak-zarzadzac-rabatami-promocjami-yPya2mj6zUP#deaktywuj-rabat-obrotowy" target="_blank">PL</a> / <a href="../../tutorials/how-to-manage-rebates-and-promotions-g05avdL0vT4#deactivate-turnover-discount" target="_blank">EN</a>. Currently, the only supported marketplace is `allegro-business-cz`. <br/> Turnover discount will stop being cumulated with the end of the current month. Discount based on cumulated turnover will stop being applied with the end of the next month. After that, the discount will be completely deactivated. <br/> When deactivating the discount that still has `ACTIVATING` status, turnover discount is deactivated immediately. In that case, no turnover discount will start being cumulated with the new month.


    HTTP: ``PUT /sale/turnover-discount/{marketplaceId}/deactivate``
    """
    params: dict[str, Any] = {}
    response = get_client().request_json(
        "PUT",
        f"/sale/turnover-discount/{marketplaceId}/deactivate",
        params=params,
    )
    return cast(dict[str, Any], response)
